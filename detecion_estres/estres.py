import joblib
import numpy as np

# Cargar el modelo entrenado y el scaler
model = joblib.load('detecion_estres/modelo_entrenado.pkl')
scaler = joblib.load('detecion_estres/scaler.pkl')

def calcular_estres(usuario, encuesta, sensores):
    # Extraer características necesarias para la predicción
    caracteristicas = np.array([[sensores.sen_temperatura, 
                                 sensores.sen_freq_respiratoria, 
                                 sensores.sen_freq_cardiaca]])

    # Normalizar las características utilizando el scaler cargado
    caracteristicas_normalizadas = scaler.transform(caracteristicas)

    # Verificar la cantidad de características esperadas por el modelo
    n_features_expected = model.n_features_in_
    n_features_provided = caracteristicas_normalizadas.shape[1]
    
    if n_features_provided != n_features_expected:
        raise ValueError(f'El modelo espera {n_features_expected} características, pero se proporcionaron {n_features_provided} características.')

    # Hacer la predicción utilizando el modelo entrenado
    prediccion = model.predict(caracteristicas_normalizadas)
    return prediccion[0]
