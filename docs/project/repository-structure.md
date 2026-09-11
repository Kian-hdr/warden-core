# Repository structure

The repository separates executable material, evidence, explanations and legal terms. Documentation is organized by topic; generated media and CAD stay with their artifact families.

```text
warden-core/
├── README.md                  Start here
├── CONTRIBUTORS.md            Team entry point
├── docs/
│   ├── project/               Team, history, scope, sources, development
│   ├── simulation/            Architecture, training, runtime, lineage
│   ├── perception/            Vincent’s datasets and dated experiments
│   ├── subsystems/            Four workstream explanations
│   ├── presentations/         Public briefs and attributed figures
│   └── media/                 Visual walkthrough
├── policies/                  Reward mathematics and experiment contracts
├── results/                   Results, source catalogue, team evidence ledger
├── software/                  Runnable package, source, examples and tests
├── hardware/                  Parametric source, CAD, previews and design notes
├── media/                     Videos, photographs, posters and provenance
├── licensing/                 Legal terms, licence texts and model access
├── third_party/               Upstream notices
└── tools/                     Repository and media validation
```

## Placement rules

- Put reward and evaluation specifications in `policies/`. Legal/access policies belong in `licensing/`.
- Keep executable software beside its tests and usage instructions. Keep CAD source and exports in `hardware/`.
- Put historical result data and provenance in `results/`; explain the result in its subject chapter.
- Give each new team claim an inspected source, date and explicit limit. Update the team ledger and source catalogue when evidence changes.
- Keep model weights, checkpoints, embeddings, private endpoints and rights-unresolved datasets outside the repository.
- Retain only small compatibility entry pages for previously shared URLs. They point to the canonical chapter and do not duplicate its contents.

The source catalogue’s older `chapter-...` anchors are stable identifiers. Their labels may retain previous file names while their destination links point into this structure.

## Validation

From the repository root, run `python3 tools/validate_repository.py` to check local references, source destinations, JSON, media hashes and prohibited model-file extensions. See [development](development.md) and the [software README](../../software/README.md) for package tests. These checks do not validate private models, physical behavior or legal ownership.
