import re, sys, os, time, warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import savemat
import tlpmSCPI

## these are constants for formatting the print statements on the terminal
PAD_I = 7    # number of spaces for index
PAD_POS = 8  # number of spaces for position
PAD_PWR = 8  # number of spaces for power
# abs is absolute, every position is expected relative to a fixed reference
# delta is difference, every position is the change relative to the previous measurement
MODES = ['abs','delta']
# N_AVG is an averaging constant that is meant to smooth out individual measurements
# TODO implement a rolling average using parallel process
N_AVG = 1
# SAVE_TYPE can be MAT or NPZ for Matlab or numpy compatible save files
SAVE_TYPE = 'MAT'
# ROOT specified the root directory in which to store saved data
ROOT = './data'
if not os.path.exists(ROOT):
    os.mkdir(ROOT)


def get_power(meter_obj):
    global N_AVG
    dt = 1/10 # the data sheet states that the update rate is 10S/s 
    pwr = 0
    pwr += meter_obj.measPower()
    # this for loop will only pause between measurements
    # if N_AVG is 1, it will not pause
    for _ in range(1,N_AVG):
        time.sleep(dt)
        pwr += meter_obj.measPower()
    return pwr/N_AVG

# ensure that the save output is a valid name
def validate_pathname(fname,ext):
    fname = os.path.join(ROOT,fname+'.'+ext)
    return fname

# mode is initialized to 1, 0 for abs, 1 for delta
mode = 1
collecting = True # used in while loop to determine exit condition of REPL
BUF_SIZE = 100
ext = SAVE_TYPE.lower()
if len(sys.argv>1):
    FNAME = validate_pathname(sys.argv[1],ext)
else:
    FNAME = os.path.join(ROOT,'default.'+ext)
    warnings.warn(f'No input name detected, saving output to {FNAME}')
position = [0 for i in range(BUF_SIZE)] # preallocate a list for storing power and position
power = [0 for i in range(BUF_SIZE)]
index = -1
delta_prev = 0
# conversion is a convenience term that makes it easier to enter data when working with 
# a micrometer. The conversion is meant to convert counts of ticks on a micrometer to 
# physical units. This can be set to 1 if you wish to enter positions as raw values 
# instead of counts
conversion = .02
# conversion = .0254 # ticks to mm, used in QuIC B
# conversion = 1


#### Functions that will be linked to commands
# all command functions have an argument which is a string

# change from abs to delta or vice versa, arg can be 'abs'/0 or 'delta'/1
def change_mode(arg):
    try:
        if arg in MODES:
            value = MODES.index(arg)
        else:
            value = float(arg)
            assert value in [0,1]
    except:
        print("Could not interpret \"{:s}\" as mode".format(arg))
        return
    global mode
    mode = int(value)

# called when you are done collecting data
def end_collection(arg):
    global collecting
    collecting = False

# called when you want to see a summary of data that has been collected
def print_state(arg):
    global position, power, index, conversion
    global PAD_I, PAD_POS, PAD_PWR, SAVE_TYPE, N_AVG
    if arg=='conversion':
        print(conversion)
        return
    if arg=='average':
        print(N_AVG)
        return
    if arg=='save_format':
        print(SAVE_TYPE)
        return
    
    fmt = "{:<"+str(PAD_I)+"s} {: >"+str(PAD_POS)+"s} | {: <"+str(PAD_PWR)+"s}"
    print(fmt.format("(Index)","Position","Power"))
    for i in range(index+1):
        print(fmt.format(f'({i})',f'{position[i]:.3f}mm',f'{power[i]*1000:.3f}mW'))

# save the state of the measurements
def save(arg):
    global position, power, index
    position_data = np.array(position[:index+1])
    order = np.argsort(position_data)
    position_data = position_data[order]
    power_data = np.array(power[:index+1])[order]

    _,ext = os.path.splitext(arg)
    data = {'position':position_data,'power':power_data}
    if ext=='.mat':
        savemat(arg,data)
    elif ext == '.npz':
        np.savez(arg,**data)
    else:
        if SAVE_TYPE=='MAT':
            savemat(arg+'.mat',data)
        elif SAVE_TYPE=='NPZ':
            np.savez(arg,**data)

# this can delete either the previous element, or the row specified by arg
def delete(arg):
    global position, power, index
    if arg:
        try:
            value = float(arg)
            assert value>=0
            assert value<(index+1)
        except:
            print("Could not interpret \"{:s}\" as index".format(arg))
            return
        ind = int(value)
        del position[ind]
        del power[ind]
        index -= 1
    else:
        # delete most recent
        if index == -1:
            return
        del position[index]
        del power[index]
        index -= 1

# this is a generic function called when a command is not recognized
def parse_error(arg):
    print('{:s} not recognized as command'.format(arg))

