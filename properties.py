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

import bpy

from bpy.props import EnumProperty, StringProperty, PointerProperty
from bpy.types import PropertyGroup, Object


def register() -> None:
    pass

    # bpy.utils.register_class(SceneProperties)
    # bpy.types.Scene.so_cut = PointerProperty(type=SceneProperties)

    btO = bpy.types.Object
    oP = ObjectProperties

    btO.shaper_orientation = oP.orientation
    btO.orientation_object = oP.orientation_object


def unregister() -> None:
    pass

    # bpy.utils.unregister_class(SceneProperties)
    btO = bpy.types.Object

    del btO.shaper_orientation
    del btO.orientation_object


class ObjectProperties(PropertyGroup):
    orientation = EnumProperty(
        name="Orientation",
        description="SO curve cut type",
        items=[('global', 'Global', 'Global Orientation', '', 1),
               ('local', 'Local', 'Local Orientation', '', 2),
               ('object', 'Object', 'Object Orientation', '', 6),
               ],
        default='global',
    )

    orientation_object = PointerProperty(
        name="from",
        description="Orientation from Object",
        type=Object,
    )
