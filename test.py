import os
from subprocess import Popen, PIPE

def normal_game(out, path):
    spath = path.replace('/p', '/s')
    with open(spath) as f:
        expect = f.read()
        if out != expect:
            print(f'path:{path}\noutput:\n{out}\nexpect:\n{expect}\n')
            os._exit(1)

def false_game(out, path):
    if out.find('false game') < 0:
        print(f'{path} is expected to be a false game')
        os._exit(1)

def bad_game(out, path):
    if out.find('bad game') < 0:
        print(f'{path} is expected to be a bad game')
        os._exit(1)

cases = {
    'p': normal_game,
    'f': false_game,
    'b': bad_game
}

for prefix, verify in cases.items():
    puzzles = [x for x in os.listdir('./puzzles') if x.startswith(prefix)]
    for p in puzzles:
        path = f'puzzles/{p}'
        with Popen(['./main.py', path], stdout=PIPE) as pr:
            out = pr.stdout.read().decode('utf-8')
            verify(out, path)

print('test pass')
