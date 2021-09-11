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
from statistics import mean

from .Shape import Shape
from .constant import TOLERANCE, PRECISION

from .helper.other import clean_dictionary

from typing import Dict, List


class Contour:
    def __init__(self, item, z, wm) -> None:
        self.item = item
        self.z = z
        self.wm = wm
        polygons = self.get_horizontal_polygons()
        self.lut_poly_shape: Dict[int, Shape] = create_lut_polygon_to_vertices(polygons)
        self.lut_edge_shapeId: Dict[tuple, int] = self.create_lut_edge_to_shapeId(polygons)

    def get_loops(self) -> dict:

        for edge, poly_ids in self.lut_edge_shapeId.items():
            if len(poly_ids) == 2:
                p0 = poly_ids[0]
                p1 = poly_ids[1]

                if p0 != p1:
                    self.merge_adjacent_coplanar_polygons(edge, p0, p1)
                    self.clean_poly(p0)

        return clean_dictionary(self.lut_poly_shape.items())

    def clean_poly(self, p) -> None:
        self.lut_poly_shape[p]: Shape = self.lut_poly_shape[p].clean()

    def merge_adjacent_coplanar_polygons(self, edge, p0, p1) -> None:

        shape0: Shape = self.lut_poly_shape[p0]
        shape1: Shape = self.lut_poly_shape[p1]

        if p0 != p1:

            i0 = shape0.edge_index(edge)
            i1 = shape1.edge_index(edge, reverse=True)

            if i0 < 0 or i1 < 0:
                return

            shape0 = shape0.delete_at(i0)
            shape1 = shape1.delete_at(i1)

            self.lut_poly_shape[p0] = shape0.concat(shape1)
            self.lut_poly_shape[p1] = Shape([])

            self.replace_index(p0, p1)
            pass

    def replace_index(self, p0, p1):
        for edge, shape in self.lut_edge_shapeId.items():
            self.lut_edge_shapeId[edge] = [p0 if v == p1 else v for v in shape]




    def get_horizontal_polygons(self) -> list:
        polygons = []

        if self.item.type != 'MESH':
            return polygons

        for polygon in self.item.data.polygons:
            zz = [(self.wm @ self.item.data.vertices[vid].co).z for vid in polygon.vertices]

            if abs(max(zz) - min(zz)) < TOLERANCE:
                z = round(mean(zz), PRECISION)
                if abs(z - self.z) < TOLERANCE:
                    polygons.append(polygon)

        return polygons

    def create_lut_edge_to_shapeId(self, polygons: object) -> dict:
        edge2shape = {}
        for p in polygons:
            for edge in p.edge_keys:
                if edge not in edge2shape:
                    edge2shape[edge] = Shape([])
                edge2shape[edge].append(p.index)
        return edge2shape


def create_lut_polygon_to_vertices(polygons: object) -> dict:
    polygon2vertices = {}
    for p in polygons:
        i = p.index
        if i not in polygon2vertices:
            polygon2vertices[i] = Shape([])
        polygon2vertices[i] = Shape([v for v in p.vertices])
    return polygon2vertices
