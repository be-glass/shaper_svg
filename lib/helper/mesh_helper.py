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
from bpy.types import Mesh, Object
#
# from .other import select_active, active_object
from lib.constant import TOLERANCE, PRECISION
from statistics import mean

from mathutils import Matrix


def horizontal_edges(item: Object) -> dict:

    horizontal_edges = {}
    for edge in item.data.edges:
        z0 = item.data.vertices[edge.vertices[0]].co.z
        z1 = item.data.vertices[edge.vertices[1]].co.z

        if abs(z0 - z1) < TOLERANCE:
            z = round(z0, PRECISION)
            if not z in horizontal_edges:
                horizontal_edges[z] = []
            horizontal_edges[z].append(edge)

    return horizontal_edges


def horizontal_polygons(item: Object) -> list:
    horizontal_polygons = []
    for polygon in item.data.polygons:
        zz = [item.data.vertices[vid].co.z for vid in polygon.vertices]

        if abs( max(zz) - min(zz)) < TOLERANCE:
            z = round(mean(zz), PRECISION)
            horizontal_polygons.append(polygon)

    return horizontal_polygons







# def shade_mesh_flat(obj) -> None:
#     for f in obj.data.polygons:
#         f.use_smooth = False
#
#
# def polygon2mesh(polygon) -> Mesh:
#     bm = bmesh.new()
#     [bm.verts.new(v) for v in polygon]
#     bm.faces.new(bm.verts)
#     bm.normal_update()
#     me = bpy.data.meshes.new("")
#     bm.to_mesh(me)
#     return me
#
#
# def create_object(polygon, col=None, name='') -> Object:
#     me = polygon2mesh(polygon)
#     obj = bpy.data.objects.new(name, me)
#     if col:
#         col.objects.link(obj)
#     return obj
#
#
# def add_plane(name, size, col=None) -> Object:  # TODO: replace without ops
#     bpy.ops.mesh.primitive_plane_add(size=size)
#
#     obj = active_object()
#
#     # delete face
#     bpy.ops.object.mode_set(mode='EDIT')
#     obj.data.polygons[0].select = True
#     bpy.ops.mesh.delete(type='ONLY_FACE')
#     bpy.ops.object.mode_set(mode='OBJECT')
#     select_active(obj)  # TODO
#
#     obj.name = name
#
#     if col:
#         for c in obj.users_collection:
#             c.objects.unlink(obj)
#         col.objects.link(obj)
#     return obj
#
#
# def fill_polygon(mesh) -> None:
#     bm = bmesh.new()
#     bm.from_mesh(mesh)
#     bm.faces.new(bm.verts)
#     bm.to_mesh(mesh)
#     bm.free()
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
            polygon2vertices[i] = []
        polygon2vertices[i] = [v for v in p.vertices]
    return polygon2vertices


def find_loops(item: object) -> dict:
    polygons = horizontal_polygons(item)
    lut_poly_vertex = create_lut_polygon_to_vertices(polygons)
    lut_edge_poly = create_lut_edge_to_polygons(polygons)
    lut_poly_poly = {p.index: p.index for p in polygons}

    for edge, poly_ids in lut_edge_poly.items():
        if len(poly_ids) == 2:

            # merge adjacent coplanar polygons

            v0, v1 = edge
            p0, p1 = poly_ids

            p0 = lut_poly_poly[p0]
            p1 = lut_poly_poly[p1]
            loop0 = lut_poly_vertex[p0]
            loop1 = lut_poly_vertex[p1]

            if p0 != p1 and v0 in loop0 and v1 in loop1:
                i = loop0.index(v0)
                loop0 = loop0[i + 1:] + loop0[:i]

                i = loop1.index(v1)
                loop1 = loop1[i + 1:] + loop1[:i]

                lut_poly_vertex[p0] = loop0 + loop1
                lut_poly_vertex[p1] = []

                lut_poly_poly[p1] = p0

    return {k: v for k, v in lut_poly_vertex.items() if v}


def transformation(active, obj) -> Matrix:
    if active.shaper_orientation == 'global':
        return obj.matrix_world
    elif active.shaper_orientation == 'object' and active.orientation_object:
        return active.orientation_object.matrix_world
    else:
        return Matrix()  # 'local'