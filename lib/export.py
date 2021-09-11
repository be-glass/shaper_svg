#  This file is part of Shaper_SVG.
#
#  Shaper_SVG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Shaper_SVG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Shaper_SVG.  If not, see <https://www.gnu.org/licenses/>.


import os
from typing import Union

from .Contour import Contour
from .constant import SVG_HEADER, SVG_RECTANGLE, LENGTH_UNIT, SVG_PATH, SVG_LINE, \
    SVG_FOOTER, RED, GREEN, BLUE, BLACK, GREY, WHITE
from ..__init__ import bl_info
from .helper.other import write
from .object_types.bounding import boundaries
from mathutils import Matrix
import bpy


def get_directory():
    path = bpy.path.abspath("//shaper_svg")
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


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

        if not bpy.data.is_saved:
            return "Please save blend file to define project path!"

        svg_src = self.svg_top()

        path = get_directory()
        if not os.path.isdir(path):
            return f"Cannot create directory {path}!"

        err = write(svg_src, self.get_filename(path))

        return err if err else False

    def get_filename(self, path) -> object:

        blend = bpy.path.display_name_from_filepath(bpy.data.filepath)

        if self.piece.shaper_orientation == 'object' and self.piece.orientation_object:
            orientation = '_' + self.piece.orientation_object.name
        elif self.piece.shaper_orientation == 'local':
            orientation = '_local'
        else:
            orientation = ''

        return os.path.join(path, f"{blend}_{self.piece.name}{orientation}.svg")

    def svg_top(self) -> str:
        return '\n'.join([
            self.svg_header(),
            # self.svg_boundary_guide(),
            self.svg_origin(),
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
        return SVG_FOOTER

    def svg_origin(self) -> str:
        return SVG_PATH.format(
            id='origin',
            points=f"0,0 {self.tick},0 0,{-2 * self.tick}",
            fill=RED,
            stroke=RED
        )

    def svg_exterior_loops(self) -> str:

        item = self.piece

        loops = Contour(item, self.piece_max.z, self.piece_wm).get_loops()

        points = []
        for loop in loops.values():
            coords = [self.piece_wm @ item.data.vertices[vid].co for vid in loop]
            points.append(' '.join(['{x:.2f},{y:.2f}'.format(x=v.x, y=-v.y) for v in coords]))

        return '\n'.join([SVG_PATH.format(
            id=item.name,
            points=points,
            fill=BLACK,
            stroke=BLACK
        ) for points in points])

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

                        cut_depth = round(self.piece_max.z - mini.z, 1)

                        loops = Contour(evaluated_item, mini.z, cut_wm).get_loops()

                        loop_id = 0
                        for loop in loops.values():
                            coords = [cut_wm @ evaluated_item.data.vertices[vid].co for vid in loop]

                            points = ' '.join(['{x:.2f},{y:.2f}'.format(x=v.x, y=-v.y) for v in coords])

                            if mini.z > self.piece_min.z:  # POCKETING CUT
                                fill = GREY
                                stroke = GREY
                            else:  # INTERIOR CUT
                                fill = WHITE
                                stroke = BLACK

                            name = f"{evaluated_item.name}({cut_depth})"
                            if loop_id > 0:
                                name += f".{loop_id}"
                            loop_id += 1

                            svg += SVG_PATH.format(
                                id=name,
                                points=points,
                                fill=fill,
                                stroke=stroke
                            ) + '\n'

        return svg

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
