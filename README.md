# Annihilation Industries · Warden Core

**A simulation-first robotics project combining learning experiments, computer vision, sensing, physical prototyping and software instrumentation.**

Kian led the project alongside Vincent, Leon and [Constantin](https://github.com/Takane0). Warden Core remains unfinished: the experiments, physical prototype and related sensing study have separate evidence and integration limits.

## Explore by subsystem

Each subsystem contains its own documentation and the public artifacts that belong to it.

| Subsystem | Contributor / workstream | What is inside |
| --- | --- | --- |
| [Simulation and learning](subsystems/simulation/README.md) | Kian | Architecture, training history, reward specifications, evaluation contracts, run identities and simulation footage. |
| [Computer vision](subsystems/perception/README.md) | Vincent | Model explanation, two dated offline experiments, dataset records and known limitations. Private datasets and model artifacts are excluded. |
| [Multi-camera sensing](subsystems/multicamera-sensing/README.md) | Leon | Related Warden Corps study, technical presentation, attributed figures and model limitations. |
| [Airframe and integration](subsystems/airframe/README.md) | Kian and Constantin: joint airframe design; Kian: landing gear; Constantin: Pi–Pixhawk integration and flight-controller programming | Assembly history, prototype photographs and hover footage, landing-leg source, STEP/STL and design checks. |
| [Observability](subsystems/observability/README.md) | Software instrumentation | Runnable Python package, source, tests, synthetic examples and engineering explanation. |

## Project-wide records

[Team contributions](project/team.md) · [History and unfinished work](project/history.md) · [Engineering tour](project/engineering-tour.md) · [Recorded results](project/evidence/README.md) · [Source catalogue](project/evidence/source-records.md) · [Media gallery](project/media-gallery.md)

```text
subsystems/
  simulation/           docs · reward-and-evaluation · results · media
  perception/           docs
  multicamera-sensing/  presentation · figures
  airframe/             docs · landing-gear · media
  observability/        src · tests · examples
project/                team · history · shared evidence · presentations
licensing/              terms · scope notices · model access · third-party notices
tools/                  repository validation
```

Reward specifications belong to the simulation subsystem. All licence notices and access terms are centralized in [licensing](licensing/README.md), with their applicable paths recorded in the [licence map](LICENSE.md).

## Run the public software

The independently runnable component is the [observability package](subsystems/observability/README.md). It records and assesses local timing/resource data; it does not command a vehicle. Its synthetic example deliberately does not produce a hardware pass.

```sh
cd subsystems/observability
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[dev]'
python -m pytest
```

[Repository checks](tools/README.md) · [Reproducibility](project/reproducibility.md)

## Confidentiality and reuse

**Model weights, checkpoints, optimizer state, embeddings and exported policy binaries remain confidential and closed source. They are not included in this repository.** The [model-access policy](licensing/model-access.md), [commercial terms](licensing/commercial-licensing.md) and [contributor rights](licensing/contributors-and-rights.md) remain in force. Project licences do not grant rights in excluded teammate or third-party material.

[Repository structure](project/repository-structure.md) · [Project scope](project/scope.md) · [Kian Tajbakhsh](https://github.com/Kian-hdr)
