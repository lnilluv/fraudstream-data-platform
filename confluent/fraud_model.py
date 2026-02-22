
from collections import Counter
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import mlflow
import numpy as np
import pandas as pd
import xgboost
from numpy import mean
from sklearn.compose import ColumnTransformer
from sklearn.datasets import make_classification
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score
from sklearn.model_selection import (GridSearchCV, RepeatedStratifiedKFold,
                                     cross_val_score, train_test_split)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

# Set your variables for your environment
EXPERIMENT_NAME = "xgboost"

# Set tracking URI to your Heroku application
mlflow.set_tracking_uri("https://mlflow.pryda.dev")

# Set experiment's info 
mlflow.set_experiment(EXPERIMENT_NAME)

# Get our experiment info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

data = pd.read_csv('data/fraudTest.csv', index_col=0)

# Call mlflow autolog
mlflow.xgboost.autolog()

with mlflow.start_run(experiment_id=experiment.experiment_id):


    X = data.drop(["is_fraud","trans_date_trans_time"], axis=1)
    y = data["is_fraud"]

    cat_cols = [ 'merchant', 'category', 'first', 'last',
                'gender', 'street', 'city', 'state', 'job', 'dob', 'trans_num']
    num_cols = ['cc_num', 'amt', 'zip', 'lat', 'long', 'city_pop', 'unix_time',
                'merch_lat', 'merch_long']

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, stratify=y)

    numeric_transformer = Pipeline(
        steps=[
        ('scaler', StandardScaler()) # standardization
    ])
        
    categorical_transformer = Pipeline(
        steps=[
            ('encoder', OneHotEncoder(handle_unknown="ignore", drop='first')) # first column will be dropped to avoid creating correlations between features
        ])
    # Use ColumnTransformer to make a preprocessor object that describes all the treatments to be done
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, num_cols),
            ('cat', categorical_transformer, cat_cols)
        ])

    # Preprocessings on train set
    X_train = preprocessor.fit_transform(X_train)

    # Create a pipeline to encode categorical columns using OneHotEncoder and fit a XGBClassifier
    model = Pipeline([
        ('classifier', XGBClassifier(scale_pos_weight=0.9))
    ])

    model.fit(X_train, Y_train)

    Y_train_pred = model.predict(X_train)
    X_test = preprocessor.transform(X_test) 
    Y_test_pred = model.predict(X_test)
    mlflow.log_metric("train_f1_score", f1_score(Y_train, Y_train_pred))
    mlflow.log_metric("test_f1_score", f1_score(Y_test, Y_test_pred))
        

