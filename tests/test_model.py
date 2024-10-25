import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import joblib
import argparse
import pandas as pd

# Nombres de las emociones en español e inglés
emotion_labels_es = ["tristeza", "alegría", "amor", "ira", "miedo", "sorpresa"]
emotion_labels_en = ["sadness", "joy", "love", "anger", "fear", "surprise"]

def load_model(language):
    model = joblib.load(f'model/emotion_model_{language}.pkl')
    vectorizer = joblib.load(f'model/vectorizer_{language}.pkl')
    return model, vectorizer

def predict_emotion(text, model, vectorizer, labels):
    text_tfidf = vectorizer.transform([text])
    prediction = model.predict(text_tfidf)
    return prediction[0]  # Devolver la etiqueta de la emoción

if __name__ == "__main__":
    # Configurar el argumento de idioma
    parser = argparse.ArgumentParser(description="Predecir la emoción usando un modelo entrenado.")
    parser.add_argument('--language', type=str, default="es", choices=["es", "en"], 
                        help="Idioma del dataset: 'es' para español o 'en' para inglés.")
    args = parser.parse_args()

    # Obtener el idioma desde los argumentos
    language = args.language

    # Seleccionar las etiquetas correspondientes al idioma
    emotion_labels = emotion_labels_es if language == "es" else emotion_labels_en

    # Cargar el modelo y el vectorizador en función del idioma
    model, vectorizer = load_model(language)

    # Texto de ejemplo para prueba
    example_text = "No entro ahí, ni de lejos, qué acojone" if language == "es" else "I won't go there, no way, it's terrifying"
    
    # Predecir la emoción
    predicted_emotion = predict_emotion(example_text, model, vectorizer, emotion_labels)
    
    # Imprimir el resultado
    print(f'Texto: "{example_text}"')
    print(f'Emoción predicha: {predicted_emotion}')
