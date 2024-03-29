import os
import shutil
import json
import runpy
import multiprocessing
import signal

scriptProc = None

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


def run(name, driver):
    path = os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

    if os.path.realpath(path) != path:
        raise FileNotFoundError

    script_globals = {}
    with open(os.path.join(path, 'data.json'), 'r') as f:
        script_globals.update(json.load(f)['data'])
    script_globals.update(driver)
    global scriptProc
    # Only run the script if one is not running
    if(scriptProc == None or not scriptProc.is_alive()):
        scriptProc = multiprocessing.Process(name = name, target=runpy.run_path, args=(path, script_globals))
        scriptProc.start()

def stop():
    global scriptProc
    os.kill(scriptProc.pid, signal.SIGINT) # scriptProc.terminate() doesn't work with gunicorn
    scriptProc.join()
