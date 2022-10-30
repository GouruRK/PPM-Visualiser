# Bitmap Visualiser

This is one of my very first school project, which was firstly made in association with [Gabriel Heude](https://github.com/ScartoLeni).

You can find the original subject [here](original%20subject.md).



## Table of content
- [Bitmap Visualiser](#bitmap-visualiser)
  - [Table of content](#table-of-content)
  - [Features](#features)
  - [How to install](#how-to-install)
  - [Next step ?](#next-step-)

## Features
* This project support PBM, PGM and PPM file format (ascii or binary, so versions P1, P2, P3, P4, P5 and P6)
* You can rotate the image directly from command line, or by pressing 'r'
* You can zoom on the image from command line (not really a zoom, but by considering that 1 pixel of the image represent x pixel on your screen)
* Convert a file to an other PPM format

## How to install

```bash
# Clone git repository
git clone https://github.com/GouruRK/PPM-Visualiser.git

# Go into the repo
cd PPM-Visualiser

# Launch
python3 main.py <file>
```

Optionnals arguments :

```bash
# Show help message
python3 main.py -h

# Launch with the file
python3 main.py <file>

# Show file parameters
python3 main.py <file> -i

# "Augment pixel size" as a zoom
python3 main.py <file> -p <size>

# Rotate
python3 main.py <file> -r <0 (default) | 90 | 180 | 270>

# Create a new file by converting an existing file to a specific format
python3 main.py <file> -c <P1 | P2 | P3 | P4 | P5 | P5>

# Indicate the name of the new converted file
python3 main.py <file> -c <P1 | P2 | P3 | P4 | P5 | P5> -o <name>
```

Note that windows user may type `py` instead of `python3`

## Next step ?

As indicated in the original subject, there are many ways to improve this project (this improvement may come lately), but here are some of them :
* Add color filters
* Enable the user to modify the file directly from the screen and saved it as a new file

___

Check out my other projects on github : [Gouru](https://github.com/GouruRK/).