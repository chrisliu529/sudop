import os
from subprocess import Popen, PIPE

puzzles = [x for x in os.listdir('./puzzle') if x.startswith('p')]
for p in puzzles:
    path = f'puzzle/{p}'
    with Popen(['./main.py', path], stdout=PIPE) as pr:
        out = pr.stdout.read().decode('utf-8')
        spath = path.replace('/p', '/s')
        with open(spath) as f:
            expect = f.read()
            if out != expect:
                print(f'output:\n{out}\nexpect:\n{expect}\n')
                os._exit(1)
