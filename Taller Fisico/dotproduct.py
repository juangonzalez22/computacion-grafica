import math

def dot_product(vector1, vector2):
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")
    
    product = 0
    for i in range(len(vector1)):
        product += vector1[i] * vector2[i]
    return product

def angle_between_vectors(vector1, vector2):
    dot_product_value = dot_product(vector1, vector2)
    magnitude1 = math.sqrt(sum(x**2 for x in vector1))
    magnitude2 = math.sqrt(sum(x**2 for x in vector2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        raise ValueError("Vectors must not be zero vectors")
    
    cos_angle = dot_product_value / (magnitude1 * magnitude2)
    angle_rad = math.acos(cos_angle)
    return math.degrees(angle_rad)