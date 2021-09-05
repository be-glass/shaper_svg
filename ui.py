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

from bpy import utils
from bpy.types import Panel
from typing import List, Type

# from .lib.blender.compartment import Compartment


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

        # soc = context.scene.so_cut
        obj = context.object
        scene = context.scene

        # Widgets
        layout.prop(obj, "shaper_orientation")

        if obj:

            if obj.shaper_orientation == "object":
                layout.prop(obj, "orientation_object")
                layout.label(text="hi")

            layout.operator("mesh.shaper_export_svg", text="Export Cuts")
            layout.label(text=obj.name)
