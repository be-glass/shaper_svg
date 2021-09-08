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
from statistics import mean

from lib.Shape import Shape
from lib.constant import TOLERANCE, PRECISION

from lib.helper.other import clean_dictionary


class Contour:
    def __init__(self, item, z, wm) -> None:
        self.item = item
        self.z = z
        self.wm = wm
        polygons = self.get_horizontal_polygons()
        self.lut_poly_shape = create_lut_polygon_to_vertices(polygons)
        self.lut_edge_poly = create_lut_edge_to_polygons(polygons)
        self.lut_poly_poly = {p.index: p.index for p in polygons}

    def get_loops(self) -> dict:

        for edge, poly_ids in self.lut_edge_poly.items():
            if len(poly_ids) == 2:
                p0 = self.lut_poly_poly[poly_ids[0]]
                p1 = self.lut_poly_poly[poly_ids[1]]

                if p0 != p1:
                    self.merge_adjacent_coplanar_polygons(edge, p0, p1)
                    self.remove_double_paths(p0)

        return clean_dictionary(self.lut_poly_shape.items())

    def remove_double_paths(self, p) -> None:

        loop0 = self.lut_poly_shape[p]
        loop = loop0 + loop0[0:2]

        clean_loop = []
        for i in range(len(loop0)):
            clean_loop.append(loop[i])
            if loop[i] == loop[i+2]:
                i += 2

        self.lut_poly_shape[p] = clean_loop


    def merge_adjacent_coplanar_polygons(self, edge, p0, p1) -> None:


        loop0 = self.lut_poly_shape[p0]
        loop1 = self.lut_poly_shape[p1]

        keep0 = loop0
        keep1 = loop1



        i0 = self.index_edge_in_poly(edge, loop0)
        i1 = self.index_edge_in_poly(edge[::-1], loop1)

        if i0 < 0 or i1 < 0:
            return

        # loop = loop_remove

        loop0 = loop0[i0 + 1:] + loop0[:i0]
        loop1 = loop1[i1 + 1:] + loop1[:i1]

        self.lut_poly_shape[p0] = loop0 + loop1
        self.lut_poly_shape[p1] = []

        keep = self.lut_poly_shape[p0]

        self.lut_poly_poly[p1] = p0

    def index_edge_in_poly(self, edge, loop):

        length = len(loop)
        if length < 2:
            return -1

        loopa = loop[length - 1:] + loop[:length-1]
        loopb = loop[1:] + loop[0:1]

        search0 = [1 if edge[0] == k else 0 for k in loop]
        search1a = [1 if edge[1] == k else 0 for k in loopa]
        search1b = [1 if edge[1] == k else 0 for k in loopb]

        search = []
        for i in range(length):
            a = search0[i]
            b = search1a[i]
            c = search1b[i]

            search.append(search0[i] + search1a[i] + search1b[i])
            
        if 2 not in search:
            return -1
        
        return search.index(2)
        




    def get_horizontal_polygons(self) -> list:
        shapes = []
        for polygon in self.item.data.polygons:
            zz = [(self.wm @ self.item.data.vertices[vid].co).z for vid in polygon.vertices]

            if abs(max(zz) - min(zz)) < TOLERANCE:
                z = round(mean(zz), PRECISION)
                if abs(z - self.z) < TOLERANCE:
                    shapes.append(polygon)

        return shapes


def create_lut_edge_to_polygons(polygons: object) -> dict:
    edge2polygons = {}
    for p in polygons:
        for edge in p.edge_keys:
            if edge not in edge2polygons:
                edge2polygons[edge] = []

            edge2polygons[edge].append(p.index)
    return edge2polygons


def create_lut_polygon_to_vertices(polygons: object) -> dict:
    polygon2vertices = {}
    for p in polygons:
        i = p.index
        if i not in polygon2vertices:
            polygon2vertices[i] = Shape([])
        polygon2vertices[i] = Shape([v for v in p.vertices])
    return polygon2vertices
