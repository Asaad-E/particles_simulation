import random
import pygame

colors = {}
colors['white'] = (250, 250, 250)
colors['black'] = ( 10,  10,  10)
colors['red']   = (200,  40,  40)
colors['blue']  = ( 40, 200,  40)
colors['green'] = ( 40,  40, 200)
    
def random_color():
    """
        Choose a random primary color
    """
    return random.choice(list(colors.values())[2:])

def random_color_vibrant():
    """
        Choose a random vibrant color,

        code for: https://www.reddit.com/user/Jsstt <- Thanks
    """
    while True:
        R, G, B = random.sample(range(0,256), 3)
        diff_sum = abs(R-G) + abs(G-B) + abs(R-B)
        if diff_sum > 200:
            return (R, G, B)
            
def vector2(x, y):
    return pygame.Vector2(x, y)

def tuple_int(arg):
    """
        Returns a tuple of integers from a tuple, list or pygame vector
    """
    return int(arg[0]), int(arg[1])

def get_real_pos(pos, offset, mag, mag_vec):
    """
        Giving a relative position gets the true position on the screen
        after applying applying the zoom and the displacement
    """
    return mag_vec + (pos + offset)*mag

def get_env_pos(pos, offset, mag, mag_vec):
    """
        Returns the position relative to an environment
        of a real position on the screen
    """
    return (pos - mag_vec)/mag - offset

def inside_window(window, real_pos, radius=0):
    """
        Detects if a circle (or point if radius = 0) is inside the screen
    """
    x, y = real_pos
    width, height = window.get_size()
    if x+radius >= 0 and x-radius <=width and y+radius >= 0 and y-radius <= height:
        return True
    else:
        return False
