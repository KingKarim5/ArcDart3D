from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18, GLUT_BITMAP_HELVETICA_12
import math
import random
# Camera-related variables
camera_pos = [0.0, -720.0, 360.0]  # mutable (arrow keys adjust it)
# Camera movement tuning (dynamic camera controls)
cam_zoom_step = 35.0    # UP/DOWN
cam_strafe_step = 30.0  # LEFT/RIGHT
cam_dist_min = 360.0
cam_dist_max = 1250.0
cam_x_limit = 520.0
cam_y_limit = 1400.0
cam_z_min = 120.0
cam_z_max = 920.0

fovY = 120  
GRID_LENGTH = 600  
rand_var = 423

rush_drain_mult_by_level = [1.00, 1.20, 1.40, 1.70, 2.00]   
rush_aim_speed_mult_by_level = [1.00, 1.20, 1.45, 1.70, 2.00]  
rush_aim_amp_mult_by_level = [1.00, 1.00, 1.06, 1.12, 1.18]    

dart_state = 0

dart_pos = [0.0, -640.0, 280.0]   
dart_vel = [0.0, 0.0, 0.0]        
dart_resolved_this_throw = False  

stuck_valid = False
stuck_pos = [0.0, 0.0, 0.0]
stuck_yaw = 0.0
stuck_pitch = 0.0


dart_yaw = 0.0    
dart_pitch = 0.0  

dt_fixed = 1.0
g = 0.28
wind_phase = 0.0

wind_gust_amp_base = 0.55
wind_gust_amp = wind_gust_amp_base
wind_gust_speed = 0.035

wind_lock_per_throw = True
wind_lock_x = 0.0
wind_lock_z = 0.0

level = 1
MAX_LEVEL = 5
level_hits = 0
hits_per_level = 5

boss_start_level = 4
boss_active = False
boss_shield_on = False
boss_phase_t = 0.0
boss_shield_on_time = 2.0
boss_shield_off_time = 2.0
boss_allowed_zones = ["T", "DBULL"]  

total_score = 0
last_hit_label = "—"
last_hit_points = 0
last_hit_accuracy = 0.0

combo_streak = 0
score_multiplier = 1
combo_accuracy_threshold = 85.0  


HEAT_N = 44  
heat = [[0 for _ in range(HEAT_N)] for _ in range(HEAT_N)]
heat_max = 1
heat_show = False  

heat_hits_total = 0
heat_sum_r = 0.0
heat_sum_r2 = 0.0
heat_best_streak = 0
heat_cur_streak = 0
heat_last_text = "—"
heat_wedge_counts = [0 for _ in range(20)]


# Fireworks / poppers (accuracy reward)
fireworks = []  
firework_max_particles = 260
firework_base_count = 46
firework_base_life = 52.0
firework_gravity_z = 0.10   
firework_drag = 0.985
firework_cooldown_frames = 0
firework_cooldown_max = 10  

game_mode = "rush"

rush_time_total = 60.0
rush_time_left = rush_time_total
rush_running = False
rush_over = False
rush_hits = 0

rush_recording = []
rush_recording_active = False
rush_recording_finished = False

replay_active = False
replay_cursor = 0.0
replay_speed = 0.05  

replay_buffer = []

best_rush_recording = []
best_rush_score = 0
best_rush_hits = 0

replay_chase_dist = 220.0
replay_side_offset = 140.0
replay_height = 75.0
replay_look_ahead = 220.0
replay_cut_blend = 0.06  
replay_orbit_radius = 780.0  

replay_view_side = 0

# One "Rewind" per round (Z)

rewind_available = True
rewind_has_snapshot = False
rewind_snapshot = None

# Trickshot state
trick_target_idx = 0
trick_hits = 0
trick_misses = 0
trick_miss_limit = 5
trick_over = False

# Replay / Ghost Run (Trickshot)
trick_recording = []
trick_recording_active = False
trick_recording_finished = False

obstacle_angle = 0.0
obstacle_speed = 1.1          
obstacle_span_deg = 54.0      
obstacle_r_in = 0.18          
obstacle_r_out = 0.94

# Used for both scoring and visuals
wedge_numbers = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]

# Call Your Shot (Mode 3)
call_active = False
call_announced = False
call_wedge_idx = 0
call_zone = "S"  # "S", "D", "T", "SBULL", "DBULL"
call_bonus = 15
call_rounds = 0
call_correct = 0
call_misses = 0
call_miss_limit = 5
call_over = False
# Persistent target for Mode 3 (always visible, like Mode 2)
call_target_wedge_idx = 0
call_target_zone = "S"  # "S", "D", "T", "SBULL", "DBULL"
call_hits = 0
# Persistent target for Mode 3 (always visible, like Mode 2)
call_target_wedge_idx = 0
call_target_zone = "S"  # "S", "D", "T", "SBULL", "DBULL"
call_hits = 0

call_recording = []
call_recording_active = False
call_recording_finished = False
board_spin_deg = 0.0
board_spin_speed = 0.30

board_center_base = [0.0, 0.0, 360.0]
board_center = [board_center_base[0], board_center_base[1], board_center_base[2]]  # mutable for mode 3
board_radius = 230.0
board_half = 270.0                   # half-size of visual square backing
stick_depth = 10.0                   # how deep the dart appears to stick in

aim_x = 0.0
aim_z = 0.0
aim_step = 6.0
aim_limit = board_radius * 0.92  
aim_locked = False

aim_phase = 0.0
aim_phase_speed = 0.022
aim_amp_x = board_radius * 0.62
aim_amp_z = board_radius * 0.46

throw_speed = 14.0

throw_start = (0.0, -640.0, 280.0)
throw_yaw = 90.0
throw_pitch = -10.0

world_margin = GRID_LENGTH + 220.0
# Aim Assist Cheat Toggle (C key)
aim_assist_mode = 0
aim_assist_wind_reduction = 0.3  
# Mode-Specific Cheats
# Mode 2 Cheat: Auto-aim snap to target (F key) - once per round

trick_autoaim_token_available = True
trick_autoaim_active = False
trick_autoaim_time_left = 0.0
trick_autoaim_duration = 4.0  # seconds to throw
trick_autoaim_snap_x = 0.0
trick_autoaim_snap_z = 0.0
trick_autoaim_bullseye_chance = 0.0   # bull is always wrong in Trickshot

# Mode 3 Cheat: Pause board spin for 0.8s after calling (P)
call_spin_pause_active = False
call_spin_pause_time_left = 0.0
call_spin_pause_duration = 5.0  # seconds

# Mode 3 Cheat: House Call Snap (F key) - auto-snap and track spinning target
call_house_snap_token_available = True
call_house_snap_active = False
call_house_snap_time_left = 0.0
call_house_snap_duration = 2.0  # seconds to throw
call_house_target_wedge_idx = 0
call_house_target_zone = "S"  # "S", "D", "T", "SBULL", "DBULL"
call_house_snap_x = 0.0
call_house_snap_z = 0.0


def draw_text(x, y, text, font=None, color=None):
    if font is None:
        font = GLUT_BITMAP_HELVETICA_18
    if color is None:
        color = (1.0, 1.0, 1.0)
    glColor3f(color[0], color[1], color[2])
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -0.6)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_right_hud_panel(x0=680, y0=520, x1=990, y1=790):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()


    glColor4f(0.06, 0.06, 0.08, 0.82) 
    glBegin(GL_QUADS)
    glVertex3f(x0, y0, 0.6)
    glVertex3f(x1, y0, 0.6)
    glVertex3f(x1, y1, 0.6)
    glVertex3f(x0, y1, 0.6)
    glEnd()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def clamp_value(v, lo, hi):
    if v < lo:
        return lo
    if v > hi:
        return hi
    return v

def _clamp01(a):
    if a < 0.0:
        return 0.0
    if a > 1.0:
        return 1.0
    return a

def spawn_fireworks(x, y, z, strength=1.0):
    global fireworks
    strength = _clamp01(strength)
    n = int(firework_base_count * (0.75 + 0.70 * strength))
    if n < 24:
        n = 24
    if n > 90:
        n = 90
    i = 0
    while i < n:
        a = random.random() * 6.283185307179586  # 2*pi
        u = random.random() * 2.0 - 1.0
        sx = math.cos(a) * math.sqrt(max(0.0, 1.0 - u * u))
        sz = math.sin(a) * math.sqrt(max(0.0, 1.0 - u * u))
        sy = u
        sy = -abs(sy) * (0.75 + 0.20 * random.random())

        # Speed scales with strength
        sp = (3.8 + 5.2 * random.random()) * (0.70 + 0.65 * strength)
        vx = sx * sp
        vy = sy * sp
        vz = sz * sp

        # Warm/cool fireworks palette
        if random.random() < 0.55:
            r = 1.0
            g = 0.65 + 0.35 * random.random()
            b = 0.10
        else:
            r = 0.10
            g = 0.75 + 0.25 * random.random()
            b = 1.0

        life = firework_base_life * (0.75 + 0.55 * random.random())
        fireworks.append([x, y, z, vx, vy, vz, life, r, g, b])

        i += 1

    # Trim oldest if too many
    if len(fireworks) > firework_max_particles:
        fireworks = fireworks[-firework_max_particles:]
def update_fireworks():
    global fireworks, firework_cooldown_frames
    if firework_cooldown_frames > 0:
        firework_cooldown_frames -= 1
    if len(fireworks) == 0:
        return
    new_list = []
    for p in fireworks:
        p[0] += p[3] * dt_fixed
        p[1] += p[4] * dt_fixed
        p[2] += p[5] * dt_fixed
        
        p[5] -= firework_gravity_z * dt_fixed
        
        p[3] *= firework_drag
        p[4] *= firework_drag
        p[5] *= firework_drag
       
        p[6] -= 1.0 * dt_fixed
        if p[6] > 0.0 and abs(p[0]) < (world_margin * 1.2) and abs(p[1]) < (world_margin * 1.2) and p[2] > -140.0:
            new_list.append(p)
    fireworks = new_list
def draw_fireworks():
    if len(fireworks) == 0:
        return
    for p in fireworks:
        life = p[6]
        fade = _clamp01(life / firework_base_life)
        r = p[7] * fade + 0.02
        g = p[8] * fade + 0.02
        b = p[9] * fade + 0.02
        glColor3f(r, g, b)
        glPushMatrix()
        glTranslatef(p[0], p[1], p[2])
        s = 0.35 + (1.0 - fade) * 0.25
        glScalef(s, s, s)
        glutSolidCube(10)
        glPopMatrix()

def _quad_xz(x0, z0, x1, z1):
    glVertex3f(x0, 0.0, z0)
    glVertex3f(x1, 0.0, z0)
    glVertex3f(x1, 0.0, z1)
    glVertex3f(x0, 0.0, z1)

def draw_digit_7seg(digit, size=10.0):
    if digit < 0 or digit > 9:
        return
    w = size
    h = size * 1.75
    t = size * 0.22
    xL = -w * 0.5
    xR = w * 0.5
    zB = -h * 0.5
    zT = h * 0.5
    zM = 0.0
    def seg_a():
        _quad_xz(xL + t * 0.45, zT - t, xR - t * 0.45, zT)
    def seg_d():
        _quad_xz(xL + t * 0.45, zB, xR - t * 0.45, zB + t)
    def seg_g():
        _quad_xz(xL + t * 0.45, zM - t * 0.5, xR - t * 0.45, zM + t * 0.5)
    def seg_f():
        _quad_xz(xL, zM + t * 0.45, xL + t, zT - t * 0.45)
    def seg_e():
        _quad_xz(xL, zB + t * 0.45, xL + t, zM - t * 0.45)
    def seg_b():
        _quad_xz(xR - t, zM + t * 0.45, xR, zT - t * 0.45)
    def seg_c():
        _quad_xz(xR - t, zB + t * 0.45, xR, zM - t * 0.45)

    # 7-seg bitmaps for 0-9: a b c d e f g
    masks = [
        (1, 1, 1, 1, 1, 1, 0),  # 0
        (0, 1, 1, 0, 0, 0, 0),  # 1
        (1, 1, 0, 1, 1, 0, 1),  # 2
        (1, 1, 1, 1, 0, 0, 1),  # 3
        (0, 1, 1, 0, 0, 1, 1),  # 4
        (1, 0, 1, 1, 0, 1, 1),  # 5
        (1, 0, 1, 1, 1, 1, 1),  # 6
        (1, 1, 1, 0, 0, 0, 0),  # 7
        (1, 1, 1, 1, 1, 1, 1),  # 8
        (1, 1, 1, 1, 0, 1, 1),  # 9
    ]

    a_on, b_on, c_on, d_on, e_on, f_on, g_on = masks[digit]
    glBegin(GL_QUADS)
    if a_on: seg_a()
    if b_on: seg_b()
    if c_on: seg_c()
    if d_on: seg_d()
    if e_on: seg_e()
    if f_on: seg_f()
    if g_on: seg_g()
    glEnd()

def draw_number_label(num, size=10.0, gap=3.0):
    if num < 0:
        return
    s = str(num)
    total_w = (len(s) * size) + ((len(s) - 1) * gap)
    x0 = -total_w * 0.5 + size * 0.5
    i = 0
    while i < len(s):
        ch = s[i]
        if ch >= "0" and ch <= "9":
            glPushMatrix()
            glTranslatef(x0 + i * (size + gap), 0.0, 0.0)
            draw_digit_7seg(int(ch), size=size)
            glPopMatrix()
        i += 1
def draw_board_numbers():
    bx, by, bz = board_center
    r_label = board_radius * 1.12
    if r_label > (board_half * 0.90):
        r_label = board_half * 0.90
    y_off = by + 1.45 

    # Digit styling
    glColor3f(0.95, 0.95, 0.95)
    size = board_radius * 0.070
    gap = size * 0.25

    i = 0
    while i < 20:
        ang_top = (i * 18.0)  
        
        if game_mode == "call":
            ang_top += board_spin_deg
        deg_std = 90.0 - ang_top
        rad = math.radians(deg_std)
        x = bx + r_label * math.cos(rad)
        z = bz + r_label * math.sin(rad)

        glPushMatrix()
        glTranslatef(x, y_off, z)
        # Rotate label so its "up" points outward from the center
        glRotatef(90.0 - deg_std, 0, 1, 0)
        draw_number_label(wedge_numbers[i], size=size, gap=gap)
        glPopMatrix()
        i += 1

