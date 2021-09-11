#  This file is part of Blender_Shaper_Origin.
#
#  Blender_Shaper_Origin is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Blender_Shaper_Origin is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Blender_Shaper_Origin.  If not, see <https://www.gnu.org/licenses/>.

LENGTH_UNIT = "mm"

PRECISION = 3
TOLERANCE = 10 ** -PRECISION


SVG_HEADER = '''\
<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Blender SVG Export by {author} v{version})  -->
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
xml:space="preserve" style="background-color:#d0d0d0" stroke-width="1%"
width="{width:.2f}{unit}" height="{height:.2f}{unit}"          
viewBox="{x0:.2f} {y0:.2f} {w:.2f} {h:.2f}">
<g>
'''
SVG_FOOTER = '</g></svg>\n'

SVG_RECTANGLE = '<rect id="{id}" x="{x}" y="{y}" width="{width:.2f}" height="{height:.2f}" style="{style}" />'
SVG_PATH = '<path id="{id}" d="M{points}Z" style="{style}" />'

SVG_PATH = '<path fill="{fill}" stroke="{stroke}" d="M{points}Z" />'

SVG_LINE = '<line id="{id}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" style="{style}" />'

RED = "#ff0000"
GREEN = "#00ff00"
BLUE = "#0000ff"
GREY = "#7f7f7f"
BLACK = "#000000"
WHITE = "#ffffff"
