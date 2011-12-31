#!/usr/bin/env python

"""
Copyright (C) 2011 Jeff Kayser

Inkscape extension to create checkerboard patterns


This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from gettext import gettext as _
import inkex
import lxml
import re
import simplestyle
import sys

def draw_square((x, y), (w, h), color, parent, id_=None):
    """Draw a w*h square at (x, y) having color color
    """
    if color == 'none':
        color = color_rgba(0)
    color = rgba_rgbalpha(color)
    style = {'stroke': 'none', 'stroke-width': '1', 'fill': color[0], 'fill-opacity': color[1]}
    attribs = {'style': simplestyle.formatStyle(style), 'height': str(h), 'width': str(w), 'x': str(x), 'y': str(y)}
    if id_ is not None:
        attribs.update({'id': id_})
    obj = inkex.etree.SubElement(parent, inkex.addNS('rect', 'svg'), attribs)

def draw_grid((x, y), rows, cols, size, color1, color2, parent):
    """Draw a rows*cols checkboard grid at (x, y) with square size of size*size,
    with squares having alternating colors color1 and color2
    """
    # Group like-colors
    group1 = inkex.etree.SubElement(parent, 'g', {'id': 'diagonal1'})
    group2 = inkex.etree.SubElement(parent, 'g', {'id': 'diagonal2'})
    for row in range(int(rows)):
        for col in range(int(cols)):
            alternate = (col + row) % 2 == 0
            color = color1 if alternate else color2
            group = group1 if alternate else group2
            id_ = 'cell{0}x{1}'.format(col, row)
            draw_square((x + col * size, y + row * size), (size, size), color, group, id_)

def color_rgba(color, include_hash=True):
    """Convert numeric color to a #RRGGBBAA hex string
    """
    # Correct for signed integer underflow
    if color < 0:
        color = 2**32 + color
    return ('#' if include_hash else '') + hex(color)[2:].zfill(8)

def rgba_rgbalpha(color):
    """Convert #RRGGBBAA hex string to tuple of #RRGGBB hex string and opacity percentage
    """
    if re.match('#?[0-9a-fA-F]{8}', color) is None:
        color = '#00000000'
    offset = 7 if color[0] == '#' else 6
    return color[:offset], float(int(color[offset:offset+2], 16)) / 0xff

class Checkerboard(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--tab", action="store", type="string", dest="tab")
        self.OptionParser.add_option("--color1", action="store", type="int", dest="color1")
        self.OptionParser.add_option("--color2", action="store", type="int", dest="color2")
        self.OptionParser.add_option("--size", action="store", type="float", dest="size")
        self.OptionParser.add_option("--rows", action="store", type="int", dest="rows")
        self.OptionParser.add_option("--cols", action="store", type="int", dest="cols")

    def effect(self):
        layer = self.current_layer
        parent = self.document.getroot()
        group = inkex.etree.SubElement(parent, 'g', {'id': 'checkerboard'})

        rows = self.options.rows
        cols = self.options.cols
        size = self.options.size
        color1 = color_rgba(self.options.color1 or 0x000000ff)
        color2 = color_rgba(self.options.color2 or 0x00000000)
        # Center checkerboard within visible viewport
        x, y = self.view_center[0] - cols * size / 2, self.view_center[1] - rows * size / 2
        draw_grid((x, y), rows, cols, size, color1, color2, group)

if __name__ == '__main__':
    e = Checkerboard()
    e.affect()
