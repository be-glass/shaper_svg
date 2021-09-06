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


from typing import Union  # , List, Tuple, Set

from mathutils import Vector
from .constant import SVG_HEADER, SVG_RECTANGLE, LENGTH_UNIT, STYLE_GUIDE
from ..__init__ import bl_info
from .helper.other import write
from .object_types.bounding import boundaries


# from bpy.types import Object

# from .constant import SVG_HEADER_TEMPLATE
# from .object_types.bounding import boundaries
# from .helper.other import write
# from .object_types.cut import Cut
# from .blender.project import Project


class Export:

    def __init__(self, context) -> None:



        self.active = context.active_object
        self.selected = context.selected_objects
        self.scene = context.scene

        scale = self.scene.unit_settings.scale_length
        min, max = boundaries(self.selected, self.active)
        self.v0: Vector = 1000 * scale * min
        self.v1: Vector = 1000 * scale * max
        self.w = (self.v1.x - self.v0.x)
        self.h = (self.v1.y - self.v0.y)
        self.version = '.'.join([str(i) for i in bl_info['version']])
        self.unit = LENGTH_UNIT

    def run(self) -> Union[str, bool]:
        if not self.selected:
            return "Nothing to export"

        if self.active.shaper_orientation == 'object' and not self.active.orientation_object:
            return "Orientation object missing"




        svg_src = self.svg_top()
        dir_name = "."
        # file_name = f'{dir_name}/{name}.svg'
        file_name = f'{dir_name}/shaper.svg'

        err = write(svg_src, file_name)

        return err if err else False

    def svg_top(self) -> str:
        return \
            self.svg_header() + \
            self.svg_body() + \
            self.svg_footer()

    def svg_header(self) -> str:
        return SVG_HEADER.format(
            x0=self.v0.x, w=self.v1.x - self.v0.x, y0=-self.v1.y, h=self.v1.y - self.v0.y,
            width=self.w, height=self.h, unit=self.unit,
            version=self.version, author=bl_info['author'],
        )

    def svg_footer(self) -> str:
        return '</svg>\n'

    def svg_body(self) -> str:
        return \
            self.svg_boundary_guide() + \
            ''.join([self.svg_boundary_loops(item) for item in self.selected])

    def svg_boundary_guide(self) -> str:
        return SVG_RECTANGLE.format(
            x=self.v0.x, y=self.v0.y,
            width=self.w, height=self.h,
            style=STYLE_GUIDE,
            unit=self.unit,
        )

    def svg_boundary_loops(self, item) -> str:
        return item.name