def _angle_from_top_clockwise_deg(dx, dz):
    deg = math.degrees(math.atan2(dz, dx))  # 0 at +X, 90 at +Z
    ang = 90.0 - deg
    while ang < 0.0:
        ang += 360.0
    while ang >= 360.0:
        ang -= 360.0
    return ang

def _spin_adjust_angle_from_top(ang_top_deg):
    rotated = ang_top_deg - board_spin_deg
    while rotated < 0.0:
        rotated += 360.0
    while rotated >= 360.0:
        rotated -= 360.0
    return rotated

def _wedge_index_from_angle(ang_from_top_deg):
    idx = int(ang_from_top_deg / 18.0)
    if idx < 0:
        return 0
    if idx > 19:
        return 19
    return idx

def _calculate_autoaim_snap_point(target_wedge_idx):
    R = board_radius
    wedge_center_deg = target_wedge_idx * 18.0
    # Keep safely inside the wedge (wedge half-width is 9°). ±3° guarantees same wedge.
    snap_angle_deg = wedge_center_deg + random.uniform(-3.0, 3.0)
    # Choose a radius band (biased toward scoring rings) but never into bull area.
    zone_roll = random.random()
    if zone_roll < 0.40:          # triple
        r_min, r_max = R * 0.48, R * 0.56
    elif zone_roll < 0.70:        # double
        r_min, r_max = R * 0.88, R * 0.995
    else:                         # single 
        r_min, r_max = R * 0.16, R * 0.48

    snap_radius = random.uniform(r_min, r_max)
    deg_std = 90.0 - snap_angle_deg
    rad = math.radians(deg_std)
    snap_x = snap_radius * math.cos(rad)
    snap_z = snap_radius * math.sin(rad)
    return snap_x, snap_z


def _calculate_house_call_snap_point(target_wedge_idx, target_zone):
    R = board_radius
    current_spin = board_spin_deg
    wedge_center_deg = target_wedge_idx * 18.0
    visual_angle_deg = wedge_center_deg + current_spin
    while visual_angle_deg < 0.0:
        visual_angle_deg += 360.0
    while visual_angle_deg >= 360.0:
        visual_angle_deg -= 360.0
    
    snap_angle_deg = visual_angle_deg
    # Choose center radius of target zone (no randomization for cheat mode)
    if target_zone == "DBULL":
        snap_radius = R * 0.03  # Center of double bull
    elif target_zone == "SBULL":
        snap_radius = R * 0.10  # Center of single bull
    elif target_zone == "T":
        snap_radius = R * 0.52  # Center of triple ring
    elif target_zone == "D":
        snap_radius = R * 0.94  # Center of double ring
    else:  # "S"
        snap_radius = R * 0.32  # Center of single zone
    deg_std = 90.0 - snap_angle_deg
    rad = math.radians(deg_std)
    
    snap_x = snap_radius * math.cos(rad)
    snap_z = snap_radius * math.sin(rad)
    return snap_x, snap_z

def _zone_from_radius(r):
    R = board_radius
    r_double_in = R * 0.88
    r_triple_out = R * 0.56
    r_triple_in = R * 0.48
    r_bull_out = R * 0.14
    r_bull_in = R * 0.06

    if r <= r_bull_in:
        return "DBULL"
    if r <= r_bull_out:
        return "SBULL"
    if r_triple_in <= r <= r_triple_out:
        return "T"
    if r_double_in <= r <= R:
        return "D"
    return "S"

def _draw_called_region():
    if not call_announced:
        return
    bx, by, bz = board_center
    R = board_radius
    y = by + 1.25

    
    col = (0.15, 0.55, 0.95) 
    glColor3f(*col)

    if call_zone == "DBULL" or call_zone == "SBULL":
        r_in = 0.0
        r_out = R * 0.06
        if call_zone == "SBULL":
            r_in = R * 0.06
            r_out = R * 0.14

        a = 0.0
        step = 0.16
        glBegin(GL_QUADS)
        while a < 6.283:
            a0 = a
            a1 = a + step
            glVertex3f(bx + r_in * math.cos(a0), y, bz + r_in * math.sin(a0))
            glVertex3f(bx + r_out * math.cos(a0), y, bz + r_out * math.sin(a0))
            glVertex3f(bx + r_out * math.cos(a1), y, bz + r_out * math.sin(a1))
            glVertex3f(bx + r_in * math.cos(a1), y, bz + r_in * math.sin(a1))
            a = a1
        glEnd()
        return
    # Sector highlight for S/D/T
    r_in = 0.0
    r_out = R
    if call_zone == "D":
        r_in = R * 0.88
        r_out = R
    elif call_zone == "T":
        r_in = R * 0.48
        r_out = R * 0.56
    else:
        r_in = R * 0.14
        r_out = R * 0.48
    center_deg = call_wedge_idx * 18.0
    if game_mode == "call":
        center_deg += board_spin_deg
    a0_top = center_deg - 9.0
    a1_top = center_deg + 9.0
    def to_std_rad(ang_top_deg):
        return math.radians(90.0 - ang_top_deg)

    ra0 = to_std_rad(a0_top)
    ra1 = to_std_rad(a1_top)
    glBegin(GL_QUADS)
    glVertex3f(bx + r_in * math.cos(ra0), y, bz + r_in * math.sin(ra0))
    glVertex3f(bx + r_out * math.cos(ra0), y, bz + r_out * math.sin(ra0))
    glVertex3f(bx + r_out * math.cos(ra1), y, bz + r_out * math.sin(ra1))
    glVertex3f(bx + r_in * math.cos(ra1), y, bz + r_in * math.sin(ra1))
    glEnd()

def _is_blocked_by_obstacle(dx, dz):
    r2 = dx * dx + dz * dz
    r_in = board_radius * obstacle_r_in
    r_out = board_radius * obstacle_r_out
    if r2 < (r_in * r_in) or r2 > (r_out * r_out):
        return False

    ang = _angle_from_top_clockwise_deg(dx, dz)
    d = ang - obstacle_angle
    while d < -180.0:
        d += 360.0
    while d > 180.0:
        d -= 360.0
    return abs(d) <= (obstacle_span_deg * 0.5)

def _spin_adjust_angle_from_top(ang_from_top_deg):
    if (game_mode != "call"):
        return ang_from_top_deg
    ang = ang_from_top_deg - board_spin_deg
    while ang < 0.0:
        ang += 360.0
    while ang >= 360.0:
        ang -= 360.0
    return ang
def _draw_boss_shield_overlay():
    if (not boss_active) or (not boss_shield_on):
        return

    bx, by, bz = board_center
    R = board_radius
    y = by + 1.62
    r_in = R * 0.48
    r_out = R * 0.56
    glColor3f(0.55, 0.15, 0.85)
    a = 0.0
    step = 0.14
    glBegin(GL_QUADS)
    while a < 6.283:
        a0 = a
        a1 = a + step
        glVertex3f(bx + r_in * math.cos(a0), y, bz + r_in * math.sin(a0))
        glVertex3f(bx + r_out * math.cos(a0), y, bz + r_out * math.sin(a0))
        glVertex3f(bx + r_out * math.cos(a1), y, bz + r_out * math.sin(a1))
        glVertex3f(bx + r_in * math.cos(a1), y, bz + r_in * math.sin(a1))
        a = a1
    glEnd()
    r_in = 0.0
    r_out = R * 0.06
    glColor3f(0.05, 0.75, 1.0)
    a = 0.0
    glBegin(GL_QUADS)
    while a < 6.283:
        a0 = a
        a1 = a + step
        glVertex3f(bx + r_in * math.cos(a0), y, bz + r_in * math.sin(a0))
        glVertex3f(bx + r_out * math.cos(a0), y, bz + r_out * math.sin(a0))
        glVertex3f(bx + r_out * math.cos(a1), y, bz + r_out * math.sin(a1))
        glVertex3f(bx + r_in * math.cos(a1), y, bz + r_in * math.sin(a1))
        a = a1
    glEnd()

def _draw_trick_obstacle():
    bx, by, bz = board_center
    R = board_radius
    r_in = R * obstacle_r_in
    r_out = R * obstacle_r_out

    # Draw as a set of thin quads across the angular span
    half = obstacle_span_deg * 0.5
    a0 = obstacle_angle - half
    a1 = obstacle_angle + half

    # Step in degrees for smoothness
    step = 6.0
    a = a0
    glColor3f(0.10, 0.10, 0.14)
    while a < a1:
        b = a + step
        if b > a1:
            b = a1
        ra = math.radians(a)
        rb = math.radians(b)
        # convert to dx/dz using TOP-based clockwise:
        # ang=0 -> +Z, ang=90 -> +X
        cxa0 = math.cos(math.radians(90.0 - a))
        sza0 = math.sin(math.radians(90.0 - a))
        cxb0 = math.cos(math.radians(90.0 - b))
        szb0 = math.sin(math.radians(90.0 - b))

        glBegin(GL_QUADS)
        glVertex3f(bx + r_in * cxa0, by + 1.10, bz + r_in * sza0)
        glVertex3f(bx + r_out * cxa0, by + 1.10, bz + r_out * sza0)
        glVertex3f(bx + r_out * cxb0, by + 1.10, bz + r_out * szb0)
        glVertex3f(bx + r_in * cxb0, by + 1.10, bz + r_in * szb0)
        glEnd()

        a = b


def draw_dartboard():
    bx, by, bz = board_center
    # Backing square (matte black)
    glBegin(GL_QUADS)
    glColor3f(0.10, 0.10, 0.10)
    glVertex3f(bx - board_half, by, bz - board_half)
    glVertex3f(bx + board_half, by, bz - board_half)
    glVertex3f(bx + board_half, by, bz + board_half)
    glVertex3f(bx - board_half, by, bz + board_half)
    glEnd()
    # Dartboard ring radii (approx proportions for visual similarity)
    r_outer = board_radius
    r_double_in = r_outer * 0.88
    r_triple_out = r_outer * 0.56
    r_triple_in = r_outer * 0.48
    r_bull_out = r_outer * 0.14
    r_bull_in = r_outer * 0.06
    # Thin black rim outside the double ring
    rim = r_outer * 1.02
    if rim < (board_half * 0.98):
        a = 0.0
        step = 0.12
        glBegin(GL_QUADS)
        glColor3f(0.02, 0.02, 0.02)
        while a < 6.283:
            a0 = a
            a1 = a + step
            x0i = bx + r_outer * math.cos(a0)
            z0i = bz + r_outer * math.sin(a0)
            x0o = bx + rim * math.cos(a0)
            z0o = bz + rim * math.sin(a0)
            x1o = bx + rim * math.cos(a1)
            z1o = bz + rim * math.sin(a1)
            x1i = bx + r_outer * math.cos(a1)
            z1i = bz + r_outer * math.sin(a1)
            glVertex3f(x0i, by + 0.2, z0i)
            glVertex3f(x0o, by + 0.2, z0o)
            glVertex3f(x1o, by + 0.2, z1o)
            glVertex3f(x1i, by + 0.2, z1i)
            a = a1
        glEnd()

    c_cream = (0.93, 0.88, 0.78)
    c_black = (0.10, 0.10, 0.10)
    c_red = (0.85, 0.12, 0.12)
    c_green = (0.10, 0.62, 0.16)

    wedges = 20
    step = (2.0 * math.pi) / wedges
   
    wedge_rot = (math.pi * 0.5) - (step * 0.5)
    if game_mode == "call":
        wedge_rot -= math.radians(board_spin_deg)

    i = 0
    while i < wedges:
        a0 = (i * step) + wedge_rot
        a1 = ((i + 1) * step) + wedge_rot
        alt = (i % 2 == 0)

        cr, cg, cb = (c_cream if alt else c_black)
        glBegin(GL_QUADS)
        glColor3f(cr, cg, cb)
        glVertex3f(bx + r_triple_out * math.cos(a0), by + 0.3, bz + r_triple_out * math.sin(a0))
        glVertex3f(bx + r_double_in * math.cos(a0), by + 0.3, bz + r_double_in * math.sin(a0))
        glVertex3f(bx + r_double_in * math.cos(a1), by + 0.3, bz + r_double_in * math.sin(a1))
        glVertex3f(bx + r_triple_out * math.cos(a1), by + 0.3, bz + r_triple_out * math.sin(a1))
        glEnd()

        cr, cg, cb = (c_red if alt else c_green)
        glBegin(GL_QUADS)
        glColor3f(cr, cg, cb)
        glVertex3f(bx + r_double_in * math.cos(a0), by + 0.4, bz + r_double_in * math.sin(a0))
        glVertex3f(bx + r_outer * math.cos(a0), by + 0.4, bz + r_outer * math.sin(a0))
        glVertex3f(bx + r_outer * math.cos(a1), by + 0.4, bz + r_outer * math.sin(a1))
        glVertex3f(bx + r_double_in * math.cos(a1), by + 0.4, bz + r_double_in * math.sin(a1))
        glEnd()

        cr, cg, cb = (c_black if alt else c_cream)
        glBegin(GL_QUADS)
        glColor3f(cr, cg, cb)
        glVertex3f(bx + r_bull_out * math.cos(a0), by + 0.5, bz + r_bull_out * math.sin(a0))
        glVertex3f(bx + r_triple_in * math.cos(a0), by + 0.5, bz + r_triple_in * math.sin(a0))
        glVertex3f(bx + r_triple_in * math.cos(a1), by + 0.5, bz + r_triple_in * math.sin(a1))
        glVertex3f(bx + r_bull_out * math.cos(a1), by + 0.5, bz + r_bull_out * math.sin(a1))
        glEnd()

        cr, cg, cb = (c_green if alt else c_red)
        glBegin(GL_QUADS)
        glColor3f(cr, cg, cb)
        glVertex3f(bx + r_triple_in * math.cos(a0), by + 0.6, bz + r_triple_in * math.sin(a0))
        glVertex3f(bx + r_triple_out * math.cos(a0), by + 0.6, bz + r_triple_out * math.sin(a0))
        glVertex3f(bx + r_triple_out * math.cos(a1), by + 0.6, bz + r_triple_out * math.sin(a1))
        glVertex3f(bx + r_triple_in * math.cos(a1), by + 0.6, bz + r_triple_in * math.sin(a1))
        glEnd()

        i += 1

    a = 0.0
    step = 0.10

    # Outer bull
    glBegin(GL_QUADS)
    glColor3f(*c_green)
    while a < 6.283:
        a0 = a
        a1 = a + step
        glVertex3f(bx + r_bull_in * math.cos(a0), by + 0.75, bz + r_bull_in * math.sin(a0))
        glVertex3f(bx + r_bull_out * math.cos(a0), by + 0.75, bz + r_bull_out * math.sin(a0))
        glVertex3f(bx + r_bull_out * math.cos(a1), by + 0.75, bz + r_bull_out * math.sin(a1))
        glVertex3f(bx + r_bull_in * math.cos(a1), by + 0.75, bz + r_bull_in * math.sin(a1))
        a = a1
    glEnd()

    # Inner bull (solid-ish red disk using ring-to-center quads)
    a = 0.0
    glBegin(GL_QUADS)
    glColor3f(*c_red)
    while a < 6.283:
        a0 = a
        a1 = a + step
        # Use very small inner radius to avoid degenerate quads
        r0 = 0.6
        glVertex3f(bx + r0 * math.cos(a0), by + 0.85, bz + r0 * math.sin(a0))
        glVertex3f(bx + r_bull_in * math.cos(a0), by + 0.85, bz + r_bull_in * math.sin(a0))
        glVertex3f(bx + r_bull_in * math.cos(a1), by + 0.85, bz + r_bull_in * math.sin(a1))
        glVertex3f(bx + r0 * math.cos(a1), by + 0.85, bz + r0 * math.sin(a1))
        a = a1
    glEnd()
    # Numbers around the rim (standard dartboard order for Trickshot guidance)
    draw_board_numbers()
    # Heatmap overlay (GL_QUADS only; no new functions)
    if heat_show and (heat_hits_total > 0) and (heat_max > 0):
        cell = (2.0 * board_radius) / float(HEAT_N)
        y_overlay = by + 0.92  # above the rings, below crosshair
        i = 0
        while i < HEAT_N:
            x0 = bx - board_radius + i * cell
            x1 = x0 + cell
            xc = (x0 + x1) * 0.5 - bx
            j = 0
            while j < HEAT_N:
                c = heat[i][j]
                if c > 0:
                    z0 = bz - board_radius + j * cell
                    z1 = z0 + cell
                    zc = (z0 + z1) * 0.5 - bz
                    if (xc * xc + zc * zc) <= (board_radius * board_radius):
                        intensity = float(c) / float(heat_max)
                        if intensity > 1.0:
                            intensity = 1.0
                        # blue -> red ramp
                        glColor3f(intensity, 0.05, 1.0 - intensity)
                        glBegin(GL_QUADS)
                        glVertex3f(x0, y_overlay, z0)
                        glVertex3f(x1, y_overlay, z0)
                        glVertex3f(x1, y_overlay, z1)
                        glVertex3f(x0, y_overlay, z1)
                        glEnd()
                j += 1
            i += 1
    cx = bx + aim_x
    cz = bz + aim_z
    dx = cx - bx
    dz = cz - bz
    d2 = dx * dx + dz * dz
    if d2 > (aim_limit * aim_limit):

        inv = aim_limit / math.sqrt(d2)
        cx = bx + dx * inv
        cz = bz + dz * inv

    cross_len = 16.0
    cross_th = 1.8
    y_off = by + 0.95
    # Dark blue crosshair
    glColor3f(0.05, 0.10, 0.45)

    # Horizontal bar
    glBegin(GL_QUADS)
    glVertex3f(cx - cross_len, y_off, cz - cross_th)
    glVertex3f(cx + cross_len, y_off, cz - cross_th)
    glVertex3f(cx + cross_len, y_off, cz + cross_th)
    glVertex3f(cx - cross_len, y_off, cz + cross_th)
    glEnd()

    # Trickshot obstacle overlay
    if game_mode == "trick":
        _draw_trick_obstacle()
    if game_mode == "call":
        _draw_called_region()
    _draw_boss_shield_overlay()
    glBegin(GL_QUADS)
    glVertex3f(cx - cross_th, y_off, cz - cross_len)
    glVertex3f(cx + cross_th, y_off, cz - cross_len)
    glVertex3f(cx + cross_th, y_off, cz + cross_len)
    glVertex3f(cx - cross_th, y_off, cz + cross_len)
    glEnd()

