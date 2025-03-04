import sys, time, warnings
from tlpmSCPI import pm16_130

try:
    meter = pm16_130()
except:
    warnings.warn('Failed to connect to PM 16-130')
    sys.exit()

print("Close with keyboard interrupt")
try:
    while True:
        power = meter.measPower()
        sys.stdout.write(f'{power*1000:>10.6f} mW      \r')
        time.sleep(.1)
except:
    print()
    meter.close()
