import pygame
import random
import sys

from Particle import Particle
from Environment import Environment
from utils import random_color, vector2, colors, get_env_pos, get_real_pos

# --------- Params of the simulation ---------
width, height = size = 800, 600
middle_size = width/2, height/2
fps = 60

# grid size
env_w = 2
env_h = 4

select = None
mouse_force = 800
preventMouse = [vector2(0, 0)] * 5

mag = 1
mag_vec = vector2(0, 0)

delay = 15 # frames
add = True
add_frame = 0

min_particles = 8
max_particles = 15

# --------- environments --------- 
env_size = env_width, env_height = int(width/env_w), int(height/env_h)
gravity_pro = 0.2

envs = []
for w in range(env_w):
    for h in  range(env_h):
        num = random.randint(min_particles, max_particles)
        env = Environment(env_size, num)
        if gravity_pro > random.random():
            env.gravity = vector2(0, 5)
        
        offset = vector2(env_width*w, env_height*h)
        envs.append([env, offset])
        
# --------- functions ---------

def zoom(amplituded):
    global mag, mag_vec
    mag *= amplituded
    mag_vec = (1 - mag)*vector2(*middle_size)

def get_mouse_pos():
    return pygame.Vector2(pygame.mouse.get_pos())

def environment_clicked():
    for env, offset in envs:
        mouse_pos = get_env_pos(get_mouse_pos(), offset, mag, mag_vec)
        top    = 0
        bottom = env.height
        left   = 0
        right  = env.width
        if top <= mouse_pos.y <= bottom and left <= mouse_pos.x <= right:
            return env, offset
    return None

def text(window, font, string, pos, color):
    text_rect = font.render(string, True, color)
    window.blit(text_rect, pos)
    
# --------- Main Loop ---------

pygame.font.init()
window = pygame.display.set_mode(size)

pygame.display.set_caption('Pygame inicio')
font = pygame.font.SysFont("Cambria", 20)
clock = pygame.time.Clock()

frame_count = 0

while True:
    frame_count += 1
    delta = clock.tick(fps)/1000
    # ----- Events -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                env_select = environment_clicked()
                if env_select != None:
                    env_mouse = get_env_pos(get_mouse_pos(), env_select[1], mag, mag_vec)
                    select = env_select[0].click_particle(env_mouse)
                    if select != None:
                        select.enabled = False
                        select.vel *= 0
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if select != None:
                force = get_mouse_pos() - preventMouse[0]
                select.apply_force(force*mouse_force/mag)
                select.enabled = True
                select = None
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_z:
                zoom(1.2)
            elif event.key == pygame.K_x:
                zoom(0.8)
            elif event.key == pygame.K_r:
                mag = 1
                mag_vec = vector2(0, 0)
                
                
    # ----- update -----
    window.fill(colors['white'])

    # -- move particle with mouse --
    if select:
        env_mouse = get_env_pos(get_mouse_pos(), env_select[1], mag, mag_vec)
        env_select[0].move_particle_with_mouse(select, env_mouse)

    # -- move window with mouse --
    if pygame.mouse.get_pressed()[2] and select == None:
        mouse_offset = get_mouse_pos() - preventMouse[-1]
        for env in envs:
            env[1] += mouse_offset/mag
    
    # -- Add particle --
    if add:
        if pygame.mouse.get_pressed()[1] and select == None:
            env_select = environment_clicked()
            if env_select != None:
                env_mouse = get_env_pos(get_mouse_pos(), env_select[1], mag, mag_vec)
                env_select[0].add_particles(1, pos=env_mouse)
                
                add = False
                add_frame = frame_count
    elif add_frame + delay < frame_count:
        add = True

    # -- display and update Environments --
    for env, env_offset in envs:
        env.update(delta)
        env.display(window, env_offset, mag, mag_vec)

    margin_right = 10
    # -- Text info --
    text(window, font, 'FPS: {}'.format(int(clock.get_fps())), (margin_right, 25), colors['black'])
    total = sum([len(env.particles) for env, offset in envs])
    text(window, font, 'Num of total particles: {}'.format(total), (margin_right, 5), colors['black'])
    
    # -- Controls --
    
    text(window, font, 'Zoom in: Z', (margin_right, height - 125), colors['black'])
    text(window, font, 'Zoom out: X', (margin_right, height - 105), colors['black'])
    text(window, font, 'Reset Zoom: R', (margin_right, height - 85), colors['black'])
    text(window, font, 'Grag: Left click', (margin_right, height - 65), colors['black'])
    text(window, font, 'Move window: Right click', (margin_right, height - 45), colors['black'])
    text(window, font, 'Add particle: Center click', (margin_right, height - 25), colors['black'])

    pygame.display.flip()
    
    preventMouse.append(get_mouse_pos())
    preventMouse.pop(0)
