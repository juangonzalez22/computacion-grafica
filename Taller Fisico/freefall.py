import math 

def time_to_fall(height, gravity):
    time = math.sqrt((2 * height) / gravity)
    return time
