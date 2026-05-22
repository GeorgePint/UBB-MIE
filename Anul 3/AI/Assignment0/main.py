from vpython import *
import numpy as np
import random
import math

# --- Configuration & Global Variables ---
CUBE_SIZE = 10.0
GRID_N = 4  # The cube is split into N*N*N subcubes
MAX_PARTICLES = 500
PARTICLE_RADIUS = 0.15
V_MAX = 5.0
target_particle_count = 100

particles = []
subcube_boxes = []

# --- Scene Setup ---
scene = canvas(title="<b>Entropy Particle Simulation</b>", width=800, height=600, center=vector(0, 0, 0))
scene.camera.pos = vector(0, 0, CUBE_SIZE * 1.5)

# Draw the main bounding box (wireframe)
d = CUBE_SIZE / 2
box(pos=vector(0, 0, 0), size=vector(CUBE_SIZE, CUBE_SIZE, CUBE_SIZE), color=color.white, opacity=0.1, shininess=0)

# --- Subcube Grid Setup ---
# We create semi-transparent boxes to represent the n*n*n grid and depict entropy via color
sub_size = CUBE_SIZE / GRID_N
start_pos = -CUBE_SIZE / 2 + sub_size / 2

for x in range(GRID_N):
    for y in range(GRID_N):
        for z in range(GRID_N):
            pos = vector(start_pos + x * sub_size, start_pos + y * sub_size, start_pos + z * sub_size)
            # Create a box for visual color mapping
            sc_box = box(pos=pos, size=vector(sub_size, sub_size, sub_size),
                         color=color.blue, opacity=0.05, visible=True)
            subcube_boxes.append({'box': sc_box, 'pos': pos, 'particles': []})

# --- UI Controls ---
scene.append_to_caption('\n\n')


def update_particle_count(s):
    global target_particle_count
    target_particle_count = int(s.value)
    count_label.text = f'Number of Particles: {target_particle_count}  '

def update_speed(s):
    speed_label.text = f'Temperature (Speed Multiplier): {s.value:1.2f}'
    # Scale current velocities by the change in the slider
    # (In a rigorous simulation, you'd scale based on the kinetic energy/temperature relationship)


sl_particles = slider(min=10, max=MAX_PARTICLES, value=100, length=200, bind=update_particle_count)
count_label = wtext(text=f'Number of Particles: {int(sl_particles.value)}  ')
scene.append_to_caption('    ')
sl_speed = slider(min=0.1, max=3.0, value=1.0, length=200, bind=update_speed)
speed_label = wtext(text=f'Temperature (Speed Multiplier): {sl_speed.value:1.2f}\n')

# Initialize starting particles
update_particle_count(sl_particles)


# --- Physics & Math Functions ---

def check_wall_collisions():
    for p in particles:
        if abs(p.pos.x) > d - PARTICLE_RADIUS:
            p.v.x = -p.v.x * 0.95  # Slight dampening
            p.pos.x = np.sign(p.pos.x) * (d - PARTICLE_RADIUS)
        if abs(p.pos.y) > d - PARTICLE_RADIUS:
            p.v.y = -p.v.y * 0.95
            p.pos.y = np.sign(p.pos.y) * (d - PARTICLE_RADIUS)
        if abs(p.pos.z) > d - PARTICLE_RADIUS:
            p.v.z = -p.v.z * 0.95
            p.pos.z = np.sign(p.pos.z) * (d - PARTICLE_RADIUS)


def check_particle_collisions():
    # Basic O(N^2) collision check
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            dist = mag(p1.pos - p2.pos)
            if dist < 2 * PARTICLE_RADIUS:
                # Simple elastic collision (exchange velocities along normal)
                normal = norm(p1.pos - p2.pos)
                relative_velocity = p1.v - p2.v
                speed_along_normal = dot(relative_velocity, normal)
                if speed_along_normal < 0:
                    # They are moving towards each other, calculate bounce
                    impulse = normal * speed_along_normal
                    p1.v = p1.v - impulse
                    p2.v = p2.v + impulse


def compute_entropy_and_colors():
    # 1. Clear previous subcube particle lists
    for sc in subcube_boxes:
        sc['particles'] = []

    # 2. Assign particles to subcubes
    for p in particles:
        # Map position to 3D grid index
        idx_x = int(min(max((p.pos.x + d) / sub_size, 0), GRID_N - 1))
        idx_y = int(min(max((p.pos.y + d) / sub_size, 0), GRID_N - 1))
        idx_z = int(min(max((p.pos.z + d) / sub_size, 0), GRID_N - 1))

        flat_idx = idx_x * (GRID_N ** 2) + idx_y * GRID_N + idx_z
        subcube_boxes[flat_idx]['particles'].append(p)

    # 3. Calculate Shannon Entropy for each subcube based on velocity direction
    for sc in subcube_boxes:
        ps = sc['particles']
        N = len(ps)
        if N < 2:
            sc['box'].opacity = 0.0  # Invisible if empty
            continue

        # Group velocities into 8 octants to find probabilities (p_i)
        octants = [0] * 8
        for p in ps:
            x_sign = 1 if p.v.x > 0 else 0
            y_sign = 1 if p.v.y > 0 else 0
            z_sign = 1 if p.v.z > 0 else 0
            octant_idx = (x_sign << 2) | (y_sign << 1) | z_sign
            octants[octant_idx] += 1

        # Calculate H = - sum(p * log2(p))
        entropy = 0
        for count in octants:
            if count > 0:
                p_i = count / N
                entropy -= p_i * math.log2(p_i)

        # Max entropy for 8 bins is log2(8) = 3.0
        normalized_entropy = min(max(entropy / 3.0, 0), 1.0)

        # Color mapping: Low Entropy = Blue, High Entropy = Red
        # Hsv mapping: H=0.66 (Blue) to H=0.0 (Red)
        sc['box'].color = color.hsv_to_rgb(vector(0.66 * (1.0 - normalized_entropy), 1, 1))
        sc['box'].opacity = 0.4  # Make visible to show entropy state


# --- Main Simulation Loop ---
dt = 0.01
while True:
    rate(100)  # Maximum 100 frames per second

    # 1. Safely add/remove particles ONLY here, between physics steps
    while len(particles) < target_particle_count:
        p = sphere(
            pos=vector(random.uniform(-d + 1, d - 1), random.uniform(-d + 1, d - 1), random.uniform(-d + 1, d - 1)),
            radius=PARTICLE_RADIUS, color=color.red)
        p.v = vector(random.uniform(-V_MAX, V_MAX), random.uniform(-V_MAX, V_MAX), random.uniform(-V_MAX, V_MAX))
        particles.append(p)

    while len(particles) > target_particle_count:
        p = particles.pop()
        p.visible = False  # Hide the sphere from the renderer

    # 2. Update positions
    speed_mult = sl_speed.value
    for p in particles:
        p.pos = p.pos + p.v * speed_mult * dt

    # 3. Handle Physics
    check_wall_collisions()
    check_particle_collisions()

    # 4. Calculate and render entropy
    compute_entropy_and_colors()

