"""Ocean portfolio hero shot. Drives Blender: builds the sky, the sea, the board,
the surfer, the camera and the grade, then renders one frame.

  Blender -b -P scene.py -- --style film|clay|toon [--samples 64] [--scale 50] [--out x.png]
"""
import argparse, json, math, os, sys
import numpy as np
import bpy, bmesh
from mathutils import Vector, Euler, Quaternion, Matrix

rad = math.radians

# ---------------------------------------------------------------- 1. the shot
RES = (1920, 1080)
CAM_POS, CAM_AIM, LENS, FSTOP = (0.5, -5.6, 0.50), (0.0, 0.0, 0.80), 35.0, 4.0
HULL_PAD = 0.22                         # m of water kept clear around the board
RIG_YAW = rad(-24)                      # board nose swings toward the camera

# ---------------------------------------------------------------- 2. the sun
SUN_AZ, SUN_EL = rad(-8.5), rad(6.0)
SUN = Vector((math.sin(SUN_AZ) * math.cos(SUN_EL), math.cos(SUN_AZ) * math.cos(SUN_EL), math.sin(SUN_EL)))
SUN_COL, SUN_POWER, HALO = (1.0, 0.45, 0.15), 14.0, 1.0
SUN_DISC, SUN_ANGLE = (40000, 500.0, (1.0, 0.95, 0.85)), rad(7.0)   # the visible disc (tightness, gain, colour); lamp softness; a 4th disc value multiplies its brightness and leaves the water's reflection to the disc
FILL_COL, FILL_POWER = (0.75, 0.6, 1.0), 220.0   # cheat light from camera side
EXPOSURE = 0.5                          # stops, film only

# ---------------------------------------------------------------- 3. the sky (horizon -> zenith)
SKY = [(0.00, (0.95, 0.20, 0.010)), (0.035, (0.80, 0.17, 0.06)), (0.11, (0.42, 0.08, 0.20)),
       (0.26, (0.13, 0.06, 0.30)), (0.60, (0.035, 0.03, 0.15))]
SKY_TOON = [(0.00, (1.00, 0.36, 0.07)), (0.04, (1.00, 0.40, 0.20)), (0.12, (0.74, 0.28, 0.44)),
            (0.28, (0.30, 0.20, 0.55)), (0.60, (0.10, 0.09, 0.33))]

# ---------------------------------------------------------------- 4. the sea
SEA = dict(film=dict(res=14, wave=0.55, chop=0.9, wind=5.0),
           clay=dict(res=6, wave=0.75, chop=0.3, wind=4.0),
           toon=dict(res=14, wave=0.60, chop=0.5, wind=4.5))
SEA_TILE, SEA_REPEAT, SEA_TIME = 40, 4, 3.0

# ---------------------------------------------------------------- 5. the surfer (tune me)
SKIN, HAIR, SHORTS, BOARD, EYE = (0.80, 0.52, 0.38), (0.16, 0.09, 0.05), (0.85, 0.22, 0.16), (0.93, 0.90, 0.80), (0.02, 0.02, 0.03)
BODY_LIFT = 0.05                        # body above board centreline
_z = BODY_LIFT
# 16 body points + head centre, board-local (nose is +x). Order: hips waist chest neck,
# L shoulder elbow hand, R shoulder elbow hand, L knee ankle toes, R knee ankle toes, head
RADII = [.112, .105, .125, .055, .062, .046, .042, .062, .046, .042, .058, .042, .036, .058, .042, .036]
POSES = dict(
    prone=[(-0.36, 0, _z + .115), (-0.12, 0, _z + .135), (0.10, 0, _z + .215), (0.25, 0, _z + .345),      # propped on elbows, shins up
           (0.14, .185, _z + .235), (0.30, .215, _z + .060), (0.49, .075, _z + .045),
           (0.14, -.185, _z + .235), (0.30, -.215, _z + .060), (0.49, -.075, _z + .060),
           (-0.80, .095, _z + .070), (-0.74, .060, _z + .430), (-0.84, .050, _z + .560),
           (-0.80, -.095, _z + .070), (-0.66, -.060, _z + .400), (-0.70, -.050, _z + .540), (0.34, 0, _z + .50)],
    paddle=[(-0.36, 0, _z + .115), (-0.12, 0, _z + .125), (0.10, 0, _z + .170), (0.26, 0, _z + .270),     # flat; arms set by the stroke
            (0.14, .185, _z + .180), (0.30, .30, _z + .10), (0.50, .34, _z),
            (0.14, -.185, _z + .180), (0.30, -.30, _z + .10), (0.50, -.34, _z),
            (-0.80, .095, _z + .070), (-1.18, .085, _z + .065), (-1.30, .085, _z + .050),
            (-0.80, -.095, _z + .070), (-1.18, -.085, _z + .065), (-1.30, -.085, _z + .050), (0.36, 0, _z + .40)],
    ride=[(-0.12, -.02, .50), (-0.08, .02, .66), (0.0, .06, .86), (0.04, .07, 1.02),                       # crouched, chest to +y
          (0.16, .05, .90), (0.36, .10, .80), (0.55, .12, .84),
          (-0.17, .07, .88), (-0.36, .14, .76), (-0.52, .20, .80),
          (0.22, .10, .38), (0.30, 0, .10), (0.30, .13, .07),
          (-0.40, .10, .36), (-0.52, 0, .10), (-0.52, .13, .07), (0.07, .07, 1.17)])
BOARD_L, BOARD_W, HEAD, REST = 2.75, 0.285, 1.0, 'prone'   # idle shot: longboard, cartoon head
# the surf shot, seconds: start paddling, on the wave, kick out, lying down again, back at the spot
T_PADDLE, T_CATCH, CARVE = 1.0, 3.4, 3.0                 # CARVE: seconds per bottom turn + top turn; a whole number of them fits one wave period
T_OUT = T_CATCH + 0.6 + 1.5 * CARVE                      # he leaves from the top of the wave
T_DOWN, T_BACK, SURF_LEN = T_OUT + 1.0, 28.0, 30.0       # SURF_LEN is a multiple of GAP/SPEED so it ends where it starts
POSE_KEYS = [(0, 'sit'), (0.5, 'sit'), (1.1, 'paddle'), (T_CATCH, 'paddle'), (T_CATCH + 0.6, 'ride'), (T_OUT + 0.3, 'ride'),
             (T_DOWN + 0.3, 'paddle'), (T_BACK - 0.3, 'paddle'), (T_BACK + 0.6, 'sit')]

# ---------------------------------------------------------------- 6. the wave shot (--shot wave)
WAVE_CAM_POS, WAVE_CAM_AIM, WAVE_LENS = (-8.0, -50.0, 5.0), (-12.0, 0.0, 0.0), 100.0   # raised, from the beach
CAM_PITCH, CAM_FOLLOW = rad(-3.2), 0.6      # tripod pan: fixed tilt (keeps the sun in frame), pans 60% of the way with him
WAVE_SPOT = (0.0, 14.0)                     # where the surfer waits, just outside the break
WAVE_H, WAVE_W, WAVE_LEAN = 1.5, 3.0, 1.1   # crest height m, half-width m, how far the crest pitches forward
WAVE_GAP, WAVE_SPEED = 24.0, 4.0            # m between swell lines, m/s toward the beach (loops every GAP/SPEED s)
PERIOD = WAVE_GAP / WAVE_SPEED              # every beach shot starts and ends on a multiple of this, where the whole sea repeats: clips join without a cut
# the About shots: the camera leaves the beach as he paddles, is alongside him one PERIOD in (moving with the wave), and is back on the beach by T_PULL
CLOSE_CAM, CLOSE_LENS, CLOSE_AIM = (-13.0, -19.0, 2.2), 85.0, (1.1, 0.0, 1.25)   # alongside: position at t = PERIOD, lens, aim offset from the surfer
T_PUSH, T_PULL = 1.0, 16.0
WAVE_YB, WAVE_PEEL = 8.0, 1.0               # break line y at x=0, and its slant (breaks first at +x, peels to -x)
WAVE_GLOW = (0.03, 0.30, 0.26)              # light through the thin crest
WAKE = 2.4                                  # s the board's foam trail lasts; shorter than the ride before the loop shot starts, so the loop closes
WATER, CLOUD = (0.0, 0.03, 0.09), (0.85, 0.28, 0.22)
SKY_GOLDEN = [(0.00, (1.00, 0.62, 0.30)), (0.025, (0.92, 0.66, 0.52)), (0.08, (0.42, 0.56, 0.86)), (0.60, (0.07, 0.22, 0.68))]
SKY_DAY = [(0.00, (0.50, 0.80, 1.00)), (0.06, (0.28, 0.62, 1.00)), (0.25, (0.10, 0.36, 0.95)), (0.60, (0.03, 0.16, 0.70))]

