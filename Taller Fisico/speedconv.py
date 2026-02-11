def convert_speed(speed, conversion):
    if conversion == 1:
        return speed * 3.6  # Convert m/s to km/h
    elif conversion == 2:
        return speed / 3.6  # Convert km/h to m/s