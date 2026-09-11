# Subsystem-first repository structure

The repository is organized by the component a reader wants to understand. Documentation and artifacts live with their subsystem; project-wide context and legal terms have their own homes.

| Home | What belongs here |
| --- | --- |
| `subsystems/simulation/` | Simulation architecture and history, reward/evaluation specifications, run identities, videos and posters. |
| `subsystems/perception/` | Classifier explanation, datasets and two dated offline experiment records. |
| `subsystems/multicamera-sensing/` | Related sensing study, its presentation, figures and figure manifest. |
| `subsystems/airframe/` | Assembly/integration documentation, physical media, landing-gear CAD source and exports. |
| `subsystems/observability/` | Runnable Python source, tests, examples and package documentation. |
| `project/` | Team, history, scope, cross-subsystem results/source catalogue, engineering tour and project brief. |
| `licensing/` | Licence texts, scoped notices, contributor rights, commercial/model access and third-party notices. |
| `tools/` | Offline repository and artifact validation. |

## Placement rules

1. Choose the owning subsystem first; add its documentation, source and artifacts there.
2. Put reward specifications in `subsystems/simulation/reward-and-evaluation/`. There is no generic policies folder.
3. Keep **all licence notices in `licensing/`**, except the repository-root `LICENSE.md` entry point. Link to a notice from a subsystem; do not duplicate it beside technical files.
4. Keep shared evidence in `project/evidence/`; subsystem-specific run records and media stay inside the owning subsystem.
5. Keep confidential weights, datasets, credentials and private implementations out of the public tree.

The earlier `docs/`, `hardware/`, `software/`, `policies/`, `results/`, `media/` and `third_party/` roots have been replaced. Repository links and source destinations use the new paths. Historical chapter anchors in the source catalogue remain stable. Previously bookmarked file paths can be located through [the subsystem index](../subsystems/README.md) or Git history.

[Validate the repository](../tools/README.md) · [Licence map](../LICENSE.md)
