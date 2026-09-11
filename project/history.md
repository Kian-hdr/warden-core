# Project history and unfinished work

The engineering record includes completed experiments and substantial unfinished integration. Dates below identify historical records, not current service availability or a newly performed hardware test.

| Record date | Work documented | What the evidence establishes |
| --- | --- | --- |
| August 28–30, 2026 | Kian’s simulation planning, environment setup, contract/dynamics checks, replay, scale profiling, partial training and media preservation | [Source-linked experiment results](evidence/README.md); the retained Stage 0 tranche is not a fully trained flight policy. |
| August 29, 2026 | Vincent’s earlier public-stills baseline | A recorded 64-image offline evaluation and uncertainty behavior; temporal video consistency was not implemented. |
| August 29, 2026 | Physical prototype build report | Kian reported assembly and mostly completed power wiring, with motor-direction/layout work outstanding. This report was human-stated. |
| August 30–September 3, 2026 | Leon’s Warden Corps study and presentation revisions | Retained modeling, figures and technical/business-presentation work; no operational network validation. |
| August 31, 2026 | Vincent’s collected-image probe | A different 291-image recorded test, with documented duplicate leakage and later preservation gaps. |
| September 1, 2026 | LL-11 landing-leg design/print-run record | A separate CAD development track; digital geometry and slicing do not establish finished printing, installed fit or load qualification. |
| September 4, 2026 | Companion-computer commissioning and interface work | Historical host/dashboard checks; connectivity loss after flight-controller connection remained unresolved in the inspected record. |
| September 11, 2026 | Public repository and documentation editions | Selected software, CAD, reviewed media and source-linked explanations; confidential and rights-restricted originals stay outside the repository. |

## What remains unfinished

- **Learning:** accepted training updates and valid checkpoint records do not establish a completed curriculum, final learned policy or autonomous full-course acceptance.
- **Perception:** the two still-image experiments are not a clean, fixed external benchmark. Video consistency and camera/weather transfer were not demonstrated.
- **Sensing:** the multi-camera physics model and synthetic tracking prototype remain separate. The methods record says the tracker is not connected to the camera signal-to-noise calculation.
- **Hardware:** recorded hover does not identify its control mode. No evidence here establishes that the trained policy, classifier and airframe flew together. Host connectivity diagnosis is distinct from flight readiness.
- **CAD:** LL-11 geometry is public and editable; installed fit, material behavior and load capacity need their own evidence.
- **Reproduction:** confidential models and rights-unresolved data are not downloadable. Public software checks cover the standalone observability package, not the private simulation or perception runtime.

The repository records these limits alongside the team’s achievements. See [team coverage](team.md), [reproducibility](reproducibility.md) and [source coverage](source-coverage.md).
