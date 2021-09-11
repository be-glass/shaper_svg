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

from . import ui, properties, operators

# https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo

bl_info = {
    "name": "Shaper Origin SVG Export",
    "author": "Be Glass",
    "blender": (2, 92, 0),
    "version": (0, 1, 0),
    "location": "3D View > Sidebar",
    "description": "SVG Export for Shaper Origin cutting lines",
    "category": "Mesh",
}

files = [ui, properties, operators]


def register() -> None:
    [file.register() for file in files]


def unregister() -> None:
    [file.unregister() for file in files]