a = argparse.ArgumentParser()
a.add_argument('--light', default='sunset', choices=['sunset', 'golden', 'day'])
a.add_argument('--shot', default='idle', choices=['idle', 'wave', 'surf', 'about', 'loop'])   # wave: beach view, he floats; surf: he catches one;
#   about: the same ride, the camera goes out to him and comes back; loop: one PERIOD of riding seen from alongside, repeats for ever (about frame 144 = loop frame 0)
a.add_argument('--start', type=int, default=0)   # first frame; with --step, lets one process per GPU share a clip
a.add_argument('--zoom', type=float, default=1.0)  # lens multiplier, for checking poses up close
a.add_argument('--aim-z', type=float, default=0.0)  # with --zoom: aim this far above the board (1.6 = his head when standing)
a.add_argument('--cam-z', type=float, default=WAVE_CAM_POS[2])  # beach camera height m; raise for close-ups so waves don't hide him
a.add_argument('--wave-h', type=float, default=WAVE_H)          # crest height m
a.add_argument('--t', type=float, default=0.0)    # seconds into the shot (stills), or clip start
a.add_argument('--style', default='film', choices=['film', 'clay', 'toon'])
a.add_argument('--samples', type=int, default=64)
a.add_argument('--scale', type=int, default=50)
a.add_argument('--out', default='')
a.add_argument('--frames', type=int, default=0)   # >0: render an idle sequence to out/<style>_loop/
a.add_argument('--step', type=int, default=1)   # render every Nth frame (spot checks)
A = a.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else [])
STYLE = A.style
SHOT = A.shot
WAVE, SURF, LOOP = SHOT != 'idle', SHOT in ('surf', 'about', 'loop'), SHOT == 'loop'
WAVE_CAM_POS, WAVE_H = (*WAVE_CAM_POS[:2], A.cam_z), A.wave_h
SPRAY_ON = WAVE and A.zoom == 1                 # spray sprites read as squares up close
NAME = f'{A.shot}_{A.light}' if WAVE else STYLE
if A.light == 'day':                    # tropical midday: high sun, turquoise water
    SKY, SUN_AZ, SUN_EL, SUN_COL, SUN_POWER, EXPOSURE = SKY_DAY, rad(-105), rad(32), (1.0, 0.95, 0.85), 5.0, 0.6
    WATER, CLOUD, WAVE_GLOW, FILL_POWER = (0.0, 0.30, 0.30), (1.0, 1.0, 1.0), (0.03, 0.45, 0.38), 0.0
if A.light == 'golden':                 # early sunset: still mostly light, warm low sun ahead and to the left
    SKY, SUN_AZ, SUN_EL, SUN_COL, SUN_POWER, EXPOSURE = SKY_GOLDEN, rad(2.0), rad(0.8), (1.0, 0.70, 0.40), 2.0, 0.5
    WATER, CLOUD, WAVE_GLOW, FILL_POWER = (0.0, 0.22, 0.25), (1.0, 0.72, 0.55), (0.04, 0.48, 0.36), 0.0
    HALO, SUN_DISC, SUN_ANGLE = 0.6, (150000, 400.0, (1.0, 0.78, 0.45), 25.0), rad(1.5)
if WAVE:                                # beach shots: adult proportions (1.8 m), a shortboard, sitting up while he waits
    BOARD_L, BOARD_W, HEAD, REST = 2.0, 0.25, 0.66, 'sit'
    SEA_TILE = int(WAVE_GAP)                # the chop tile; the loop shot slides the sea one WAVE_GAP per PERIOD, so it must repeat at that
    if LOOP: POSE_KEYS = [(0, 'ride')]
    RADII = [.105, .098, .118, .052, .056, .044, .038, .056, .044, .038, .060, .043, .036, .060, .043, .036]
    POSES = dict(
        sit=[(-.30, 0, .15), (-.29, 0, .35), (-.26, 0, .59), (-.24, 0, .74),                                 # astride the board, legs in the water
             (-.25, .19, .66), (-.20, .25, .39), (.02, .17, .22), (-.25, -.19, .66), (-.20, -.25, .39), (.02, -.17, .22),
             (-.02, .27, .02), (-.06, .29, -.40), (.08, .29, -.50), (-.02, -.27, .02), (-.06, -.29, -.40), (.08, -.29, -.50), (-.22, 0, .89), (6, 0, .9)],
        paddle=[(-.30, 0, .15), (-.10, 0, .16), (.14, 0, .21), (.29, 0, .29),                                # chest arched; arms set by the stroke
                (.16, .19, .22), (.30, .30, .12), (.50, .34, .05), (.16, -.19, .22), (.30, -.30, .12), (.50, -.34, .05),
                (-.74, .09, .12), (-1.18, .08, .11), (-1.36, .08, .08), (-.74, -.09, .12), (-1.18, -.08, .11), (-1.36, -.08, .08), (.40, 0, .39), (6, 0, .6)],
        ride=[(-.36, -.04, .82), (-.35, .03, .99), (-.31, .13, 1.18), (-.29, .17, 1.31),                     # surf stance, chest to +y and opened toward the nose, right foot forward
              (-.47, .24, 1.22), (-.56, .38, 1.03), (-.50, .55, .90), (-.14, .06, 1.25), (.02, .08, 1.03), (.22, .16, .92),
              (-.50, .20, .50), (-.62, -.03, .10), (-.58, .16, .06), (-.10, .18, .52), (-.06, -.03, .10), (.08, .11, .06), (-.25, .22, 1.45), (4, 1.2, .7)])
    # the figure (MakeHuman via the MPFB extension): 0..1 sliders, then the asset files under assets/
    HUMAN = dict(gender=1.0, age=0.45, muscle=0.7, weight=0.4, height=0.5, proportions=0.6, race=dict(asian=0.0, caucasian=1.0, african=0.0))
    HUMAN_SKIN, HUMAN_HAIR, HUMAN_TALL = 'skins/young_caucasian_male/young_caucasian_male.mhmat', 'hair/short02/short02.mhclo', 1.80
    HUMAN_HAIR_PUFF, HUMAN_HAIR_DROP, HUMAN_HAIR_WAVE = (1.08, 1.10, 1.18), 0.6, 0.03   # the hair cap scaled out from the head's centre, its lower half lengthened, then lumped into waves (m)
    SHORTS = (0.72, 0.09, 0.06)
    HUMAN_FACE = {'head/head-oval': 0.8, 'head/head-age-decr': 0.5, 'head/head-scale-horiz-decr': 0.3, 'chin/chin-width-decr': 0.4, 'chin/chin-bones-incr': 0.3,   # MPFB detail targets: a younger, slimmer face
                  'mouth/mouth-upperlip-volume-incr': 0.3, 'mouth/mouth-lowerlip-volume-incr': 0.3}
    HUMAN_TAN, HUMAN_HAIR_TINT = (0.95, 0.80, 0.70), (0.36, 0.25, 0.18)      # multiplied into the skin and hair colour
SUN = Vector((math.sin(SUN_AZ) * math.cos(SUN_EL), math.cos(SUN_AZ) * math.cos(SUN_EL), math.sin(SUN_EL)))


# ================================================================ node helpers
def put(sock, v):
    if isinstance(v, bpy.types.NodeSocket): sock.id_data.links.new(v, sock)
    elif isinstance(v, (tuple, list)) and len(v) == 3 and len(sock.default_value) == 4: sock.default_value = (*v, 1)
    else: sock.default_value = v

def node(nt, kind, **props):
    n = nt.nodes.new(kind)
    for k, v in props.items(): setattr(n, k, v)
    return n

