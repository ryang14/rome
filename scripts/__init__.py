import os
import shutil
import json
import runpy
from rome import drivers


def new(name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    try:
        os.mkdir(path)
    except:
        raise
    else:
        # Create the data file to hold points, constants, etc.
        # This can be edited by the framework and is available to the script at runtime
        with open(os.path.join(path, 'data.json'), 'w') as f:
            json.dump({'data': {}}, f)

        # Create the main script file
        open(os.path.join(path, '__main__.py'), 'w')


def delete(name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    shutil.rmtree(path)


def list():
    scripts = []
    for f in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), f, 'data.json')):
            scripts.append(f)
    return scripts


def load(name):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    try:
        with open(os.path.join(path, 'data.json'), 'r') as f:
            return json.load(f)['data']
    except:
        raise


def save(name, data):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    try:
        with open(os.path.join(path, 'data.json'), 'w') as f:
            json.dump({'data': data}, f)
    except:
        raise


def run(name, driver='sim'):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    script_globals = {}
    try:
        with open(os.path.join(path, 'data.json'), 'r') as f:
            script_globals.update(json.load(f)['data'])
        driver = drivers.run(driver)
        script_globals.update(driver)
        runpy.run_path(path, init_globals=script_globals)
    except:
        raise
