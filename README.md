# GoPro API for Python

[![GitHub issues](https://img.shields.io/github/issues/konradit/gopro-py-api.svg)](https://github.com/konradit/gopro-py-api/issues) [![Github All Releases](https://img.shields.io/badge/download-gh-red.svg)](https://github.com/KonradIT/gopro-py-api/releases) [![PyPi Version](http://img.shields.io/pypi/v/goprocam.svg)](https://pypi.python.org/pypi/goprocam)

Unofficial GoPro API Library for Python - connect to GoPro cameras via WiFi.
![](http://i.imgur.com/kA0Rf1b.png)

## Notice:

Project has been updated to support Hero10 Black + OpenGoPro v2 + USB control. Further is needed to support these features:

- Python3.8 typing
- Custom exceptions
- Integration tests
- BLE support (using [gopro-ble-py](https://github.com/konradit/gopro-ble-py))
- Hero9 (v1.21 & 1.22 fw) / Hero10 (OpenGoPro v2) USB identifier Autodiscovery
- Stacktraces
- More robust examples, with boilerplate code ready for use

Project covers a decade worth of camera releases, naturally something might've broken as development focuses on the newer cameras. Hopefully nothing broke.

Acknowledgments to GoPro for the OpenGoPro API spec release.

\- @konradit
### Compatibility:

- HERO3
- HERO3+
- HERO4 (including HERO Session)
- HERO+
- HERO5 (including HERO5 Session)
- HERO6
- Fusion 1
- HERO7 (Black)
- HERO8 Black
- MAX
- HERO9 Black
- HERO10 Black

## WiFi vs USB:

Hero3..Hero8 (incl. MAX/Fusion/Session) all use WiFi (and some use Bluetooth) for controls, media management, status updates and live preview

Hero9 Black and Hero10 Black have Webcam functionality, and Hero10 Black is officially exposing the API server over USB Ethernet with full camera control capabilities

Hero9 Black requires using an older firmware to get ability to take photos. See [the compatibility chart](https://github.com/KonradIT/goprowifihack/blob/master/HERO9/HERO9-Functionality-Compatibility-Chart.md)

### Installation

From PyPi:

```
pip install goprocam
```

Git (unstable):

```bash
git clone http://github.com/konradit/gopro-py-api
cd gopro-py-api
python setup.py install
```

**Tested on Python 3.6.0** -- **works on Linux and Windows and Mac**

### Quick start:

Connect your camera to your computer via WiFi (WiFi on the camera must be on!)

```python
from goprocam import GoProCamera, constants

goproCamera = GoProCamera.GoPro()

goproCamera.shoot_video(10)
```

### Examples:

See [examples](/examples) for examples on how to use this API.

### Documentation:

Documentation is available: [docs](/docs)

### Video screencap:

- HERO4 Black: https://vimeo.com/209079783
- HERO4 Session: https://vimeo.com/209129019
- HERO3 Black: https://vimeo.com/209181246
- HERO5 Black: https://vimeo.com/235135652
- HERO7 Black: https://www.youtube.com/watch?v=i-X4fPVfoW0
