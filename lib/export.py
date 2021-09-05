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


from typing import Union, List, Tuple, Set

from bpy.types import Object

# from .constant import SVG_HEADER_TEMPLATE
# from .object_types.bounding import boundaries
# from .helper.other import write
# from .object_types.cut import Cut
# from .blender.project import Project

from ..__init__ import bl_info


class Export:

    def __init__(self, context) -> None:
        self.context = context

    def run(self) -> Union[str, bool]:
        pass # TODO

