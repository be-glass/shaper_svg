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

from collections import deque


class Shape(list):

    def clean(self):

        loop0 = self
        loop = loop0 + loop0[0:2]

        clean_shape = Shape([])
        for i in range(len(loop0)):
            clean_shape.append(loop[i])
            if loop[i] == loop[i + 2]:
                i += 2

        return clean_shape

    def delete_at(self, i: int):
        return Shape(self[i + 1:] + self[:i])

    def concat(self, b):
        return Shape(self+b)

    def edge_index(self, edge_tuple, reverse=False):
        shape = self
        edge = list(edge_tuple)
        if reverse:
            edge.reverse()

        length = len(shape)
        if length < 2:
            return -1

        shapeA = shape[length - 1:] + shape[:length - 1]
        shapeB = shape[1:] + shape[0:1]

        search0 = [1 if edge[0] == k else 0 for k in shape]
        search1a = [1 if edge[1] == k else 0 for k in shapeA]
        search1b = [1 if edge[1] == k else 0 for k in shapeB]

        search = []
        for i in range(length):
            search.append(search0[i] + search1a[i] + search1b[i])

        if 2 not in search:
            return -1

        return search.index(2)
