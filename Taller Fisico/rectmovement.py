import math

def movement_in_line(start_speed, acceleration, time):
    distance = (start_speed * time) + (0.5 * acceleration * (time ** 2))
    return distance