def fmath(nt, op, x, y=None):
    n = node(nt, 'ShaderNodeMath', operation=op); put(n.inputs[0], x)
    if y is not None: put(n.inputs[1], y)
    return n.outputs[0]

def vmath(nt, op, x, y, out='Vector'):
    n = node(nt, 'ShaderNodeVectorMath', operation=op); put(n.inputs[0], x); put(n.inputs[1], y)
    return n.outputs[out]

def mix(nt, fac, x, y, blend='MIX'):
    n = node(nt, 'ShaderNodeMix', data_type='RGBA', blend_type=blend)
    put(n.inputs[0], fac); put(n.inputs[6], x); put(n.inputs[7], y)
    return n.outputs[2]

def ramp(nt, fac, stops, constant=False):
    n = node(nt, 'ShaderNodeValToRGB'); cr = n.color_ramp
    cr.interpolation = 'CONSTANT' if constant else 'LINEAR'
    while len(cr.elements) < len(stops): cr.elements.new(0.5)
    for e, (p, c) in zip(cr.elements, stops): e.position, e.color = p, (*c, 1)
    put(n.inputs[0], fac)
    return n.outputs[0]

def step(nt, x, edge):
    return fmath(nt, 'GREATER_THAN', x, edge)

def new_mat(name):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    return m, nt, node(nt, 'ShaderNodeOutputMaterial')

