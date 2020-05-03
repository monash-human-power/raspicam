# MHP_Raspicam
[![All Contributors](https://img.shields.io/badge/all_contributors-5-orange.svg?style=flat-square)](#contributors)

This repo contains code used to run the Monash Human Power camera system. The `master` branch is write protected to ensure it is always left in a working state.

## Important-changes log
  - Added `requirements.txt` to work with virtualenv (see Dependencies below)
  - Code for V1.5 is in `Legacy` folder, code for V2 is in `CameraOverlay` folder
  - Refactor GLOBAL_DATA -> DAS_DATA and REQUIRED_DATA -> POWER_MODEL_DATA

## Dependencies
To install OpenCV, RPi.GPIO, paho-mqtt on Raspberry Pi: **haven't tested on fresh Raspberry Pi**
  - install virtual env `sudo pip3 install virualenv`
  - in MHP_Raspicam folder, run 
    ```
    virtualenv venv
    source venv/bin/activate   
    ```
  - install python dependencies `pip3 install -r requirements.txt`
  - have an `.env` file in the `CameraOverlay` folder with the variable `MHP_CAMERA` set to either `primary` or `secondary` and `MHP_BIKE` set to `V2` or `V3`.
  - create an ``config.json` file in the `CameraOverlay` directory with attribute `activeOverlay` that points to the overlay file that is currently active, for instance it could be `{ "activeOverlay": "overlay_all_stats.py" }`

## Tests

Located under `CameraOverlays/tests`. Enter 'pytest' in the terminal to run all tests.

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