#!/bin/bash -e

./fademaid.py -i woman.png -d woman.fade

exit 0

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
