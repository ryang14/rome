import os
import shutil
import json
import runpy


def new(name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    try:
        os.mkdir(path)
    except:
        raise
    else:
        # Create the parameter file to hold points, constants, etc.
        # This can be edited by the framework and is available to the driver at runtime
        with open(os.path.join(path, 'parameters.json'), 'w') as f:
            json.dump({'parameters': {}}, f)

        # Create the main driver file
        open(os.path.join(path, '__main__.py'), 'w')


def delete(name):
    if not name == 'sim':  # Don't delete the simulator
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

        if os.path.realpath(path) != path:
            raise FileNotFoundError

        shutil.rmtree(path)


def list():
    drivers = []
    for f in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), f, 'parameters.json')):
            drivers.append(f)
    return drivers


def load(name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    try:
        with open(os.path.join(path, 'parameters.json'), 'r') as f:
            return json.load(f)['parameters']
    except:
        raise


def save(name, parameters):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    try:
        with open(os.path.join(path, 'parameters.json'), 'w') as f:
            json.dump({'parameters': parameter}, f)
    except:
        raise


def run(name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    driver_globals = {}
    try:
        with open(os.path.join(path, 'parameters.json'), 'r') as f:
            driver_globals.update(json.load(f)['parameters'])
        return runpy.run_path(path, init_globals=driver_globals)
    except:
        raise
