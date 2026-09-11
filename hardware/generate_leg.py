"""LL-11: connected thin-wall five-bay PAHT-CF open-web landing leg.

Every diagonal joins both swept chords. Units are millimetres.
Digital prototype; physical fit and load capacity remain unverified.
"""
from pathlib import Path
import argparse, json, math
import cadquery as cq
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'generated'
WIDTH = 28.0
HEIGHT = 65.0
PILOT = 4.0
DEPTH = 7.0
INNER_CENTERS = [(x, y) for y in (-8.2, 7.8) for x in (-8.0, 8.0)]
LEFT = [(-9.0, 11.3), (-6.0, 21.44), (-3.0, 31.58), (0.0, 41.72), (3.0, 51.86), (6.0, 62.0)]
RIGHT = [(10.0, 11.3), (13.0, 21.44), (16.0, 31.58), (19.0, 41.72), (22.0, 51.86), (25.0, 62.0)]
FL = (3.0, 63.0)
FR = (31.0, 63.0)
CHORD_WIDTH = 1.6
BRACE_WIDTH = 1.2
FOOT_WIDTH = 4.2
BRACE_BOW = 4.0

def slab(points, depth=WIDTH, radius=0):
    face = cq.Face.makeFromWires(cq.Workplane('XY').polyline(points).close().val())
    if radius:
        face = face.fillet2D(radius, face.Vertices())
    return cq.Workplane('XY').newObject([face]).extrude(depth)

def member(a, b, width, depth=WIDTH):
    (dx, dy) = (b[0] - a[0], b[1] - a[1])
    length = math.hypot(dx, dy)
    angle = math.degrees(math.atan2(dy, dx))
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    beam = cq.Workplane('XY').rect(length, width).extrude(depth).rotate((0, 0, 0), (0, 0, 1), angle).translate((mid[0], mid[1], 0))
    for p in (a, b):
        beam = beam.union(cq.Workplane('XY').center(*p).circle(width / 2).extrude(depth))
    return beam

def chain(points, width):
    result = member(points[0], points[1], width)
    for (a, b) in zip(points[1:-1], points[2:]):
        result = result.union(member(a, b, width))
    return result.clean()

def bowed_brace(a, b, panel):
    """Create one connected two-segment brace with an in-bay flexure knee."""
    (dx, dy) = (b[0] - a[0], b[1] - a[1])
    length = math.hypot(dx, dy)
    (nx, ny) = (-dy / length, dx / length)
    sign = -1 if panel in (1, 2, 4) else 1
    knee = ((a[0] + b[0]) / 2 + sign * nx * BRACE_BOW, (a[1] + b[1]) / 2 + sign * ny * BRACE_BOW)
    return dict(name=f'panel_{panel}', panel=panel, start=a, knee=knee, end=b, points=(a, knee, b))
CONNECTED_BRACES = []
for i in range(5):
    (a, b) = (RIGHT[i], LEFT[i + 1]) if i % 2 == 0 else (LEFT[i], RIGHT[i + 1])
    CONNECTED_BRACES.append(bowed_brace(a, b, i + 1))

def horizontal_bore(x, z, d=PILOT):
    cut = cq.Workplane(obj=cq.Solid.makeCylinder(d / 2, DEPTH + 0.02, cq.Vector(x, -0.02, z), cq.Vector(0, 1, 0)))
    return cut.union(cq.Workplane(obj=cq.Solid.makeCone(d / 2 + 0.25, d / 2, 0.25, cq.Vector(x, 0, z), cq.Vector(0, 1, 0))))

def shaft_clearance():
    r = 6.0
    q = r / math.sqrt(2)
    return cq.Workplane('XZ').center(-0.3, WIDTH / 2 + 0.3).moveTo(-q, q).lineTo(0, r * math.sqrt(2)).lineTo(q, q).threePointArc((0, -r), (-q, q)).close().extrude(-20.04).translate((0, -0.02, 0))

def mount_blank():
    return slab([(-14.2, 0), (13.8, 0), (13.8, 9.0), (11.2, 11.5), (-8.8, 11.5), (-14.2, 9.0)], radius=0.8)

def uncut_leg():
    body = mount_blank().union(chain(LEFT + [FL], CHORD_WIDTH)).union(chain(RIGHT + [FR], CHORD_WIDTH))
    for brace in CONNECTED_BRACES:
        body = body.union(chain(brace['points'], BRACE_WIDTH))
    return body.union(member(FL, FR, FOOT_WIDTH)).clean()

def leg():
    body = uncut_leg()
    for (px, py) in INNER_CENTERS:
        body = body.cut(horizontal_bore(py, WIDTH / 2 - px))
    return body.cut(shaft_clearance()).clean()

def volume(shape):
    properties = GProp_GProps()
    error = BRepGProp.VolumeProperties_s(shape.wrapped, properties, 1e-10, True, False)
    if error >= 1e-08:
        raise ValueError('Volume integration did not converge')
    return properties.Mass()

def generate(out):
    """Export only the leg, then check STEP round-trip geometry."""
    out.mkdir(parents=True, exist_ok=True)
    model = leg()
    shape = model.val()
    if not shape.isValid() or len(shape.Solids()) != 1:
        raise ValueError('Expected one valid solid')
    step = out / 'LL11_leg.step'
    stl = out / 'LL11_leg.stl'
    cq.exporters.export(model, str(step))
    cq.exporters.export(model, str(stl), tolerance=0.025, angularTolerance=0.1)
    restored = cq.importers.importStep(str(step)).val()
    if not restored.isValid() or len(restored.Solids()) != 1:
        raise ValueError('Invalid STEP round-trip')
    original_volume = volume(shape)
    delta = abs(volume(restored) - original_volume)
    if delta > max(0.0001, original_volume * 1e-08):
        raise ValueError('STEP volume changed')
    bounds = shape.BoundingBox()
    restored_bounds = restored.BoundingBox()
    if max((abs(getattr(bounds, k) - getattr(restored_bounds, k)) for k in ('xmin', 'ymin', 'zmin', 'xmax', 'ymax', 'zmax'))) > 1e-05:
        raise ValueError('STEP bounds changed')
    report = {'revision': 'LL11-0.11.0', 'units': 'mm', 'valid_solid': True, 'solid_count': 1, 'volume_mm3': original_volume, 'bounds_xyz_mm': [bounds.xlen, bounds.ylen, bounds.zlen], 'step_roundtrip': True, 'step_volume_delta_mm3': delta, 'physical_fit_verified': False, 'physical_load_capacity_verified': False, 'reference_assembly_checked': False}
    (out / 'geometry-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=OUT)
    generate(parser.parse_args().out)
