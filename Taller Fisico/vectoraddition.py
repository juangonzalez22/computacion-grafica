def vector_addition(vector1, vector2):
    final_vector = []

    if len(vector1) != len(vector2):
        raise ValueError("Vectors must be of the same length")
    
    for i in range(len(vector1)):
        final_vector.append(vector1[i] + vector2[i])
    return final_vector