def drift_coords(nt):
    """Object coords wrapped round a cylinder whose axis lies across the wave's travel diagonal: textures repeat
    after one WAVE_GAP of drift in x and y, which is how far the loop shot slides the sea."""
    s = node(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(node(nt, 'ShaderNodeTexCoord').outputs['Object'], s.inputs[0])
    R = WAVE_GAP * math.sqrt(2) / (2 * math.pi)
    a = fmath(nt, 'MULTIPLY', fmath(nt, 'ADD', s.outputs[0], s.outputs[1]), 1 / (math.sqrt(2) * R))
    c = node(nt, 'ShaderNodeCombineXYZ')
    put(c.inputs[0], fmath(nt, 'MULTIPLY', fmath(nt, 'COSINE', a), R)); put(c.inputs[1], fmath(nt, 'MULTIPLY', fmath(nt, 'SINE', a), R))
    put(c.inputs[2], fmath(nt, 'MULTIPLY', fmath(nt, 'SUBTRACT', s.outputs[0], s.outputs[1]), 1 / math.sqrt(2)))
    return c.outputs[0]

def bump(nt, layers, vec=None):
    """layers: [(noise scale, strength)] chained into one normal."""
    nrm = None
    for sc, st in layers:
        nz = node(nt, 'ShaderNodeTexNoise'); put(nz.inputs['Scale'], sc); put(nz.inputs['Detail'], 4.0)
        nt.links.new(vec or node(nt, 'ShaderNodeTexCoord').outputs['Object'], nz.inputs['Vector'])
        b = node(nt, 'ShaderNodeBump'); put(b.inputs['Strength'], st); put(b.inputs['Height'], nz.outputs[0])
        put(b.inputs['Distance'], 0.5 / sc)
        if nrm: put(b.inputs['Normal'], nrm)
        nrm = b.outputs[0]
    return nrm


# ================================================================ materials
TOON_KEY = Vector((-0.45, -0.65, 0.6)).normalized()

def surface(name, col, rough=0.5, sss=0.0):
    """Material for a solid part, in the active style."""
    m, nt, out = new_mat(name)
    if STYLE == 'toon':                                  # analytic cel shading, no lights needed
        N = node(nt, 'ShaderNodeNewGeometry').outputs['Normal']
        lit = step(nt, vmath(nt, 'DOT_PRODUCT', N, tuple(TOON_KEY), 'Value'), 0.05)
        shade = tuple(c * k for c, k in zip(col, (0.42, 0.34, 0.60)))
        c = mix(nt, lit, shade, col)
        rim = step(nt, vmath(nt, 'DOT_PRODUCT', N, tuple(SUN), 'Value'), 0.55)
        c = mix(nt, rim, c, (1.0, 0.80, 0.55))
        e = node(nt, 'ShaderNodeEmission'); put(e.inputs[0], c)
        nt.links.new(e.outputs[0], out.inputs[0])
        return m
    p = node(nt, 'ShaderNodeBsdfPrincipled')
    put(p.inputs['Base Color'], col)
    if STYLE == 'clay':
        put(p.inputs['Roughness'], 0.85); put(p.inputs['Subsurface Weight'], 0.12)
        put(p.inputs['Subsurface Radius'], (0.02, 0.012, 0.008))
        put(p.inputs['Normal'], bump(nt, [(14.0, 0.7), (140.0, 0.35)]))
    else:
        put(p.inputs['Roughness'], rough); put(p.inputs['Subsurface Weight'], sss)
        put(p.inputs['Subsurface Radius'], (0.03, 0.012, 0.006))
    nt.links.new(p.outputs[0], out.inputs[0])
    return m

def sea_material():
    m, nt, out = new_mat('sea')
    if STYLE == 'toon':
        g = node(nt, 'ShaderNodeNewGeometry')
        N, I, P = g.outputs['Normal'], g.outputs['Incoming'], g.outputs['Position']
        z = node(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(P, z.inputs[0])
        c = ramp(nt, fmath(nt, 'ADD', fmath(nt, 'MULTIPLY', z.outputs[2], 1.6), 0.5),
                 [(0.0, (0.03, 0.07, 0.22)), (0.42, (0.06, 0.13, 0.33)), (0.60, (0.12, 0.22, 0.45))], True)
        facing = vmath(nt, 'DOT_PRODUCT', N, I, 'Value')
        c = mix(nt, step(nt, 0.16, facing), c, (0.45, 0.27, 0.48))       # grazing: mauve sky
        c = mix(nt, step(nt, 0.06, facing), c, (0.95, 0.47, 0.30))       # horizon: orange
        R = vmath(nt, 'REFLECT', vmath(nt, 'MULTIPLY', I, (-1.0, -1.0, -1.0)), N)
        rs = vmath(nt, 'DOT_PRODUCT', R, tuple(SUN), 'Value')
        c = mix(nt, step(nt, rs, 0.988), c, (1.0, 0.60, 0.25))            # glitter path
        c = mix(nt, step(nt, rs, 0.997), c, (1.0, 0.93, 0.75))
        e = node(nt, 'ShaderNodeEmission'); put(e.inputs[0], c)
        nt.links.new(e.outputs[0], out.inputs[0])
        return m
    p = node(nt, 'ShaderNodeBsdfPrincipled')
    if STYLE == 'clay':
        put(p.inputs['Base Color'], (0.025, 0.09, 0.24)); put(p.inputs['Roughness'], 0.30)
        put(p.inputs['Normal'], bump(nt, [(0.9, 1.0), (3.0, 0.9), (45.0, 0.3)]))
    else:
        put(p.inputs['Base Color'], WATER); put(p.inputs['Roughness'], 0.04)
        put(p.inputs['IOR'], 1.33)
        vec = drift_coords(nt) if WAVE else None
        put(p.inputs['Normal'], bump(nt, [(1.6, 0.30), (9.0, 0.30), (40.0, 0.15)], vec))
        if WAVE:                                          # whitewater and a lit crest, driven by wave_shape()
            nz = node(nt, 'ShaderNodeTexNoise'); put(nz.inputs['Scale'], 1.8); put(nz.inputs['Detail'], 7.0)
            nt.links.new(vec, nz.inputs['Vector'])
            fo = node(nt, 'ShaderNodeAttribute', attribute_name='foam').outputs['Fac']
            f = ramp(nt, fmath(nt, 'MULTIPLY', fo, fmath(nt, 'ADD', nz.outputs[0], 0.45)), [(0.30, (0, 0, 0)), (0.55, (1, 1, 1))])
            put(p.inputs['Base Color'], mix(nt, f, WATER, (0.85, 0.80, 0.85)))
            far = fmath(nt, 'MINIMUM', fmath(nt, 'MAXIMUM', fmath(nt, 'MULTIPLY', fmath(nt, 'SUBTRACT', node(nt, 'ShaderNodeCameraData').outputs['View Distance'], 70.0), 0.0015), 0.0), 0.25)
            put(p.inputs['Roughness'], fmath(nt, 'ADD', fmath(nt, 'MULTIPLY', f, 0.7), fmath(nt, 'ADD', far, 0.04)))   # far water: chop too fine to model, so blur it
            put(p.inputs['Emission Color'], WAVE_GLOW)
            put(p.inputs['Emission Strength'], node(nt, 'ShaderNodeAttribute', attribute_name='glow').outputs['Fac'])
    nt.links.new(p.outputs[0], out.inputs[0])
    return m


# ================================================================ sky
def build_sky():
    w = bpy.data.worlds.new('sky'); w.use_nodes = True; nt = w.node_tree; nt.nodes.clear()
    out = node(nt, 'ShaderNodeOutputWorld'); bg = node(nt, 'ShaderNodeBackground')
    d = node(nt, 'ShaderNodeTexCoord').outputs['Generated']
    toon = STYLE == 'toon'
    z = node(nt, 'ShaderNodeSeparateXYZ'); nt.links.new(d, z.inputs[0])
    stops = SKY if not toon else [(p * 0.8, c) for p, c in SKY_TOON]
    c = ramp(nt, z.outputs[2], stops, toon)
    if not toon:                                          # soft streaks of cloud
        mp = node(nt, 'ShaderNodeMapping'); nt.links.new(d, mp.inputs[0]); put(mp.inputs['Scale'], (1.0, 1.0, 9.0))
        nz = node(nt, 'ShaderNodeTexNoise'); nt.links.new(mp.outputs[0], nz.inputs['Vector'])
        put(nz.inputs['Scale'], 2.2); put(nz.inputs['Detail'], 5.0)
        cl = ramp(nt, nz.outputs[0], [(0.45, (0, 0, 0)), (0.72, (1, 1, 1))])
        c = mix(nt, fmath(nt, 'MULTIPLY', cl, 0.35), c, CLOUD)
    s = fmath(nt, 'MAXIMUM', vmath(nt, 'DOT_PRODUCT', d, tuple(SUN), 'Value'), 0.0)
    if toon:
        c = mix(nt, step(nt, s, 0.989), c, (1.0, 0.62, 0.30))
        c = mix(nt, step(nt, s, 0.9955), c, (1.0, 0.80, 0.45))
        c = mix(nt, step(nt, s, 0.9990), c, (1.0, 0.97, 0.85))
    else:
        for power, gain, col, *boost in [(6, 0.10, (1.0, 0.35, 0.05)), (40, 0.55, (1.0, 0.40, 0.06)), (300, 1.6, (1.0, 0.50, 0.10)),
                                 (2500, 5.0, (1.0, 0.70, 0.30)), SUN_DISC]:
            g = fmath(nt, 'MULTIPLY', fmath(nt, 'POWER', s, power), gain * HALO)
            c = mix(nt, g, c, tuple(v * (boost or [1])[0] for v in col), 'ADD')    # the mix factor clamps at 1; boost goes past it
    nt.links.new(c, bg.inputs[0]); nt.links.new(bg.outputs[0], out.inputs[0])
    bpy.context.scene.world = w


# ================================================================ sea
def build_sea():
    cfg = SEA[STYLE]
    me = bpy.data.meshes.new('sea'); ob = bpy.data.objects.new('sea', me); link(ob)
    if WAVE:                                              # own grid, fine near the surfer (the same one in every beach shot); the ocean only adds chop
        global BASE
        u = np.linspace(-1, 1, 720); n = len(u); i = np.arange(n * n).reshape(n, n)
        gx, gy = np.meshgrid(-8 + 40 * u + 130 * u ** 5, 6 + 40 * u + 130 * u ** 5)
        BASE = np.c_[gx.ravel(), gy.ravel(), np.zeros(n * n)].astype('f')
        me.from_pydata(BASE.tolist(), [], np.c_[i[:-1, :-1].ravel(), i[:-1, 1:].ravel(), i[1:, 1:].ravel(), i[1:, :-1].ravel()].tolist())
        me.attributes.new('foam', 'FLOAT', 'POINT'); me.attributes.new('glow', 'FLOAT', 'POINT')
    for name in ('ocean', 'ocean2') if WAVE else ('ocean',):     # beach shots: two copies of the chop, crossfaded by chop_at() so it repeats every PERIOD
        o = ob.modifiers.new(name, 'OCEAN')
        o.geometry_mode, o.repeat_x, o.repeat_y = ('DISPLACE', 1, 1) if WAVE else ('GENERATE', SEA_REPEAT, SEA_REPEAT)
        o.resolution = o.viewport_resolution = cfg['res']
        o.spatial_size, o.depth, o.time = SEA_TILE, 200.0, SEA_TIME
        o.wind_velocity, o.wave_scale, o.choppiness = cfg['wind'], cfg['wave'] * (0.4 if WAVE else 1), cfg['chop']
        o.wave_alignment, o.wave_direction, o.random_seed = 0.35, rad(70), 4
    me.materials.append(sea_material())
    co = sea_points(ob) if not WAVE else BASE * 0
    ob.location = (-(co[:, 0].min() + co[:, 0].max()) / 2, -(co[:, 1].min() + co[:, 1].max()) / 2, 0)
    for p in ob.data.polygons: p.use_smooth = True
    far = bpy.data.meshes.new('far'); bm = bmesh.new()       # flat sea out to the horizon
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=6000); bm.to_mesh(far); bm.free()
    far.materials.append(me.materials[0]); fo = bpy.data.objects.new('far', far); fo.location.z = -0.25; link(fo)
    return ob

def chop_at(sea, t):
    """The chop never repeats by itself, so fade a copy that started one PERIOD later in over the first: at t = PERIOD it is the sea of t = 0."""
    tau = t % PERIOD; w = tau / PERIOD; n = math.hypot(w, 1 - w)
    for name, back, part in (('ocean', 0.0, 1 - w), ('ocean2', PERIOD, w)):
        o = sea.modifiers[name]; o.time, o.wave_scale = SEA_TIME + tau - back, SEA[STYLE]['wave'] * 0.4 * max(part / n, 1e-4)

def swell(x, y, t):
    """Lines of swell roll in from +y. Each grows toward the break line, pitches forward,
    breaks (first at +x, peeling toward -x), then runs on to the beach as fading whitewater.
    Returns height, forward lean, foam and crest glow at base points x, y."""
    yb = WAVE_YB + WAVE_PEEL * x
    z, dy, foam, glow = (np.zeros(len(x), 'f') for _ in range(4))
    for k in range(-3, 9):
        yc = k * WAVE_GAP - (WAVE_SPEED * t) % WAVE_GAP             # this crest
        d = yc - yb                                                 # >0 not yet broken
        size = np.where(d > 0, 0.25 + 0.75 * np.clip(1 - d / 50, 0, 1), np.exp(np.minimum(d, 0) / 16)) * np.exp(-(x / 70) ** 4)
        broke, steep = np.clip(-d / 4, 0, 1), np.clip(1 - d / 25, 0, 1)
        u = (y - yc) / WAVE_W; g = np.exp(-u * u)                   # u=0 at the crest, >0 behind it
        z += WAVE_H * size * g * (1 - 0.45 * broke)
        dy -= WAVE_LEAN * WAVE_H * size * steep * g * g * (1 - 0.7 * broke)
        foam = np.maximum(foam, size * (broke * np.where(u > 0, np.exp(-u / 3.5), np.exp(-(u / 1.3) ** 2)) + 0.3 * steep ** 3 * g ** 6))
        glow += steep * size * np.exp(-(u + 0.4) ** 2) * (1 - broke)
    return z, dy, foam, glow

def height(x, y, t):
    """Swell height at world x, y (undoes the forward lean by fixed-point iteration)."""
    yb = y
    for _ in range(8): z, dy, *_ = swell(x, yb, t); yb = y - dy
    return z

def clock(t):
    """Shot time -> (swell time, time along the surfer's path, how far the sea has slid in x and y).
    The loop shot is seen from a frame that moves with the wave: the swell holds still, the surfer carves on it, the water slides past."""
    return (PERIOD, PERIOD + t, WAVE_SPEED * t) if LOOP else (t, t, 0.0)

def wave_shape(sea, t):
    tw, tv, D = clock(t)
    x, y = BASE[:, 0], BASE[:, 1]
    z, dy, foam, glow = swell(x, y, tw)
    z += foam * 0.12 * (1.3 + np.sin(3.1 * x + 1.7 * y + 4 * math.pi / PERIOD * tv) * np.sin(2.3 * y - 1.3 * x))   # lumpy whitewater
    co = BASE.copy(); co[:, 2] = z; co[:, 1] += dy
    if SURF:                                                        # the board's wake: a foam trail that widens and fades
        for tau in np.arange(0, WAKE, 0.03):
            if tv - tau < T_CATCH + 0.15 or (tv - tau > T_OUT + 0.6 and not LOOP): continue
            px, py, yaw, _ = surf_path(tv - tau)
            px, py = px + D - 0.6 * math.cos(yaw), py + D - 0.6 * math.sin(yaw)
            i = np.flatnonzero((np.abs(co[:, 0] - px) < 1.5) & (np.abs(co[:, 1] - py) < 1.5))
            d2 = (co[i, 0] - px) ** 2 + (co[i, 1] - py) ** 2
            foam[i] = np.maximum(foam[i], (1 - tau / WAKE) ** 1.5 * np.exp(-d2 / (0.28 + 0.22 * tau) ** 2))
    co[:, :2] -= D                                                  # slide the sea: its chop and textures are fixed to the mesh, the object moves back by D
    sea.location = bpy.data.objects['far'].location = (D, D, 0); bpy.data.objects['far'].location.z = -0.25
    me = sea.data
    me.vertices.foreach_set('co', co.ravel())
    me.attributes['foam'].data.foreach_set('value', foam)
    me.attributes['glow'].data.foreach_set('value', glow.astype('f'))
    me.update()

def build_spray():
    """Droplets as tiny tetrahedra on ballistic arcs, thrown off the breaking lip. Each fires once per PERIOD, so the spray repeats with the swell.
    (The board's own spray at the top turn is drawn by the page, where it turns into the card's title.)"""
    global SPRAY
    rng = np.random.default_rng(1); n = 32000
    tb, r = rng.uniform(0, PERIOD, n), rng.random((n, 6))
    size, life = 0.006 + 0.014 * r[:, 5] ** 2, 0.45 + 0.5 * rng.random(n)
    yc = rng.integers(0, 2, n) * WAVE_GAP - WAVE_SPEED * tb         # the lip, where each wave is just breaking
    x = (yc - WAVE_YB) / WAVE_PEEL + 3.0 * r[:, 0] - 0.5
    p0 = np.c_[x, yc - 1.2 - 0.8 * r[:, 1], WAVE_H * (0.7 + 0.2 * r[:, 2])]
    v0 = np.c_[r[:, 3] - 0.5, -(WAVE_SPEED + 1 + 2.5 * r[:, 4]), 1.0 + 2.5 * r[:, 5]]
    if LOOP: p0[:, :2] -= WAVE_SPEED * (PERIOD - tb)[:, None]; v0[:, :2] += WAVE_SPEED    # the same droplets, seen from the wave's frame
    tet = np.array([(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)], 'f')
    me = bpy.data.meshes.new('spray'); i = 4 * np.arange(n)[:, None]
    me.from_pydata(np.zeros((4 * n, 3)).tolist(), [], np.concatenate([i + f for f in ((0, 1, 2), (0, 3, 1), (0, 2, 3), (1, 3, 2))]).tolist())
    m, nt, out = new_mat('spray'); p = node(nt, 'ShaderNodeBsdfPrincipled')
    put(p.inputs['Base Color'], (0.9, 0.9, 0.92)); put(p.inputs['Roughness'], 0.5)
    put(p.inputs['Emission Color'], (1.0, 0.9, 0.8)); put(p.inputs['Emission Strength'], 0.15)
    nt.links.new(p.outputs[0], out.inputs[0]); me.materials.append(m)
    link(bpy.data.objects.new('spray', me)); SPRAY = (me, tb, p0, v0, size, life, tet)

def spray_at(t):
    me, tb, p0, v0, size, life, tet = SPRAY
    age = (t - tb) % PERIOD; on = age < life
    c = p0 + v0 * age[:, None]; c[:, 2] -= 3.5 * age * age; c[~on] = (0, 0, -30)
    s = np.where(on, size * np.sqrt(np.clip(1 - age / life, 0, 1)), 0) * (1 - 0.6 * camera_at(t)[1])    # finer when the camera is alongside
    me.vertices.foreach_set('co', (c[:, None, :] + tet[None] * s[:, None, None]).astype('f').ravel()); me.update()

def sea_points(ob):
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
    ev = ob.evaluated_get(dg); m = ev.to_mesh()
    co = np.empty(len(m.vertices) * 3, 'f'); m.vertices.foreach_get('co', co); ev.to_mesh_clear()
    return co.reshape(-1, 3) + np.array(ob.location, 'f')

def float_on(sea, rig, cx=0.0, cy=0.0, yaw=None, roll=0.0):
    """Sit the rig on the local water plane: height plus tilt from a least-squares fit."""
    co = sea_points(sea) - np.array((cx, cy, 0), 'f')
    near = co[(np.abs(co[:, 0]) < 1.3) & (np.abs(co[:, 1]) < 1.3)]
    (sx, sy, h), *_ = np.linalg.lstsq(np.c_[near[:, 0], near[:, 1], np.ones(len(near))], near[:, 2], rcond=None)
    rig.location = (cx, cy, h + 0.015)
    rig.rotation_mode = 'QUATERNION'
    rig.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(Vector((-sx, -sy, 1))) @ Quaternion((0, 0, 1), RIG_YAW if yaw is None else yaw) @ Quaternion((1, 0, 0), roll)


# ================================================================ board + surfer
def link(ob, coll=None):
    (coll or bpy.context.scene.collection).objects.link(ob); return ob

def finish(ob, mat, rig, coll, subsurf=0):
    for p in ob.data.polygons: p.use_smooth = True
    ob.data.materials.append(mat)
    if subsurf: s = ob.modifiers.new('sub', 'SUBSURF'); s.levels = s.render_levels = subsurf
    ob.parent = rig; return link(ob, coll)

def blob(name, at, scale, mat, rig, coll, rot=(0, 0, 0)):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=40, v_segments=20, radius=1.0); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); ob.location, ob.scale, ob.rotation_euler = at, scale, rot
    return finish(ob, mat, rig, coll)

