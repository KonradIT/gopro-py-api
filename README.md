# GoPro API for Python 

Unofficial GoPro API Library for Python - connect to HERO3/3+/4/5/+ via WiFi.

![](http://i.imgur.com/kA0Rf1b.png)


###Compatibility:

- HERO3
- HERO3+
- HERO4 (including HERO Session)
- HERO+
- HERO5

###Installation

```bash
pip install goproapi
```

Or from source

```bash
git clone http://github.com/konradit/gopropy
cd gopropy
python setup.py install
```

###Usage:

```python
gopro = GoProCamera()
gopro.shutter(start)
time.sleep(10)
gopro.shutter(stop)
```

