# GoPro API for Python 

[![GitHub issues](https://img.shields.io/github/issues/konradit/gopro-py-api.svg)](https://github.com/konradit/gopro-py-api/issues) [![Github All Releases](https://img.shields.io/badge/download-gh-red.svg)](https://github.com/KonradIT/gopro-py-api/releases) [![PyPi Version](http://img.shields.io/pypi/v/goprocam.svg)](https://pypi.python.org/pypi/goprocam)

Unofficial GoPro API Library for Python - connect to GoPro cameras via WiFi.
![](http://i.imgur.com/kA0Rf1b.png)


### Compatibility:

- HERO3
- HERO3+
- HERO4 (including HERO Session)
- HERO+
- HERO5 (including HERO5 Session)
- HERO6 
- Fusion 1
- HERO7 (Black)

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

* HERO4 Black: https://vimeo.com/209079783
* HERO4 Session: https://vimeo.com/209129019
* HERO3 Black: https://vimeo.com/209181246
* HERO5 Black: https://vimeo.com/235135652
* HERO7 Black: https://www.youtube.com/watch?v=i-X4fPVfoW0