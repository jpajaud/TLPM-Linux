import os, platform, re, warnings
import pyvisa

# add enum
# need to design a simple gui with plotting and statistics

# VisaIOError: VI_ERROR_CONN_LOST (-1073807194): The connection for the given session has been lost.

# this allows one ot override the serial scanning function
# by default, the code will choose the first address it finds
# if two devices are connected, this environment variable can 
# be set in order to force which device is accessed

SERIAL = os.getenv('SERIAL_TL_PM16_130')

class pm16_130:
    def __init__(self,backend=None,event=None):
        self.idVendor  = '0x'+hex(0x1313)[2:].upper() # only want numbers to be capital
        self.idProduct = '0x'+hex(0x807b)[2:].upper()
        self.serial    = SERIAL
        self.open      = False
        self.event     = event
        if backend not in [None,'@py']:
            raise RuntimeError(f"Backend '{backend}' not recognized")
        self.backend   = backend

        if not self.init_device():
            raise RuntimeError(f"Device not found with address {self.address}")

    def __enter__(self):
        return self
    
    def __exit__(self,exception_type,exception_value,exception_traceback):
        self.close()

    def __str__(self):
        return f"PM16-130 ({'Open' if self.open else 'Closed'})"

    def __repr__(self):
        return str(self)
    
    def query(self,cmd):
        try:
            value = self.device.query(cmd)
            return value
        except pyvisa.VisaIOError:
            self.device.close() # perhaps send signal as well
            if self.event is not None:
                self.event.set()

    def write(self,cmd):
        try:
            self.device.write(cmd)
        except pyvisa.VisaIOError:
            self.device.close() # perhaps send signal as well
            if self.event is not None:
                self.event.set()

    def init_device(self):
        backend_args = (self.backend,) if self.backend is not None else ()
        rm = pyvisa.ResourceManager(*backend_args)
        resources = rm.list_resources()
        # scan through resource list, backend tells format
        # self.serial is None if no environment variable is set
        # setting environment variable will override behavior of scan_address
        self.address = self.scan_address(resources)
        available = self.address in resources # this is needed in case self.serial is set by environment variable

        if not available:
            self.device = None
            self.open = False
        else:
            self.device = rm.open_resource(self.address)
            self.open = True
        return self.open
    
    def scan_address(self,resources):

        replace_pattern = r'\(\\d\+\)'
        search_pattern = r'(\d+)'
        if self.backend is None:
            template = f'USB0::{self.idVendor}::{self.idProduct}::{search_pattern}::INSTR'
        elif self.backend == '@py':
            template = f'USB0::{int(self.idVendor,16)}::{int(self.idProduct,16)}::{search_pattern}::0::INSTR'
        
        if self.serial is not None:
            return re.sub(replace_pattern,self.serial,template)
        
        pattern = re.compile(template)
        for resource in resources:
            matches = pattern.findall(resource)
            if len(matches)==1:
                self.serial = int(matches[0])
                return re.sub(replace_pattern,str(self.serial),template)
                
        if self.serial is None:
            raise RuntimeError('Serial pattern not found')

    def close(self):
        if self.open:
            self.device.close()
            self.open = False

    def getWavelength(self):
        if self.open:
            value = self.query("SENS:CORR:WAV?")
            return float(value)
        else:
            return None

    def setWavelength(self,wavelength):
        if self.open:
            assert (wavelength<=1100) and (wavelength>=400), f"Wavelength of {wavelength:f}nm is out of range"
            self.write(f"SENS:CORR:WAV {wavelength:.6f}")

    def getPhotodiodeResponsivity(self):
        if self.open:
            value = self.device.query("SENS:CORR:POW:PDI:RESP?")
            return float(value)
        else:
            return None
        
    def getPowerAutoRange(self):
        if self.open:
            value = self.device.query("SENS:POW:RANGE:AUTO?")
            return int(value)
        else:
            return None

    def setPowerAutoRange(self,value):
        if self.open:
            assert value in [0,1], "Invalid value for Autorange"
            self.device.write(f"SENS:POW:RANG:AUTO {value:d}")
    
    def getPowerRange(self):
        if self.open:
            value = self.device.query("SENS:POW:RANG?")
            return float(value)
        else:
            return None

    def setPowerRange(self,value):
        if self.open:
            assert (value<.5) and (value>5e-9), "Power value is out of range"
            self.device.query(f"SENS:POW:RANG {value}")

    def getPowerRef(self):
        if self.open:
            value = self.device.query("SENS:POW:REF?")
            return float(value)
        else:
            return None

    def getPowerUnit(self):
        if self.open:
            value = self.device.query("SENS:POW:UNIT?")
            return int(value)
        else:
            return None

    def measPower(self):
        if self.open:
            value = self.device.query("MEAS:SCAL:POW?")
            return float(value)
        else:
            return None

    def reset(self):
        if self.open:
            value = self.device.query("*RST")
            # return self.device.query("SYST:ERR?")

    def selfTest(self):
        if self.open:
            value = self.device.query("*TST?")
            # return is an integer with different error numbers
            # error numbers are not listed in any manuals (might be able to extract from TLPM.dll)
            return int(value)
        else:
            return None

    def checkError(self):
        if self.open:
            value = self.device.query("SYST:ERR?")
            return value
        else:
            return None

    def getCalibrationMsg(self):
        if self.open:
            value = self.device.query("CAL:STR?")
            return value
        else:
            return None
