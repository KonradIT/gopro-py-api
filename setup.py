from setuptools import setup
import json
with open("README.md", "r") as fh:
    long_description = fh.read()
with open("version.json", "r") as ver:
    version = json.loads(ver.read())['release_version']

setup(name='goprocam',
      version=version,
      description='GoPro WiFi API Wrapper for Python - Compatible with HERO3, HERO3+, HERO4, HERO5, HERO+, HERO6',
      url='http://github.com/konradit/gopro-py-api',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Konrad Iturbe',
      author_email='mail@chernowii.com',
      license='MIT',
      packages=['goprocam'],
      zip_safe=False)
