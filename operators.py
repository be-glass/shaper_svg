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
import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class
# from mathutils import Matrix
from typing import List, Type, Set
from .lib.export import Export


def operators() -> List[Type[Operator]]:
    return [
        MESH_OT_shaper_export_svg,
    ]


def register() -> None:
    for widget in operators():
        register_class(widget)


def unregister() -> None:
    for widget in operators():
        unregister_class(widget)


class MESH_OT_shaper_export_svg(Operator):
    bl_idname = "mesh.shaper_export_svg"
    bl_label = "Shaper Export"
    bl_description = "Export SVG for Shaper Origin"

    def execute(self, context) -> Set[str]:

        result = Export(context).run()

        if result == False:
            self.report({'INFO'}, ' Export done')
            return {'FINISHED'}
        elif result:
            self.report({'WARNING'}, result)
            return {'FINISHED'}
        else:
            self.report({'ERROR'}, "Export Failed")
            return {'CANCELLED'}