def draw_board_stand():
    bx, by, bz = board_center
    r_outer = board_radius
    bottom_z = bz - (r_outer * 1.02)  
    if bottom_z < 40.0:
        bottom_z = 40.0

    pole_radius = 10.0
    pole_height = bottom_z 

    # Base plate
    glPushMatrix()
    glTranslatef(bx, by, 6.0)
    glColor3f(0.72, 0.55, 0.10)  # darker gold base
    glScalef(2.6, 1.2, 0.35)
    glutSolidCube(40)
    glPopMatrix()

    # Pole
    glPushMatrix()
    glTranslatef(bx, by, 0.0)
    glColor3f(1.00, 0.84, 0.20)  # gold
    gluCylinder(gluNewQuadric(), pole_radius, pole_radius, pole_height, 12, 12)
    glPopMatrix()

    # Small connector piece up to the board (slightly thicker)
    glPushMatrix()
    glTranslatef(bx, by, pole_height - 8.0)
    glColor3f(0.95, 0.80, 0.18)
    gluCylinder(gluNewQuadric(), pole_radius * 1.15, pole_radius * 1.15, 16.0, 12, 12)
    glPopMatrix()


def preview_dart_pose():
    cx, cy, cz = camera_pos
    tx, ty, tz = board_center

    dx = tx - cx
    dy = ty - cy
    dz = tz - cz
    d2 = dx * dx + dy * dy + dz * dz
    eps2 = 1e-12
    if d2 > eps2:
        inv = 1.0 / math.sqrt(d2)
        dx *= inv
        dy *= inv
        dz *= inv
    else:
        dx, dy, dz = 0.0, 1.0, 0.0

    dist = 165.0
    x = cx + dx * dist + 22.0
    y = cy + dy * dist
    z = cz + dz * dist - 70.0

    yaw = math.degrees(math.atan2(dy, dx))
    h2 = dx * dx + dy * dy
    if h2 > eps2:
        pitch = -math.degrees(math.atan2(dz, math.sqrt(h2)))
    else:
        pitch = 0.0

    return x, y, z, yaw, pitch


def draw_trajectory_prediction():
    if dart_state == 1:
        return  
    
    if not aim_locked:
        return  
    
    tx = board_center[0] + aim_x
    ty = board_center[1]
    tz = board_center[2] + aim_z
    
    start_pos = list(throw_start)
    dx = tx - start_pos[0]
    dy = ty - start_pos[1]
    dz = tz - start_pos[2]
    eps2 = 1e-12
    
    d2 = dx * dx + dy * dy + dz * dz
    if d2 <= eps2:
        return
    
    dist = math.sqrt(d2)
    T = dist / throw_speed
    if T < 10.0:
        T = 10.0
    if T > 60.0:
        T = 60.0
    
    wind_phase_local = wind_phase
    gust = wind_gust_amp * math.sin(wind_phase_local)
    if aim_assist_mode == 2 or aim_assist_mode == 3:
        gust *= aim_assist_wind_reduction
    
    sy = start_pos[1]
    wx = 0.0
    wz = 0.0
    if sy < -120.0:
        wx = 0.05 + 0.25 * gust
        wz = 0.00
    elif sy < 140.0:
        wx = 0.65 + 0.55 * gust
        wz = 0.02
    else:
        wx = -0.55 + 0.45 * gust
        wz = 0.00
    
    if aim_assist_mode == 2 or aim_assist_mode == 3:
        wx *= aim_assist_wind_reduction
        wz *= aim_assist_wind_reduction
    
    ax = wx if wind_lock_per_throw else 0.0
    ay = 0.0
    az = wz if wind_lock_per_throw else 0.0
    az -= g
    
    vel_x = (dx - 0.5 * ax * T * T) / T
    vel_y = (dy - 0.5 * ay * T * T) / T
    vel_z = (dz - 0.5 * az * T * T) / T
    
    # Simulate trajectory
    pos_x, pos_y, pos_z = start_pos[0], start_pos[1], start_pos[2]
    vel_x_sim, vel_y_sim, vel_z_sim = vel_x, vel_y, vel_z
    
    trajectory_points = []
    by = board_center[1]
    max_steps = 200
    step = 0
    
    while step < max_steps:
        trajectory_points.append((pos_x, pos_y, pos_z))
        prev_y = trajectory_points[-2][1] if len(trajectory_points) > 1 else start_pos[1]
        if prev_y < by and pos_y >= by:
            if step > 0:
                    t_hit = (by - prev_y) / (pos_y - prev_y) if (pos_y - prev_y) != 0 else 0.0
                    prev_x = trajectory_points[-2][0] if len(trajectory_points) > 1 else start_pos[0]
                    prev_z = trajectory_points[-2][2] if len(trajectory_points) > 1 else start_pos[2]
                    hit_x = prev_x + (pos_x - prev_x) * t_hit
                    hit_z = prev_z + (pos_z - prev_z) * t_hit
                    trajectory_points.append((hit_x, by, hit_z))
            break
        
        if wind_lock_per_throw:
            vel_x_sim += wx * dt_fixed
            vel_z_sim += wz * dt_fixed
        else:
            wind_phase_sim = wind_phase + (step * wind_gust_speed * dt_fixed)
            gust_sim = wind_gust_amp * math.sin(wind_phase_sim)
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                gust_sim *= aim_assist_wind_reduction
            
            wx_sim = 0.0
            wz_sim = 0.0
            if pos_y < -120.0:
                wx_sim = 0.05 + 0.25 * gust_sim
                wz_sim = 0.00
            elif pos_y < 140.0:
                wx_sim = 0.65 + 0.55 * gust_sim
                wz_sim = 0.02
            else:
                wx_sim = -0.55 + 0.45 * gust_sim
                wz_sim = 0.00
            
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                wx_sim *= aim_assist_wind_reduction
                wz_sim *= aim_assist_wind_reduction
            
            vel_x_sim += wx_sim * dt_fixed
            vel_z_sim += wz_sim * dt_fixed
        
        # Apply gravity
        vel_z_sim -= g * dt_fixed
        
        pos_x += vel_x_sim * dt_fixed
        pos_y += vel_y_sim * dt_fixed
        pos_z += vel_z_sim * dt_fixed
        
        step += 1
        
        if abs(pos_x) > world_margin or abs(pos_y) > world_margin or pos_z < -80.0:
            break
    
    if len(trajectory_points) < 2:
        return
    
    glColor3f(0.15, 0.4, 0.6)
    line_thickness = 1.5
    
    i = 0
    while i < len(trajectory_points) - 1:
        p0 = trajectory_points[i]
        p1 = trajectory_points[i + 1]
        dx_line = p1[0] - p0[0]
        dy_line = p1[1] - p0[1]
        dz_line = p1[2] - p0[2]
        len_line = math.sqrt(dx_line * dx_line + dy_line * dy_line + dz_line * dz_line)
        
        if len_line > eps2:
            perp_x = -dz_line / len_line * line_thickness
            perp_z = dx_line / len_line * line_thickness
            
            glBegin(GL_QUADS)
            glVertex3f(p0[0] - perp_x, p0[1], p0[2] - perp_z)
            glVertex3f(p0[0] + perp_x, p0[1], p0[2] + perp_z)
            glVertex3f(p1[0] + perp_x, p1[1], p1[2] + perp_z)
            glVertex3f(p1[0] - perp_x, p1[1], p1[2] - perp_z)
            glEnd()
        
        i += 1


