# FadeMaid

**Fade me like one of your French girls.**

FadeMaid is an editor for screen-values mapped to a multicolor bitmap for Commodore 64.
It runs on 64 bit versions of Linux, MacOS, Windows and other systems supported by Python. 


![screenshot](./screenshot.png)

# Why FadeMaid?

reason | description
---|---
open source | easy to modify and to improve, any useful contribution is highly welcome
portable | available on Linux, MacOS, Windows and any other system supported by Python3
easy to use | editing is a bliss, instant preview


# Usage

For a list of quick keyboard shortcuts and other information see file [cheatsheet.md](cheatsheet.md) or the full documentation in /doc.


# Commandline Usage

    FadeMaid v2.0 [build 211113-164348] *** by WolF
    usage: fademaid.py [-h] [-i IMAGE_FILE] [-d DATA_FILE]

    You can edit char-wise values with this.

    optional arguments:
      -h, --help            show this help message and exit
      -i IMAGE_FILE, --image_file IMAGE_FILE
                            background image filename
      -d DATA_FILE, --data_file DATA_FILE
                            fademaid data filename

    Example: ./fademaid.py -i image.png -d data.bin



# File Format

The data is stored as a continuous 1000 bytes corresponding to the 40x25 screen of a Commodore 64 bitmap.



# Authors

* fieserWolF/Abyss-Connection - *code* - [https://github.com/fieserWolF](https://github.com/fieserWolF) [https://csdb.dk/scener/?id=3623](https://csdb.dk/scener/?id=3623)
* The Mysterious Art/Abyss-Connection - *logo graphics* - [https://csdb.dk/scener/?id=3501](https://csdb.dk/scener/?id=3501)

# Getting Started

FadeMaid comes in two flavors:

- standalone executable for 64-bit systems Linux (MacOS/Darwin and Windows might follow) (see [releases](https://github.com/fieserWolF/ditheridoo/releases))
- Python3 script

## Run the standalone executable

Just download your bundle at [releases](https://github.com/fieserWolF/fademaid/releases) and enjoy.
Keep in mind that only 64bit systems are supported as I could not find a 32bit system to generate the bundle.


### Note for Windows users

If some antivirus scanner puts FadeMaid into quarantine because it suspects a trojan or virus, simply put it out there again.
It isn`t harmful, I used PyInstaller to bundle the standalone executable for you.
Unfortunately, the PyInstaller bootloader triggers a false alarm on some systems.
I even tried my best and re-compiled the PyInstaller bootloader so that this should not happen anymore. Keep your fingers crossed ;)


### Note for MacOS users

Your system might complain that the code is not signed by a certificated developer. Well, I am not, so I signed the program on my own. 
```
"FadeMaid" can`t be opened because it is from an unidentified developer.
```
You need to right-click or Control-click the app and select “Open”.



## Run the Python3 script directly

Download _ditheridoo.py_ and the whole _resource_ - directory into the same folder on your computer.

### Prerequisites

At least this is needed to run the script directly:

- python 3
- python tkinter module
- python "The Python Imaging Library" (PIL)

Normally, you would use pip like this:
```
pip3 install tk pillow
```

On my Debian GNU/Linux machine I use apt-get to install everything needed:
```
apt-get update
apt-get install python3 python3-tk python3-pil python3-pil.imagetk
```


# Changelog

## Future plans


- maybe: implement multiple layers

Any help and support in any form is highly appreciated.

If you have a feature request, a bug report or if you want to offer help, please, contact me:

[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)


## Changes in 2.01

- control buttons
- save data as - function
- toggle showing the grid and the values
- auto mode for continuous drawing with increasing or decreasing values
- about window
- various bug-fixes and optimizations


## Changes in 2.0

- complete rewrite from scratch in python


## Changes in 1.0

- initial release


# License

_FadeMaid editor for Commodore 64 screen-values._

_Copyright (C) 2021 fieserWolF / Abyss-Connection_

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

See the [LICENSE](LICENSE) file for details.

For further questions, please contact me at
[http://csdb.dk/scener/?id=3623](http://csdb.dk/scener/?id=3623)
or
[wolf@abyss-connection.de](wolf@abyss-connection.de)

For Python3, The Python Imaging Library (PIL), Tcl/Tk and other used source licenses see file [LICENSE_OTHERS](LICENSE_OTHERS).