def tube(name, pts, edges, mat, rig, coll):
    """Skin-modifier body: pts = [(x, y, z, radius)]; first point is the root."""
    me = bpy.data.meshes.new(name); me.from_pydata([p[:3] for p in pts], edges, [])
    ob = bpy.data.objects.new(name, me); link(ob, coll)
    sk = ob.modifiers.new('skin', 'SKIN'); sk.use_smooth_shade = True
    for i, (v, p) in enumerate(zip(me.skin_vertices[0].data, pts)):
        v.radius = (p[3], p[3]); v.use_root = i == 0
    s = ob.modifiers.new('sub', 'SUBSURF'); s.levels = s.render_levels = 2
    me.materials.append(mat); ob.parent = rig
    return ob

def build_board(rig, coll):
    L, nx, nr = BOARD_L, 48, 20
    V, F = [], []
    for i, s in enumerate(np.linspace(-1, 1, nx)):
        w = BOARD_W * (1 - abs(s) ** (2.2 if s > 0 else 3.2)) ** 0.6 + 0.002
        t = 0.036 * (1 - abs(s) ** 4) ** 0.5 + 0.003
        rock = 0.085 * s * s * (1.5 if s > 0 else 0.5)
        for j in range(nr):
            c, sn = math.cos(2 * math.pi * j / nr), math.sin(2 * math.pi * j / nr)
            V.append((s * L / 2, w * math.copysign(abs(c) ** 0.75, c), t * math.copysign(abs(sn) ** 0.85, sn) + rock))
        if i: F += [((i - 1) * nr + j, (i - 1) * nr + (j + 1) % nr, i * nr + (j + 1) % nr, i * nr + j) for j in range(nr)]
    me = bpy.data.meshes.new('board'); me.from_pydata(V, [], F)
    # hull: unrendered sheet just under the board, wider by HULL_PAD; the sea is pressed down onto it
    H = [(s * L / 2 * 1.12, sy * (BOARD_W * (1 - abs(s) ** 3) ** 0.6 + HULL_PAD), 0.085 * s * s * (1.5 if s > 0 else 0.5) - 0.055)
         for s in np.linspace(-1, 1, nx) for sy in (1, -1)]
    hm = bpy.data.meshes.new('hull'); hm.from_pydata(H, [], [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(nx - 1)])
    hull = link(bpy.data.objects.new('hull', hm)); hull.parent, hull.hide_render = rig, True
    w = bpy.data.objects['sea'].modifiers.new('press', 'SHRINKWRAP')
    w.target, w.wrap_method, w.use_project_z = hull, 'PROJECT', True
    w.use_negative_direction, w.use_positive_direction = True, False
    w.show_viewport = False                                 # float_on reads the undisturbed sea
    return finish(bpy.data.objects.new('board', me), surface('board', BOARD, 0.25), rig, coll, 1)