def keyboardListener(key, x, y):
    global dart_state, dart_pos, dart_vel, dart_resolved_this_throw
    global dart_yaw, dart_pitch
    global aim_x, aim_z
    global aim_locked
    global wind_lock_x, wind_lock_z
    global wind_gust_amp, wind_phase
    global total_score, last_hit_label, last_hit_points, last_hit_accuracy
    global combo_streak, score_multiplier
    global heat, heat_max, heat_show
    global heat_hits_total, heat_sum_r, heat_sum_r2, heat_best_streak, heat_cur_streak, heat_last_text, heat_wedge_counts
    global level, level_hits, boss_active, boss_shield_on, boss_phase_t
    global game_mode
    if key == b'h' or key == b'H':
        heat_show = not heat_show
        return

    global rush_time_left, rush_running, rush_over, rush_hits
    global rush_recording, rush_recording_active, rush_recording_finished
    global trick_recording, trick_recording_active, trick_recording_finished
    global replay_active, replay_cursor, replay_speed
    global replay_buffer
    global best_rush_recording, best_rush_score, best_rush_hits
    global replay_view_side
    global trick_target_idx, trick_hits
    global trick_misses, trick_miss_limit, trick_over
    global obstacle_angle
    global board_center, board_center_base
    global call_active, call_announced, call_wedge_idx, call_zone, call_rounds, call_correct
    global call_recording, call_recording_active, call_recording_finished
    global board_spin_deg
    global stuck_valid
    global rewind_available, rewind_has_snapshot, rewind_snapshot
    global aim_assist_mode
    global trick_autoaim_token_available, trick_autoaim_active, trick_autoaim_time_left
    global trick_autoaim_snap_x, trick_autoaim_snap_z
    global call_spin_pause_active, call_spin_pause_time_left, call_spin_pause_duration
    global call_house_snap_token_available, call_house_snap_active, call_house_snap_time_left
    global call_house_target_wedge_idx, call_house_target_zone
    global call_house_snap_x, call_house_snap_z
    global call_misses, call_miss_limit, call_over
    global call_target_wedge_idx, call_target_zone, call_hits  # Added missing globals

    # -------------------------
    # Aim Assist Cheat Toggle (C)
    # -------------------------
    if key == b'c' or key == b'C':
        aim_assist_mode = (aim_assist_mode + 1) % 2
        if aim_assist_mode == 0:
            last_hit_label = "AIM ASSIST: OFF"
        elif aim_assist_mode == 1:
            last_hit_label = "AIM ASSIST: TRAJECTORY"
        return

    # Mode 3: Manual Aim Controls (A, D, S, X)
    
    if game_mode == "call" and dart_state != 1:
        # User requested controls: A=Left, D=Right, S=Up, X=Down
        changed = False
        if key == b'a' or key == b'A':
            aim_x -= aim_step
            changed = True
        elif key == b'd' or key == b'D':
            aim_x += aim_step
            changed = True
        elif key == b's' or key == b'S':
            aim_z += aim_step
            changed = True
        elif key == b'x' or key == b'X':
            aim_z -= aim_step
            changed = True
        
        if changed:
            # Clamp to circular board limit
            d2 = aim_x * aim_x + aim_z * aim_z
            lim2 = aim_limit * aim_limit
            if d2 > lim2:
                dist = math.sqrt(d2)
                aim_x = (aim_x / dist) * aim_limit
                aim_z = (aim_z / dist) * aim_limit
            return
    # Mode 2 Cheat: Auto-Aim Snap (F key) - once per round
    if key == b'f' or key == b'F':
        if game_mode == "trick":
            if trick_over:
                last_hit_label = "AUTO-AIM: GAME OVER"
                return
            if not trick_autoaim_token_available:
                last_hit_label = "AUTO-AIM: ALREADY USED"
                return
            if trick_autoaim_active:
                last_hit_label = "AUTO-AIM: ALREADY ACTIVE"
                return
            if dart_state == 1:
                last_hit_label = "AUTO-AIM: WAIT FOR DART"
                return
            
            snap_x, snap_z = _calculate_autoaim_snap_point(trick_target_idx)
            trick_autoaim_snap_x = snap_x
            trick_autoaim_snap_z = snap_z
            
            aim_x = snap_x
            aim_z = snap_z
            aim_locked = True
            
            # Activate auto-aim timer
            trick_autoaim_token_available = False
            trick_autoaim_active = True
            trick_autoaim_time_left = trick_autoaim_duration
            
            # Show target wedge in message
            last_hit_label = f"🎯 AUTO-AIM → TARGET {wedge_numbers[trick_target_idx]} ({trick_autoaim_duration}s)"
            return
        elif game_mode == "call":
            # Mode 3 Cheat: House Call Snap (F key) - once per round
            if call_over:
                last_hit_label = "HOUSE CALL: GAME OVER"
                return
            if not call_house_snap_token_available:
                last_hit_label = "HOUSE CALL: ALREADY USED"
                return
            if call_house_snap_active:
                last_hit_label = "HOUSE CALL: ALREADY ACTIVE"
                return
            if dart_state == 1:
                last_hit_label = "HOUSE CALL: WAIT FOR DART"
                return
            
            # Match house call target with the current Mode 3 target
            call_house_target_wedge_idx = call_target_wedge_idx
            call_house_target_zone = call_target_zone
            
            # Calculate initial snap point (will be updated in idle() as board spins)
            snap_x, snap_z = _calculate_house_call_snap_point(call_house_target_wedge_idx, call_house_target_zone)
            call_house_snap_x = snap_x
            call_house_snap_z = snap_z
            
            # Snap crosshair to calculated point
            aim_x = snap_x
            aim_z = snap_z
            
            # Lock aim automatically
            aim_locked = True
            
            # Activate house call snap timer
            call_house_snap_token_available = False
            call_house_snap_active = True
            call_house_snap_time_left = call_house_snap_duration
            
            # Activate spin pause as part of the cheat
            call_spin_pause_active = True
            call_spin_pause_time_left = call_spin_pause_duration
            
            # Show target in message
            if call_house_target_zone == "DBULL":
                target_text = "BULL (50)"
            elif call_house_target_zone == "SBULL":
                target_text = "OUTER BULL (25)"
            else:
                target_text = f"{call_house_target_zone}{wedge_numbers[call_house_target_wedge_idx]}"
            last_hit_label = f"🏠 HOUSE CALL → {target_text} ({call_house_snap_duration}s)"
            return
        else:
            last_hit_label = "F KEY: ONLY IN MODES 2/3"
            return
    # Replay controls (Rush)
    if key == b'g' or key == b'G':
        if game_mode == "call" and call_recording_finished and (len(call_recording) > 2):
            replay_active = True
            replay_cursor = 0.0
            replay_speed = 0.35
            replay_buffer = list(call_recording)
        elif game_mode == "trick" and trick_recording_finished and (len(trick_recording) > 2):
            replay_active = True
            replay_cursor = 0.0
            replay_speed = 0.35
            replay_buffer = list(trick_recording)
        elif rush_recording_finished and (len(rush_recording) > 2):
            replay_active = True
            replay_cursor = 0.0
            replay_speed = 0.35
            replay_buffer = list(rush_recording)
        elif trick_recording_finished and (len(trick_recording) > 2):
            replay_active = True
            replay_cursor = 0.0
            replay_speed = 0.35
            replay_buffer = list(trick_recording)
        return
    if key == b'n' or key == b'N':
        replay_active = False
        replay_buffer = []
        return
    if key == b'w' or key == b'W':
        replay_view_side = -1
        return
    if key == b'e' or key == b'E':
        replay_view_side = 1
        return

    if key == b'l' or key == b'L':
        if dart_state != 1:
            aim_locked = not aim_locked
        return
    # One Rewind per round (Z)
    
    if key == b'z' or key == b'Z':
        if replay_active:
            last_hit_label = "REWIND DISABLED DURING REPLAY"
            return
        if (not rewind_available) or (not rewind_has_snapshot) or (rewind_snapshot is None):
            last_hit_label = "REWIND NOT AVAILABLE"
            return
        snap = rewind_snapshot

        dart_state = snap["dart_state"]
        dart_resolved_this_throw = snap["dart_resolved"]
        dart_pos[0], dart_pos[1], dart_pos[2] = snap["dart_pos"]
        dart_vel[0], dart_vel[1], dart_vel[2] = snap["dart_vel"]
        dart_yaw = snap["dart_yaw"]
        dart_pitch = snap["dart_pitch"]

        aim_x = snap["aim_x"]
        aim_z = snap["aim_z"]
        aim_locked = snap["aim_locked"]

        wind_lock_x = snap["wind_lock_x"]
        wind_lock_z = snap["wind_lock_z"]
        wind_gust_amp = snap["wind_gust_amp"]
        wind_phase = snap["wind_phase"]

        total_score = snap["total_score"]
        last_hit_label = "REWIND!"
        last_hit_points = snap["last_hit_points"]
        last_hit_accuracy = snap["last_hit_accuracy"]
        combo_streak = snap["combo_streak"]
        score_multiplier = snap["score_multiplier"]

        stuck_valid = snap["stuck_valid"]
        stuck_pos[0], stuck_pos[1], stuck_pos[2] = snap["stuck_pos"]
        stuck_yaw = snap["stuck_yaw"]
        stuck_pitch = snap["stuck_pitch"]

        heat = snap["heat"]
        heat_max = snap["heat_max"]
        heat_show = snap["heat_show"]
        heat_hits_total = snap["heat_hits_total"]
        heat_sum_r = snap["heat_sum_r"]
        heat_sum_r2 = snap["heat_sum_r2"]
        heat_best_streak = snap["heat_best_streak"]
        heat_cur_streak = snap["heat_cur_streak"]
        heat_last_text = snap["heat_last_text"]
        heat_wedge_counts = snap["heat_wedge_counts"]

        level = snap["level"]
        level_hits = snap["level_hits"]
        boss_active = snap["boss_active"]
        boss_shield_on = snap["boss_shield_on"]
        boss_phase_t = snap["boss_phase_t"]
        game_mode = snap["game_mode"]
        rush_time_left = snap["rush_time_left"]
        rush_running = snap["rush_running"]
        rush_over = snap["rush_over"]
        rush_hits = snap["rush_hits"]

        trick_target_idx = snap["trick_target_idx"]
        trick_hits = snap["trick_hits"]
        obstacle_angle = snap["obstacle_angle"]

        call_active = snap["call_active"]
        call_announced = snap["call_announced"]
        call_wedge_idx = snap["call_wedge_idx"]
        call_zone = snap["call_zone"]
        call_rounds = snap["call_rounds"]
        call_correct = snap["call_correct"]

        board_spin_deg = snap["board_spin_deg"]

        aim_assist_mode = snap.get("aim_assist_mode", 0)
        if "rush_recording_len" in snap:
            n = snap["rush_recording_len"]
            if n < 0:
                n = 0
            if n < len(rush_recording):
                rush_recording = rush_recording[:n]

        rewind_available = False
        return

    if key == b'1':
        game_mode = "rush"
        rush_time_left = rush_time_total
        rush_running = False
        rush_over = False
        rush_hits = 0
        replay_active = False
        replay_cursor = 0.0
        replay_speed = 1.0
        replay_view_side = 0
        rush_recording = []
        rush_recording_active = False
        rush_recording_finished = False
        rewind_available = True
        rewind_has_snapshot = False
        rewind_snapshot = None
        trick_hits = 0
        trick_target_idx = random.randint(0, 19)
        board_center[0] = board_center_base[0]
        board_center[1] = board_center_base[1]
        board_center[2] = board_center_base[2]
        last_hit_label = "—"
        return
    if key == b'2':
        game_mode = "trick"
        trick_hits = 0
        trick_misses = 0
        trick_over = False
        trick_recording = []
        trick_recording_active = False
        trick_recording_finished = False
        trick_target_idx = random.randint(0, 19)
        obstacle_angle = 0.0
        board_center[0] = board_center_base[0]
        board_center[1] = board_center_base[1]
        board_center[2] = board_center_base[2]
        last_hit_label = "—"
        rewind_available = True
        rewind_has_snapshot = False
        rewind_snapshot = None

        trick_autoaim_token_available = True
        trick_autoaim_active = False
        trick_autoaim_time_left = 0.0
        trick_autoaim_snap_x = 0.0
        trick_autoaim_snap_z = 0.0
        return
    if key == b'3' or key == b'4':
        game_mode = "call"
        call_active = True
        call_announced = False
        call_wedge_idx = 0
        call_zone = "S"
        call_rounds = 0
        call_correct = 0
        call_misses = 0
        call_over = False
        call_hits = 0
        
        call_target_wedge_idx = random.randint(0, 19)
        zone_roll = random.random()
        if zone_roll < 0.15:  # 15% bullseye
            if random.random() < 0.5:
                call_target_zone = "DBULL"
            else:
                call_target_zone = "SBULL"
        elif zone_roll < 0.40:  # 25% triple
            call_target_zone = "T"
        elif zone_roll < 0.70:  # 30% double
            call_target_zone = "D"
        else:  # 30% single
            call_target_zone = "S"
        call_recording = []
        call_recording_active = False
        call_recording_finished = False
        board_spin_deg = 0.0
        last_hit_label = "—"
        rewind_available = True
        rewind_has_snapshot = False
        rewind_snapshot = None
        # Reset Mode 3 cheats
        call_spin_pause_active = False
        call_spin_pause_time_left = 0.0
        call_house_snap_token_available = True
        call_house_snap_active = False
        call_house_snap_time_left = 0.0
        call_house_target_wedge_idx = 0
        call_house_target_zone = "S"
        call_house_snap_x = 0.0
        call_house_snap_z = 0.0
        global fireworks, firework_cooldown_frames
        fireworks = []
        firework_cooldown_frames = 0
        return

    if key == b' ':
        if dart_state != 1:
            if not aim_locked:
                aim_locked = True
            if game_mode == "rush" and rush_over:
                return
            if game_mode == "trick" and trick_over:
                last_hit_label = "MODE 2 GAME OVER (R to reset)"
                return
            if game_mode == "call":
                if call_over:
                    last_hit_label = "MODE 3 GAME OVER (R to reset)"
                    return
                if (not call_house_snap_active) and (not call_announced):
                    last_hit_label = "PRESS P TO CALL OR F FOR HOUSE CALL"
                    return

            if rewind_available and (not replay_active):
                rewind_snapshot = {
                    "dart_state": dart_state,
                    "dart_resolved": dart_resolved_this_throw,
                    "dart_pos": (dart_pos[0], dart_pos[1], dart_pos[2]),
                    "dart_vel": (dart_vel[0], dart_vel[1], dart_vel[2]),
                    "dart_yaw": dart_yaw,
                    "dart_pitch": dart_pitch,
                    "aim_x": aim_x,
                    "aim_z": aim_z,
                    "aim_locked": aim_locked,
                    "wind_lock_x": wind_lock_x,
                    "wind_lock_z": wind_lock_z,
                    "wind_gust_amp": wind_gust_amp,
                    "wind_phase": wind_phase,
                    "total_score": total_score,
                    "last_hit_points": last_hit_points,
                    "last_hit_accuracy": last_hit_accuracy,
                    "combo_streak": combo_streak,
                    "score_multiplier": score_multiplier,
                    "stuck_valid": stuck_valid,
                    "stuck_pos": (stuck_pos[0], stuck_pos[1], stuck_pos[2]),
                    "stuck_yaw": stuck_yaw,
                    "stuck_pitch": stuck_pitch,
                    "heat": [row[:] for row in heat],
                    "heat_max": heat_max,
                    "heat_show": heat_show,
                    "heat_hits_total": heat_hits_total,
                    "heat_sum_r": heat_sum_r,
                    "heat_sum_r2": heat_sum_r2,
                    "heat_best_streak": heat_best_streak,
                    "heat_cur_streak": heat_cur_streak,
                    "heat_last_text": heat_last_text,
                    "heat_wedge_counts": list(heat_wedge_counts),
                    "level": level,
                    "level_hits": level_hits,
                    "boss_active": boss_active,
                    "boss_shield_on": boss_shield_on,
                    "boss_phase_t": boss_phase_t,
                    "game_mode": game_mode,
                    "rush_time_left": rush_time_left,
                    "rush_running": rush_running,
                    "rush_over": rush_over,
                    "rush_hits": rush_hits,
                    "trick_target_idx": trick_target_idx,
                    "trick_hits": trick_hits,
                    "obstacle_angle": obstacle_angle,
                    "call_active": call_active,
                    "call_announced": call_announced,
                    "call_wedge_idx": call_wedge_idx,
                    "call_zone": call_zone,
                    "call_rounds": call_rounds,
                    "call_correct": call_correct,
                    "board_spin_deg": board_spin_deg,
                    "rush_recording_len": len(rush_recording),
                    "aim_assist_mode": aim_assist_mode,
                }
                rewind_has_snapshot = True

            dart_state = 1
            dart_resolved_this_throw = False
            
            # Mode 2 Cheat: Deactivate auto-aim when dart is thrown
            if game_mode == "trick" and trick_autoaim_active:
                trick_autoaim_active = False
                trick_autoaim_time_left = 0.0
            
            if game_mode == "rush" and (not rush_running) and (not rush_over):
                rush_running = True
                # --- Start recording this Rush run on first throw
                rush_recording = []
                rush_recording_active = True
                rush_recording_finished = False
            if game_mode == "trick" and (not trick_recording_active) and (not trick_recording_finished) and (not trick_over):
                trick_recording = []
                trick_recording_active = True
                trick_recording_finished = False
            # Mode 3 replay: start recording if not already active
            if game_mode == "call":
                if not call_recording_active:
                    call_recording = []
                    call_recording_active = True
                    call_recording_finished = False
                # Deactivate house call snap when dart is thrown
                if call_house_snap_active:
                    call_house_snap_active = False
                    call_house_snap_time_left = 0.0
            dart_pos[0], dart_pos[1], dart_pos[2] = throw_start
            tx = board_center[0] + aim_x
            ty = board_center[1]
            tz = board_center[2] + aim_z

            wind_phase_local = wind_phase
            gust = wind_gust_amp * math.sin(wind_phase_local)
            
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                gust *= aim_assist_wind_reduction
            sy = dart_pos[1]
            wx = 0.0
            wz = 0.0
            if sy < -120.0:
                wx = 0.05 + 0.25 * gust
                wz = 0.00
            elif sy < 140.0:
                wx = 0.65 + 0.55 * gust
                wz = 0.02
            else:
                wx = -0.55 + 0.45 * gust
                wz = 0.00
           
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                wx *= aim_assist_wind_reduction
                wz *= aim_assist_wind_reduction
            wind_lock_x = wx
            wind_lock_z = wz

            dx = tx - dart_pos[0]
            dy = ty - dart_pos[1]
            dz = tz - dart_pos[2]
            eps2 = 1e-12

            d2 = dx * dx + dy * dy + dz * dz
            if d2 > eps2:
                dist = math.sqrt(d2)
                T = dist / throw_speed
                if T < 10.0:
                    T = 10.0
                if T > 60.0:
                    T = 60.0

                ax = (wind_lock_x if wind_lock_per_throw else 0.0)
                ay = 0.0
                az = (wind_lock_z if wind_lock_per_throw else 0.0) - g

                dart_vel[0] = (dx - 0.5 * ax * T * T) / T
                dart_vel[1] = (dy - 0.5 * ay * T * T) / T
                dart_vel[2] = (dz - 0.5 * az * T * T) / T
            else:
                
                dart_vel[0] = 0.0
                dart_vel[1] = throw_speed
                dart_vel[2] = 0.0

            vx, vy, vz = dart_vel[0], dart_vel[1], dart_vel[2]
            h2 = vx * vx + vy * vy
            if h2 > eps2:
                dart_yaw = math.degrees(math.atan2(vy, vx))
                horiz = math.sqrt(h2)
                dart_pitch = -math.degrees(math.atan2(vz, horiz))
            else:
                dart_yaw = throw_yaw
                dart_pitch = throw_pitch

    # Reset dart (R)
    if key == b'r' or key == b'R':
        replay_active = False
        replay_cursor = 0.0
        replay_speed = 1.0
        replay_view_side = 0
        rewind_available = True
        rewind_has_snapshot = False
        rewind_snapshot = None
        dart_state = 0
        dart_resolved_this_throw = False
        dart_pos[0], dart_pos[1], dart_pos[2] = throw_start
        dart_vel[0], dart_vel[1], dart_vel[2] = 0.0, 0.0, 0.0
        dart_yaw = 0.0
        dart_pitch = 0.0
        aim_x = 0.0
        aim_z = 0.0
        aim_locked = False
        stuck_valid = False

        #Reset
        total_score = 0
        last_hit_label = "—"
        last_hit_points = 0
        last_hit_accuracy = 0.0
        combo_streak = 0
        score_multiplier = 1

        # Reset heatmap + analytics
        heat = [[0 for _ in range(HEAT_N)] for _ in range(HEAT_N)]
        heat_max = 1
        heat_show = False
        heat_hits_total = 0
        heat_sum_r = 0.0
        heat_sum_r2 = 0.0
        heat_best_streak = 0
        heat_cur_streak = 0
        heat_last_text = "—"
        heat_wedge_counts = [0 for _ in range(20)]

        # Reset progression / boss
        level = 1
        level_hits = 0
        boss_active = False
        boss_shield_on = False
        boss_phase_t = 0.0
        wind_gust_amp = wind_gust_amp_base

        # Reset modes
        rush_time_left = rush_time_total
        rush_running = False
        rush_over = False
        rush_hits = 0
        rush_recording = []
        rush_recording_active = False
        rush_recording_finished = False
        replay_buffer = []
        best_rush_recording = []
        best_rush_score = 0
        best_rush_hits = 0
        trick_hits = 0
        trick_misses = 0
        trick_over = False
        trick_recording = []
        trick_recording_active = False
        trick_recording_finished = False
        trick_target_idx = random.randint(0, 19)
        obstacle_angle = 0.0
        board_center[0] = board_center_base[0]
        board_center[1] = board_center_base[1]
        board_center[2] = board_center_base[2]
        call_active = (game_mode == "call")  # Keep active if we are in this mode
        call_announced = False
        call_wedge_idx = 0
        call_zone = "S"
        call_rounds = 0
        call_correct = 0
        call_hits = 0
        call_misses = 0
        call_over = False
        
        # Reset Mode 3 persistent target
        call_target_wedge_idx = random.randint(0, 19)
        zone_roll = random.random()
        if zone_roll < 0.15: 
            if random.random() < 0.5: call_target_zone = "DBULL"
            else: call_target_zone = "SBULL"
        elif zone_roll < 0.40: call_target_zone = "T"
        elif zone_roll < 0.70: call_target_zone = "D"
        else: call_target_zone = "S"

        call_recording = []
        call_recording_active = False
        call_recording_finished = False
        board_spin_deg = 0.0

        # Reset cheat tokens
        trick_autoaim_token_available = True
        trick_autoaim_active = False
        trick_autoaim_time_left = 0.0
        trick_autoaim_snap_x = 0.0
        trick_autoaim_snap_z = 0.0
        
        call_spin_pause_active = False
        call_spin_pause_time_left = 0.0
        call_house_snap_token_available = True
        call_house_snap_active = False
        call_house_snap_time_left = 0.0

        fireworks = []
        firework_cooldown_frames = 0