# this allows you to change the conversion between samples
def set_conversion(arg):
    global conversion
    try:
        value = float(arg)
        assert value > 0
    except:
        print("Could not interpret \"{:s}\" as conversion".format(arg))
        return
    conversion = value

# this allows you to change the file type of the save file
def set_savetype(arg):
    global SAVE_TYPE
    if arg in ['MAT','NPZ']:
        SAVE_TYPE = arg
    else:
        print(f'{arg} is not a valid file type')

# this allows you to change the averaging number for each measurement
def set_average(arg):
    global N_AVG
    if isinstance(arg,int):
        if arg>0:
            N_AVG = arg
    else:
        print(f'Expected positive integer, got "{arg}"')

# reset all constants to default
def default(arg):
    global conversion, mode
    conversion = .0254
    mode = 1

# if any data have been entered out of order either using abs mode or with a negative delta value
# this command will sort the stored data
def sort_position(arg):
    global position, power, index
    position[:index+1],power[:index+1] = zip(*sorted(zip(position[:index+1],power[:index+1])))
    
# display a useful help screen with a list of all commands
def help_fn(arg):
    # 'mode':change_mode,'end':end_collection,'delete':delete,'print':print_state,'conversion':set_conversion,'save':save,'default':default,'sort':sort_position,'help':help_fn
    print('mode [%d/%s]    : argument is abs/0 absolute positioning, delta/1 relative to previous step')
    print('end/exit        : stop collection')
    print('delete [%d]     : delete index %d or previous index if no argument')
    print('print [%s]      : print data if no argument or print state of  argument, %s can be "conversion"')
    print('conversion [%f] : set conversion to %f, true delta = delta*conversion, abs = abs*conversion')
    print('save %s         : save to filename specified by %s')
    print('savetype %s     : argument is "MAT" or "NPZ", sets file type of save to .mat or .npz')
    print('average %d      : set number of average for each point, sample rate is 15Hz')
    print('default         : restore default mode and conversion')
    print('sort            : sort data by position column')

# collect a single data point and append it to the global position and power lists
def process_input(cin,meter):
    global position, power, index
    global BUF_SIZE, FNAME, FNAME_MAT, SAVE_TYPE, delta_prev, conversion
    try:
        if not cin:
            if mode == 0:
                # absolute mode
                raise ValueError()
            position_value = delta_prev
            if (index != -1):
                assert position_value > 0
                position_value += position[index]
        else:
            position_value = float(cin)*conversion
            delta_prev = position_value
            if (mode == 1):
                # delta
                if (index != -1):
                    assert position_value > 0
                    position_value += position[index] # add current position to previous
                else:
                    position_value = 0
    except:
        print("Could not interpret \"{:s}\" as position".format(cin))
        return
    power_value = get_power(meter)
    index += 1
    if index>(len(position)-1):
        position += [0 for i in range(BUF_SIZE)]
        power += [0 for i in range(BUF_SIZE)]
    

    position[index] = position_value
    power[index] = power_value
    
    position_data = np.array(position[:index+1])
    power_data = np.array(power[:index+1])
    order = np.argsort(position_data)
    
    mdict = {'position':position_data[order],'power':power_data[order]}
    root,ext = os.path.splitext(FNAME)
    if SAVE_TYPE=='MAT':
        savemat(root+'.mat',mdict)
    elif SAVE_TYPE=='NPZ':
        np.savez(root+'.npz',position=position_data[order],power=power_data[order])

# list of all commands that can be used
# each command is a key with a function as its value
# whenever the input is not a number, this dictionary is queried with get to determine action
CMD = {'mode':change_mode,'end':end_collection,'exit':end_collection,'delete':delete,'print':print_state,'conversion':set_conversion,'save':save,'default':default,'sort':sort_position, 'savetype':set_savetype, 'average':set_average,'help':help_fn}
pat = re.compile('({:s})'.format('|'.join(CMD.keys())))
meter = tlpmSCPI.pm16_130()

while collecting:
    cin = input("({:s}) >> ".format(MODES[mode])) # request input
    if (m:=pat.search(cin)) is not None: # search for command
        handler = CMD.get(cin[slice(*m.span())],parse_error) # determine what to call
        handler(cin[slice(m.end(),None)].strip()) # pass argument to handler function
    else:
        process_input(cin,meter) # if no command, collect 1 datum

### this will be executed once all data has been collected
# do something with results
position_data = np.array(position[:index+1])
order = np.argsort(position_data)
position_data = position_data[order]
power_data = np.array(power[:index+1])[order]

# plot marginalized profile as a quick diagnostic
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(position_data,-np.gradient(power_data,position_data))

ax.set_xlabel('Position')
ax.set_ylabel('Power Gradient')
plt.show()