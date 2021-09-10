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


from typing import Union

from .Contour import Contour
from .constant import SVG_HEADER, SVG_RECTANGLE, LENGTH_UNIT, STYLE_GUIDE, SVG_POLYGON, STYLE_CUT, SVG_LINE, \
    STROKE_BLUE, STROKE_RED, STROKE_GREEN
from .helper.mesh_helper import transformation
from ..__init__ import bl_info
from .helper.other import write
from .object_types.bounding import boundaries




class Export:

    def __init__(self, context) -> None:

        self.context = context
        self.piece = context.active_object
        self.version = '.'.join([str(i) for i in bl_info['version']])
        self.unit = LENGTH_UNIT
        self.piece_wm = transformation(self.piece)

        # drawing boundaries
        self.piece_min, self.piece_max = boundaries(context, self.piece)
        self.w = (self.piece_max.x - self.piece_min.x)
        self.h = (self.piece_max.y - self.piece_min.y)

    def run(self) -> Union[str, bool]:

        if self.piece.shaper_orientation == 'object' and not self.piece.orientation_object:
            return "Orientation object missing"

        svg_src = self.svg_top()
        dir_name = "."
        # file_name = f'{dir_name}/{name}.svg'
        file_name = f'{dir_name}/shaper.svg'

        err = write(svg_src, file_name)

        return err if err else False

    def svg_top(self) -> str:
        return '\n'.join([
            self.svg_header(),
            self.svg_boundary_guide(),
            self.svg_exterior_loops(),
            # self.svg_interior_loops(),
            self.svg_footer()
        ])

    def svg_header(self) -> str:
        return SVG_HEADER.format(
            x0=self.piece_min.x, w=self.w, y0=-self.piece_max.y, h=self.h,
            width=self.w, height=self.h, unit=self.unit,
            version=self.version, author=bl_info['author'],
        )

    def svg_footer(self) -> str:
        return '</svg>\n'

    def svg_boundary_guide(self) -> str:
        return \
            SVG_RECTANGLE.format(
                x=self.piece_min.x, y=-self.piece_max.y,
                width=self.w, height=self.h,
                style=STROKE_BLUE,
            ) + \
            SVG_LINE.format(
                x1 = self.piece_min.x,
                x2 = self.piece_max.x,
                y1 = 0,
                y2 = 0,
                style = STROKE_RED
            ) + \
            SVG_LINE.format(
                x1 = 0,
                x2 = 0,
                y1 = -self.piece_min.y,
                y2 = -self.piece_max.y,
                style = STROKE_GREEN
            )

    def svg_exterior_loops(self) -> str:

        item = self.piece
        
        loops = Contour(item, self.piece_max.z, self.piece_wm).get_loops()

        points = []
        for loop in loops.values():
            coords = [self.piece_wm @ item.data.vertices[vid].co for vid in loop]
            points.append(' '.join(['{x:.2f},{y:.2f}'.format(x=v.x, y=-v.y) for v in coords]))

        return '\n'.join([SVG_POLYGON.format(points=points, style=STYLE_CUT) for points in points])



    # def svg_interior_loops(self) -> str:
    #
    #     points = []
    #
    #     for modifier in self.piece.modifiers:
    #         if modifier.operation == 'DIFFERENCE' and modifier.operand_type == 'OBJECT':
    #
    #             item = modifier.object
    #
    #             if item:
    #
    #                 mini, maxi = boundaries(self.context, item)
    #
    #                 loops = Contour(item, mini.z, self.piece_wm).get_loops()
    #
    #                 for loop in loops.values():
    #                     coords = [self.piece_wm @ item.data.vertices[vid].co for vid in loop]
    #                     points.append(' '.join(['{x:.2f},{y:.2f}'.format(x=v.x, y=v.y) for v in coords]))
    #
    #     return '\n'.join([SVG_POLYGON.format(points=points, style=STYLE_CUT) for points in points])
