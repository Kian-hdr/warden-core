# Physical airframe and electronics

[Constantin · Takane0](https://github.com/Takane0) led the physical FPV prototype and the flight-controller/electronics integration work. The retained media shows the folding airframe, motors, wiring, electronics packaging and outdoor hover.

## Integration layers

```mermaid
flowchart TB
    A[Folding airframe and motors] --> P[Power distribution and ESC wiring]
    P --> F[Flight controller and orientation]
    F --> C[Companion compute and camera]
    C --> T[Telemetry and recorded system state]
```

The physical work gives the autonomy and perception software a real packaging target: the airframe must carry power electronics, flight control, compute, sensing and telemetry inside a constrained folding structure.

| View | Record |
| --- | --- |
| Assembly and wiring | ![Open frame and wiring](../media/physical/assembly-wiring.jpg) |
| Open configuration | ![Prototype open](../media/physical/prototype-open.jpg) |
| Folded configuration | ![Prototype folded](../media/physical/prototype-folded.jpg) |
| Outdoor hover | [![Prototype hovering](../media/physical/outdoor-hover.jpg)](../media/physical/prototype-hover.mp4?raw=1) |

The separate LL-11 package adds editable parametric landing-leg geometry, STEP/STL exchange files and digital integrity checks. See [hardware](../hardware/README.md).
