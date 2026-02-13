import numpy as np

lista = [1, 2, 3, 4, 5]
array = np.array(lista)

lista2d = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20, 21], [22, 23, 24], [25, 26, 27]]

arr2D = np.array(lista2d)

print(arr2D)

print("Shape: ", arr2D.shape)
print(type(arr2D.shape))


print("Dimensiones: " , arr2D.ndim , " - Previo: " , array.ndim)
print("Size: ", arr2D.size)
print("Tipo: ", arr2D.dtype)


print(np.arange(10))

print([arr2D[0:2,1:2]])