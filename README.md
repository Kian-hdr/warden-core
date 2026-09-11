# Annihilation Industries · Warden Core

Engineering from our Warden Core project: tools for understanding compute pipelines and a parametric landing-leg prototype.

I led Annihilation Industries at the European Defense Tech Hackathon in Hamburg, bringing together simulation, software, hardware development and the project presentation. This repository collects two parts of that work that can be explored independently.

<img src="media/prototype-open.jpg" alt="Warden Core prototype with arms open" width="480">

*Prototype assembly on the workbench. [Build photos and simulation preview](media/README.md).*

## Explore the work

| Project | What you can inspect |
| --- | --- |
| [Pipeline observability](software/) | Python tools for capturing timing and resource data, assembling logs and assessing a compute pipeline, with automated tests. |
| [LL-11 landing leg](hardware/) | Parametric CAD source, STEP and STL exports, and the design assumptions behind the connected multibay prototype. |
| [Development approach](docs/development.md) | How we separate implementation, digital checks and physical results. |

![LL-11 leg-only digital prototype](hardware/images/LL11_leg.png)

*LL-11 CAD preview. Physical fit and load capacity have not been established.*

## Where the project stands

Warden Core began as a simulation-first flight research project. The wider development archive includes simulation experiments, checkpoints and prototype material. A saved model or a rendered clip does not establish reliable autonomous flight, and we have not established physical autonomous flight or transfer of a learned policy to hardware.

The software here records and evaluates pipeline data. It does not connect to a flight controller or command a vehicle. The landing leg is a digital prototype with further fabrication and bench work ahead.

## Behind the scenes

My [EDTH Instagram highlight](https://www.instagram.com/stories/highlights/17880192807625231/) shows the project behind the scenes. Instagram may require sign-in. These stories document the build process; the technical scope and checks are described alongside the files here.

Kian Tajbakhsh · [GitHub](https://github.com/Kian-hdr)

See [repository scope](docs/scope.md) for what is included and the reuse notice.
