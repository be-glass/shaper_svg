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


from bpy.types import Object


def write(content, file_name) -> str:
    try:
        with open(file_name, 'w') as file:
            file.writelines(content)
    except IOError as err:
        return str(err)

    return False  # no error


def clean_dictionary(dictionary: Object) -> dict:
    a = dictionary
    b = {k: v for k, v in dictionary if v}

    return {k: v for k, v in dictionary if v}
