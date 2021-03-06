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

from bpy import utils
from bpy.types import Panel
from typing import List, Type


def panels() -> List[Type[Panel]]:
    return [
        BG_PT_Shaper_SVG,
    ]


def register() -> None:
    for widget in panels():
        utils.register_class(widget)


def unregister() -> None:
    for widget in panels():
        utils.unregister_class(widget)


class Shaper_Panel(Panel):
    bl_category = "Shaper SVG"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


class BG_PT_Shaper_SVG(Shaper_Panel):
    bl_label = "Export Shaper SVG"

    def draw(self, context) -> None:
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = True

        obj = context.object

        if obj and obj.type != 'MESH':
            layout.label(text="Select a mesh object.")

        else:
            # Widgets

            layout.label(text=obj.name)
            layout.prop(obj, "shaper_orientation")

            if obj.shaper_orientation == "object":
                layout.prop(obj, "orientation_object")

            layout.operator("mesh.shaper_export_svg", text="Export Cuts")
