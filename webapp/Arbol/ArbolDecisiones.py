import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier

def clasificar(sintomas_usuario):
    if not sintomas_usuario:
        raise ValueError("No se proporcionaron síntomas")

    if not isinstance(sintomas_usuario, list):
        raise ValueError("Los síntomas deben ser proporcionados como una lista")

    sintomas_usuario = ','.join(sintomas_usuario)
    csv_path = 'webapp/arbol/datos_medicos2.csv'
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el archivo CSV en la ruta: {csv_path}")

    data = pd.read_csv(csv_path)
    data['sintomas_completos'] = data.apply(lambda row: ','.join([row['sintoma1'], row['sintoma2'], row['sintoma3'], row['sintoma4']]), axis=1)

    X_train, X_test, y_train, y_test = train_test_split(data['sintomas_completos'], data['enfermedad'], test_size=0.2, random_state=42)

    gb_model = GradientBoostingClassifier(learning_rate=0.01, max_depth=500, n_estimators=300, random_state=42)
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    gb_model.fit(X_train_vectorized, y_train)

    sintomas_usuario_vectorized = vectorizer.transform([sintomas_usuario])
    probabilidades_gb = gb_model.predict_proba(sintomas_usuario_vectorized)[0]

    resultados_gb = pd.DataFrame({'Enfermedad': gb_model.classes_, 'Probabilidad': probabilidades_gb})
    resultados_gb = resultados_gb.sort_values(by='Probabilidad', ascending=False)
    resultados_gb['Probabilidad'] = resultados_gb['Probabilidad'] * 100
    resultados_top5_gb = resultados_gb.head(5)

    print("--------------------------------------------------------------------------------------")
    print("Síntomas del paciente: ", sintomas_usuario)
    print("--------------------------------------------------------------------------------------")
    print("Diagnóstico diferencial:")
    print("-------------------------------------------")
    print(resultados_top5_gb)
    print("-------------------------------------------")

    return resultados_top5_gb
