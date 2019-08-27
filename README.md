# Introduction 
This package helps you get started with using Azure Machine Learning Studio integrated with Sesam for both training models and running them operationally over datasets

![Sesam AMLS](https://github.com/sesam-community/wiki/raw/master/pictures/Sesam%20-%20Azure%20Machine%20Learning%20Studio.png "Sesam Azure Machine Learning Architecture")

# Getting Started
This guide presumes knowledge about using Microsoft Azure Machine Learning Studio and setting up of experiments and webservices

# Training data sets
Use Sesam to create a published CSV endpoint with your training data. This URL can be used directly in the "import data" function within Azure ML.

[CSV endpoint pipe configuration](https://docs.sesam.io/configuration.html#the-csv-endpoint-sink)

# Integrating sesam with the Azure ML webservice
To operationalise your Azure ML trained model, setup a webservice and then use this microservice to integrate with Sesam. Ensure that the schema delivered to the microservice is the same as in the training set above.

Example microservice config:
---------------------------
```
{
  "_id": "azure-ml-service",
  "connect_timeout": 60,
  "docker": {
    "environment": {
      "AZUREML_API_TOKEN": "$SECRET(azureml)",
      "LOG_LEVEL": "DEBUG",
      "SESAM-API": "https://datahub-xxxxxxxx.sesam.cloud/api/",
      "SESAM-JWT": "$SECRET(own-jwt)"
    },
    "image": "<docker repo>",
    "memory": 128,
    "password": "<password>",
    "port": 5001,
    "username": "<username>"
  },
  "read_timeout": 7200,
  "type": "system:microservice",
  "use_https": false,
  "verify_ssl": true
}
```
