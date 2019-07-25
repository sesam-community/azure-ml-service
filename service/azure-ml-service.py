from flask import Flask, request, Response
import os
import cherrypy
import json
import logging
import paste.translogger
import requests

app = Flask(__name__)

logger = logging.getLogger("azureml-service")

# settings dependent on environment variables
APITOKEN = os.environ.get("AZUREML_API_TOKEN", "")

#@app.route('/token', methods=['GET'])
#def gettoken():
#    return Response(status=200, response=APITOKEN)

@app.route('/', methods=['GET'])
def root():
    return Response(status=200, response="Working.")

@app.route('/run_ml', methods=['POST'])
def run_ml():
    def format_Request(entities):

        inputs = {}
        input1 = {}
        colnames = []
        values_list = []
        values = []
        globalparams = {}

        for index, entity in enumerate(entities):
            #print("entity "+entity+" : " + str(entities[entity]))
            if entity[0] != "_":
                colnames.append(entity.split(":",2)[1])
                values.append(entities[entity])
        values_list.append(values)
        input1["ColumnNames"] = colnames
        input1["Values"] = values_list
        inputs["input1"] = input1
        request_json = {}
        request_json["Inputs"] = inputs
        request_json["GlobalParameters"] = globalparams 
        return(json.dumps(request_json))

    def get_ML_result(entity_id, entities):

        print(entity_id)

        request_json = format_Request(entities)
        #print(str(request_json))
        headers = {
            'Authorization': 'Bearer ' + APITOKEN,
            'Content-Type': 'application/json'
            }
        data = requests.post("https://ussouthcentral.services.azureml.net/workspaces/f139d7eda47d4d65ad14e0a592a015a0/services/6d3d9b7d503b4cca9a42d1be4107d700/execute?api-version=2.0&details=true", headers=headers, data=request_json)
        data_json = json.loads(data.text)

        properties = {}
        properties['_id'] = entity_id

        for index, entity in enumerate(data_json['Results']['output1']['value']['ColumnNames']):
            properties[str(entity).replace(" ","-")] = data_json['Results']['output1']['value']['Values'][0][index]



        yield json.dumps(properties)

    # get entities from request
    entities = request.get_json()

    entity_id = entities.get('_id')
    print(type(entity_id))
    
    # create the response
    return Response(get_ML_result(entity_id, entities), mimetype='application/json')


if __name__ == '__main__':
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Log to stdout, change to or add a (Rotating)FileHandler to log to a file
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(logging.Formatter(format_string))
    logger.addHandler(stdout_handler)

    # Comment these two lines if you don't want access request logging
    app.wsgi_app = paste.translogger.TransLogger(app.wsgi_app, logger_name=logger.name,
                                                 setup_console_handler=False)
    app.logger.addHandler(stdout_handler)

    logger.propagate = False
    logger.setLevel(logging.INFO)

    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5001,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


