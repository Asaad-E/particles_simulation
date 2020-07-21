import pygame
import pygame.gfxdraw
import random
from utils import tuple_int, get_real_pos, inside_window

class Particle:

    def __init__(self, pos, radius, color):
        self.pos   = pygame.Vector2(pos)
        self.radius  = radius
        self.color = color
        self.mass = radius**2
        
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        
        self.elasticity = 0.95
        self.enabled = True
        
    def apply_force(self, force):
        self.acc += force/self.mass
        
    def accelerate(self, acc):
        self.acc += acc
        
    def update(self, delta):
        self.vel += self.acc
        self.acc *= 0
        
        self.pos += self.vel * delta
        
    def inside(self, other):
        """
            detect if another particle is inside it.
        """
        dist_squared = (self.pos - other.pos).magnitude_squared()
        if 0 < dist_squared < (self.radius + other.radius)**2:
            return True
        else:
            return False
    
    def collision(self, other):
        """
            Detects if two particles collide,
            if they do, it gets the new speeds for each one.

            The formula used is that of Collision elastic in two dimensions.
        """
        if self.inside(other):
            # avoid division by zero
            dist_squared = max((self.pos - other.pos).magnitude_squared(), 1)
            
            old_v1 = self.vel
            old_v2 = other.vel
            common = 2/(self.mass + other.mass)

            self.vel = old_v1 - other.mass*common * ((old_v1-old_v2).dot(self.pos-other.pos)/dist_squared) * (self.pos-other.pos)
            other.vel = old_v2 - self.mass*common * ((old_v2-old_v1).dot(other.pos-self.pos)/dist_squared) * (other.pos-self.pos)

            self.vel  *= self.elasticity
            other.vel *= other.elasticity

            # Move one of the two particles to avoid overlapping
            collide_dir = self.pos - other.pos
            intercention = max(-collide_dir.magnitude()+self.radius+other.radius, 1)
            r = random.randint(1, 2)
            if r == 1:
                self.pos += collide_dir.normalize()*intercention
            else:
                other.pos += -collide_dir.normalize()*intercention
                
    def display(self, window, offset, mag, mag_vec):
        """
            Get the true position of the particle on the screen,
            if it is inside it, draw it
        """
        real_pos = get_real_pos(self.pos, offset, mag, mag_vec)
        real_radius = self.radius*mag
        if inside_window(window, real_pos, real_radius):
            args = window, *tuple_int(real_pos), int(real_radius), self.color
            pygame.gfxdraw.aacircle(*args)
            pygame.gfxdraw.filled_circle(*args)
