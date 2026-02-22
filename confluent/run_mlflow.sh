docker run -it\
 -p 4001:4001\
 -v "$(pwd):/home/app"\
 -e APP_URI="https://mlflow.pryda.dev"\
 -e BACKEND_STORE_URI=$BACKEND_STORE_URI\
 -e ARTIFACT_STORE_URI=$ARTIFACT_STORE_URI\
 -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID\
 -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY\
 mlflow python fraud_model.py