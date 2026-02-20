import matplotlib.pyplot as plt
import numpy as np

ruta = "images/gengar2.png"
imagen = plt.imread(ruta)


def extraer_capa(imagen, capa):
    capa_extraida = np.copy(imagen)
    if capa == "roja":
        capa_extraida[:, :, 1] = capa_extraida[:, :, 2] = 0
    elif capa == "verde":
        capa_extraida[:, :, 0] = capa_extraida[:, :, 2] = 0
    elif capa == "azul":
        capa_extraida[:, :, 0] = capa_extraida[:, :, 1] = 0
    elif capa == "cyan":
        capa_extraida[:, :, 0] = 0
    elif capa == "magenta":
        capa_extraida[:, :, 1] = 0
    elif capa == "amarillo":
        capa_extraida[:, :, 2] = 0