def build_surfer(rig, coll):
    skin, shorts, hair, eye = surface('skin', SKIN, 0.55, 0.25), surface('shorts', SHORTS, 0.8), surface('hair', HAIR, 0.7), surface('eye', EYE, 0.2)
    tube('body', [(*q, r) for q, r in zip(POSES[REST], RADII)], [(0, 1), (1, 2), (2, 3), (2, 4), (4, 5), (5, 6), (2, 7), (7, 8), (8, 9),
                                                                  (0, 10), (10, 11), (11, 12), (0, 13), (13, 14), (14, 15)], skin, rig, coll)
    tube('shorts', [(0, 0, 0, .140), (0, 0, 0, .125), (0, 0, 0, .090), (0, 0, 0, .090)], [(0, 1), (0, 2), (0, 3)], shorts, rig, coll)
    head = link(bpy.data.objects.new('head', None), coll); head.parent = rig; head.scale = (HEAD,) * 3   # big cartoon head; its parts ride on this
    blob('skull', (0, 0, 0), (.165, .150, .160), skin, head, coll)
    blob('hair', (-.035, 0, .045), (.168, .160, .140), hair, head, coll, (0, rad(-18), 0))
    for dx, dy, dz, r in [(.085, .07, .135, .06), (.10, 0, .145, .065), (.085, -.07, .135, .06), (.04, .10, .10, .06), (.04, -.10, .10, .06)]:
        blob('tuft', (dx, dy, dz), (r * 1.25, r, r * .8), hair, head, coll)
    for sy in (1, -1):
        blob('eye', (.148, sy * .058, .015), (.014, .020, .028), eye, head, coll)
        blob('ear', (-.005, sy * .150, -.005), (.030, .016, .040), skin, head, coll)
    blob('nose', (.165, 0, -.030), (.030, .024, .022), skin, head, coll)
    set_pose(np.array(POSES[REST]))

def tint(nt, col):
    """Multiply col into every linked Base Color in a node tree (and the groups inside it)."""
    for n in list(nt.nodes):
        if n.type == 'GROUP' and n.node_tree: tint(n.node_tree, col)
        if n.type == 'BSDF_PRINCIPLED' and n.inputs['Base Color'].links:
            src = n.inputs['Base Color'].links[0].from_socket
            m = nt.nodes.new('ShaderNodeMix'); m.data_type, m.blend_type = 'RGBA', 'MULTIPLY'; m.inputs[0].default_value = 1.0
            m.inputs[7].default_value = (*col, 1); nt.links.new(src, m.inputs[6]); nt.links.new(m.outputs[2], n.inputs['Base Color'])

def build_human(rig, coll):
    """A rigged MakeHuman figure, standing on the board's origin facing the nose; set_pose drives its bones."""
    import addon_utils; addon_utils.enable('bl_ext.blender_org.mpfb')
    from bl_ext.blender_org.mpfb.services.humanservice import HumanService
    from bl_ext.blender_org.mpfb.services.targetservice import TargetService
    assets = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    h = HumanService.create_human(macro_detail_dict={**TargetService.get_default_macro_info_dict(), **HUMAN})
    import bl_ext.blender_org.mpfb as mpfb
    for k, w in HUMAN_FACE.items(): TargetService.load_target(h, os.path.join(os.path.dirname(mpfb.__file__), 'data', 'targets', k + '.target.gz'), weight=w)
    arm = HumanService.add_builtin_rig(h, 'game_engine')
    HumanService.set_character_skin(os.path.join(assets, HUMAN_SKIN), h)
    for kind, f in (('Eyes', 'eyes/low-poly/low-poly.mhclo'), ('Eyebrows', 'eyebrows/eyebrow001/eyebrow001.mhclo'),
                    ('Eyelashes', 'eyelashes/eyelashes01/eyelashes01.mhclo'), ('Hair', HUMAN_HAIR)):
        HumanService.add_mhclo_asset(os.path.join(assets, f), h, asset_type=kind)
    B = arm.data.bones
    sh = h.copy(); sh.data = h.data.copy(); sh.name = 'shorts'; link(sh)       # boardshorts: the body's own hips and thighs, puffed out
    co = [v.co.copy() for v in h.data.vertices]
    if sh.data.shape_keys:                                           # bake the body's morphs into the copy
        co = [k.co.copy() for k in sh.shape_key_add(name='mix', from_mix=True).data]; sh.shape_key_clear()
        for v, c in zip(sh.data.vertices, co): v.co = c
    bm = bmesh.new(); bm.from_mesh(sh.data); dl = bm.verts.layers.deform.verify(); g = h.vertex_groups['body'].index
    lo, hi = B['calf_l'].head_local.z + 0.10, B['pelvis'].head_local.z + 0.12
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if g not in v[dl] or not lo < v.co.z < hi + 0.04 or abs(v.co.x) > 0.3], context='VERTS')
    bmesh.ops.holes_fill(bm, edges=bm.edges, sides=8)
    bm.to_mesh(sh.data); bm.free()
    h.vertex_groups['body'].remove([v.index for v in h.data.vertices if lo + 0.06 < co[v.index].z < hi - 0.02 and abs(co[v.index].x) < 0.3])   # no skin under them to poke through
    pg = sh.vertex_groups.new(name='puff')
    for v in sh.data.vertices: pg.add([v.index], min(1.0, 0.25 + (hi + 0.04 - v.co.z) / 0.06), 'REPLACE')
    hair = next(c for c in arm.children if os.path.basename(HUMAN_HAIR)[:-6] in c.name); c = (B['head'].head_local + B['head'].tail_local) / 2
    for v in hair.data.vertices:
        d = v.co - c; v.co = c + Vector((d.x * HUMAN_HAIR_PUFF[0], d.y * HUMAN_HAIR_PUFF[1], d.z * (HUMAN_HAIR_PUFF[2] if d.z > 0 else 1 + HUMAN_HAIR_DROP)))
    tx = bpy.data.textures.new('wave', 'CLOUDS'); tx.noise_scale = 0.05
    d = hair.modifiers.new('wave', 'DISPLACE'); d.texture, d.strength, d.mid_level, d.texture_coords = tx, HUMAN_HAIR_WAVE, 0.5, 'LOCAL'; hair.modifiers.move(len(hair.modifiers) - 1, 0)
    for ob, col in (h, HUMAN_TAN), (hair, HUMAN_HAIR_TINT):
        for m in ob.data.materials: tint(m.node_tree, col)
    sh.data.materials.clear(); sh.data.materials.append(surface('shorts', SHORTS, 0.8))
    for m in [m for m in sh.modifiers if m.type != 'ARMATURE']: sh.modifiers.remove(m)
    d = sh.modifiers.new('puff', 'DISPLACE'); d.strength, d.mid_level, d.vertex_group = 0.03, 0.0, 'puff'; sh.modifiers.move(len(sh.modifiers) - 1, 0)
    m = sh.modifiers.new('drape', 'SMOOTH'); m.factor, m.iterations = 0.8, 14; sh.modifiers.move(len(sh.modifiers) - 1, 1)   # cloth hangs across the creases
    arm.parent, arm.rotation_euler, arm.scale = rig, (0, 0, rad(90)), (HUMAN_TALL / B['head'].tail_local.z,) * 3
    set_pose(np.array(POSES[REST]))

