"""
Tests des routes de téléchargement, du ZIP sur disque et de l'IP client.
"""
import time
from io import BytesIO
from types import SimpleNamespace

import pytest

import main
from main import OptimizationJob, get_client_ip, jobs


def _wait_completed(client, job_id, timeout=15):
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = client.get(f"/api/job/{job_id}").json()
        if data["status"] == "completed":
            return data
        time.sleep(0.1)
    raise AssertionError("job non terminé")


def _optimize(client, image_bytes, n=1):
    files = [("files", (f"i{i}.png", BytesIO(image_bytes), "image/png")) for i in range(n)]
    r = client.post("/api/optimize", files=files, data={"format": "webp", "quality": "75"})
    assert r.status_code == 200, r.text
    job_id = r.json()["job_id"]
    _wait_completed(client, job_id)
    return job_id


@pytest.mark.integration
def test_single_file_then_zip_download(client, simple_image_bytes):
    job_id = _optimize(client, simple_image_bytes, n=2)

    r = client.get(f"/api/download/{job_id}")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/zip"

    r = client.get(f"/api/download/{job_id}/image-01.webp")
    assert r.status_code == 200
    assert 'filename="image-01.webp"' in r.headers["content-disposition"]

    assert client.get(f"/api/download-zip/{job_id}").status_code == 200


@pytest.mark.integration
def test_staging_dir_removed_after_processing(client, simple_image_bytes):
    job_id = _optimize(client, simple_image_bytes)
    assert not jobs[job_id].staging_dir.exists()


@pytest.mark.security
def test_single_file_requires_successful_result(client):
    job = OptimizationJob("job-status-check")
    jobs[job.job_id] = job
    (job.output_dir / "residue.bin").write_bytes(b"x")

    # Présent sur disque mais jamais enregistré comme résultat réussi
    assert client.get(f"/api/download/{job.job_id}/residue.bin").status_code == 404

    job.add_progress({"type": "image_processed", "optimized_name": "residue.bin", "success": True})
    assert client.get(f"/api/download/{job.job_id}/residue.bin").status_code == 200


@pytest.mark.security
def test_zip_refused_when_too_large(client, monkeypatch):
    job = OptimizationJob("job-big-zip")
    job.status = "completed"
    jobs[job.job_id] = job
    (job.output_dir / "a.bin").write_bytes(b"x" * 2048)
    (job.output_dir / "b.bin").write_bytes(b"x" * 2048)
    monkeypatch.setattr(main, "MAX_ZIP_SIZE_BYTES", 1024)

    r = client.get(f"/api/download-zip/{job.job_id}")
    assert r.status_code == 413


def _request(headers, host="10.0.0.1"):
    return SimpleNamespace(headers=headers, client=SimpleNamespace(host=host))


def test_client_ip_ignores_forwarded_header_without_trusted_proxy(monkeypatch):
    monkeypatch.setattr(main, "TRUSTED_PROXY_COUNT", 0)
    assert get_client_ip(_request({"x-forwarded-for": "1.2.3.4"})) == "10.0.0.1"


def test_client_ip_uses_last_trusted_hop(monkeypatch):
    monkeypatch.setattr(main, "TRUSTED_PROXY_COUNT", 1)
    # L'entrée de gauche est forgeable par le client ; celle ajoutée par le proxy est à droite
    assert get_client_ip(_request({"x-forwarded-for": "6.6.6.6, 203.0.113.9"})) == "203.0.113.9"
    assert get_client_ip(_request({})) == "10.0.0.1"
