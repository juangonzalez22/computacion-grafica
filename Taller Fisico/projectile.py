import math

def max_reach(initial_speed, angle, gravity):
    angle_rad = math.radians(angle)
    return (initial_speed ** 2) * math.sin(2 * angle_rad) / gravity

def max_height(initial_speed, angle, gravity):
    angle_rad = math.radians(angle)
    return (initial_speed ** 2) * (math.sin(angle_rad) ** 2) / (2 * gravity)
