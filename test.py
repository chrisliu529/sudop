import os
from subprocess import Popen, PIPE

puzzles = [x for x in os.listdir('./puzzles') if x.startswith('p')]
for p in puzzles:
    path = f'puzzles/{p}'
    with Popen(['./main.py', path], stdout=PIPE) as pr:
        out = pr.stdout.read().decode('utf-8')
        spath = path.replace('/p', '/s')
        with open(spath) as f:
            expect = f.read()
            if out != expect:
                print(f'path:{path}\noutput:\n{out}\nexpect:\n{expect}\n')
                os._exit(1)

false_games = [x for x in os.listdir('./puzzles') if x.startswith('f')]
for p in false_games:
    path = f'puzzles/{p}'
    with Popen(['./main.py', path], stdout=PIPE) as pr:
        out = pr.stdout.read().decode('utf-8')
        if out.find('false') < 0:
            print(f'{path} is expected to be a false game')
            os._exit(1)