def specialKeyListener(key, x, y):
    global camera_pos

    cx, cy, cz = camera_pos[0], camera_pos[1], camera_pos[2]
    tx, ty, tz = board_center

    fx = tx - cx
    fy = ty - cy
    fz = tz - cz
    f2 = fx * fx + fy * fy + fz * fz
    eps2 = 1e-12
    if f2 <= eps2:
        fx, fy, fz = 0.0, 1.0, 0.0
        f2 = 1.0

    invf = 1.0 / math.sqrt(f2)
    fx *= invf
    fy *= invf
    fz *= invf

    ux, uy, uz = 0.0, 0.0, 1.0

    rx = fy * uz - fz * uy
    ry = fz * ux - fx * uz
    rz = fx * uy - fy * ux
    r2 = rx * rx + ry * ry + rz * rz
    if r2 > eps2:
        invr = 1.0 / math.sqrt(r2)
        rx *= invr
        ry *= invr
        rz *= invr
    else:
        rx, ry, rz = 1.0, 0.0, 0.0

    # Apply movement
    if key == GLUT_KEY_UP:
        cx += fx * cam_zoom_step
        cy += fy * cam_zoom_step
        cz += fz * cam_zoom_step
    elif key == GLUT_KEY_DOWN:
        cx -= fx * cam_zoom_step
        cy -= fy * cam_zoom_step
        cz -= fz * cam_zoom_step
    elif key == GLUT_KEY_LEFT:
        # Move west (left relative to view direction)
        cx -= rx * cam_strafe_step
        cy -= ry * cam_strafe_step
        cz -= rz * cam_strafe_step
    elif key == GLUT_KEY_RIGHT:
        # Move east (right relative to view direction)
        cx += rx * cam_strafe_step
        cy += ry * cam_strafe_step
        cz += rz * cam_strafe_step
    else:
        return

    # Clamp distance to target
    dx = tx - cx
    dy = ty - cy
    dz = tz - cz
    d2 = dx * dx + dy * dy + dz * dz
    if d2 > eps2:
        dist = math.sqrt(d2)
        if dist < cam_dist_min:
            s = cam_dist_min / dist
            cx = tx - dx * s
            cy = ty - dy * s
            cz = tz - dz * s
        elif dist > cam_dist_max:
            s = cam_dist_max / dist
            cx = tx - dx * s
            cy = ty - dy * s
            cz = tz - dz * s

    board_safety_margin = board_radius * 0.5  
    if cy > (ty - board_safety_margin):
        cy = ty - board_safety_margin

    # Clamp world bounds (prevents losing the board)
    cx = clamp_value(cx, -cam_x_limit, cam_x_limit)
    cy = clamp_value(cy, -cam_y_limit, cam_y_limit)
    cz = clamp_value(cz, cam_z_min, cam_z_max)

    camera_pos[0], camera_pos[1], camera_pos[2] = cx, cy, cz


def mouseListener(button, state, x, y):
    global dart_state, dart_pos, dart_vel, dart_yaw, dart_pitch
    global aim_x, aim_z
    global aim_locked
    global wind_lock_x, wind_lock_z
    global dart_resolved_this_throw
    global game_mode, rush_running, rush_over
    global trick_over
    global call_announced
    global aim_assist_mode
    global trick_autoaim_active, trick_autoaim_time_left
    global rush_recording, rush_recording_active, rush_recording_finished
    global trick_recording, trick_recording_active, trick_recording_finished
    global call_recording, call_recording_active, call_recording_finished
    global total_score, last_hit_points, last_hit_accuracy, combo_streak, score_multiplier, last_hit_label
    global heat, heat_max, heat_show
    global heat_hits_total, heat_sum_r, heat_sum_r2, heat_best_streak, heat_cur_streak, heat_last_text, heat_wedge_counts
    global level, level_hits, boss_active, boss_shield_on, boss_phase_t, wind_gust_amp, wind_phase
    global trick_target_idx, trick_hits, obstacle_angle
    global call_active, call_wedge_idx, call_zone, call_rounds, call_correct
    global call_misses, call_miss_limit, call_over
    global call_house_snap_token_available, call_house_snap_active, call_house_snap_time_left
    global call_house_target_wedge_idx, call_house_target_zone
    global call_house_snap_x, call_house_snap_z
    global call_target_wedge_idx, call_target_zone, call_hits
    global board_spin_deg
    global stuck_valid, stuck_pos, stuck_yaw, stuck_pitch
    global replay_active
    global rewind_available, rewind_has_snapshot, rewind_snapshot
    global fireworks, firework_cooldown_frames
    global call_spin_pause_active, call_spin_pause_time_left, call_spin_pause_duration


    # Right click: Call Your Shot (Mode 3)
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if game_mode == "call" and dart_state != 1:
            if not aim_locked:
                last_hit_label = "LOCK AIM (L) THEN RIGHT CLICK"
                return

            dx = aim_x
            dz = aim_z
            r = math.sqrt(dx * dx + dz * dz)
            call_zone = _zone_from_radius(r)
            ang = _angle_from_top_clockwise_deg(dx, dz)
        
            ang = _spin_adjust_angle_from_top(ang)
            ang += 9.0
            while ang >= 360.0:
                ang -= 360.0
            call_wedge_idx = _wedge_index_from_angle(ang)
            call_announced = True

            if call_zone == "DBULL":
                last_hit_label = "CALLED: BULL (50)"
            elif call_zone == "SBULL":
                last_hit_label = "CALLED: OUTER BULL (25)"
            else:
                last_hit_label = f"CALLED: {call_zone}{wedge_numbers[call_wedge_idx]}"
            return

    # Left click: throw
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if dart_state != 1:
            if not aim_locked:
                aim_locked = True
            if game_mode == "rush" and rush_over:
                return
            if game_mode == "trick" and trick_over:
                last_hit_label = "MODE 2 GAME OVER (R to reset)"
                return
            if game_mode == "call":
                if call_over:
                    last_hit_label = "MODE 3 GAME OVER (R to reset)"
                    return
                if (not call_house_snap_active) and (not call_announced):
                    last_hit_label = "RIGHT CLICK TO CALL OR F FOR HOUSE CALL"
                    return

            if rewind_available and (not replay_active):
                rewind_snapshot = {
                    "dart_state": dart_state,
                    "dart_resolved": dart_resolved_this_throw,
                    "dart_pos": (dart_pos[0], dart_pos[1], dart_pos[2]),
                    "dart_vel": (dart_vel[0], dart_vel[1], dart_vel[2]),
                    "dart_yaw": dart_yaw,
                    "dart_pitch": dart_pitch,
                    "aim_x": aim_x,
                    "aim_z": aim_z,
                    "aim_locked": aim_locked,
                    "wind_lock_x": wind_lock_x,
                    "wind_lock_z": wind_lock_z,
                    "wind_gust_amp": wind_gust_amp,
                    "wind_phase": wind_phase,
                    "total_score": total_score,
                    "last_hit_points": last_hit_points,
                    "last_hit_accuracy": last_hit_accuracy,
                    "combo_streak": combo_streak,
                    "score_multiplier": score_multiplier,
                    "stuck_valid": stuck_valid,
                    "stuck_pos": (stuck_pos[0], stuck_pos[1], stuck_pos[2]),
                    "stuck_yaw": stuck_yaw,
                    "stuck_pitch": stuck_pitch,
                    "heat": [row[:] for row in heat],
                    "heat_max": heat_max,
                    "heat_show": heat_show,
                    "heat_hits_total": heat_hits_total,
                    "heat_sum_r": heat_sum_r,
                    "heat_sum_r2": heat_sum_r2,
                    "heat_best_streak": heat_best_streak,
                    "heat_cur_streak": heat_cur_streak,
                    "heat_last_text": heat_last_text,
                    "heat_wedge_counts": list(heat_wedge_counts),
                    "level": level,
                    "level_hits": level_hits,
                    "boss_active": boss_active,
                    "boss_shield_on": boss_shield_on,
                    "boss_phase_t": boss_phase_t,
                    "game_mode": game_mode,
                    "rush_time_left": rush_time_left,
                    "rush_running": rush_running,
                    "rush_over": rush_over,
                    "rush_hits": rush_hits,
                    "trick_target_idx": trick_target_idx,
                    "trick_hits": trick_hits,
                    "obstacle_angle": obstacle_angle,
                    "call_active": call_active,
                    "call_announced": call_announced,
                    "call_wedge_idx": call_wedge_idx,
                    "call_zone": call_zone,
                    "call_rounds": call_rounds,
                    "call_correct": call_correct,
                    "board_spin_deg": board_spin_deg,
                    "rush_recording_len": len(rush_recording),
                    "aim_assist_mode": aim_assist_mode,
                }
                rewind_has_snapshot = True
            dart_state = 1
            dart_resolved_this_throw = False
            
            # Mode 2 Cheat: Deactivate auto-aim when dart is thrown
            if game_mode == "trick" and trick_autoaim_active:
                trick_autoaim_active = False
                trick_autoaim_time_left = 0.0
            
            if game_mode == "rush" and (not rush_running) and (not rush_over):
                rush_running = True
                rush_recording = []
                rush_recording_active = True
                rush_recording_finished = False
            if game_mode == "trick" and (not trick_recording_active) and (not trick_recording_finished) and (not trick_over):
                trick_recording = []
                trick_recording_active = True
                trick_recording_finished = False

            # Mode 3 replay: start recording if not already active
            if game_mode == "call":
                if not call_recording_active:
                    call_recording = []
                    call_recording_active = True
                    call_recording_finished = False
                # Deactivate house call snap when dart is thrown
                if call_house_snap_active:
                    call_house_snap_active = False
                    call_house_snap_time_left = 0.0
            dart_pos[0], dart_pos[1], dart_pos[2] = throw_start

            tx = board_center[0] + aim_x
            ty = board_center[1]
            tz = board_center[2] + aim_z
            dx = tx - dart_pos[0]
            dy = ty - dart_pos[1]
            dz = tz - dart_pos[2]
            eps2 = 1e-12

            wind_phase_local = wind_phase
            gust = wind_gust_amp * math.sin(wind_phase_local)
           
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                gust *= aim_assist_wind_reduction
            sy = dart_pos[1]
            wx = 0.0
            wz = 0.0
            if sy < -120.0:
                wx = 0.05 + 0.25 * gust
                wz = 0.00
            elif sy < 140.0:
                wx = 0.65 + 0.55 * gust
                wz = 0.02
            else:
                wx = -0.55 + 0.45 * gust
                wz = 0.00
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                wx *= aim_assist_wind_reduction
                wz *= aim_assist_wind_reduction
            wind_lock_x = wx
            wind_lock_z = wz

            d2 = dx * dx + dy * dy + dz * dz
            if d2 > eps2:
                dist = math.sqrt(d2)
                T = dist / throw_speed
                if T < 10.0:
                    T = 10.0
                if T > 60.0:
                    T = 60.0

                ax = (wind_lock_x if wind_lock_per_throw else 0.0)
                ay = 0.0
                az = (wind_lock_z if wind_lock_per_throw else 0.0) - g

                dart_vel[0] = (dx - 0.5 * ax * T * T) / T
                dart_vel[1] = (dy - 0.5 * ay * T * T) / T
                dart_vel[2] = (dz - 0.5 * az * T * T) / T
            else:
                dart_vel[0] = 0.0
                dart_vel[1] = throw_speed
                dart_vel[2] = 0.0

            vx, vy, vz = dart_vel[0], dart_vel[1], dart_vel[2]
            h2 = vx * vx + vy * vy
            if h2 > eps2:
                dart_yaw = math.degrees(math.atan2(vy, vx))
                horiz = math.sqrt(h2)
                dart_pitch = -math.degrees(math.atan2(vz, horiz))
            else:
                dart_yaw = throw_yaw
                dart_pitch = throw_pitch


