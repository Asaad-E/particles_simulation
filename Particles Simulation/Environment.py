import pygame
import random
from Particle import Particle
from utils import random_color_vibrant, random_color, vector2, get_real_pos

class Environment:
    """
        Container that handles the particles it contains
    """

    def __init__(self, size, num=0):
        self.width, self.height = self.size = size
        self.particles = []
        self.add_particles(num)
        
        self.drag = 0.001
        self.gravity = pygame.Vector2(0, 0)

        self.border_color = (10, 10, 10)
        self.border_points = [vector2(0, 0), vector2(self.width, 0), vector2(self.width ,self.height), vector2(0, self.height), vector2(0, 0)]
        self.w = 2

    def add_particles(self, n=1, **kargs):
        """
            Add an amount n of particles with the past kargs
        """
        margin = 10
        for i in range(n):
            repeat = True
            while repeat:
                inside = False
                radius = kargs.get('radius', random.randint(10, 15))
                pos = kargs.get('pos', (random.randint(radius+margin, self.width-radius-margin),\
                                       random.randint(radius+margin, self.height-radius-margin)))
                color = kargs.get('color', random_color_vibrant())
                speed = kargs.get('speed', random.randint(20, 100))
                vel = vector2(0, 1).rotate(random.uniform(0, 360))*speed
                new_particle = Particle(pos, radius, color)
                new_particle.vel = vel
                
                if 'pos' not in kargs:
                    for particles in self.particles:
                        if particles.inside(new_particle):
                            inside = True
                            break
                
                if inside == False:
                    self.particles.append(new_particle)
                    repeat = False

    def drag_particle(self, p):
        """
            Model drag with F = drag * V ^ 2 * unit_V
        """
        if p.vel.magnitude_squared() > 0:
            p.apply_force(-p.vel.normalize()*self.drag*p.vel.magnitude())
            
    def set_gravity(self, ax, ay):
        self.gravity = pygame.Vector2(ax, ay)
        
    def draw_border(self, window, offset, mag, mag_vec):
        """
            draws the edges of the container,
            obtained the actual position of each point
        """
        common = window, self.border_color, True
        o = offset
        w = int(max(2, self.w*mag))
        for i in range(4):
            p1 = get_real_pos(self.border_points[i], offset, mag, mag_vec)
            p2 = get_real_pos(self.border_points[i+1], offset, mag, mag_vec)
            pygame.draw.lines(*common, [p1, p2], w)

    def update(self, delta):
        """
            Update the states of each particle
        """
        for i, p in enumerate(self.particles):
            if p.enabled:
                p.accelerate(self.gravity)
                self.drag_particle(p)
                for p2 in self.particles[i+1:]:
                    if p2.enabled:
                        p.collision(p2)
                p.update(delta)
                self.edge(p)
                
    def display(self, window, offset, mag, mag_vec):
        """
            Draw the container and all the particles in the environment
        """
        for p in self.particles:
            p.display(window, offset, mag, mag_vec)
  
        self.draw_border(window, offset, mag, mag_vec)
            
    def click_particle(self, mouse_pos):
        """
            With the mouse position it detects if a particle has been clicked,
            if it does it returns that particle
        """
        for p in self.particles:
            if (mouse_pos-p.pos).magnitude_squared() <= p.radius**2:
                return p
        return None

    def move_particle_with_mouse(self, particle, mouse_pos):
        """
            Move the selected particle to the mouse position
            without leaving the edges of the Environment
        """
        env_mouse_pos = mouse_pos
        if env_mouse_pos.x - particle.radius >= 0 and env_mouse_pos.x + particle.radius<= self.width:
            particle.pos.x = env_mouse_pos.x
        else:
            if env_mouse_pos.x - particle.radius > 0:
                particle.pos.x = self.width - particle.radius
            else:
                particle.pos.x = particle.radius
        if env_mouse_pos.y - particle.radius >= 0 and env_mouse_pos.y + particle.radius<= self.height:
            particle.pos.y = env_mouse_pos.y
        else:
            if env_mouse_pos.y - particle.radius > 0:
                particle.pos.y = self.height - particle.radius
            else:
                particle.pos.y = particle.radius

    def edge(self, particle):
        """
            Check that the particles do not escape from the environment
        """
        w, h = self.size
        if particle.pos.x + particle.radius > w:
            particle.pos.x = w - particle.radius
            particle.vel.x *= -1
            particle.vel *= particle.elasticity
        elif particle.pos.x - particle.radius < 0:
            particle.pos.x = particle.radius
            particle.vel.x *= -1
            particle.vel *= particle.elasticity

        if particle.pos.y + particle.radius > h:
            particle.pos.y = h - particle.radius
            particle.vel.y *= -1
            particle.vel *= particle.elasticity
        elif particle.pos.y - particle.radius < 0:
            particle.pos.y = particle.radius
            particle.vel.y *= -1
            particle.vel *= particle.elasticity

