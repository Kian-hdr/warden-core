# Warden Core engineering brief

## 1. A simulation-first autonomy stack

Warden Core connects parallel simulation, policy learning, deterministic evaluation, offline perception, physical integration and evidence preservation.

## 2. The Isaac Sim agent

The agent receives a four-frame, 260-value observation history at 50 Hz. Its action enters a bounded rate-control and quad-X allocation layer while Isaac Sim advances physics at 250 Hz.

[How the Isaac agent works](../../subsystems/simulation/README.md)

## 3. Reward and policy mathematics

The published policy specification contains the complete dense shaping equation, nine coefficients, clearance barrier, bounded episodic ledger, terminal reward and terminal-dominance proof.

[Open the reward policy](../../subsystems/simulation/reward-and-evaluation/reward-policy.md)

## 4. Verified simulator execution

The completed dynamics gate covered 800 cases, 526,800 telemetry records and 400 exact replay pairs. The GPU scale profile measured 15 real-Isaac runs and selected 2,048 parallel environments at 64,094.408 transitions per second.

[Inspect verified results](../evidence/README.md)

## 5. Autonomous corridor demonstration

[![Model-based autonomous corridor flight](../../subsystems/simulation/media/posters/corridor-flight.png)](../../subsystems/simulation/media/autonomous/corridor-flight.mp4?raw=1)

The 15-second direct Isaac Sim render records 450 frames, 15.485 metres of travel, zero collisions, zero command saturations and zero safety interventions in the recorded scenario.

## 6. Computer vision

Vincent’s separate offline baseline uses frozen ResNet18 features and a linear six-class head trained on CPU. Its held-out record reports 0.891 accuracy and 0.863 macro-F1 on 64 images.

[How the computer-vision model works](../../subsystems/perception/README.md)

## 7. Multi-camera sensing

Leon’s related Warden Corps study models five 4K monochrome cameras, 3-of-5 coincidence and sparse voxel ray crossing to turn multiple image bearings into a shared 3D point and worldline.

[Explore the camera-network study](../../subsystems/multicamera-sensing/presentation/camera-study.md)

## 8. Physical prototype

Kian and Constantin jointly designed the airframe. Kian developed the landing gear; Constantin handled Raspberry Pi–Pixhawk integration and flight-controller programming/configuration. The retained gallery shows assembly, folding configuration and outdoor hover.

[Physical integration](../../subsystems/airframe/docs/integration.md)

## 9. Evidence chain

Every public result connects source revision, configuration, runtime identity, telemetry, media and checksum records.

[Run identities](../../subsystems/simulation/results/run-identities.md) · [Source records](../evidence/source-records.md)

## 10. Team and access

| Contributor | Recorded contribution |
| --- | --- |
| Kian | Project lead, joint airframe design, landing gear, Isaac/Brev autonomy, evaluation, evidence, media and presentation integration |
| Vincent | Supervised computer-vision baseline |
| Leon | Warden Corps multi-camera sensing study and presentation |
| [Constantin](https://github.com/Takane0) | Joint airframe design; Raspberry Pi–Pixhawk integration and flight-controller programming/configuration |

Public software and documentation are available under the repository’s [licensing map](../../licensing/README.md). Model weights remain closed source under the [model-access policy](../../licensing/model-access.md).
