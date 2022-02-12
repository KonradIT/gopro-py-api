from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='goprocam',
      version="4.2.0",
      description='GoPro WiFi API Wrapper for Python - Compatible with HERO3, HERO3+, HERO4, HERO5, HERO+, HERO6, HERO7, HERO8, HERO9, HERO10, MAX, FUSION',
      url='http://github.com/konradit/gopro-py-api',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='Konrad Iturbe',
      author_email='mail@chernowii.com',
      license='MIT',
      packages=['goprocam'],
      zip_safe=False)
