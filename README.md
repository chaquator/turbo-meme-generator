# Turbo Meme Generator

A tool I made that uses templates and simages (short for "surrogate images") to generate abstract sh*tposts.

Runs on Python 3.4(.2)

## Usage
I'm literally gonna let [argparse](https://docs.python.org/3/library/argparse.html) write this for me because I don't want to waste the effort.
```
usage: turbomeme.py [-h] [-c file] [-sl dir] [-tl dir] [-q int] [-co count] out

Churns memes at the speed of sound

positional arguments:
  out                   Output file (or directory if you're using count)

optional arguments:
  -h, --help            show this help message and exit
  -c file, --config file
                        Specify custom config. The default config is in the
                        same directory as the install.
  -sl dir, --simages-location dir
                        Location for simages
  -tl dir, --templates-location dir
                        Location for templates
  -q int, --quality int
                        Quality of image from 1 (worst) to 95 (best)
  -co count, --count count
                        Specify how many memes you intend to output
```

## Sample images
![WHAT ARE THOOOSE](samples/1.jpg)
![WHAT ARE THOOOSE](samples/2.jpg)
![WHAT ARE THOOOSE](samples/3.jpg)
![WHAT ARE THOOOSE](samples/4.jpg)
![WHAT ARE THOOOSE](samples/5.jpg)
![WHAT ARE THOOOSE](samples/6.jpg)
![WHAT ARE THOOOSE](samples/7.jpg)
![WHAT ARE THOOOSE](samples/8.jpg)

## Install
Check [releases](https://github.com/Chaquator/turbo-meme-generator/releases)

## Build
Run `setup.py` inside the directory to compile it into a single `.exe` file. 

Dependencies (that aren't included in a standard install of Python 3.4.2):
- [py2exe](http://www.py2exe.org/) (only if you plan to build with `setup.py` obviously)
- [Pillow](https://python-pillow.github.io/) (fork of old PIL, updated for Python 3.4)

## Licenses
what?