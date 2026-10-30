"""Geometry invariants for the fixed EXP-011 diagonal/grid discriminator."""
from collections import Counter
import importlib.util
from pathlib import Path
import struct

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("grid_probe", ROOT / "scripts/terrain-deck-grid-probe.py")
probe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(probe)


@pytest.fixture(scope="module")
def variants():
    base = probe.reference()
    if not (base.reference().SOURCE / "LEVEL.DAT").exists():
        pytest.skip("retail work-copy fixture unavailable")
    return {(nx, nz, flip): probe.build(nx, nz, flip_top=flip)
            for nx, nz in probe.GRIDS for flip in (False, True)}


def mesh(dat):
    return probe.reference().reference().LevelDat.parse(dat).static_mesh_reference("primary", 160)


def xyz(ref, face):
    return [struct.unpack_from("<3h", ref.payload.vertices[i // 12].to_bytes())
            for i in face.vertex_byte_offsets]


def cross(a, b, c):
    u = [b[i] - a[i] for i in range(3)]
    v = [c[i] - a[i] for i in range(3)]
    return (u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0])


@pytest.mark.parametrize("args", ((0, 4), (4, 0), (5, 5), (True, 4), (4, 5.0), (4, "5")))
def test_unsupported_or_aliased_grid_rejected(args):
    with pytest.raises(ValueError):
        probe.build(*args)


def test_flip_requires_boolean():
    with pytest.raises(ValueError):
        probe.build(flip_top=1)


def test_four_by_four_preserves_banked_fixture_byte_for_byte(variants):
    terrain, dat, _ = variants[4, 4, False]
    old_terrain, old_dat, _ = probe.reference().build(divisions=4)
    assert terrain == old_terrain
    assert dat == old_dat


@pytest.mark.parametrize("grid", probe.GRIDS)
def test_diagonal_change_preserves_vertices_and_corner_attribute_pairs(variants, grid):
    _, before, meta = variants[*grid, False]
    _, after, other = variants[*grid, True]
    a, b = mesh(before), mesh(after)
    assert meta["vertex_count"] == other["vertex_count"]
    assert meta["face_count"] == other["face_count"]
    assert [v.to_bytes() for v in a.payload.vertices] == [v.to_bytes() for v in b.payload.vertices]
    for original, changed, origin in zip(a.payload.faces, b.payload.faces, meta["source_faces"]):
        av = list(zip(original.vertex_byte_offsets, original.field_words))
        bv = list(zip(changed.vertex_byte_offsets, changed.field_words))
        assert bv == (av[1:] + av[:1] if origin["source_face"] == 1 else av)
    start = a.geometry_offset
    size = meta["mesh160_replaced_prefix_bytes"]
    assert before[:start] == after[:start]
    assert before[start + size:] == after[start + size:]


@pytest.mark.parametrize("key", [(nx, nz, flip) for nx, nz in probe.GRIDS for flip in (False, True)])
def test_same_surface_coverage_winding_and_conforming_top_edges(variants, key):
    terrain, dat, meta = variants[key]
    source_terrain, source, _ = probe.reference().build(divisions=1)
    original, candidate = mesh(source), mesh(dat)
    assert terrain == source_terrain
    start, size = candidate.geometry_offset, meta["mesh160_replaced_prefix_bytes"]
    assert size <= meta["known_capacity"] == 1336
    assert dat[:start] == source[:start]
    assert dat[start + size:] == source[start + size:]
    area = Counter()
    edges = Counter()
    for face, origin in zip(candidate.payload.faces, meta["source_faces"]):
        points = xyz(candidate, face)
        source_points = xyz(original, original.payload.faces[origin["source_face"]])
        normal = cross(*source_points[:3])
        axis = next(i for i, v in enumerate(normal) if v)
        assert all(p[axis] == source_points[0][axis] for p in points)
        for tri in ((points[0], points[1], points[2]), (points[0], points[2], points[3])):
            n = cross(*tri)
            assert n[axis] * normal[axis] > 0
            assert all(n[i] == 0 for i in range(3) if i != axis)
            area[origin["source_face"]] += n[axis]
        if origin["source_face"]:
            for a, b in zip(points, points[1:] + points[:1]):
                edges[a, b] += 1
    for i, face in enumerate(original.payload.faces):
        points = xyz(original, face)
        n = cross(*points[:3])
        axis = next(j for j, v in enumerate(n) if v)
        assert area[i] == n[axis] + cross(points[0], points[2], points[3])[axis]
    top_y = xyz(original, original.payload.faces[1])[0][1]
    # Every top/internal edge has an exact reverse partner; no T-junction at the rim.
    for (a, b), count in edges.items():
        if a[1] == b[1] == top_y:
            assert count == edges[b, a] == 1


def test_output_refuses_nonwork_and_existing_directory(tmp_path):
    with pytest.raises(ValueError, match="work/copies"):
        probe.write_fixture(tmp_path / "refused")
    if not (ROOT / 'work/copies').is_dir():
        pytest.skip('retail work copies unavailable')
    with pytest.raises(FileExistsError):
        probe.write_fixture(ROOT / "work/copies")
