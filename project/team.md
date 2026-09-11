# Team contributions

Warden Core is unfinished. This is the documented work of Kian, Leon, Vincent and Constantin, including completed outputs, historical experiments and unresolved integration work. Documentation completeness does not mean the prototype is complete.

Vincent’s GitHub profile is [vwiczk](https://github.com/vwiczk). Constantin’s GitHub profile is [Takane0](https://github.com/Takane0). Kian confirmed both account mappings on 2026-09-11.

| Contributor | Contribution and retained outputs | Evidence and limits |
| --- | --- | --- |
| **Kian Tajbakhsh** | Project leadership; Brev/Isaac environment and simulation experiments; policy and evaluation contracts; observability software; evidence preservation, rendering, joint airframe design with Constantin, landing-gear development and presentation/repository integration. | [Simulation](../subsystems/simulation/README.md), [software](../subsystems/observability/engineering.md), [CAD](../subsystems/airframe/landing-gear/engineering.md), [results](evidence/README.md). Simulation and digital CAD checks are separate from physical qualification. |
| **[Vincent · vwiczk](https://github.com/vwiczk)** | Offline computer-vision dataset workflow, frozen-feature linear classifiers, CPU training, two recorded evaluations, confusion/error analysis and explicit uncertainty handling. | [Two experiment records](../subsystems/perception/docs/experiments.md). The August 29 ingest was Vincent’s solo work; Leon’s initially planned support does not establish a contribution to it. |
| **Leon** | Related Warden Corps sensing concept, physics-study direction, technical/presentation material and figures. The retained package also records valuation and investor-presentation work. | [Sensing study](../subsystems/multicamera-sensing/README.md), [presentation record](../subsystems/multicamera-sensing/presentation/camera-study.md). Modeling, synthetic studies and pitch work do not establish a deployed camera network or integration with the classifier or flight controller. |
| **[Constantin](https://github.com/Takane0)** | Joint airframe design with Kian, physical prototype assembly, Raspberry Pi–Pixhawk integration and flight-controller programming/configuration. | [Hardware integration history](../subsystems/airframe/docs/integration.md), [photographs and hover](../subsystems/airframe/media/README.md). Kian confirmed the integration/programming contribution; the hover recording’s control mode remains undocumented. |

## How the contributions connect

Kian’s simulation work established a place to study autonomous navigation and preserve experiment evidence. Vincent’s work evaluated what a still-image classifier could distinguish. Leon’s related study explored multi-view sensing and communicated its assumptions through a technical briefing. Kian and Constantin worked together on the airframe design: Kian developed the landing gear, while Constantin handled the Raspberry Pi–Pixhawk integration and programmed/configured the flight controller. The observability and CAD packages provide independently inspectable software and geometry.

These are separate workstreams. There is no source-backed claim here that Leon’s camera model, Vincent’s classifier, a trained Isaac policy and the physical airframe operated together as an autonomous system.

## Coverage and provenance

The [team work ledger](evidence/team-work.json) maps each contribution to its source records and public chapter. Source IDs refer to the [archived document catalogue](evidence/source-records.md), which retains document dates and hashes. The catalogue identifies the source version, not proof that a historical runtime still operates today.

The [project history and unfinished work](history.md) describes the remaining gaps. [Contributor rights](../licensing/contributors-and-rights.md) governs reuse; credit does not imply a transfer of ownership. Model weights, checkpoints, embeddings and exported policies remain confidential and closed source under the unchanged [model-access policy](../licensing/model-access.md).
