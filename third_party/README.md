# Media credits and notices

The simulation media was rendered in NVIDIA Isaac Sim. The Iris surrogate was obtained through Pegasus Simulator v4.5.1, pinned at `db7bf43a5b26b0dd56ec18d0afb682383862fbd3`.

The upstream Iris asset credits Lorenz Meier and Thomas Gubler, with the original model created by Thomas Gubler and sourced from PX4 SITL Gazebo. Its asset-specific licence is BSD 3-Clause, copyright 2012–2023 PX4 Development Team. Pegasus Simulator is also distributed under BSD 3-Clause, copyright 2023 Marcelo Fialho Jacinto.

- [Iris asset notice](PX4-Iris-LICENSE.txt)
- [Pegasus Simulator notice](Pegasus-LICENSE.txt)
- [Pinned upstream Iris licence](https://github.com/PegasusSimulator/PegasusSimulator/blob/db7bf43a5b26b0dd56ec18d0afb682383862fbd3/docs/licenses/assets/iris-license.rst)
- [Pinned Pegasus licence](https://github.com/PegasusSimulator/PegasusSimulator/blob/db7bf43a5b26b0dd56ec18d0afb682383862fbd3/LICENSE)

The project’s procedural scene composition, cameras and presentation are distinct from the upstream robot model. This repository publishes rendered video, not the raw USD asset or simulator software. Names identify contributors and tools; no endorsement is implied. The project reuse notice does not replace these third-party notices.

## Early PPO debug recording

The early checkpoint recording uses [Isaac Drone Racer](https://github.com/kousheekc/isaac_drone_racer/tree/d530f67768d53701454f406e4da967e0e9c30842) at revision `d530f67768d53701454f406e4da967e0e9c30842`. The pinned project contains the gate and five-inch-drone assets used by its default task and is licensed under BSD 3-Clause, copyright 2025 Kousheek Chakraborty. The [upstream notice](Isaac-Drone-Racer-LICENSE.txt) is retained. The clip is initial checkpoint playback, not a demonstration of completed gate racing. No model weights or raw asset files are distributed here.
