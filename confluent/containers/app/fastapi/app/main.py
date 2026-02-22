# app/main.py
import mlflow 
import uvicorn
import json
import pandas as pd 
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from app.db import dispose_engine, get_or_create_user, get_users, init_db
import warnings
import platform
from PIL import Image
from app.utils import image2tensor, pred2label, labels
import tensorflow as tf
import numpy as np

app = FastAPI(title="BrainSight Public API")

@app.get("/")
async def read_root():
    return await get_users()

#class PredictionFeatures(BaseModel):
#    BrainDisease: float


@app.post("/predictionalz", tags=["Deep Learning classification: Alzheimer"])
async def post_picture(file: UploadFile= File(...)):
    """ 
    Alzheimer detection
    """
    img = await file.read()
    img_batch = image2tensor(img, dim=(176, 208))
    
    logged_model = 'runs:/b347c773a181434fae3e122921c1d937/model'
    model = mlflow.tensorflow.load_model(logged_model, keras_model_kwargs={'compile':False})
    
    prediction = model.predict(img_batch)[0]    
    print(prediction)
        
    prediction_label = pred2label(prediction)
        
    response = {
            "prediction" : prediction.tolist(), 
            "predicted_label": prediction_label, 
            "labels": labels
            }
    print(response)
    return response



@app.post("/predictionbt", tags=["Deep Learning classification: Brain Tumors"])
async def post_picture(file: UploadFile= File(...)):
    """
    Brain tumor detection 
    """
    img = await file.read()
    img_batch = image2tensor(img, dim=(176, 208))

    logged_model = 'runs:/b347c773a181434fae3e122921c1d937/model'
    model = mlflow.tensorflow.load_model(logged_model, keras_model_kwargs={'compile':False})

    prediction = model.predict(img_batch)[0]
    print(prediction)

    prediction_label = pred2label(prediction)

    response = {
            "prediction" : prediction.tolist(),
            "predicted_label": prediction_label,
            "labels": labels
            }
    print(response)
    return response

@app.on_event("startup")
async def startup():
    await init_db()
    await get_or_create_user(email="test@test.com")


@app.on_event("shutdown")
async def shutdown():
    await dispose_engine()
