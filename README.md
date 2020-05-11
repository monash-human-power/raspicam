# MHP_Raspicam
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors)

This repo contains code used to run the Monash Human Power camera system. It is write protected to ensure it is always left in a working state.

## Installation

Firstly, you'll need to create a `.env` file containing either `MHP_CAMERA=primary` or `MHP_CAMERA=secondary`. Optionally, you may set the overlay run when the physical switch on the display is toggled by modifying `config.json`. An example of this file's contents could be `{ "activeOverlay": "overlay_all_stats.py" }`.

To install dependencies, you will need [poetry](https://python-poetry.org/docs/#installation) installed on your computer. Our guide to poetry may be found on [notion](https://www.notion.so/Getting-Started-with-Poetry-770384c0205c4cf39c4bf7216060d5d2).

At this point in time, you'll also need Python 3.7 installed. Python 3.6 may also work (untested), but right now, the OpenCV version we are using does not have a build available for Python 3.8. I used [pyenv](https://github.com/pyenv/pyenv) to quickly switch between python versions.

With that done, dependencies may be installed using `poetry install --dev`. You may then start a shell with `poetry shell`.

## Usage

*You must be in a poetry shell to run any scripts/tests (see above).*

### Overlay development

Any overlay (e.g. `overlay_top_strip.py`) may be run from the terminal with Python. You will need a computer with a webcam. The `--host` argument can be used to specify an MQTT broker.

### Running on Raspberry Pi displays

Overlays may be run from the terminal, as before. However, for use on the bike, you should have `switch_demo.py` and `orchestrator.py` running on startup. Currently, this is run automatically by `/etc/rc.local` on the display Pis, but they may also be run manually.

## Tests
1) orchestrator_test.py = Test script for orchestrator.py. Enter 'pytest' in the terminal to run the test file
2) mqtt_message_test.py = Test script that sends messages to the camera overlay. Initially run mqtt_message_test.py along with mqtt_test.py from the DAS repo, Finally run overlay_all_stats.py.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/pdgra1"><img src="https://avatars3.githubusercontent.com/u/33751672?v=4" width="100px;" alt="pdgra1"/><br /><sub><b>pdgra1</b></sub></a><br /><a href="https://github.com/monash-human-power/raspicam/commits?author=pdgra1" title="Code">💻</a></td>
    <td align="center"><a href="https://khlee.me"><img src="https://avatars3.githubusercontent.com/u/18709969?v=4" width="100px;" alt="Angus Lee"/><br /><sub><b>Angus Lee</b></sub></a><br /><a href="https://github.com/monash-human-power/raspicam/commits?author=khanguslee" title="Code">💻</a></td>
    <td align="center"><a href="https://twitter.com/harsilspatel"><img src="https://avatars1.githubusercontent.com/u/25992839?v=4" width="100px;" alt="Harsil Patel"/><br /><sub><b>Harsil Patel</b></sub></a><br /><a href="https://github.com/monash-human-power/raspicam/commits?author=harsilspatel" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/lakshjaisinghani"><img src="https://avatars3.githubusercontent.com/u/45281017?v=4" width="100px;" alt="Laksh Jaisinghani"/><br /><sub><b>Laksh Jaisinghani</b></sub></a><br /><a href="https://github.com/monash-human-power/raspicam/commits?author=lakshjaisinghani" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/hallgchris"><img src="https://avatars2.githubusercontent.com/u/17876556?v=4" width="100px;" alt="Christopher Hall"/><br /><sub><b>Christopher Hall</b></sub></a><br /><a href="https://github.com/monash-human-power/raspicam/commits?author=hallgchris" title="Code">💻</a></td>
  </tr>
</table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!