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

from typing import List


class Shape(list):

    def clean(self):

        shape = self
        shape1 = Shape([])
        for i in shape.range():
            if shape.mod(i - 1) != shape.mod(i + 1):
                shape1.append(shape[i])

        shape2 = Shape([])
        for i in shape1.range():
            if shape1[i] != shape1.mod(i + 1):
                shape2.append(shape1[i])

        return shape2

    def mod(self, i):
        return self[i % len(self)]

    def range(self):
        return range(len(self))

    def delete_at(self, i: int):
        return Shape(self[i + 1:] + self[:i])

    def concat(self, b):
        return Shape(self + b)

    def edge_index(self, edge_tuple, reverse=False):
        shape = self
        edge = list(edge_tuple)
        if reverse:
            edge.reverse()

        length = len(shape)
        if length < 2:
            return -1

        search0 = shape.find_value(edge[0])
        search1 = shape.find_value(edge[1])

        search = []
        for i in range(length):
            search.append(search0[i]
                          + search1[(i - 1) % length]
                          + search1[(i + 1) % length]
                          )

        if 2 not in search:
            return -1

        return search.index(2)

    def find_value(self, value) -> List[int]:
        return [1 if value == k else 0 for k in self]
