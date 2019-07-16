#!/usr/bin/python3

from mpyc.runtime import mpc
import numpy as np

import ast
import sys





secint = mpc.SecInt()
secfxp = mpc.SecFxp()


nb_parties = len(mpc.parties)
print(nb_parties)

my_pid = mpc.pid
print(my_pid)

with open(f'DATA/v{my_pid}.txt') as f:

    vi_string = f.read()
    vi = ast.literal_eval(vi_string)

    if type(vi) is int:
        print('Single integer')
        sec_vi = secint(vi)

    elif type(vi) is float:
        print('Single float')
        sec_vi = secfxp(vi)

    elif type(vi) is list:
        if type(vi[0]) is int:
            print('List of integers')
            sec_vi = list(map(secint, vi))

        elif type(vi[0]) is float:
            print('List of floats')
            sec_vi = list(map(secfxp, vi))

        else:
            print(f'Unsupported type: {type(vi[0])}')
            sys.exit()

    else:
        print(f'Unsupported type: {type(vi)}')
        sys.exit()



###############################################################################
print('\n' + "="*50)
mpc.run(mpc.start())   #### START THE MPC ROUNDS OF COMPUTATION ####
print("="*50,'\n');
###############################################################################


all_sec_vi = mpc.input(sec_vi)

cmd = 'std'

if cmd == 'min':
    sec_minimum = mpc.min(all_sec_vi)
    minimum = mpc.run(mpc.output(sec_minimum))
    print(minimum)

elif cmd == 'max':
    sec_maximum = mpc.max(all_sec_vi)
    maximum = mpc.run(mpc.output(sec_maximum))
    print(maximum)

elif cmd == 'mean':
    sec_sum = mpc.sum(all_sec_vi)
    sec_mean = mpc.div(sec_sum, nb_parties)
    mean = mpc.run(mpc.output(sec_mean))
    print(mean)

elif cmd == 'std':
    sec_sum = mpc.sum(all_sec_vi)
    sec_mean = mpc.div(sec_sum, nb_parties)
    sec_stddev = mpc.pow(mpc.sub(all_sec_vi[0], sec_mean), 2)
    for v in all_sec_vi[1:]:
        sec_stddev = mpc.add(sec_stddev, mpc.pow(mpc.sub(v, sec_mean), 2))
    stddev = np.sqrt( float(mpc.run(mpc.output(sec_stddev))) / float(nb_parties) )
    print(stddev)


###############################################################################
print('\n'+'='*50)
mpc.run(mpc.shutdown())    #### END THE MPC ROUNDS OF COMPUTATION ####
print('='*50)
###############################################################################