def setupCamera():
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    x, y, z = camera_pos
    gluLookAt(x, y, z,  # Camera position
              board_center[0], board_center[1], board_center[2],  # Look-at target (board center)
              0, 0, 1)  # Up vector (z-axis)

def idle():

    global dart_state, dart_pos, dart_vel, dart_yaw, dart_pitch
    global wind_phase
    global wind_lock_x, wind_lock_z
    global wind_gust_amp
    global aim_x, aim_z, aim_locked, aim_phase
    global aim_assist_mode
    global dart_resolved_this_throw
    global total_score, last_hit_label, last_hit_points, last_hit_accuracy
    global combo_streak, score_multiplier
    global heat, heat_max, heat_show
    global heat_hits_total, heat_sum_r, heat_sum_r2, heat_best_streak, heat_cur_streak, heat_last_text, heat_wedge_counts
    global game_mode
    global rush_time_left, rush_running, rush_over, rush_hits
    global rush_recording, rush_recording_active, rush_recording_finished
    global replay_active, replay_cursor, replay_speed
    global replay_buffer
    global best_rush_recording, best_rush_score, best_rush_hits
    global stuck_valid, stuck_pos, stuck_yaw, stuck_pitch
    global trick_target_idx, trick_hits
    global trick_recording, trick_recording_active, trick_recording_finished
    global trick_misses, trick_miss_limit, trick_over
    global obstacle_angle
    global board_center, board_center_base
    global call_active, call_announced, call_wedge_idx, call_zone, call_rounds, call_correct
    global call_recording, call_recording_active, call_recording_finished
    global board_spin_deg
    global level, level_hits, hits_per_level
    global boss_start_level, boss_active, boss_shield_on, boss_phase_t
    global boss_shield_on_time, boss_shield_off_time, boss_allowed_zones
    global trick_autoaim_token_available, trick_autoaim_active, trick_autoaim_time_left
    global trick_autoaim_snap_x, trick_autoaim_snap_z
    global call_spin_pause_active, call_spin_pause_time_left
    global call_house_snap_token_available, call_house_snap_active, call_house_snap_time_left
    global call_house_target_wedge_idx, call_house_target_zone
    global call_house_snap_x, call_house_snap_z
    global call_misses, call_miss_limit, call_over
    global dart_state, dart_resolved_this_throw
    global trick_misses, trick_over, trick_miss_limit
    global last_hit_label, last_hit_points, last_hit_accuracy, combo_streak, score_multiplier
    global call_target_wedge_idx, call_target_zone, call_hits  
    
    game_dt = 1.0 / 60.0

    # Mode-Specific Cheat Timers
    
    # Mode 2: Auto-aim timer - auto-miss if not thrown in time
    if game_mode == "trick" and trick_autoaim_active:
        trick_autoaim_time_left -= game_dt
        if trick_autoaim_time_left <= 0.0:
            trick_autoaim_time_left = 0.0
            trick_autoaim_active = False
            
            # Auto-miss if dart wasn't thrown
            if dart_state != 1:
                # Count as a miss
                if not trick_over:
                    trick_misses += 1
                    last_hit_label = "AUTO-AIM: TIME OUT (MISS)"
                    last_hit_points = 0
                    last_hit_accuracy = 0.0
                    combo_streak = 0
                    score_multiplier = 1
                    
                    if trick_misses >= trick_miss_limit:
                        trick_over = True
                        last_hit_label = "MODE 2 GAME OVER"
                        if trick_recording_active:
                            trick_recording_active = False
                            trick_recording_finished = True
    
    # Mode 3: Spin pause timer
    if game_mode == "call" and call_spin_pause_active:
        call_spin_pause_time_left -= game_dt
        if call_spin_pause_time_left <= 0.0:
            call_spin_pause_time_left = 0.0
            call_spin_pause_active = False
    
    # Mode 3: House Call Snap timer and tracking
    if game_mode == "call" and call_house_snap_active:
        call_house_snap_time_left -= game_dt
        if call_house_snap_time_left <= 0.0:
            call_house_snap_time_left = 0.0
            call_house_snap_active = False
            
            # Auto-miss if dart wasn't thrown
            if dart_state != 1:
                # Count as a miss
                if not call_over:
                    call_misses += 1
                    last_hit_label = "HOUSE CALL: TIME OUT (MISS)"
                    last_hit_points = 0
                    last_hit_accuracy = 0.0
                    combo_streak = 0
                    score_multiplier = 1
                    
                    if call_misses >= call_miss_limit:
                        call_over = True
                        last_hit_label = "MODE 3 GAME OVER"
                        if call_recording_active:
                            call_recording_active = False
                            call_recording_finished = True
        else:
            # Update snap point to track the spinning target
            snap_x, snap_z = _calculate_house_call_snap_point(call_house_target_wedge_idx, call_house_target_zone)
            call_house_snap_x = snap_x
            call_house_snap_z = snap_z

    # Replay playback (Rush): drive dart pose from recorded frames (no physics/scoring)
    if replay_active:
        if len(replay_buffer) < 2:
            replay_active = False
            glutPostRedisplay()
            return

        replay_cursor += replay_speed
        idx = int(replay_cursor)
        if idx >= len(replay_buffer) - 1:
            replay_active = False
            glutPostRedisplay()
            return

        frac = replay_cursor - float(idx)
        if frac < 0.0:
            frac = 0.0
        if frac > 1.0:
            frac = 1.0

        fr0 = replay_buffer[idx]
        fr1 = replay_buffer[idx + 1]

        dart_state = fr0[0]
        dart_pos[0] = fr0[1] * (1.0 - frac) + fr1[1] * frac
        dart_pos[1] = fr0[2] * (1.0 - frac) + fr1[2] * frac
        dart_pos[2] = fr0[3] * (1.0 - frac) + fr1[3] * frac
        dart_yaw = fr0[4] * (1.0 - frac) + fr1[4] * frac
        dart_pitch = fr0[5] * (1.0 - frac) + fr1[5] * frac

        stuck_valid = fr0[6]
        stuck_pos[0] = fr0[7] * (1.0 - frac) + fr1[7] * frac
        stuck_pos[1] = fr0[8] * (1.0 - frac) + fr1[8] * frac
        stuck_pos[2] = fr0[9] * (1.0 - frac) + fr1[9] * frac
        stuck_yaw = fr0[10] * (1.0 - frac) + fr1[10] * frac
        stuck_pitch = fr0[11] * (1.0 - frac) + fr1[11] * frac

        
        if len(fr0) >= 13 and len(fr1) >= 13:
            val = fr0[12] * (1.0 - frac) + fr1[12] * frac
            if game_mode == "trick":
                obstacle_angle = val
            elif game_mode == "call":
                board_spin_deg = val

        glutPostRedisplay()
        return

    # Fireworks particles update (only when not replaying)
    update_fireworks()

    wind_gust_amp = wind_gust_amp_base * (1.0 + 0.12 * (level - 1))
    if wind_gust_amp > 1.40:
        wind_gust_amp = 1.40
    if wind_gust_amp < 0.20:
        wind_gust_amp = 0.20


    boss_active = (level >= boss_start_level)
    if boss_active:
        boss_phase_t += game_dt
        if boss_shield_on:
            if boss_phase_t >= boss_shield_on_time:
                boss_phase_t = 0.0
                boss_shield_on = False
        else:
            if boss_phase_t >= boss_shield_off_time:
                boss_phase_t = 0.0
                boss_shield_on = True
    else:
        boss_shield_on = False
        boss_phase_t = 0.0
    # --- Mode-1 difficulty scaling based on level (clamped 1 to 5)
    idx = max(0, min(level, 5) - 1)

    rush_drain_mult = 1.0
    if game_mode == "rush":
        rush_drain_mult = rush_drain_mult_by_level[idx]

    if game_mode == "rush" and rush_running and (not rush_over):
        rush_time_left -= (game_dt * rush_drain_mult)
        if rush_time_left <= 0.0:
            rush_time_left = 0.0

            if level < MAX_LEVEL:
                level += 1
                rush_time_left = rush_time_total  # Reset timer to 60 seconds
                last_hit_label = f"LEVEL UP → {level}"

            else:
                # At max level, game over
                rush_over = True
                rush_running = False
                last_hit_label = "TIME UP"
                if rush_recording_active:
                    rush_recording_active = False
                    rush_recording_finished = True

                    if (total_score > best_rush_score) or (rush_hits > best_rush_hits):
                        best_rush_score = total_score
                        best_rush_hits = rush_hits
                        best_rush_recording = list(rush_recording)

    
    if game_mode == "trick":
        obstacle_angle += obstacle_speed
        while obstacle_angle >= 360.0:
            obstacle_angle -= 360.0
        while obstacle_angle < 0.0:
            obstacle_angle += 360.0

    board_center[0] = board_center_base[0]
    board_center[1] = board_center_base[1]
    board_center[2] = board_center_base[2]

    if game_mode == "call":
        # Mode 3 Cheat: Pause board spin when active
        if not call_spin_pause_active:
            board_spin_deg += board_spin_speed
            while board_spin_deg >= 360.0:
                board_spin_deg -= 360.0

    if dart_state == 0:
        dart_pos[0], dart_pos[1], dart_pos[2] = throw_start
        dart_vel[0], dart_vel[1], dart_vel[2] = 0.0, 0.0, 0.0

        tx = board_center[0] + aim_x
        ty = board_center[1]
        tz = board_center[2] + aim_z
        dx = tx - dart_pos[0]
        dy = ty - dart_pos[1]
        dz = tz - dart_pos[2]
        eps2 = 1e-12
        h2 = dx * dx + dy * dy
        if h2 > eps2:
            dart_yaw = math.degrees(math.atan2(dy, dx))
            horiz = math.sqrt(h2)
            dart_pitch = -math.degrees(math.atan2(dz, horiz))

    if dart_state != 1:
        if game_mode == "trick" and trick_autoaim_active:
            aim_x = trick_autoaim_snap_x
            aim_z = trick_autoaim_snap_z
            # Ensure aim stays locked during auto-aim
            aim_locked = True
        elif game_mode == "call" and call_house_snap_active:
            # Mode 3: Track the spinning target
            aim_x = call_house_snap_x
            aim_z = call_house_snap_z
            # Ensure aim stays locked during house call
            aim_locked = True
        elif not aim_locked and game_mode != "call":
            # --- Mode-1 scaling: faster + wider as level increases (Levels 1..5)
            idx = max(0, min(level, 5) - 1)

            local_phase_speed = aim_phase_speed
            local_amp_x = aim_amp_x
            local_amp_z = aim_amp_z

            if game_mode == "rush":
                local_phase_speed *= rush_aim_speed_mult_by_level[idx]
                amp_mult = rush_aim_amp_mult_by_level[idx]
                local_amp_x *= amp_mult
                local_amp_z *= amp_mult

            aim_phase += local_phase_speed

            aim_x = local_amp_x * math.sin(aim_phase * 1.00)
            aim_z = local_amp_z * math.sin(aim_phase * 1.37 + 1.1)

            # Clamp 
            d2 = aim_x * aim_x + aim_z * aim_z
            lim2 = aim_limit * aim_limit
            if d2 > lim2:
                inv = aim_limit / math.sqrt(d2)
                aim_x *= inv
                aim_z *= inv

    if dart_state == 1:
        px, py, pz = dart_pos[0], dart_pos[1], dart_pos[2]
        if wind_lock_per_throw:
            wx = wind_lock_x
            wz = wind_lock_z
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                wx *= aim_assist_wind_reduction
                wz *= aim_assist_wind_reduction
        else:
            wind_phase += wind_gust_speed
            gust = wind_gust_amp * math.sin(wind_phase)
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                gust *= aim_assist_wind_reduction

            wx = 0.0
            wz = 0.0
            if py < -120.0:
                wx = 0.05 + 0.25 * gust
                wz = 0.00
            elif py < 140.0:
                wx = 0.65 + 0.55 * gust
                wz = 0.02
            else:
                wx = -0.55 + 0.45 * gust
                wz = 0.00
            if aim_assist_mode == 2 or aim_assist_mode == 3:
                wx *= aim_assist_wind_reduction
                wz *= aim_assist_wind_reduction

        dart_vel[0] += wx * dt_fixed
        dart_vel[2] += wz * dt_fixed

        eps2 = 1e-12

        # Gravity
        dart_vel[2] -= g * dt_fixed

        # Integrate
        nx = px + dart_vel[0] * dt_fixed
        ny = py + dart_vel[1] * dt_fixed
        nz = pz + dart_vel[2] * dt_fixed

        by = board_center[1]
        if py < by and ny >= by:
            denom = (ny - py)
            if denom != 0.0:
                t = (by - py) / denom
            else:
                t = 0.0
            hit_x = px + (nx - px) * t
            hit_z = pz + (nz - pz) * t
            dx = hit_x - board_center[0]
            dz = hit_z - board_center[2]
            d2_hit = (dx * dx + dz * dz)
            if d2_hit <= (board_radius * board_radius):
                # Score once per throw
                if not dart_resolved_this_throw:
                    dart_resolved_this_throw = True

                    # Radius and accuracy
                    r = math.sqrt(d2_hit)
                    acc = 100.0 * (1.0 - (r / board_radius))
                    if acc < 0.0:
                        acc = 0.0
                    if acc > 100.0:
                        acc = 100.0
                    last_hit_accuracy = acc

                    # -------- Fireworks poppers on high accuracy (>= 85%) in ANY mode --------
                    global firework_cooldown_frames
                    if acc >= 85.0 and firework_cooldown_frames <= 0:
                        strength = (acc - 85.0) / 15.0  # 85..100 -> 0..1
                        if strength < 0.0:
                            strength = 0.0
                        if strength > 1.0:
                            strength = 1.0

                        # Spawn slightly off the board plane so it "pops" outward visibly
                        spawn_fireworks(hit_x, by - 6.0, hit_z, strength=strength)
                        firework_cooldown_frames = firework_cooldown_max

                    ang_from_top = _angle_from_top_clockwise_deg(dx, dz)
                    # Shift by half a wedge so 0° (top) is the CENTER of wedge 0 (matches drawn wedges/numbers)
                    ang_from_top = _spin_adjust_angle_from_top(ang_from_top)
                    ang_from_top += 9.0
                    while ang_from_top >= 360.0:
                        ang_from_top -= 360.0
                    wedge_idx = _wedge_index_from_angle(ang_from_top)
                    if wedge_idx < 0:
                        wedge_idx = 0
                    if wedge_idx > 19:
                        wedge_idx = 19

                    base = wedge_numbers[wedge_idx]

                    R = board_radius
                    r_double_in = R * 0.88
                    r_triple_out = R * 0.56
                    r_triple_in = R * 0.48
                    r_bull_out = R * 0.14
                    r_bull_in = R * 0.06

                    # Zone + points
                    zone = "S"
                    pts = base
                    if r <= r_bull_in:
                        zone = "DBULL"
                        pts = 50
                    elif r <= r_bull_out:
                        zone = "SBULL"
                        pts = 25
                    elif r_triple_in <= r <= r_triple_out:
                        zone = "T"
                        pts = base * 3
                    elif r_double_in <= r <= R:
                        zone = "D"
                        pts = base * 2
                    else:
                        zone = "S"
                        pts = base

                    blocked = (game_mode == "trick" and _is_blocked_by_obstacle(dx, dz))

                    # Apply mode rules
                    award = True
                    if blocked:
                        award = False
                        # Penalty for hitting the obstacle in Trickshot mode
                        penalty = 5
                        total_score -= penalty
                        if total_score < 0:
                            total_score = 0
                        last_hit_label = f"BLOCKED (-{penalty})"
                        last_hit_points = -penalty
                        last_hit_accuracy = acc
                        combo_streak = 0
                        score_multiplier = 1
                        if game_mode == "trick" and (not trick_over):
                            trick_misses += 1
                            if trick_misses >= trick_miss_limit:
                                trick_over = True
                                last_hit_label = "MODE 2 GAME OVER"
                                if trick_recording_active:
                                    trick_recording_active = False
                                    trick_recording_finished = True
                    elif game_mode == "trick":
                        # Must hit a specific wedge number (bull counts as wrong here)
                        if zone == "SBULL" or zone == "DBULL":
                            award = False
                        elif wedge_idx != trick_target_idx:
                            award = False

                        if not award:
                            last_hit_label = f"WRONG (target {wedge_numbers[trick_target_idx]})"
                            last_hit_points = 0
                            combo_streak = 0
                            score_multiplier = 1
                            if not trick_over:
                                trick_misses += 1
                                if trick_misses >= trick_miss_limit:
                                    trick_over = True
                                    last_hit_label = "MODE 2 GAME OVER"
                                    if trick_recording_active:
                                        trick_recording_active = False
                                        trick_recording_finished = True
                        else:
                            trick_hits += 1
                            trick_target_idx = random.randint(0, 19)
                            # Reset auto-aim token when hitting a new target (new "round")
                            trick_autoaim_token_available = True
                            trick_autoaim_active = False
                            trick_autoaim_time_left = 0.0
                            trick_autoaim_snap_x = 0.0
                            trick_autoaim_snap_z = 0.0
                    elif game_mode == "rush":
                        if not rush_over:
                            rush_hits += 1
                    elif game_mode == "call":
                        # Check if house call target was hit (if house call is active)
                        if call_house_snap_active:
                            hit_match = False
                            if call_house_target_zone == "DBULL" or call_house_target_zone == "SBULL":
                                hit_match = (zone == call_house_target_zone)
                            else:
                                hit_match = (zone == call_house_target_zone and wedge_idx == call_house_target_wedge_idx)
                            
                            if not hit_match:
                                award = False
                                last_hit_label = f"HOUSE CALL: WRONG (wanted {call_house_target_zone}{wedge_numbers[call_house_target_wedge_idx] if call_house_target_zone != 'DBULL' and call_house_target_zone != 'SBULL' else ''})"
                                last_hit_points = 0
                                combo_streak = 0
                                score_multiplier = 1
                                if not call_over:
                                    call_misses += 1
                                    if call_misses >= call_miss_limit:
                                        call_over = True
                                        last_hit_label = "MODE 3 GAME OVER"
                                        if call_recording_active:
                                            call_recording_active = False
                                            call_recording_finished = True
                            else:
                                call_house_snap_token_available = True
                                call_house_snap_active = False
                                call_house_snap_time_left = 0.0
                                if zone == "DBULL":
                                    hit_text = "BULL (50)"
                                elif zone == "SBULL":
                                    hit_text = "OUTER BULL (25)"
                                else:
                                    hit_text = f"{zone}{base}"
                                last_hit_label = f"HOUSE CALL: HIT! {hit_text}"
                        else:
                            # Persistent target mode: must hit the persistent target
                            hit_match = False
                            if call_target_zone == "DBULL" or call_target_zone == "SBULL":
                                hit_match = (zone == call_target_zone)
                            else:
                                hit_match = (zone == call_target_zone and wedge_idx == call_target_wedge_idx)
                            
                            if not hit_match:
                                award = False
                                target_text = ""
                                if call_target_zone == "DBULL":
                                    target_text = "BULL (50)"
                                elif call_target_zone == "SBULL":
                                    target_text = "OUTER BULL (25)"
                                else:
                                    target_text = f"{call_target_zone}{wedge_numbers[call_target_wedge_idx]}"
                                last_hit_label = f"WRONG (target {target_text})"
                                last_hit_points = 0
                                combo_streak = 0
                                score_multiplier = 1
                                if not call_over:
                                    call_misses += 1
                                    if call_misses >= call_miss_limit:
                                        call_over = True
                                        last_hit_label = "MODE 3 GAME OVER"
                                        if call_recording_active:
                                            call_recording_active = False
                                            call_recording_finished = True
                            else:
                                # Correct hit! Generate new target
                                call_hits += 1
                                call_target_wedge_idx = random.randint(0, 19)
                                zone_roll = random.random()
                                if zone_roll < 0.15:  # 15% bullseye
                                    if random.random() < 0.5:
                                        call_target_zone = "DBULL"
                                    else:
                                        call_target_zone = "SBULL"
                                elif zone_roll < 0.40:  # 25% triple
                                    call_target_zone = "T"
                                elif zone_roll < 0.70:  # 30% double
                                    call_target_zone = "D"
                                else:  # 30% single
                                    call_target_zone = "S"
                                call_house_snap_token_available = True
                        
                        pass

                    if award and boss_active and boss_shield_on:
                        if zone not in boss_allowed_zones:
                            award = False
                            last_hit_label = "SHIELDED (only TRIPLE & BULL)"
                            last_hit_points = 0
                            combo_streak = 0
                            score_multiplier = 1

                    heat_hits_total += 1
                    heat_sum_r += r
                    heat_sum_r2 += (r * r)
                    heat_wedge_counts[wedge_idx] += 1

                    cell = (2.0 * board_radius) / float(HEAT_N)
                    ii = int((dx + board_radius) / cell)
                    jj = int((dz + board_radius) / cell)
                    if ii < 0: ii = 0
                    if ii >= HEAT_N: ii = HEAT_N - 1
                    if jj < 0: jj = 0
                    if jj >= HEAT_N: jj = HEAT_N - 1

                    di = -1
                    while di <= 1:
                        dj = -1
                        while dj <= 1:
                            ai = ii + di
                            aj = jj + dj
                            if (ai >= 0) and (ai < HEAT_N) and (aj >= 0) and (aj < HEAT_N):
                                add = 3 if (di == 0 and dj == 0) else 1
                                heat[ai][aj] += add
                                if heat[ai][aj] > heat_max:
                                    heat_max = heat[ai][aj]
                            dj += 1
                        di += 1

                    if award:
                        # High-accuracy streak (>= 85%) — non-scoring hits reset elsewhere
                        if acc >= 85.0:
                            heat_cur_streak += 1
                            if heat_cur_streak > heat_best_streak:
                                heat_best_streak = heat_cur_streak
                        else:
                            heat_cur_streak = 0

                        heat_last_text = f"SCORE acc={acc:.1f}% wedge={base}"

                        # Combo system: (Tracking only, multiplier disabled)
                        if acc >= combo_accuracy_threshold:
                            combo_streak += 1
                        else:
                            combo_streak = 0
                        score_multiplier = 1  

                        gained = int(pts * score_multiplier)
                        total_score += gained
                        last_hit_points = gained

                        if zone == "SBULL":
                            last_hit_label = "Outer Bull (25)"
                        elif zone == "DBULL":
                            last_hit_label = "Bullseye (50)"
                        else:
                            last_hit_label = f"{zone}{base} (+{gained})"

                        if game_mode == "call" and call_announced:
                            call_rounds += 1
                            hit_match = False
                            if call_zone == "DBULL" or call_zone == "SBULL":
                                hit_match = (zone == call_zone)
                            else:
                                hit_match = (zone == call_zone and wedge_idx == call_wedge_idx)

                            if hit_match:
                                call_correct += 1
                                total_score += call_bonus
                                last_hit_points += call_bonus
                                last_hit_label = f"CALLED! +{call_bonus} ({zone}{base})"
                            else:
                                last_hit_label = f"MISS CALL (wanted {call_zone}{wedge_numbers[call_wedge_idx]})"

                            call_announced = False

                    else:
                        heat_cur_streak = 0
                        heat_last_text = f"HIT (No Score) acc={acc:.1f}%"

                stuck_valid = True
                stuck_pos[0] = hit_x
                stuck_pos[1] = by - stick_depth
                stuck_pos[2] = hit_z
                stuck_yaw = dart_yaw
                stuck_pitch = dart_pitch
                dart_state = 0
                dart_vel[0], dart_vel[1], dart_vel[2] = 0.0, 0.0, 0.0
                dart_pos[0], dart_pos[1], dart_pos[2] = throw_start
            else:
                if not dart_resolved_this_throw:
                    dart_resolved_this_throw = True
                    last_hit_label = "MISS"
                    last_hit_points = 0
                    last_hit_accuracy = 0.0
                    combo_streak = 0
                    score_multiplier = 1
                    heat_last_text = "MISS"
                    heat_cur_streak = 0
                    if game_mode == "rush":
                        pass
                    if game_mode == "trick":
                        if not trick_over:
                            trick_misses += 1
                            if trick_misses >= trick_miss_limit:
                                trick_over = True
                                last_hit_label = "MODE 2 GAME OVER"
                                if trick_recording_active:
                                    trick_recording_active = False
                                    trick_recording_finished = True
                    if game_mode == "call":
                        if call_announced:
                            call_rounds += 1
                            call_announced = False
                        # Miss counts as a miss
                        if not call_over:
                            call_misses += 1
                            if call_misses >= call_miss_limit:
                                call_over = True
                                last_hit_label = "MODE 3 GAME OVER"
                                if call_recording_active:
                                    call_recording_active = False
                                    call_recording_finished = True
                dart_pos[0], dart_pos[1], dart_pos[2] = nx, ny, nz
        else:
            dart_pos[0], dart_pos[1], dart_pos[2] = nx, ny, nz
        vx, vy, vz = dart_vel[0], dart_vel[1], dart_vel[2]
        h2 = vx * vx + vy * vy
        if h2 > eps2:
            dart_yaw = math.degrees(math.atan2(vy, vx))
            horiz = math.sqrt(h2)
            dart_pitch = -math.degrees(math.atan2(vz, horiz))

        if abs(dart_pos[0]) > world_margin or abs(dart_pos[1]) > world_margin or dart_pos[2] < -80.0:
            dart_state = 0
            dart_vel[0], dart_vel[1], dart_vel[2] = 0.0, 0.0, 0.0
            dart_pos[0], dart_pos[1], dart_pos[2] = throw_start

    # Frame recording (Rush / Trickshot)
    if (not replay_active) and (game_mode == "rush") and rush_recording_active:
        rush_recording.append((
            dart_state,
            dart_pos[0], dart_pos[1], dart_pos[2],
            dart_yaw, dart_pitch,
            stuck_valid,
            stuck_pos[0], stuck_pos[1], stuck_pos[2],
            stuck_yaw, stuck_pitch
        ))
    if (not replay_active) and (game_mode == "trick") and trick_recording_active:
        trick_recording.append((
            dart_state,
            dart_pos[0], dart_pos[1], dart_pos[2],
            dart_yaw, dart_pitch,
            stuck_valid,
            stuck_pos[0], stuck_pos[1], stuck_pos[2],
            stuck_yaw, stuck_pitch,
            obstacle_angle
        ))
    # Mode 3 replay: records entire session (includes board_spin_deg)
    if (not replay_active) and (game_mode == "call") and call_recording_active:
        call_recording.append((
            dart_state,
            dart_pos[0], dart_pos[1], dart_pos[2],
            dart_yaw, dart_pitch,
            stuck_valid,
            stuck_pos[0], stuck_pos[1], stuck_pos[2],
            stuck_yaw, stuck_pitch,
            board_spin_deg
        ))
    glutPostRedisplay()

