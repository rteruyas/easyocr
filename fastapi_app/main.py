from fastapi import FastAPI, File, UploadFile
from PIL import Image
from datetime import datetime
import easyocr as ocr
import numpy as np
import json
import mlflow
from mlflow.tracking import MlflowClient

# on commence par loader le modele. Si on le trouve pas, on va le creer dans model_storage_directory
# le modele est deja entraine
reader = ocr.Reader(['en','fr'], model_storage_directory = './models/')
app = FastAPI()
db = []

mlflow.set_tracking_uri("http://mlflow:5000")
experiment_name = "EASYOCR"

##########################
# FastAPI endpoints
@app.get('/')
async def read_root():
        return{'message': 'Welcome to FASTAPI'}


@app.post('/extract')
async def extract_text(file: UploadFile = File(...)):
    im = Image.open(file.file)
    
    before_run = datetime.now() #current date and time
    result = reader.readtext(im) #fonction principal pour extraire texte
    after_run = datetime.now() #current date and time

    delta = after_run - before_run
    time_in_seconds = delta.days * 24 *3600 + delta.seconds
    print(f'time in seconds for experiment: {time_in_seconds}') 

    result_text = [] #results

    for text in result:
        result_text.append(text[1])

    response = {'message': json.dumps(result_text)}
    
    #mlflow log experiment
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run():
        mlflow.log_metric("runtime_in_seconds",f'{time_in_seconds}')
        #mlflow.log_metric('results',json.dumps(result_text))

    print(response)

    return response