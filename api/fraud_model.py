import os
from datetime import datetime
from pathlib import Path
import boto3
import mlflow
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from botocore.client import Config

import pandas as pd
import numpy as np

import imblearn
import xgboost
from numpy import mean
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn.compose import ColumnTransformer

from collections import Counter
from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score,RepeatedStratifiedKFold
from xgboost import XGBClassifier
from imblearn.pipeline import Pipeline
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler


from sklearn.metrics import f1_score

import joblib

# login to S3-compatible object storage from environment variables
s3_endpoint_url = os.getenv("S3_ENDPOINT_URL")
s3_access_key = os.getenv("S3_ACCESS_KEY_ID")
s3_secret_key = os.getenv("S3_SECRET_ACCESS_KEY")
s3_bucket_name = os.getenv("S3_BUCKET_NAME")

s3 = None
if s3_endpoint_url and s3_access_key and s3_secret_key:
    s3 = boto3.resource(
        "s3",
        endpoint_url=s3_endpoint_url,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key,
        config=Config(signature_version="s3v4"),
        region_name=os.getenv("S3_REGION", "us-east-1"),
    )

if s3 is not None and s3_bucket_name:
    s3.Bucket(s3_bucket_name).upload_file(Path(__file__).name, str(datetime.now()) + Path(__file__).name)

# Set your variables for your environment
EXPERIMENT_NAME = "modele-description"

# Set tracking URI to your Heroku application
mlflow.set_tracking_uri("https://mlflow.fraud-detection.live")

# Set experiment's info 
mlflow.set_experiment(EXPERIMENT_NAME)

# Get our experiment info
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)

# Call mlflow autolog
#mlflow.sklearn.autolog()
mlflow.sklearn.autolog()

with mlflow.start_run(experiment_id=experiment.experiment_id):
    # indent
    


# %%


    # %%
    data = pd.read_csv('data/fraudTest.csv', index_col=0)

    # %%
    # labels=["Genuine","Fraud"]

    # fraud_or_not = data["is_fraud"].value_counts().tolist()
    # values = [fraud_or_not[0], fraud_or_not[1]]

    # fig = px.pie(values=data['is_fraud'].value_counts(), names=labels , width=700, height=400, color_discrete_sequence=["LightGreen","Blue"]
    #             ,title="Fraud vs Genuine transactions")
    # fig.show()

    # %%
    # plt.figure(figsize=(3,4))
    # ax = sns.countplot(x='is_fraud',data=data,palette="gray")
    # for i in ax.containers:
    #     ax.bar_label(i,)

    # %% [markdown]
    # we have 99,6% of Genuine transactions and only 0,386%of fraud transactions

    # %% [markdown]
    # We can not use accuracy as score because of imbalanced data! Better to use F1-score or other metrics!

    # %% [markdown]
    # ## Data pre-processing

    # %%
    # Drop duplicates lines : 
    data.drop_duplicates(inplace=True)
    data.shape

    # %% [markdown]
    # ### Under-sampling Data to get balanced Dataset
    #  

    # %%
    # define dataset
    X, y = make_classification(n_samples=100000, weights=[0.99], flip_y=0)

    # define undersample strategy
    undersample = RandomUnderSampler(sampling_strategy=0.5)

    # %%
    # define pipeline
    steps = [('under', undersample), ('model', XGBClassifier())]
    pipeline = Pipeline(steps=steps)

    # fit and apply the transform
    X_under, y_under = undersample.fit_resample(X, y)

    # print(Counter(y))
    # print(Counter(y_under))

    # %%
    # evaluate pipeline
    cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
    scores = cross_val_score(pipeline, X, y, scoring='f1_micro', cv=cv, n_jobs=-1)
    score = mean(scores)
    print('F1 Score: %.3f' % score)

    # %%
    from sklearn.model_selection import train_test_split
    # Divide dataset Train set & Test set 
    print("Dividing into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X_under, y_under, stratify=y_under, test_size = 0.2)

    # %%
    model = Pipeline(steps=[
            ("Classifier",XGBClassifier())
        ])

    # %%
    model.fit(X_train, y_train)

    train_pred = model.predict(X_train)
    test_pred = model.predict(X_test)

    print("f1-score on train set : ", f1_score(y_train, train_pred))
    print("f1-score on test set : ", f1_score(y_test, test_pred))

    # %% [markdown]
    # ## Preparing the API

    # # %%
    # from joblib import dump, load
    # dump(model, 'model_xg.joblib')

    # # %%
    # predictionFeatures = { }

    # # %%
    # data = pd.DataFrame(dict(predictionFeatures), index=[0])
    # data

    # # %%
    # loaded_model = load('model_xg.joblib')

    # # %%
    # prediction = loaded_model.predict(data)
    # response = {"predictions": prediction.tolist()[0]}

