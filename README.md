# MHP Raspicam
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors)

This repo contains code used to run the Monash Human Power camera system. The `master` branch is write protected to ensure it is always left in a working state.

## Installation

1. **Setup `.env` file**

    Duplicate `.env.example` into `.env` and alter the environment variables accordingly. This file is how the overlay knows whether it is primary or secondary, the bike it is on, the broker IP and the screen resolution.

2. **Configure `config.json`**

    Optionally, you may set the overlay to run when the physical switch on the display is toggled by modifying `config.json`. An example of this file's contents could be `{ "activeOverlay": "overlay_all_stats.py" }`.

3. **Install Python 3.7 with `pyenv`**

    At this point in time, you'll also need Python 3.7 installed, as currently, the OpenCV version we are using does not have a build available for Python 3.8. [pyenv](https://github.com/pyenv/pyenv) may be used to quickly switch between python versions. To do this,

    - Install `pyenv`.
        - Linux installation (including Pi) [here](https://github.com/pyenv/pyenv-installer). You may need to install these dependencies from [here](https://github.com/pyenv/pyenv/wiki/Common-build-problems) (use Debian dependencies fo the Raspbery Pi)
        - macOS installation: See [pyenv's github](https://github.com/pyenv/pyenv)
        - Windows installation: See [pyenv-win](https://github.com/pyenv-win/pyenv-win)
    - Install Python 3.7 with `pyenv install 3.7.7`,
    - and finally, set it as your current python version with `pyenv local 3.7.7`.

4. **Install OpenCV dependencies**

    You will likely need to install some dependencies for OpenCV to run, especially if you are on a Raspberry Pi. To do this, run
    ```bash
    sudo apt install libgtk-3-0 libavformat58 libtiff5 libcairo2 libqt4-test libpango-1.0-0 libopenexr23 libavcodec58 libilmbase23 libatk1.0-0 libpangocairo-1.0-0 libwebp6 libqtgui4 libavutil56 libjasper1 libqtcore4 libcairo-gobject2 libswscale5 libgdk-pixbuf2.0-0
    ```

5. **Install poetry and python dependencies**

    To install dependencies, you will need [poetry](https://python-poetry.org/docs/#installation) installed on your computer.

    With that done, `raspicam` dependencies may be installed using `poetry install --dev`.

6. **Install and enable `systemd` services (optional)**

    If you are setting up `raspicam` on the actual display Pis, enable and start the `raspicam` services so that `raspicam` begins on startup.

    ```bash
    # Install the raspicam services
    ./service/install.sh
    # Enable running on boot, and start running now
    systemctl --user enable --now raspicam-orchestrator
    systemctl --user enable --now raspicam-switch
    ```

## Usage

**Important:** *You must be in a poetry shell to run any scripts/tests.* To start a poetry shell, run `poetry shell`. You may exit the shell at any time with `exit`.

### Overlay development

Any overlay (e.g. `overlay_top_strip.py`) may be run from the terminal with Python. If your computer does not have a webcam, you may replace the video feed with a static background specified with the `--bg` option. The `--host` argument can be used to specify an MQTT broker.

### Running on Raspberry Pi displays

If you are trying run an overlay over VNC, you will need to enable direct capture mode on the Pi's VNC server. Right click on the VNC logo in the Pi's system tray, click `Options -> Troubleshooting -> Enable direct capture mode -> OK`.

Overlays may be run from the terminal, as before. However, for use on the bike, you should have `switch.py` and `orchestrator.py` running on startup using systemd services as described in [Installation](#installation). Once this is setup, you can view the output of the two scripts with

```bash
systemctl --user status raspicam-orchestrator
```

You may also find `systemctl`'s `start`, `stop`, `restart` and `disable` commands useful.

## Tests

Located under `tests`. Enter `pytest` in the terminal to run all tests.

## Utilities
`mqtt_message_test.py`: Script that sends messages to the camera overlay. First, run `mqtt_message_test.py` along with `mqtt_test.py` from the DAS repo, Finally run `overlay_all_stats.py`.

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