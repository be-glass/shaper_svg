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

# import bmesh
# import bpy
#
# from .other import select_active, active_object

from mathutils import Matrix




def transformation(obj) -> Matrix:
    if obj.shaper_orientation == 'global':
        return obj.matrix_world
    elif obj.shaper_orientation == 'object' and obj.orientation_object:
        rwm = obj.orientation_object.matrix_world.copy()
        rwm.invert()
        return rwm @ obj.matrix_world

    else:
        return Matrix()
