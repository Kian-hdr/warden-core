# Building Warden Core

A look at the hardware assembly, folding frame and simulation development.

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

## Simulation development

![Warden Skyline parallel simulation architecture preview, not trained, not certified](simulation-preview.png)

A development preview of parallel simulated environments. The original “not trained” and “not certified” labels are retained; this image is not a trained-policy result.

More behind the scenes: [EDTH Instagram highlight](https://www.instagram.com/stories/highlights/17880192807625231/).

## Development videos

### Parallel simulation preview

[![Parallel simulated scenes, scripted preview](videos/parallel-simulation-preview.jpg)](videos/parallel-simulation-preview.mp4)

[Watch the 8-second preview](videos/parallel-simulation-preview.mp4). Sixteen views illustrate the scene layout using scripted reference motion. The original “not trained” and “not certified” labels remain visible. This is a simulation-development visualization, not successful trained-policy playback.

### Virtual-camera calibration

[![Camera calibration, gravity disabled, not autonomous flight](videos/camera-calibration.jpg)](videos/camera-calibration.mp4)

[Watch the 10-second camera-calibration render](videos/camera-calibration.mp4). The camera moves around an Iris surrogate with gravity disabled. This checks the visual capture setup; it is not a hover-controller or autonomous-flight demonstration. The limitation is labelled throughout the video.

Both videos are compressed viewing copies of retained project renders. No third-party SDK or raw robot asset is bundled. The Iris surrogate is an upstream model, not our physical airframe. See [media credits](../third_party/README.md).

## Gate-course development

### Initial PPO checkpoint playback

[![Initial PPO checkpoint in a gate environment](videos/ppo-initial-debug.jpg)](videos/ppo-initial-debug.mp4)

[Watch the two-second debug recording](videos/ppo-initial-debug.mp4). This is playback of an initial `agent_24.pt` checkpoint from Isaac Drone Racer. The counter refers to 24 configured trainer steps, not laps or complete course runs. The agent remains near the start and the recording contains no usable gate-racing trajectory. It is preserved as an early experiment, with that context labelled in the video.

### Mapped-course chase view

[![Behavioral baseline in a mapped course](videos/course-baseline-chase.jpg)](videos/course-baseline-chase.mp4)

[Watch the ten-second chase view](videos/course-baseline-chase.mp4). This uses a PX4-style behavioral baseline to visualize a mapped course. It is not a learned policy or native PX4 SITL demonstration.

### Mapped-course first-person view

[![First-person view of the behavioral baseline](videos/course-baseline-fpv.jpg)](videos/course-baseline-fpv.mp4)

[Watch the ten-second first-person view](videos/course-baseline-fpv.mp4). This is another camera view of the baseline workflow. Both course videos retain their full original duration, with descriptive overlays added for this public copy. See [upstream credits](../third_party/README.md).

## Outdoor physical-prototype recording

[![Physical prototype hovering outdoors](physical/outdoor-hover.jpg)](videos/prototype-hover.mp4)

[Watch the supplied hover recording](videos/prototype-hover.mp4). The airframe is visibly airborne. The control mode is not documented by the recording, so this is presented as a physical-build demonstration rather than learned-policy evidence. Audio and source metadata were removed from the public copy. The full original remains in the project library.

[More images with engineering explanations](../docs/visual-walkthrough.md).
