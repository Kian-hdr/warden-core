# Team contributions

Warden Core is unfinished. This is the documented work of Kian, Leon, Vincent and Konstantin, including completed outputs, historical experiments and unresolved integration work. Documentation completeness does not mean the prototype is complete.

The earlier source records spell Konstantin’s name **Constantin** and are retained as historical attribution. This page uses Kian’s current spelling, Konstantin, while retaining the historical spelling in the attribution record. No additional full names or account identities are inferred.

| Contributor | Contribution and retained outputs | Evidence and limits |
| --- | --- | --- |
| **Kian Tajbakhsh** | Project leadership; Brev/Isaac environment and simulation experiments; policy and evaluation contracts; observability software; evidence preservation, rendering, landing-leg CAD development and presentation/repository integration. | [Simulation](../subsystems/isaac-agent.md), [software](../../software/engineering.md), [CAD](../../hardware/engineering.md), [results](../../results/README.md). Simulation and digital CAD checks are separate from physical qualification. |
| **Vincent** | Offline computer-vision dataset workflow, frozen-feature linear classifiers, CPU training, two recorded evaluations, confusion/error analysis and explicit uncertainty handling. | [Two experiment records](../perception/experiments.md). The August 29 ingest was Vincent’s solo work; Leon’s initially planned support does not establish a contribution to it. |
| **Leon** | Related Warden Corps sensing concept, physics-study direction, technical/presentation material and figures. The retained package also records valuation and investor-presentation work. | [Sensing study](../subsystems/multicamera-sensing.md), [presentation record](../presentations/warden-corps-camera-study.md). Modeling, synthetic studies and pitch work do not establish a deployed camera network or integration with the classifier or flight controller. |
| **Konstantin / Constantin** | Physical prototype assembly, folding airframe and flight-controller/electronics integration work. | [Hardware integration history](../subsystems/hardware-integration.md), [photographs and hover](../../media/physical/README.md). The recording’s control mode is undocumented; later Pi software work is not automatically attributed to the hardware owner. |

## How the contributions connect

Kian’s simulation work established a place to study autonomous navigation and preserve experiment evidence. Vincent’s work evaluated what a still-image classifier could distinguish. Leon’s related study explored multi-view sensing and communicated its assumptions through a technical briefing. Konstantin assembled the physical prototype and worked through its electronics integration. The observability and CAD packages provide independently inspectable software and geometry.

These are separate workstreams. There is no source-backed claim here that Leon’s camera model, Vincent’s classifier, a trained Isaac policy and the physical airframe operated together as an autonomous system.

## Coverage and provenance

The [team work ledger](../../results/team-work.json) maps each contribution to its source records and public chapter. Source IDs refer to the [archived document catalogue](../../results/source-records.md), which retains document dates and hashes. The catalogue identifies the source version, not proof that a historical runtime still operates today.

The [project history and unfinished work](history.md) describes the remaining gaps. [Contributor rights](../../licensing/contributors-and-rights.md) governs reuse; credit does not imply a transfer of ownership. Model weights, checkpoints, embeddings and exported policies remain confidential and closed source under the unchanged [model-access policy](../../licensing/model-access.md).
