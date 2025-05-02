from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import joblib

app = FastAPI()

# Correct CORS setup for FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

encoder = joblib.load('encoder.pkl')
vectorizer = joblib.load('vectorizer.pkl')
loaded_model = joblib.load('sentimentanalyze.pkl')

wnl = WordNetLemmatizer()

def preprocessText(text):
    text = text.lower()

    tokens = word_tokenize(text)

    filtered = [token for token in tokens if token.isalpha()]

    lemmas = [wnl.lemmatize(x) for x in filtered]

    return ' '.join(lemmas)


class feature(BaseModel):
    text: str

@app.post('/predict')
def predict(data: feature):
    try:
        filteredinput = preprocessText(data.text)
        input_vect = vectorizer.transform([filteredinput])
        prediction = loaded_model.predict(input_vect)
        encoded_pred = encoder.inverse_transform(prediction)
        return (f'Prediction : {encoded_pred[0]}')
    except Exception as e:
        return HTTPException(status_code = 500, detail = str(e))