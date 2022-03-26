

def translate_range(v, from_min,from_max, to_min, to_max):
    from_span = from_max - from_min
    to_span = to_max - to_min

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(v - from_min) / float(from_span)

    # Convert the 0-1 range into a value in the right range.
    return to_min + (valueScaled * to_span)

print(translate_range(0.5, 0,2, -10, 10))
