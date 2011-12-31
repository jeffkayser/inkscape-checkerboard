# Checkerboard for Inkscape

This is a simple [Inkscape](http://inkscape.org/) extension that will generate customizable checkboards.

## Installing

Copy ```checkerboard.py``` and ```checkerboard.inx``` to the following typical directory:

- Linux - ```~/.config/inkscape/extensions``` (for your user only); ```/usr/share/inkscape/extensions``` (for all users)
- OS X - ```/Applications/Inkscape.app/Contents/Resources/extensions```
- Windows - ```C:\Program Files\Inkscape\share\extensions```

## Usage

1. Open *Extensions* > *Render* > *Checkerboard...* from the Inkscape menu
2. On the *Params* tab, choose the cell size (size of constituent the squares) and number of rows and columns
3. On the *1st color* and *2nd color* tabs, select the colors for the two sets of squares
4. Click **Apply**

The checkerboard will be centered in your current viewport. It is in a group with an id of ```checkerboard```, which consists of two subgroups of each set of cells, named ```diagonal1``` and ```diagonal2```. This facilitates changing the colors and other properties of each set quickly and easily. Within the diagonal groups, the cells have an id of ```cellAxB```, where A is the column and B is the row in which they appear. A and B are zero-indexed, and increase left-to-right and top-to-bottom respectively. The intent of this was to hopefully simplify any kind of scripted processing you may want to do on the result.