def aim(P, d):
    """Turn bone matrix P about its head, by the shortest rotation, so the bone points along d."""
    M = (P.col[1].xyz.rotation_difference(d).to_matrix() @ P.to_3x3()).to_4x4(); M.translation = P.translation; return M

def reach(a, t, pole, l1, l2):
    """Two-bone IK from a toward t, bending toward pole: the middle joint and the end it actually reaches."""
    n = t - a; d = min(max(n.length, abs(l1 - l2) + 1e-3), l1 + l2 - 1e-3); n.normalize()
    c = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d); side = pole - a; side -= n * side.dot(n); side.normalize()
    return a + l1 * (c * n + math.sqrt(1 - c * c) * side), a + d * n

def pose_human(q):
    arm = bpy.data.objects['Human.rig']; B = arm.data.bones
    q = [Vector((y, -x, z)) / arm.scale.x for x, y, z in q]          # board-local -> armature space (he faces -y, left is +x)
    spine = {'spine_01': q[1] - q[0], 'spine_02': q[2] - q[1], 'spine_03': q[3] - q[2], 'neck_01': q[16] - q[3], 'head': (q[16] - q[3]).normalized() + Vector((0, 0, 2.5))}   # head: chin up, so he looks ahead when prone
    M, ends = {}, {}
    for b in B:
        n = b.name; base, _, side = n.rpartition('_'); o = 3 * (side == 'r')
        P0 = M[b.parent.name] @ b.parent.matrix_local.inverted() @ b.matrix_local if b.parent else b.matrix_local.copy(); P = P0
        if n == 'pelvis':                                           # rigid: up along the lower spine, square to the shoulders
            u = (q[1] - q[0]).normalized(); l = q[4] - q[7]; l = (l - u * l.dot(u)).normalized(); f = l.cross(u)
            R = Matrix((l, -f, u)).transposed().to_4x4()
            P = Matrix.Translation(q[0]) @ R @ Matrix.Translation(-b.head_local) @ b.matrix_local
        elif n in spine:
            P = aim(P, spine[n])
            if n == 'head':                                         # then turn the face (rest: -y) toward the look point
                y = P.col[1].xyz; f = P.to_3x3() @ (b.matrix_local.to_3x3().inverted() @ Vector((0, -1, 0))); d = q[17] - P.translation
                f -= y * f.dot(y); d -= y * d.dot(y); P = aim(P, y); R = f.rotation_difference(d).to_matrix().to_4x4()
                P = Matrix.Translation(P.translation) @ R @ Matrix.Translation(-P.translation) @ P
        elif base in ('thigh', 'upperarm'):
            k = 10 if base == 'thigh' else 4; mid = B[('calf_' if base == 'thigh' else 'lowerarm_') + side]; end = B[('foot_' if base == 'thigh' else 'hand_') + side]
            ends[side + base[0]] = reach(P.translation, q[k + (1 if base == 'thigh' else 2) + o], q[k + (0 if base == 'thigh' else 1) + o],
                                         (mid.head_local - b.head_local).length, (end.head_local - mid.head_local).length)
            P = aim(P, ends[side + base[0]][0] - P.translation)
        elif base in ('calf', 'lowerarm'): P = aim(P, ends[side + 'tu'[base == 'lowerarm']][1] - P.translation)
        elif base == 'foot': P = aim(P, q[12 + o] - q[11 + o])
        M[n] = P; arm.pose.bones[n].matrix_basis = P0.inverted() @ P

def set_pose(q):
    """q: 17 board-local points (see POSES). Moves the body, the shorts and the head."""
    if WAVE: return pose_human(q)
    bpy.data.objects['body'].data.vertices.foreach_set('co', q[:16].ravel()); bpy.data.objects['body'].data.update()
    sh = np.array([q[0] + (0, 0, .003), q[0] + 0.67 * (q[1] - q[0]), q[0] + 0.75 * (q[10] - q[0]), q[0] + 0.75 * (q[13] - q[0])])
    bpy.data.objects['shorts'].data.vertices.foreach_set('co', sh.ravel()); bpy.data.objects['shorts'].data.update()
    bpy.data.objects['head'].location = q[16]

def key(keys, t):
    """Neighbouring keys around t and the eased blend between them."""
    i = max(k for k in range(len(keys)) if keys[k][0] <= t); j = min(i + 1, len(keys) - 1)
    f = (t - keys[i][0]) / (keys[j][0] - keys[i][0]) if j > i else 0.0
    return keys[i][1], keys[j][1], f * f * (3 - 2 * f)

def pose_at(t):
    def pts(name):
        q = np.array(POSES[name])
        if name == 'paddle':                                # alternate strokes: reach forward over the water, pull back through it
            for sh, el, ha, side, ph in ((4, 5, 6, 1, 0.0), (7, 8, 9, -1, math.pi)):
                a = 2 * math.pi * 1.0 * t + ph
                q[ha] = (0.32 + 0.40 * math.cos(a), side * .34, 0.05 - 0.16 * math.sin(a))
                q[el] = (q[sh] + q[ha]) / 2 + (0, side * .07, .09)
        if name == 'ride':                                  # sink into the turns
            q[:, 2] = np.where(q[:, 2] > .12, .12 + (q[:, 2] - .12) * (1 - 0.09 * min(abs(surf_path(t)[3]) / 0.6, 1)), q[:, 2])
        return q
    a, b, f = key(POSE_KEYS, t)
    return pts(a) * (1 - f) + pts(b) * f

def surf_pos(t):
    """Board x, y through the surf shot: wait, paddle in, carve along the face ahead of the peel, pull off, paddle back."""
    spot = np.array(WAVE_SPOT)
    def ride(t):                                            # in the wave's frame: out onto the shoulder and up, back to the pocket and down
        yc = WAVE_GAP - WAVE_SPEED * t; ph = 2 * math.pi / CARVE * (t - T_CATCH - 0.6)
        return np.array(((yc - WAVE_YB) / WAVE_PEEL - 2.5 - 1.5 * (1 - math.cos(ph)), yc - 2.9 - 1.1 * math.cos(ph)))
    def out(f):                                             # coast to a stop; the wave passes under him
        return ride(T_OUT) + (ride(T_OUT) - ride(T_OUT - 0.01)) / 0.01 * (T_DOWN - T_OUT) * (f - f * f / 2)
    if t < T_PADDLE: return spot
    if t < T_CATCH: return spot + (ride(T_CATCH) - spot) * ((t - T_PADDLE) / (T_CATCH - T_PADDLE)) ** 2
    if t < T_OUT or LOOP: return ride(t)                    # the loop shot never leaves the wave
    if t < T_DOWN: return out((t - T_OUT) / (T_DOWN - T_OUT))
    u = min((t - T_DOWN) / (T_BACK - T_DOWN), 1.0); f = 0.6 * u + 0.4 * u * u * (3 - 2 * u)
    return out(1.0) * (1 - f) + spot * f

def build_path():
    """Tabulate the surf shot at 48 Hz: position, heading (the direction he travels) and bank (into each turn)."""
    global TS, POS, YAW, ROLL, MID
    TS = np.arange(0, SURF_LEN + 0.5, 1 / 48)
    POS = np.array([surf_pos(t) for t in TS]); v = np.gradient(POS, 1 / 48, axis=0)
    go = np.hypot(v[:, 0], v[:, 1]) > 0.5
    yaw = np.interp(TS, TS[go], np.unwrap(np.arctan2(v[go, 1], v[go, 0])))
    def sm(a, b): f = np.clip((TS - a) / (b - a), 0, 1); return f * f * (3 - 2 * f)
    def blur(a, k): return np.convolve(np.pad(a, k, mode='edge'), np.ones(2 * k + 1) / (2 * k + 1), 'valid')
    home = rad(90)                                          # he sits facing out to sea, before and after
    f = sm(0.3, T_PADDLE + 0.4); yaw = (1 - f) * home + f * yaw
    f = sm(T_BACK - 0.3, T_BACK + 1.2); yaw = (1 - f) * yaw + f * (home + 2 * math.pi * round((yaw[-1] - home) / (2 * math.pi)))
    YAW = blur(yaw, 8)
    ROLL = blur(np.clip(-0.33 * np.gradient(YAW, 1 / 48), -0.6, 0.6) * sm(T_CATCH + 0.1, T_CATCH + 0.5) * (1 - sm(T_OUT + 0.2, T_OUT + 0.8) * (not LOOP)), 4)
    MID = np.c_[blur(POS[:, 0], round(CARVE * 24)), blur(POS[:, 1], round(CARVE * 24))]   # the path with the carving averaged out, for the camera

