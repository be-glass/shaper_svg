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
    STROKE_BLUE, STROKE_RED, STROKE_GREEN, SHAPER_MAX_DEPTH, EXTERIOR_CUT, INTERIOR_CUT, POCKETING_CUT
from ..__init__ import bl_info
from .helper.other import write
from .object_types.bounding import boundaries
from mathutils import Matrix


class Export:

    def __init__(self, context) -> None:

        self.context = context
        if not context.active_object:
            return

        self.piece = context.active_object
        self.version = '.'.join([str(i) for i in bl_info['version']])
        self.unit = LENGTH_UNIT
        self.piece_wm = self.transformation()

        # drawing boundaries
        self.piece_min, self.piece_max = boundaries(context, self.piece, self.piece_wm)
        self.w = (self.piece_max.x - self.piece_min.x)
        self.h = (self.piece_max.y - self.piece_min.y)
        self.tick = (self.w + self.h) / 20

    def run(self) -> Union[str, bool]:

        if not self.context.active_object:
            return "There is no active object."

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
            self.svg_interior_loops(),
            self.svg_footer()
        ])

    def svg_header(self) -> str:
        x = self.piece_min.x - self.tick
        y = -self.piece_max.y - self.tick
        w = self.w + 2 * self.tick
        h = self.h + 2 * self.tick

        return SVG_HEADER.format(
            x0=x, w=self.w + 2 * self.tick, y0=y, h=self.h + 2 * self.tick,
            width=w, height=h, unit=self.unit,
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
                x1=self.piece_min.x - self.tick,
                x2=self.piece_max.x + self.tick,
                y1=0,
                y2=0,
                style=STROKE_RED
            ) + \
            SVG_LINE.format(
                x1=0,
                x2=0,
                y1=-self.piece_min.y + self.tick,
                y2=-self.piece_max.y - self.tick,
                style=STROKE_GREEN
            )

    def svg_exterior_loops(self) -> str:

        item = self.piece

        loops = Contour(item, self.piece_max.z, self.piece_wm).get_loops()

        points = []
        for loop in loops.values():
            coords = [self.piece_wm @ item.data.vertices[vid].co for vid in loop]
            points.append(' '.join(['{x:.2f},{y:.2f}'.format(x=v.x, y=-v.y) for v in coords]))

        return '\n'.join([SVG_POLYGON.format(points=points, style=EXTERIOR_CUT) for points in points])

    def transformation(self, cut_obj=None) -> Matrix:

        obj = cut_obj if cut_obj else self.piece

        if self.piece.shaper_orientation == 'global':
            return obj.matrix_world

        elif self.piece.shaper_orientation == 'object' and self.piece.orientation_object:
            rwm = self.piece.orientation_object.matrix_world.copy()
            rwm.invert()
            return rwm @ obj.matrix_world

        else:
            return Matrix()

    def svg_interior_loops(self) -> str:

        svg = ""
        dg = self.context.evaluated_depsgraph_get()

        for modifier in self.piece.modifiers:
            if modifier.type == 'BOOLEAN' \
                    and modifier.operation == 'DIFFERENCE':

                if modifier.operand_type == 'OBJECT' \
                        and modifier.object:

                    cut_items = [modifier.object]

                elif modifier.operand_type == 'COLLECTION' \
                        and modifier.collection:

                    cut_items = modifier.collection.objects

                else:
                    return svg

                for cut_item in cut_items:

                    evaluated_item = cut_item.evaluated_get(dg)
                    cut_wm = self.transformation(cut_obj=evaluated_item)

                    mini, maxi = boundaries(self.context, evaluated_item, cut_wm)

                    if mini.z < self.piece_max.z < maxi.z:

                        loops = Contour(evaluated_item, mini.z, cut_wm).get_loops()

                        for loop in loops.values():
                            coords = [cut_wm @ evaluated_item.data.vertices[vid].co for vid in loop]

                            points = ' '.join(['{x:.2f},{y:.2f}'.format(x=v.x, y=-v.y) for v in coords])
                            cut_type = POCKETING_CUT if mini.z > self.piece_min.z else INTERIOR_CUT

                            svg += SVG_POLYGON.format(points=points, style=cut_type) + '\n'

        return svg