def showScreen():
    global game_mode, rush_over, trick_over, call_rounds, call_correct, call_bonus
    global rewind_available, heat_show, level, level_hits, hits_per_level
    global boss_active, boss_shield_on
    global aim_assist_mode
    global trick_autoaim_token_available, trick_autoaim_active, trick_autoaim_time_left
    global call_spin_pause_active, call_spin_pause_time_left
    global trick_target_idx, trick_hits, trick_misses, trick_miss_limit
    global rush_time_left, rush_hits
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size
    glDisable(GL_DEPTH_TEST)
    # Replay camera (Rush): FIXED broadcast cams around the BOARD (east/west feel)
   
    if replay_active and len(replay_buffer) > 2:
        i = int(replay_cursor)
        if i < 0:
            i = 0
        if i >= len(replay_buffer) - 1:
            i = len(replay_buffer) - 2

        N = float(len(replay_buffer) - 1)
        if N < 1.0:
            N = 1.0
        t = float(i) / N  
        camA_deg = -45.0   
        camB_deg = -135.0  

        # User override: W = west cam, E = east cam; else auto cut at midpoint
        if replay_view_side < 0:
            side_deg = camB_deg
        elif replay_view_side > 0:
            side_deg = camA_deg
        else:
            side_deg = camA_deg if t < 0.5 else camB_deg
            if replay_cut_blend > 0.0:
                w = replay_cut_blend
                if t >= (0.5 - w) and t <= (0.5 + w) and (2.0 * w) > 1e-9:
                    alpha = (t - (0.5 - w)) / (2.0 * w)  # 0..1
                    if alpha < 0.0:
                        alpha = 0.0
                    if alpha > 1.0:
                        alpha = 1.0
                    side_deg = camA_deg * (1.0 - alpha) + camB_deg * alpha

        ang = math.radians(side_deg)

        bx, by, bz = board_center[0], board_center[1], board_center[2]
        camx = bx + replay_orbit_radius * math.cos(ang)
        camy = by + replay_orbit_radius * math.sin(ang)
        camz = bz + replay_height

        # Direction from dart to board
        dx = bx - dart_pos[0]
        dy = by - dart_pos[1]
        dz = bz - dart_pos[2]
        dm = math.sqrt(dx * dx + dy * dy + dz * dz)
        if dm < 1e-9:
            dx, dy, dz = 0.0, 1.0, 0.0
            dm = 1.0
        dx, dy, dz = dx / dm, dy / dm, dz / dm

        # Keep replay stable: always look at the board center (reduces perceived motion)
        tgtx, tgty, tgtz = bx, by, bz

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(fovY, 1.25, 0.1, 1500)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(camx, camy, camz, tgtx, tgty, tgtz, 0, 0, 1)
    else:
        setupCamera() 

    draw_board_stand()
    draw_dartboard()
    # Trajectory prediction (Aim Assist)
    if (aim_assist_mode == 1 or aim_assist_mode == 3) and (not replay_active):
        draw_trajectory_prediction()

    # Dart (drawn with cylinder + cone)

    # Draw last stuck dart (if any)
    if stuck_valid:
        glPushMatrix()
        glTranslatef(stuck_pos[0], stuck_pos[1], stuck_pos[2])
        glRotatef(-90.0, 1, 0, 0)
        glRotatef(stuck_yaw, 0, 0, 1)
        glRotatef(stuck_pitch, 1, 0, 0)
        glColor3f(0.75, 0.75, 0.75)
        gluCylinder(gluNewQuadric(), 4.0, 3.0, 58.0, 10, 10)
        glTranslatef(0, 0, 58.0)
        glColor3f(0.95, 0.55, 0.10)
        gluCylinder(gluNewQuadric(), 3.2, 0.1, 14.0, 10, 10)
        glTranslatef(0, 0, -72.0)
        glColor3f(0.20, 0.80, 1.00)
        glutSolidCube(10)
        glPopMatrix()

    # Draw the active dart (in-hand when not flying, in-flight when flying)
    glPushMatrix()
    glTranslatef(dart_pos[0], dart_pos[1], dart_pos[2])
    glRotatef(-90.0, 1, 0, 0)        
    glRotatef(dart_yaw, 0, 0, 1)     
    glRotatef(dart_pitch, 1, 0, 0)     
    glColor3f(0.85, 0.85, 0.85)
    gluCylinder(gluNewQuadric(), 4.0, 3.0, 58.0, 10, 10)

    # Tip (cone)
    glTranslatef(0, 0, 58.0)
    glColor3f(0.95, 0.55, 0.10)
    gluCylinder(gluNewQuadric(), 3.2, 0.1, 14.0, 10, 10)

    # Tail (small fins via cube)
    glTranslatef(0, 0, -72.0)
    glColor3f(0.20, 0.80, 1.00)
    glutSolidCube(10)
    glPopMatrix()

    # Fireworks poppers (3D).
    if not replay_active:
        draw_fireworks()

    if not replay_active:
        # Enable depth test only for HUD to separate text from background
        glEnable(GL_DEPTH_TEST)
        glDepthMask(GL_TRUE)  # Enable depth writing for HUD

    gold = (1.0, 0.84, 0.20)
    white = (1.0, 1.0, 1.0)
    cyan = (0.4, 0.8, 1.0)
    orange = (1.0, 0.65, 0.2)
    purple = (0.8, 0.6, 1.0)
    green = (0.4, 1.0, 0.6)
    red = (1.0, 0.4, 0.4)

    draw_text(10, 780, f"Score: {total_score}", color=gold)
    draw_text(10, 750, f"Level: {level}/5 (Time-based)", color=gold)
    draw_text(650, 780, f"Last Hit: {last_hit_label}", color=white)
    draw_text(650, 750, f"Points: +{last_hit_points}", color=gold)
    draw_text(850, 780, f"🎯 ACCURACY: {last_hit_accuracy:.1f}%", color=gold)

    if game_mode == "rush":
        draw_text(10, 650, f"Mode 1: Timed Rush (Press 1)", color=gold)
        draw_text(10, 620, f"Time Left: {rush_time_left:0.1f}s", color=white)
        draw_text(10, 590, f"Hits: {rush_hits}", color=white)
        draw_text(10, 560, f"Score: {total_score}", color=gold)
        draw_text(10, 530, f"Level: {level}", color=gold)
        draw_text(10, 500, f"Accuracy: {last_hit_accuracy:.1f}%", color=gold)

        if rush_over:
            draw_text(300, 550, f"🏆 TIME UP! Level {level} Complete!", color=gold)
            draw_text(300, 520, f"Press R to reset or 2/3 to switch modes", color=white)

    elif game_mode == "trick":
        draw_text(10, 650, f"Mode 2: Trickshot (Press 2)", color=gold)
        draw_text(10, 620, f"Target: {wedge_numbers[trick_target_idx]}", color=white)
        draw_text(10, 590, f"Hits: {trick_hits} | Misses: {trick_misses}/{trick_miss_limit}", color=white)
        draw_text(10, 560, f"Score: {total_score} | Accuracy: {last_hit_accuracy:.1f}%", color=gold)

        if trick_autoaim_active:
            autoaim_color = cyan if trick_autoaim_time_left > 0.5 else orange
            draw_text(10, 530, f"🎯 AUTO-AIM: {trick_autoaim_time_left:.1f}s", color=autoaim_color)
        elif trick_autoaim_token_available:
            draw_text(10, 530, f"F = Auto-Aim Snap (READY)", color=green)
        else:
            draw_text(10, 530, f"F = Auto-Aim Snap (USED)", color=white)

        if trick_over:
            draw_text(10, 500, f"💀 GAME OVER! Missed target {trick_miss_limit} times", color=gold)
            draw_text(10, 470, f"Press R to reset", color=white)
        else:
            draw_text(10, 500, f"⚠️  Rotating blocker active", color=white)
            draw_text(10, 470, f"Hit target wedge only!", color=white)

    elif game_mode == "call":
        x = 10
        y = 650
        dy = 34   

        def put(txt, color=white):
            nonlocal y
            draw_text(x, y, txt, color=color)
            y -= dy

        
        put("Mode 3: Call Your Shot (Press 3)", gold)

        if call_target_zone == "DBULL":
            target_text = "BULL (50)"
        elif call_target_zone == "SBULL":
            target_text = "OUTER BULL (25)"
        else:
            target_text = f"{call_target_zone}{wedge_numbers[call_target_wedge_idx]}"

        put(f"Target: {target_text}", cyan)
        put(f"Hits: {call_hits} | Misses: {call_misses}/{call_miss_limit}", white)
        put(f"Score: {total_score} | Accuracy: {last_hit_accuracy:.1f}%", gold)

        if not call_over:
            put("A/D/S/X = Move | Right-Click = Call ", white)
        else:
            put("Press R to reset", white)

        if call_over:
            put(f"💀 GAME OVER! Missed {call_miss_limit} times", gold)
        else:
            if call_house_snap_active:
                if call_house_target_zone == "DBULL":
                    ttxt = "BULL (50)"
                elif call_house_target_zone == "SBULL":
                    ttxt = "OUTER BULL (25)"
                else:
                    ttxt = f"{call_house_target_zone}{wedge_numbers[call_house_target_wedge_idx]}"
                house_color = cyan if call_house_snap_time_left > 0.5 else orange
                put(f"🏠 HOUSE CALL: {ttxt} ({call_house_snap_time_left:.1f}s)", house_color)

            elif call_spin_pause_active:
                put(f"⏸️ SPIN PAUSE: {call_spin_pause_time_left:.1f}s", cyan)

            else:
                if call_house_snap_token_available:
                    put("F = House Call Snap (READY)", green)
                else:
                    put("F = House Call Snap (USED)", white)

        if call_rounds > 0:
            pct = (100.0 * call_correct) / call_rounds
            put(f"Call Accuracy: {call_correct}/{call_rounds} ({pct:.0f}%)", white)
        
        else:
            put("No shots called yet", white)

    draw_text(10, 340, f"Controls: Z = Rewind ({'READY' if rewind_available else 'USED'})", color=white)
    
    if game_mode != "call":
        draw_text(10, 420, f"H = Toggle Heatmap | L = Lock Crosshair", color=white)
        draw_text(10, 400, f"R = Reset Game | 1/2/3 = Switch Modes", color=white)
    else:
        draw_text(10, 420, f"H = Toggle Heatmap", color=white)
        draw_text(10, 400, f"1/2/3 = Switch Modes", color=white)

    # Aim Assist status
    if aim_assist_mode == 0:
        assist_text = "C = Aim Assist: OFF"
        assist_color = white
    elif aim_assist_mode == 1:
        assist_text = "C = Aim Assist: TRAJECTORY"
        assist_color = cyan
    elif aim_assist_mode == 2:
        assist_text = "C = Aim Assist: WIND REDUCE"
        assist_color = green
    else:
        assist_text = "C = Aim Assist: BOTH"
        assist_color = purple
    draw_text(10, 370, assist_text, color=assist_color)
    
    # Mode 2 cheat control
    if boss_active and not heat_show:
        draw_text(650, 720, f"Boss Shield: {'🛡️ ON' if boss_shield_on else '✅ OFF'}", color=gold if boss_shield_on else white)

    if heat_show:
        draw_text(650, 690, f"🔥 Heatmap Active - Shows hit distribution", color=gold)

    if not replay_active:
        glDisable(GL_DEPTH_TEST)

    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically
    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()