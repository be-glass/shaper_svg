#   This file is part of Shaper_SVG.
#  #
#   Shaper_SVG is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  #
#   Shaper_SVG is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with Shaper_SVG.  If not, see <https://www.gnu.org/licenses/>.
#

from mathutils import Vector
from typing import Tuple


def boundaries(context, obj, wm) -> Tuple[Vector, Vector]:
    x = []
    y = []
    z = []
    scale = context.scene.unit_settings.scale_length

    bb = obj.bound_box
    for p in range(8):
        v = wm @ Vector([bb[p][0], bb[p][1], bb[p][2]])

        x.append(v[0])
        y.append(v[1])
        z.append(v[2])

    mini = 1000 * scale * Vector([min(x), min(y), min(z)])
    maxi = 1000 * scale * Vector([max(x), max(y), max(z)])

    return mini, maxi
