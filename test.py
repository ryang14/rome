from drivers.sim import Sim, Point, Pointj
import scripts

arm = Sim()

# Temporary CLI for testing

def cmdHelp(args):
    print('Commands:')
    for command in commands.keys():
        print(command)

def cmdMove(args):
    arm.move(Point(x=float(args[1]), y=float(args[2]), z=float(args[3]), rx=float(args[4]), ry=float(args[5]), rz=float(args[6])))
    print(arm.here())

def cmdMovej(args):
    arm.move(Pointj(j1=float(args[1]), j2=float(args[2]), j3=float(args[3]), j4=float(args[4]), j5=float(args[5]), j6=float(args[6])))
    print(arm.herej())

def cmdHere(args):
    print(arm.here())

def cmdHerej(args):
    print(arm.herej())

def cmdNewScript(args):
    try:
        scripts.new(args[1])
    except OSError:
        print('Script exists')

def cmdListScript(args):
    print(scripts.list())

def cmdLoadScript(args):
    try:
        scripts.load(args[1])
    except OSError:
        print('Script load failed')

def cmdSaveScript(args):
    try:
        scripts.save(args[1])
    except OSError:
        print('Script save failed')

def cmdRunScript(args):
    try:
        scripts.run(args[1])
    except OSError:
        print('Script run failed')


commands = {
    'help': cmdHelp,
    'move': cmdMove,
    'movej': cmdMovej,
    'here': cmdHere,
    'herej': cmdHerej,
    'new': cmdNewScript,
    'list': cmdListScript,
    'load': cmdLoadScript,
    'save': cmdSaveScript,
    'run': cmdRunScript
    }

while True:
    command = str(input('>'))
    args = command.split(' ')

    try:
        commands[args[0]](args)
    except KeyError:
        cmdHelp(args)
