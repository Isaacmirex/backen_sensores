import joblib
import numpy as np

# Cargar el modelo entrenado
model = joblib.load('detecion_estres/modelo_entrenado.pkl')

def calcular_estres(usuario, encuesta, sensores):
    # Extraer características necesarias para la predicción
    caracteristicas = np.array([[sensores.sen_temperatura, 
                                 sensores.sen_freq_respiratoria, 
                                 sensores.sen_freq_cardiaca]])

    # Verificar la cantidad de características esperadas por el modelo
    n_features_expected = model.n_features_in_
    n_features_provided = caracteristicas.shape[1]
    
    if n_features_provided != n_features_expected:
        raise ValueError(f'El modelo espera {n_features_expected} características, pero se proporcionaron {n_features_provided} características.')

    prediccion = model.predict(caracteristicas)
    return prediccion[0]
