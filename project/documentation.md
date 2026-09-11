# Warden Core documentation

[Team contributions](team.md) · [History and unfinished work](history.md) · [Repository structure](repository-structure.md)

Annihilation Industries brought together simulation, computer vision, software tooling and a physical prototype. These pages describe the work completed and how the pieces were developed.

[Subsystem map](../subsystems/README.md) · [Presentation materials](presentations/README.md) · [Verified results](evidence/README.md)

| Read | Covers |
| --- | --- |
| [Project and engineering progress](overview.md) | The workstreams, concrete outputs and project leadership. |
| [Verified engineering results](evidence/README.md) | Completed real-Isaac integration, dynamics, replay, scale, training and media results. |
| [System architecture](../subsystems/simulation/docs/architecture.md) | The cloud, simulator, observation, control, reward and evidence architecture. |
| [Flight and simulation media](evidence/media-provenance.md) | Exact video roles, measurements, provenance and source identities. |
| [NVIDIA Brev and Isaac Sim](../subsystems/simulation/docs/simulation.md) | The cloud development setup, simulator stack and media workflow. |
| [Acro-racing reward policy](../subsystems/simulation/reward-and-evaluation/reward-policy.md) | The complete recorded reward equation, bounded shaping ledger, terminal proof and coefficient ranges. |
| [Vault source coverage](source-coverage.md) | Which project records are summarized or distributed here. |
| [Training and evaluation](../subsystems/simulation/docs/training.md) | Checkpointed experiments, repeatability and the distinction between learning and visualization. |
| [Computer vision](../subsystems/perception/docs/README.md) | Vincent’s offline baseline and the dataset workflow. |
| [Dataset record](../subsystems/perception/docs/dataset.md) | Dataset versions, recorded partitions and publication boundaries. |
| [Software engineering](../subsystems/observability/engineering.md) | Data contracts, timestamps, hashing, assessment logic and failure behavior. |
| [Computational geometry studies](../subsystems/airframe/landing-gear/computational-geometry.md) | Four separately recorded PicoGK studies and their digital evidence. |
| [Experiment artifacts](../subsystems/simulation/docs/artifact-lineage.md) | Contracts, checkpoint/export lineage, recovery packages and media review. |
| [Public source records](evidence/source-records.md) | Document identities, dates and publication forms behind the chapters. |
| [Hardware engineering](../subsystems/airframe/landing-gear/engineering.md) | Geometry construction, topology changes, mesh/export checks and numerical screening. |
| [Visual walkthrough](visual-walkthrough.md) | Assembly, recorded hover, course views and CAD layer images. |
| [Reproducibility](reproducibility.md) | Artifact identity, source-to-public transformations and remote readback. |
| [Development approach](development.md) | How source, checks, outputs and handoffs fit together. |
| [Media gallery](media-gallery.md) | Autonomous-flight, simulator and physical-prototype media. |
| [Source notes and acknowledgements](sources.md) | Evidence records and the tools used. |

Runnable software is in [software](../subsystems/observability/). The editable landing-leg design is in [hardware](../subsystems/airframe/landing-gear/).

Model weights and exported policy artifacts remain closed source. See the [model-access policy](../licensing/model-access.md) for commercial, education and academic requests.