def surf_path(t):
    return tuple(float(np.interp(t, TS, a)) for a in (POS[:, 0], POS[:, 1], YAW, ROLL))


# ================================================================ camera, lights, render
def build_camera(rig):
    pos, aim, lens = (WAVE_CAM_POS, WAVE_CAM_AIM, WAVE_LENS) if WAVE else (CAM_POS, CAM_AIM, LENS)
    cam = bpy.data.cameras.new('cam'); cam.lens, cam.sensor_width = lens * A.zoom, 36
    cam.dof.use_dof, cam.dof.focus_object, cam.dof.aperture_fstop = STYLE != 'toon', rig, (1.6 if STYLE == 'clay' else 11 if WAVE else FSTOP)
    co = link(bpy.data.objects.new('cam', cam)); co.location = pos
    co.rotation_euler = (Vector(aim) - Vector(pos)).to_track_quat('-Z', 'Y').to_euler()
    bpy.context.scene.camera = co

def camera_at(t):
    """Where the camera is and how close it is (0 on the beach .. 1 alongside). It arrives alongside already moving with the wave."""
    beach, close, v = Vector(WAVE_CAM_POS), Vector(CLOSE_CAM), Vector((-WAVE_SPEED, -WAVE_SPEED, 0))
    def path(p0, v0, p1, v1, t0, t1):                       # cubic Hermite: position and speed set at both ends
        T = t1 - t0; f = (t - t0) / T
        return (2 * f ** 3 - 3 * f * f + 1) * p0 + (f ** 3 - 2 * f * f + f) * T * v0 + (3 * f * f - 2 * f ** 3) * p1 + (f ** 3 - f * f) * T * v1, f * f * (3 - 2 * f)
    if LOOP: return close, 1.0
    if SHOT != 'about' or not T_PUSH < t < T_PULL: return beach, 0.0
    if t < PERIOD: return path(beach, v * 0, close, v, T_PUSH, PERIOD)
    p, k = path(close, v, beach, v * 0, PERIOD, T_PULL); return p, 1 - k

def follow(rig, t):                                        # beach: a tripod pan, part of the way with the surfer; alongside: half-follows his carving
    co = bpy.context.scene.camera; pos, k = camera_at(t)
    co.location, co.data.lens = pos, (WAVE_LENS + (CLOSE_LENS - WAVE_LENS) * k) * A.zoom
    d = Vector(WAVE_CAM_AIM).lerp(rig.location + Vector((0, 0, A.aim_z)), CAM_FOLLOW if A.zoom == 1 else 1.0) - pos
    if A.zoom == 1: d.z = math.hypot(d.x, d.y) * math.tan(CAM_PITCH)
    if k:
        _, tv, D = clock(t); mid = Vector((np.interp(tv, TS, MID[:, 0]) + D, np.interp(tv, TS, MID[:, 1]) + D, 0))
        tgt = mid.lerp(rig.location, 0.5); tgt.z = 0          # level horizon: the tilt does not follow him up and down the face
        d = d.normalized().lerp((tgt + Vector(CLOSE_AIM) - pos).normalized(), k)
    co.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()

def track(rig):
    """Where the board (centre, tail) and the surfer's chest are in the frame: x, y as fractions from the bottom-left. The page aims its spray with this."""
    from bpy_extras.object_utils import world_to_camera_view as view
    bpy.context.view_layer.update(); sc = bpy.context.scene
    return [round(v, 4) for p in ((0, 0, 0.1), (-0.7, 0, 0.05), (-0.25, 0.1, 1.0)) for v in view(sc, sc.camera, rig.matrix_world @ Vector(p))[:2]]

def build_lights():
    s = bpy.data.lights.new('sun', 'SUN'); s.energy, s.color, s.angle = SUN_POWER, SUN_COL, SUN_ANGLE
    so = link(bpy.data.objects.new('sun', s)); so.visible_glossy = len(SUN_DISC) < 4; so.rotation_euler = (-SUN).to_track_quat('-Z', 'Y').to_euler()
    f = bpy.data.lights.new('fill', 'AREA'); f.energy, f.color, f.size = FILL_POWER * (2.2 if STYLE == 'clay' else 1), FILL_COL, 5.0
    fo = link(bpy.data.objects.new('fill', f)); fo.location = (2.5, -5.0, 3.0); fo.visible_glossy = False
    fo.rotation_euler = (Vector((0, 0, 0.3)) - fo.location).to_track_quat('-Z', 'Y').to_euler()

def setup_render(coll):
    sc = bpy.context.scene; r = sc.render
    r.engine, r.resolution_x, r.resolution_y, r.resolution_percentage = 'CYCLES', *RES, A.scale
    sc.cycles.samples, sc.cycles.use_denoising = A.samples, True
    try:
        pr = bpy.context.preferences.addons['cycles'].preferences; pr.compute_device_type = 'METAL' if sys.platform == 'darwin' else 'OPTIX'; pr.get_devices()
        for d in pr.devices: d.use = d.type != 'CPU'
        sc.cycles.device = 'GPU'
    except Exception as e: print('gpu off:', e)
    sc.view_settings.view_transform = 'AgX'
    if STYLE == 'film': sc.view_settings.exposure = EXPOSURE
    for look in ('AgX - Punchy', 'Punchy', 'AgX - Medium High Contrast', 'Medium High Contrast'):
        try: sc.view_settings.look = look; print('look', look); break
        except TypeError: pass
    if STYLE == 'toon':
        sc.view_settings.view_transform = 'Standard'
        r.use_freestyle = True; r.line_thickness = 2.2
        ls = bpy.context.view_layer.freestyle_settings.linesets.new('ink')
        ls.select_by_collection, ls.collection = True, coll
        ls.linestyle.color = (0.07, 0.04, 0.16)
    r.image_settings.file_format = 'PNG'
    r.filepath = os.path.abspath(A.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', f'{NAME}.png'))


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    coll = bpy.data.collections.new('surfer'); bpy.context.scene.collection.children.link(coll)
    rig = link(bpy.data.objects.new('rig', None), coll)
    build_sky(); sea = build_sea()
    build_board(rig, coll); (build_human if WAVE else build_surfer)(rig, coll)
    if SURF: build_path()
    if SPRAY_ON: build_spray()
    def at(t):                                             # the sea moves, the board rides it
        _, tv, D = clock(t)
        if WAVE: chop_at(sea, t); wave_shape(sea, t)
        else: sea.modifiers['ocean'].time = SEA_TIME + t
        x, y, yaw, roll = surf_path(tv) if SURF else (*WAVE_SPOT, rad(90), 0) if WAVE else (0, 0, None, 0)
        if SURF: set_pose(pose_at(tv))
        if SPRAY_ON: spray_at(t)
        float_on(sea, rig, x + D, y + D, yaw, roll)
        if WAVE and bpy.context.scene.camera: follow(rig, t)
    at(A.t); build_camera(rig); at(A.t); build_lights(); setup_render(coll)
    r = bpy.context.scene.render
    if not A.frames:
        bpy.ops.render.render(write_still=True); print('wrote', r.filepath, 'track', track(rig)); return
    base = os.path.join(os.path.dirname(r.filepath), f'{NAME}_loop'); tr = {}
    for f in range(A.start, A.frames, A.step):
        r.filepath = os.path.join(base, f'f{f:04d}.png')
        at(A.t + f / 24); tr[f] = track(rig)
        if not os.path.exists(r.filepath): bpy.ops.render.render(write_still=True)   # resume an interrupted run
    os.makedirs(base, exist_ok=True); json.dump(tr, open(os.path.join(base, f'track{A.start}.json'), 'w'))
    print('wrote', base)


main()
