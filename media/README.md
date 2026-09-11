# Building Warden Core

A look at the hardware assembly, folding frame and simulation development.

Rights differ by file. Project-created simulation media is available noncommercially under CC BY-NC-SA 4.0, subject to upstream notices. The physical photographs and hover footage are excluded pending confirmation of the photographer or videographer's rights. See the exact [media rights map](LICENSE.md).

## Assembly and wiring

![Open frame and wiring during assembly](assembly-wiring.jpg)

The frame opened up during assembly, showing the wiring, motor mounts and electronics.

## Open configuration

![Prototype with arms open](prototype-open.jpg)

The prototype laid out on a table with its arms open.

## Folded configuration

![Prototype with arms folded](prototype-folded.jpg)

The same build with its arms folded alongside the frame.

These photographs document assembly and configuration. They do not establish flight performance or autonomous operation, and they do not show validation of the separate LL-11 landing-leg design.

More behind the scenes: [EDTH Instagram highlight](https://www.instagram.com/stories/highlights/17880192807625231/).

## Development videos

### Model-based autonomous corridor flight

[![Model-based autonomous trajectory controller](videos/model-based-autonomous-corridor.png)](videos/model-based-autonomous-corridor.mp4?raw=1)

[Watch the 15-second autonomous corridor demonstration](videos/model-based-autonomous-corridor.mp4?raw=1). The physically simulated Iris surrogate travels 15.485 metres through the recorded fictional corridor scenario. Runtime and independent QA recorded 450/450 frames, zero collisions, zero command saturations, zero safety interventions and successful technical, motion, visual and provenance review.

### Verified simulation montage

[![Warden Iris simulation montage](videos/verified-simulation-montage.png)](videos/verified-simulation-montage.mp4?raw=1)

[Watch the 34.5-second simulation reel](videos/verified-simulation-montage.mp4?raw=1). Title cards separate exterior camera calibration, mapped-course chase and first-person views. All three source clips passed full decode and representative-frame review.

### Virtual-camera calibration

[![Isaac Sim virtual-camera calibration](videos/camera-calibration.jpg)](videos/camera-calibration.mp4?raw=1)

[Watch the 10-second camera-calibration render](videos/camera-calibration.mp4?raw=1). The exterior camera moves around the Iris surrogate and demonstrates the direct virtual-camera capture workflow.

Both videos are compressed viewing copies of retained project renders. No third-party SDK or raw robot asset is bundled. The Iris surrogate is an upstream model, not our physical airframe. See [media credits](../third_party/README.md).

## Gate-course development

### Mapped-course chase view

[![Behavioral baseline in a mapped course](videos/course-baseline-chase.jpg)](videos/course-baseline-chase.mp4?raw=1)

[Watch the ten-second chase view](videos/course-baseline-chase.mp4?raw=1). The verified PX4-style behavioral baseline records the mapped course from an external tracking camera.

### Mapped-course first-person view

[![First-person view of the behavioral baseline](videos/course-baseline-fpv.jpg)](videos/course-baseline-fpv.mp4?raw=1)

[Watch the ten-second first-person view](videos/course-baseline-fpv.mp4?raw=1). This is another camera view of the baseline workflow. Both course videos retain their full original duration, with descriptive overlays added for this public copy. See [upstream credits](../third_party/README.md).

## Outdoor physical-prototype recording

[![Physical prototype hovering outdoors](physical/outdoor-hover.jpg)](videos/prototype-hover.mp4?raw=1)

[Watch the supplied hover recording](videos/prototype-hover.mp4?raw=1). The airframe is visibly airborne and demonstrates the assembled physical prototype in flight. The public copy retains the full visual duration; the full original remains in the project library.

[More images with engineering explanations](../docs/visual-walkthrough.md).

[Complete flight-media provenance and measurements](../docs/flight-media.md).
