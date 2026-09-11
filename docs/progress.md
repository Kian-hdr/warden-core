# Engineering progress

I led Annihilation Industries’ Warden Core project at the European Defense Tech Hackathon in Hamburg. The work brought together cloud simulation, experimental machine learning, hardware assembly and the presentation of the project. My role covered the simulation and evaluation workflow, engineering coordination, retained development records, video and pitch material. Vincent developed the separate computer-vision baseline.

## From idea to working development tools

The project produced more than presentation material. Its archive contains source repositories, frozen experiment configurations, recorded simulation outputs, model checkpoints and a physical prototype. This public collection makes the independently useful parts accessible and explains how the wider development work was organized.

| Workstream | Concrete output |
| --- | --- |
| Cloud simulation | A Brev-hosted Isaac Sim / Isaac Lab development environment, recorded runtime identities and repeatable experiment structure. |
| Training workflow | Checkpointed experimental runs with configuration, logs and evaluation records retained alongside the outputs. |
| Computer vision | An offline still-image baseline using pretrained visual features and a separately trained classification head, with saved training and error records. |
| Software | A standalone pipeline observability package with four command-line tools and 44 passing tests at publication. |
| Hardware | A photographed folding-frame prototype, wiring and assembly work, recorded outdoor hover, plus a separate editable LL-11 landing-leg design. |
| Communication | Build photographs, simulation-development media and a public explanation of the engineering process. |

## Connecting the workstreams

The simulation and perception work were separate experiments. Perception results were not evidence that the flight system could recognize objects in operation. Likewise, a simulation checkpoint was not evidence that the physical prototype could fly autonomously. Keeping those boundaries explicit helped define what the next integration step would need to demonstrate.

The [build gallery](../media/README.md) shows the physical assembly in open and folded configurations. The [CAD package](../hardware/) preserves the LL-11 source and exchange files. The [software package](../software/) can be explored with synthetic data without connecting any vehicle.
