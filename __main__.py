import os
from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import scripts
import drivers

app = FlaskAPI(__name__)

# Enable CORS so we can run the fromt end dev server separately
CORS(app, resources={r'/*': {'origins': '*'}})

# Driver to use
driver = 'sim'


def script_repr(name):
    return {
        'url': request.host_url.rstrip('/') + url_for('scripts_detail', name=name),
        'run': request.host_url.rstrip('/') + url_for('scripts_run', name=name),
        'data': scripts.load(name),
        'name': name
    }


@app.route("/scripts", methods=['GET', 'POST'])
def scripts_list():
    # Create script
    if request.method == 'POST':
        name = str(request.data.get('name'))
        scripts.new(name)
        return script_repr(name), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [script_repr(name) for name in sorted(scripts.list())]


@app.route("/scripts/<string:name>/", methods=['GET', 'PUT', 'DELETE'])
def scripts_detail(name):
    if request.method == 'PUT':
        data = request.data.get('data')
        scripts.save(name, data)
        return script_repr(name)

    elif request.method == 'DELETE':
        scripts.delete(name)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    return script_repr(name)


@app.route("/scripts/<string:name>/run", methods=['GET'])
def scripts_run(name):
    try:
        scripts.run(name, driver)
    except:
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR
    else:
        return script_repr(name)


def driver_repr(name):
    return {
        'url': request.host_url.rstrip('/') + url_for('drivers_detail', name=name),
        'select': request.host_url.rstrip('/') + url_for('drivers_select', name=name),
        'data': drivers.load(name),
        'name': name
    }


@app.route("/drivers", methods=['GET', 'POST'])
def drivers_list():
    # Create driver
    if request.method == 'POST':
        name = str(request.data.get('name'))
        drivers.new(name)
        return driver_repr(name), status.HTTP_201_CREATED

    # request.method == 'GET'
    return [driver_repr(name) for name in sorted(drivers.list())]


@app.route("/drivers/<string:name>/", methods=['GET', 'PUT', 'DELETE'])
def drivers_detail(name):
    if request.method == 'PUT':
        data = request.data.get('data')
        drivers.save(name, data)
        return driver_repr(name)

    elif request.method == 'DELETE':
        drivers.delete(name)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    return driver_repr(name)


@app.route("/drivers/<string:name>/select", methods=['GET'])
def drivers_select(name):
    global driver
    driver = name
    return driver_repr(name)


def browse_repr(path, name):
    return {
        'url': request.host_url.rstrip('/') + url_for('browser', urlFilePath=os.path.join(path, name)),
        'name': name
    }


@app.route('/browser')
def browse():
    try:
        return {'type': 'folder', 'contents': [browse_repr('', name) for name in sorted(os.listdir(os.path.dirname(__file__)))]}
    except:
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/browser/<path:urlFilePath>')
def browser(urlFilePath):
    try:
        path = os.path.join(os.path.dirname(__file__), urlFilePath)

        if os.path.realpath(path) != path:
            return '', status.HTTP_500_INTERNAL_SERVER_ERROR

        if os.path.isfile(path):
            with open(path, 'r') as f:
                return {'type': 'file', 'contents': f.read()}
        
        if os.path.isdir(path):
            return {'type': 'folder', 'url': request.host_url.rstrip('/') + url_for('browser', urlFilePath=urlFilePath), 'contents': [browse_repr(urlFilePath, name) for name in sorted(os.listdir(path))]}

    except:
        return '', status.HTTP_500_INTERNAL_SERVER_ERROR


if __name__ == "__main__":
    app.run(debug=True)
