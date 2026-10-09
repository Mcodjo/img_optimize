# DRX — Système Multi-Agents

> Autorité absolue : LAGOYE Hans (L8)

## Architecture du système

DRX est un système multi-agents d'ingénierie logicielle à orchestration hiérarchique.
L'agent principal `drx` orchestre les sous-agents ci-dessous.

Agents réellement présents dans le dépôt (`.github/agents/`) :

| Agent | Rôle | Fichier | Skill associé |
|---|---|---|---|
| `drx` | Orchestrateur principal | `.github/agents/drx.agent.md` | — |
| `drx-design` | UI/UX & direction artistique | `.github/agents/drx-design.agent.md` | `.github/skills/drx-design/SKILL.md` |
| `drx-sec` | Sécurité offensive & audit | `.github/agents/drx-sec.agent.md` | `.github/skills/drx-sec/SKILL.md` |
| `drx-test` | Tests & couverture qualité | `.github/agents/drx-test.agent.md` | `.github/skills/drx-test/SKILL.md` |
| `drx-perf` | Performance & profiling | `.github/agents/drx-perf.agent.md` | `.github/skills/drx-perf/SKILL.md` |
| `drx-doc` | Documentation technique | `.github/agents/drx-doc.agent.md` | `.github/skills/drx-doc/SKILL.md` |
| `drx-drawio-merise` | Diagrammes MERISE Draw.io | `.github/agents/drx-drawio-merise.agent.md` | `.github/skills/drawio-merise/SKILL.md` |
| `drx-drawio-uml` | Diagrammes UML Draw.io | `.github/agents/drx-drawio-uml.agent.md` | `.github/skills/drawio-uml/SKILL.md` |

Les rôles `drx-arch`, `drx-code`, `drx-api`, `drx-data`, `drx-deploy`, `drx-infra`, `drx-mobile`,
`drx-monitor` et `drx-seo` sont prévus par le système DRX mais **n'ont pas de fichier dans ce dépôt** :
l'orchestrateur `drx` traite ces sujets lui-même.

Les instructions générales (rôle, style, revue de code) sont dans `.github/copilot-instructions.md`
(modèle : `.github/templates/copilot-instructions.template.md`).

## Utilisation

- **GitHub Copilot (VS Code)** : sélectionner l'agent dans le sélecteur de modes (fichiers `*.agent.md`).
- **Claude Code** : ce fichier `AGENTS.md` est lu automatiquement ; les skills sont consultables en
  lisant le `SKILL.md` correspondant.

## Mémoire et propositions

Les fichiers de mémoire DRX (`.opencode/drx-memory.md`, `.opencode/drx-proposals.md`) ne sont pas
versionnés (`.opencode` est dans `.gitignore`). Les décisions durables du projet sont dans
`doc/DECISIONS/` (ADR) et `doc/BACKLOG.md`.
