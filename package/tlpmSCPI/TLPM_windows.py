# Code provided by ThorLabs with OPM software
# Assumes installation in default location with C:/Program Files/IVI Foundation/VISA/Win64/Bin/ with TLPM_xx.dll
# This is only needed to interface on Windows platforms

import os
from ctypes import cdll,c_long,c_uint32,c_uint16,c_uint8,byref,create_string_buffer,c_bool, c_char, c_char_p,c_int,c_int16,c_int8,c_double,c_float,sizeof,c_voidp, Structure

_VI_ERROR = (-2147483647-1)
VI_ON = 1
VI_OFF = 0
TLPM_VID_THORLABS = (0x1313)  # Thorlabs
TLPM_PID_TLPM_DFU = (0x8070)  # PM100D with DFU interface enabled
TLPM_PID_PM100A_DFU = (0x8071)  # PM100A with DFU interface enabled
TLPM_PID_PM100USB = (0x8072)  # PM100USB with DFU interface enabled
TLPM_PID_PM160USB_DFU = (0x8073)  # PM160 on USB with DFU interface enabled
TLPM_PID_PM160TUSB_DFU = (0x8074)  # PM160T on USB with DFU interface enabled
TLPM_PID_PM400_DFU = (0x8075)  # PM400 on USB with DFU interface enabled
TLPM_PID_PM101_DFU = (0x8076)  # PM101 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM102_DFU = (0x8077)  # PM102 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM103_DFU = (0x807A)  # PM103 on USB with DFU interface enabled (Interface 0 TMC, Interface 1 DFU)
TLPM_PID_PM100D = (0x8078)  # PM100D w/o DFU interface
TLPM_PID_PM100A = (0x8079)  # PM100A w/o DFU interface
TLPM_PID_PM160USB = (0x807B)  # PM160 on USB w/o DFU interface
TLPM_PID_PM160TUSB = (0x807C)  # PM160T on USB w/o DFU interface
TLPM_PID_PM400 = (0x807D)  # PM400 on USB w/o DFU interface
TLPM_PID_PM101 = (0x807E)  # reserved
TLPM_PID_PMTest = (0x807F)  # PM Test Platform
TLPM_PID_PM200 = (0x80B0)  # PM200
TLPM_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8070 || VI_ATTR_MODEL_CODE==0x8078)}"
PM100A_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8071 || VI_ATTR_MODEL_CODE==0x8079)}"
PM100USB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x8072}"
PM160USB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8073 || VI_ATTR_MODEL_CODE==0x807B)}"
PM160TUSB_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8074 || VI_ATTR_MODEL_CODE==0x807C)}"
PM200_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x80B0}"
PM400_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8075 || VI_ATTR_MODEL_CODE==0x807D)}"
PM101_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8076)}"
PM102_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8077)}"
PM103_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x807A}"
PMTest_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && VI_ATTR_MODEL_CODE==0x807F}"
PM100_FIND_PATTERN = "USB?*::0x1313::0x807?::?*::INSTR"
PMxxx_FIND_PATTERN = "USB?*INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x8070 || VI_ATTR_MODEL_CODE==0x8078 || " \
"VI_ATTR_MODEL_CODE==0x8071 || VI_ATTR_MODEL_CODE==0x8079 || " \
"VI_ATTR_MODEL_CODE==0x8072 || " \
"VI_ATTR_MODEL_CODE==0x8073 || VI_ATTR_MODEL_CODE==0x807B || " \
"VI_ATTR_MODEL_CODE==0x8074 || VI_ATTR_MODEL_CODE==0x807C || " \
"VI_ATTR_MODEL_CODE==0x8075 || VI_ATTR_MODEL_CODE==0x807D || " \
"VI_ATTR_MODEL_CODE==0x8076 || VI_ATTR_MODEL_CODE==0x807E || " \
"VI_ATTR_MODEL_CODE==0x8077 || VI_ATTR_MODEL_CODE==0x807F || " \
"VI_ATTR_MODEL_CODE==0x807A || " \
"VI_ATTR_MODEL_CODE==0x80B0)}"
PMBT_FIND_PATTERN = "ASRL?*::INSTR{VI_ATTR_MANF_ID==0x1313 && (VI_ATTR_MODEL_CODE==0x807C || VI_ATTR_MODEL_CODE==0x807B)}"
PMUART_FIND_PATTERN_VISA = "ASRL?*::INSTR"
PMUART_FIND_PATTERN_COM = "COM?*"
TLPM_BUFFER_SIZE = 256  # General buffer size
TLPM_ERR_DESCR_BUFFER_SIZE = 512  # Buffer size for error messages
VI_INSTR_WARNING_OFFSET = (0x3FFC0900 )
VI_INSTR_ERROR_OFFSET = (_VI_ERROR + 0x3FFC0900 )
VI_INSTR_ERROR_NOT_SUPP_INTF = (VI_INSTR_ERROR_OFFSET + 0x01 )
VI_INSTR_WARN_OVERFLOW = (VI_INSTR_WARNING_OFFSET + 0x01 )
VI_INSTR_WARN_UNDERRUN = (VI_INSTR_WARNING_OFFSET + 0x02 )
VI_INSTR_WARN_NAN = (VI_INSTR_WARNING_OFFSET + 0x03 )
TLPM_ATTR_SET_VAL = (0)
TLPM_ATTR_MIN_VAL = (1)
TLPM_ATTR_MAX_VAL = (2)
TLPM_ATTR_DFLT_VAL = (3)
TLPM_ATTR_AUTO_VAL = (9)
TLPM_INDEX_1 = (1)
TLPM_INDEX_2 = (2)
TLPM_INDEX_3 = (3)
TLPM_INDEX_4 = (4)
TLPM_INDEX_5 = (5)
TLPM_PEAK_FILTER_NONE = (0)
TLPM_PEAK_FILTER_OVER = (1)
TLPM_REG_STB = (0)  # < Status Byte Register
TLPM_REG_SRE = (1)  # < Service Request Enable
TLPM_REG_ESB = (2)  # < Standard Event Status Register
TLPM_REG_ESE = (3)  # < Standard Event Enable
TLPM_REG_OPER_COND = (4)  # < Operation Condition Register
TLPM_REG_OPER_EVENT = (5)  # < Operation Event Register
TLPM_REG_OPER_ENAB = (6)  # < Operation Event Enable Register
TLPM_REG_OPER_PTR = (7)  # < Operation Positive Transition Filter
TLPM_REG_OPER_NTR = (8)  # < Operation Negative Transition Filter
TLPM_REG_QUES_COND = (9)  # < Questionable Condition Register
TLPM_REG_QUES_EVENT = (10)  # < Questionable Event Register
TLPM_REG_QUES_ENAB = (11)  # < Questionable Event Enable Reg.
TLPM_REG_QUES_PTR = (12)  # < Questionable Positive Transition Filter
TLPM_REG_QUES_NTR = (13)  # < Questionable Negative Transition Filter
TLPM_REG_MEAS_COND = (14)  # < Measurement Condition Register
TLPM_REG_MEAS_EVENT = (15)  # < Measurement Event Register
TLPM_REG_MEAS_ENAB = (16)  # < Measurement Event Enable Register
TLPM_REG_MEAS_PTR = (17)  # < Measurement Positive Transition Filter
TLPM_REG_MEAS_NTR = (18)  # < Measurement Negative Transition Filter
TLPM_REG_AUX_COND = (19)  # < Auxiliary Condition Register
TLPM_REG_AUX_EVENT = (20)  # < Auxiliary Event Register
TLPM_REG_AUX_ENAB = (21)  # < Auxiliary Event Enable Register
TLPM_REG_AUX_PTR = (22)  # < Auxiliary Positive Transition Filter
TLPM_REG_AUX_NTR = (23)  # < Auxiliary Negative Transition Filter
TLPM_STATBIT_STB_AUX = (0x01)  # < Auxiliary summary
TLPM_STATBIT_STB_MEAS = (0x02)  # < Device Measurement Summary
TLPM_STATBIT_STB_EAV = (0x04)  # < Error available
TLPM_STATBIT_STB_QUES = (0x08)  # < Questionable Status Summary
TLPM_STATBIT_STB_MAV = (0x10)  # < Message available
TLPM_STATBIT_STB_ESB = (0x20)  # < Event Status Bit
TLPM_STATBIT_STB_MSS = (0x40)  # < Master summary status
TLPM_STATBIT_STB_OPER = (0x80)  # < Operation Status Summary
TLPM_STATBIT_ESR_OPC = (0x01)  # < Operation complete
TLPM_STATBIT_ESR_RQC = (0x02)  # < Request control
TLPM_STATBIT_ESR_QYE = (0x04)  # < Query error
TLPM_STATBIT_ESR_DDE = (0x08)  # < Device-Specific error
TLPM_STATBIT_ESR_EXE = (0x10)  # < Execution error
TLPM_STATBIT_ESR_CME = (0x20)  # < Command error
TLPM_STATBIT_ESR_URQ = (0x40)  # < User request
TLPM_STATBIT_ESR_PON = (0x80)  # < Power on
TLPM_STATBIT_QUES_VOLT = (0x0001)  # < questionable voltage measurement
TLPM_STATBIT_QUES_CURR = (0x0002)  # < questionable current measurement
TLPM_STATBIT_QUES_TIME = (0x0004)  # < questionable time measurement
TLPM_STATBIT_QUES_POW = (0x0008)  # < questionable power measurement
TLPM_STATBIT_QUES_TEMP = (0x0010)  # < questionable temperature measurement
TLPM_STATBIT_QUES_FREQ = (0x0020)  # < questionable frequency measurement
TLPM_STATBIT_QUES_PHAS = (0x0040)  # < questionable phase measurement
TLPM_STATBIT_QUES_MOD = (0x0080)  # < questionable modulation measurement
TLPM_STATBIT_QUES_CAL = (0x0100)  # < questionable calibration
TLPM_STATBIT_QUES_ENER = (0x0200)  # < questionable energy measurement
TLPM_STATBIT_QUES_10 = (0x0400)  # < reserved
TLPM_STATBIT_QUES_11 = (0x0800)  # < reserved
TLPM_STATBIT_QUES_12 = (0x1000)  # < reserved
TLPM_STATBIT_QUES_INST = (0x2000)  # < instrument summary
TLPM_STATBIT_QUES_WARN = (0x4000)  # < command warning
TLPM_STATBIT_QUES_15 = (0x8000)  # < reserved
TLPM_STATBIT_OPER_CAL = (0x0001)  # < The instrument is currently performing a calibration.
TLPM_STATBIT_OPER_SETT = (0x0002)  # < The instrument is waiting for signals it controls to stabilize enough to begin measurements.
TLPM_STATBIT_OPER_RANG = (0x0004)  # < The instrument is currently changing its range.
TLPM_STATBIT_OPER_SWE = (0x0008)  # < A sweep is in progress.
TLPM_STATBIT_OPER_MEAS = (0x0010)  # < The instrument is actively measuring.
TLPM_STATBIT_OPER_TRIG = (0x0020)  # < The instrument is in a �wait for trigger� state of the trigger model.
TLPM_STATBIT_OPER_ARM = (0x0040)  # < The instrument is in a �wait for arm� state of the trigger model.
TLPM_STATBIT_OPER_CORR = (0x0080)  # < The instrument is currently performing a correction (Auto-PID tune).
TLPM_STATBIT_OPER_SENS = (0x0100)  # < Optical powermeter sensor connected and operable.
TLPM_STATBIT_OPER_DATA = (0x0200)  # < Measurement data ready for fetch.
TLPM_STATBIT_OPER_THAC = (0x0400)  # < Thermopile accelerator active.
TLPM_STATBIT_OPER_11 = (0x0800)  # < reserved
TLPM_STATBIT_OPER_12 = (0x1000)  # < reserved
TLPM_STATBIT_OPER_INST = (0x2000)  # < One of n multiple logical instruments is reporting OPERational status.
TLPM_STATBIT_OPER_PROG = (0x4000)  # < A user-defined programming is currently in the run state.
TLPM_STATBIT_OPER_15 = (0x8000)  # < reserved
TLPM_STATBIT_MEAS_0 = (0x0001)  # < reserved
TLPM_STATBIT_MEAS_1 = (0x0002)  # < reserved
TLPM_STATBIT_MEAS_2 = (0x0004)  # < reserved
TLPM_STATBIT_MEAS_3 = (0x0008)  # < reserved
TLPM_STATBIT_MEAS_4 = (0x0010)  # < reserved
TLPM_STATBIT_MEAS_5 = (0x0020)  # < reserved
TLPM_STATBIT_MEAS_6 = (0x0040)  # < reserved
TLPM_STATBIT_MEAS_7 = (0x0080)  # < reserved
TLPM_STATBIT_MEAS_8 = (0x0100)  # < reserved
TLPM_STATBIT_MEAS_9 = (0x0200)  # < reserved
TLPM_STATBIT_MEAS_10 = (0x0400)  # < reserved
TLPM_STATBIT_MEAS_11 = (0x0800)  # < reserved
TLPM_STATBIT_MEAS_12 = (0x1000)  # < reserved
TLPM_STATBIT_MEAS_13 = (0x2000)  # < reserved
TLPM_STATBIT_MEAS_14 = (0x4000)  # < reserved
TLPM_STATBIT_MEAS_15 = (0x8000)  # < reserved
TLPM_STATBIT_AUX_NTC = (0x0001)  # < Auxiliary NTC temperature sensor connected.
TLPM_STATBIT_AUX_EMM = (0x0002)  # < External measurement module connected.
TLPM_STATBIT_AUX_UPCS = (0x0004)  # < User Power Calibration supported by this instrument
TLPM_STATBIT_AUX_UPCA = (0x0008)  # < User Power Calibration active status
TLPM_STATBIT_AUX_EXPS = (0x0010)  # < External power supply connected
TLPM_STATBIT_AUX_BATC = (0x0020)  # < Battery charging
TLPM_STATBIT_AUX_BATL = (0x0040)  # < Battery low
TLPM_STATBIT_AUX_IPS = (0x0080)  # < Apple(tm) authentification supported. True if an authentification co-processor is installed.
TLPM_STATBIT_AUX_IPF = (0x0100)  # < Apple(tm) authentification failed. True if the authentification setup procedure failed.
TLPM_STATBIT_AUX_9 = (0x0200)  # < reserved
TLPM_STATBIT_AUX_10 = (0x0400)  # < reserved
TLPM_STATBIT_AUX_11 = (0x0800)  # < reserved
TLPM_STATBIT_AUX_12 = (0x1000)  # < reserved
TLPM_STATBIT_AUX_13 = (0x2000)  # < reserved
TLPM_STATBIT_AUX_14 = (0x4000)  # < reserved
TLPM_STATBIT_AUX_15 = (0x8000)  # < reserved
TLPM_LINE_FREQ_50 = (50)  # < line frequency in Hz
TLPM_LINE_FREQ_60 = (60)  # < line frequency in Hz
TLPM_INPUT_FILTER_STATE_OFF = (0)
TLPM_INPUT_FILTER_STATE_ON = (1)
TLPM_ACCELERATION_STATE_OFF = (0)
TLPM_ACCELERATION_STATE_ON = (1)
TLPM_ACCELERATION_MANUAL = (0)
TLPM_ACCELERATION_AUTO = (1)
TLPM_STAT_DARK_ADJUST_FINISHED = (0)
TLPM_STAT_DARK_ADJUST_RUNNING = (1)
TLPM_AUTORANGE_CURRENT_OFF = (0)
TLPM_AUTORANGE_CURRENT_ON = (1)
TLPM_CURRENT_REF_OFF = (0)
TLPM_CURRENT_REF_ON = (1)
TLPM_ENERGY_REF_OFF = (0)
TLPM_ENERGY_REF_ON = (1)
TLPM_FREQ_MODE_CW = (0)
TLPM_FREQ_MODE_PEAK = (1)
TLPM_AUTORANGE_POWER_OFF = (0)
TLPM_AUTORANGE_POWER_ON = (1)
TLPM_POWER_REF_OFF = (0)
TLPM_POWER_REF_ON = (1)
TLPM_POWER_UNIT_WATT = (0)
TLPM_POWER_UNIT_DBM = (1)
SENSOR_SWITCH_POS_1 = (1)
SENSOR_SWITCH_POS_2 = (2)
TLPM_AUTORANGE_VOLTAGE_OFF = (0)
TLPM_AUTORANGE_VOLTAGE_ON = (1)
TLPM_VOLTAGE_REF_OFF = (0)
TLPM_VOLTAGE_REF_ON = (1)
TLPM_IODIR_INP = (VI_OFF)
TLPM_IODIR_OUTP = (VI_ON)
TLPM_IOLVL_LOW = (VI_OFF)
TLPM_IOLVL_HIGH = (VI_ON)
DIGITAL_IO_CONFIG_INPUT = (0)
DIGITAL_IO_CONFIG_OUTPUT = (1)
DIGITAL_IO_CONFIG_INPUT_ALT = (2)
DIGITAL_IO_CONFIG_OUTPUT_ALT = (3)
SENSOR_TYPE_NONE = 0x0  # No sensor. This value is used to mark sensor data for 'no sensor connected'.
SENSOR_TYPE_PD_SINGLE = 0x1  # Single photodiode sensor. Only one ipd input active at the same time.
SENSOR_TYPE_THERMO = 0x2  # Thermopile sensor
SENSOR_TYPE_PYRO = 0x3  # Pyroelectric sensor
SENSOR_TYPE_4Q = 0x4  # 4Q Sensor
SENSOR_SUBTYPE_NONE = 0x0  # No sensor. This value is used to mark RAM data structure for 'no sensor connected'. Do not write this value to the EEPROM.
SENSOR_SUBTYPE_PD_ADAPTER = 0x01  # Photodiode adapter (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_STD = 0x02  # Standard single photodiode sensor (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_FSR = 0x03  # One single photodiode. Filter position set by a slide on the sensor selects responsivity data set to use. (no temperature sensor)
SENSOR_SUBTYPE_PD_SINGLE_STD_T = 0x12  # Standard single photodiode sensor (with temperature sensor)
SENSOR_SUBTYPE_THERMO_ADAPTER = 0x01  # Thermopile adapter (no temperature sensor)
SENSOR_SUBTYPE_THERMO_STD = 0x02  # Standard thermopile sensor (no temperature sensor)
SENSOR_SUBTYPE_THERMO_STD_T = 0x12  # Standard thermopile sensor (with temperature sensor)
SENSOR_SUBTYPE_PYRO_ADAPTER = 0x01  # Pyroelectric adapter (no temperature sensor)
SENSOR_SUBTYPE_PYRO_STD = 0x02  # Standard pyroelectric sensor (no temperature sensor)
SENSOR_SUBTYPE_PYRO_STD_T = 0x12  # Standard pyroelectric sensor (with temperature sensor)
TLPM_SENS_FLAG_IS_POWER = 0x0001  # Power sensor
TLPM_SENS_FLAG_IS_ENERGY = 0x0002  # Energy sensor
TLPM_SENS_FLAG_IS_RESP_SET = 0x0010  # Responsivity settable
TLPM_SENS_FLAG_IS_WAVEL_SET = 0x0020  # Wavelength settable
TLPM_SENS_FLAG_IS_TAU_SET = 0x0040  # Time constant tau settable
TLPM_SENS_FLAG_HAS_TEMP = 0x0100  # Temperature sensor included

class TLPM:

	def __init__(self):
		if sizeof(c_voidp) == 4:
			fname = "C:/Program Files/IVI Foundation/VISA/Win64/Bin/TLPM_32.dll"
		else:
			fname = "C:/Program Files/IVI Foundation/VISA/Win64/Bin/TLPM_64.dll"
		if not os.path.exists(fname):
			raise RuntimeError(f'Thorlabs TLPM software not found at {fname}')
		self.dll = cdll.LoadLibrary(fname)
		self.devSession = c_long()
		self.devSession.value = 0

	def __testForError(self, status):
		if status < 0:
			self.__throwError(status)
		return status

	def __throwError(self, code):
		msg = create_string_buffer(1024)
		self.dll.TLPM_errorMessage(self.devSession, c_int(code), msg)
		raise NameError(c_char_p(msg.raw).value)

	def open(self, resourceName, IDQuery, resetDevice):
		"""
		This function initializes the instrument driver session and performs the following initialization actions:
		
		(1) Opens a session to the Default Resource Manager resource and a session to the specified device using the Resource Name.
		(2) Performs an identification query on the instrument.
		(3) Resets the instrument to a known state.
		(4) Sends initialization commands to the instrument.
		(5) Returns an instrument handle which is used to distinguish between different sessions of this instrument driver.
		
		Notes:
		(1) Each time this function is invoked a unique session is opened.  
		
		Args:
			resourceName (create_string_buffer)
			IDQuery (c_bool):This parameter specifies whether an identification query is performed during the initialization process.
			
			VI_OFF (0): Skip query.
			VI_ON  (1): Do query (default).
			
			resetDevice (c_bool):This parameter specifies whether the instrument is reset during the initialization process.
			
			VI_OFF (0) - no reset 
			VI_ON  (1) - instrument is reset (default)
			
		Returns:
			int: The return value, 0 is for success
		"""
		self.dll.TLPM_close(self.devSession)
		self.devSession.value = 0
		pInvokeResult = self.dll.TLPM_init(resourceName, IDQuery, resetDevice, byref(self.devSession))
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def close(self):
		"""
		This function closes the instrument driver session.
		
		Note: The instrument must be reinitialized to use it again.
		
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_close(self.devSession)
		return pInvokeResult

	def findRsrc(self, resourceCount):
		"""
		This function finds all driver compatible devices attached to the PC and returns the number of found devices.
		
		Note:
		(1) The function additionally stores information like system name about the found resources internally. This information can be retrieved with further functions from the class, e.g. <Get Resource Description> and <Get Resource Information>.
		
		
		Args:
			resourceCount(c_uint32 use with byref) : The number of connected devices that are supported by this driver.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_findRsrc(self.devSession, resourceCount)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getRsrcName(self, index, resourceName):
		"""
		This function gets the resource name string needed to open a device with <Initialize>.
		
		Notes:
		(1) The data provided by this function was updated at the last call of <Find Resources>.
		
		Args:
			index(c_uint32) : This parameter accepts the index of the device to get the resource descriptor from.
			
			Notes: 
			(1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
			
			resourceName(create_string_buffer(1024)) : This parameter returns the resource descriptor. Use this descriptor to specify the device in <Initialize>.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getRsrcName(self.devSession, index, resourceName)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getRsrcInfo(self, index, modelName, serialNumber, manufacturer, deviceAvailable):
		"""
		This function gets information about a connected resource.
		
		Notes:
		(1) The data provided by this function was updated at the last call of <Find Resources>.
		
		Args:
			index(c_uint32) : This parameter accepts the index of the device to get the resource descriptor from.
			
			Notes: 
			(1) The index is zero based. The maximum index to be used here is one less than the number of devices found by the last call of <Find Resources>.
			
			modelName(create_string_buffer(1024)) : This parameter returns the model name of the device.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) Serial interfaces over Bluetooth will return the interface name instead of the device model name.
			serialNumber(create_string_buffer(1024)) : This parameter returns the serial number of the device.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) The serial number is not available for serial interfaces over Bluetooth.
			manufacturer(create_string_buffer(1024)) : This parameter returns the manufacturer name of the device.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this parameter.
			(3) The manufacturer name is not available for serial interfaces over Bluetooth.
			deviceAvailable(c_int16 use with byref) : Returns the information if the device is available.
			Devices that are not available are used by other applications.
			
			Notes:
			(1) You may pass VI_NULL if you do not need this parameter.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getRsrcInfo(self.devSession, index, modelName, serialNumber, manufacturer, deviceAvailable)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def writeRegister(self, reg, value):
		"""
		This function writes the content of any writable instrument register. Refer to your instrument's user's manual for more details on status structure registers.
		
		
		Args:
			reg(c_int16) : Specifies the register to be used for operation. This parameter can be any of the following constants:
			
			  TLPM_REG_SRE         (1): Service Request Enable
			  TLPM_REG_ESE         (3): Standard Event Enable
			  TLPM_REG_OPER_ENAB   (6): Operation Event Enable Register
			  TLPM_REG_OPER_PTR    (7): Operation Positive Transition
			  TLPM_REG_OPER_NTR    (8): Operation Negative Transition
			  TLPM_REG_QUES_ENAB  (11): Questionable Event Enable Reg.
			  TLPM_REG_QUES_PTR   (12): Questionable Positive Transition
			  TLPM_REG_QUES_NTR   (13): Questionable Negative Transition
			  TLPM_REG_MEAS_ENAB  (16): Measurement Event Enable Register
			  TLPM_REG_MEAS_PTR   (17): Measurement Positive Transition
			  TLPM_REG_MEAS_NTR   (18): Measurement Negative Transition
			  TLPM_REG_AUX_ENAB   (21): Auxiliary Event Enable Register
			  TLPM_REG_AUX_PTR    (22): Auxiliary Positive Transition
			  TLPM_REG_AUX_NTR    (23): Auxiliary Negative Transition 
			
			value(c_int16) : This parameter specifies the new value of the selected register.
			
			These register bits are defined:
			
			STATUS BYTE bits (see IEEE488.2-1992 §11.2)
			TLPM_STATBIT_STB_AUX        (0x01): Auxiliary summary
			TLPM_STATBIT_STB_MEAS       (0x02): Device Measurement Summary
			TLPM_STATBIT_STB_EAV        (0x04): Error available
			TLPM_STATBIT_STB_QUES       (0x08): Questionable Status Summary
			TLPM_STATBIT_STB_MAV        (0x10): Message available
			TLPM_STATBIT_STB_ESB        (0x20): Event Status Bit
			TLPM_STATBIT_STB_MSS        (0x40): Master summary status
			TLPM_STATBIT_STB_OPER       (0x80): Operation Status Summary
			
			STANDARD EVENT STATUS REGISTER bits (see IEEE488.2-1992 §11.5.1)
			TLPM_STATBIT_ESR_OPC        (0x01): Operation complete
			TLPM_STATBIT_ESR_RQC        (0x02): Request control
			TLPM_STATBIT_ESR_QYE        (0x04): Query error
			TLPM_STATBIT_ESR_DDE        (0x08): Device-Specific error
			TLPM_STATBIT_ESR_EXE        (0x10): Execution error
			TLPM_STATBIT_ESR_CME        (0x20): Command error
			TLPM_STATBIT_ESR_URQ        (0x40): User request
			TLPM_STATBIT_ESR_PON        (0x80): Power on
			
			QUESTIONABLE STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_QUES_VOLT      (0x0001): Questionable voltage measurement
			TLPM_STATBIT_QUES_CURR      (0x0002): Questionable current measurement
			TLPM_STATBIT_QUES_TIME      (0x0004): Questionable time measurement
			TLPM_STATBIT_QUES_POW       (0x0008): Questionable power measurement
			TLPM_STATBIT_QUES_TEMP      (0x0010): Questionable temperature measurement
			TLPM_STATBIT_QUES_FREQ      (0x0020): Questionable frequency measurement
			TLPM_STATBIT_QUES_PHAS      (0x0040): Questionable phase measurement
			TLPM_STATBIT_QUES_MOD       (0x0080): Questionable modulation measurement
			TLPM_STATBIT_QUES_CAL       (0x0100): Questionable calibration
			TLPM_STATBIT_QUES_ENER      (0x0200): Questionable energy measurement
			TLPM_STATBIT_QUES_10        (0x0400): Reserved
			TLPM_STATBIT_QUES_11        (0x0800): Reserved
			TLPM_STATBIT_QUES_12        (0x1000): Reserved
			TLPM_STATBIT_QUES_INST      (0x2000): Instrument summary
			TLPM_STATBIT_QUES_WARN      (0x4000): Command warning
			TLPM_STATBIT_QUES_15        (0x8000): Reserved
			
			OPERATION STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_OPER_CAL       (0x0001): The instrument is currently performing a calibration.
			TLPM_STATBIT_OPER_SETT      (0x0002): The instrument is waiting for signals to stabilize for measurements.
			TLPM_STATBIT_OPER_RANG      (0x0004): The instrument is currently changing its range.
			TLPM_STATBIT_OPER_SWE       (0x0008): A sweep is in progress.
			TLPM_STATBIT_OPER_MEAS      (0x0010): The instrument is actively measuring.
			TLPM_STATBIT_OPER_TRIG      (0x0020): The instrument is in a “wait for trigger” state of the trigger model.
			TLPM_STATBIT_OPER_ARM       (0x0040): The instrument is in a “wait for arm” state of the trigger model.
			TLPM_STATBIT_OPER_CORR      (0x0080): The instrument is currently performing a correction (Auto-PID tune).
			TLPM_STATBIT_OPER_SENS      (0x0100): Optical powermeter sensor connected and operable.
			TLPM_STATBIT_OPER_DATA      (0x0200): Measurement data ready for fetch.
			TLPM_STATBIT_OPER_THAC      (0x0400): Thermopile accelerator active.
			TLPM_STATBIT_OPER_11        (0x0800): Reserved
			TLPM_STATBIT_OPER_12        (0x1000): Reserved
			TLPM_STATBIT_OPER_INST      (0x2000): One of n multiple logical instruments is reporting OPERational status.
			TLPM_STATBIT_OPER_PROG      (0x4000): A user-defined programming is currently in the run state.
			TLPM_STATBIT_OPER_15        (0x8000): Reserved
			
			Thorlabs defined MEASRUEMENT STATUS REGISTER bits
			TLPM_STATBIT_MEAS_0         (0x0001): Reserved
			TLPM_STATBIT_MEAS_1         (0x0002): Reserved
			TLPM_STATBIT_MEAS_2         (0x0004): Reserved
			TLPM_STATBIT_MEAS_3         (0x0008): Reserved
			TLPM_STATBIT_MEAS_4         (0x0010): Reserved
			TLPM_STATBIT_MEAS_5         (0x0020): Reserved
			TLPM_STATBIT_MEAS_6         (0x0040): Reserved
			TLPM_STATBIT_MEAS_7         (0x0080): Reserved
			TLPM_STATBIT_MEAS_8         (0x0100): Reserved
			TLPM_STATBIT_MEAS_9         (0x0200): Reserved
			TLPM_STATBIT_MEAS_10        (0x0400): Reserved
			TLPM_STATBIT_MEAS_11        (0x0800): Reserved
			TLPM_STATBIT_MEAS_12        (0x1000): Reserved
			TLPM_STATBIT_MEAS_13        (0x2000): Reserved
			TLPM_STATBIT_MEAS_14        (0x4000): Reserved
			TLPM_STATBIT_MEAS_15        (0x8000): Reserved
			
			Thorlabs defined Auxiliary STATUS REGISTER bits
			TLPM_STATBIT_AUX_NTC        (0x0001): Auxiliary NTC temperature sensor connected.
			TLPM_STATBIT_AUX_EMM        (0x0002): External measurement module connected.
			TLPM_STATBIT_AUX_2          (0x0004): Reserved
			TLPM_STATBIT_AUX_3          (0x0008): Reserved
			TLPM_STATBIT_AUX_EXPS       (0x0010): External power supply connected
			TLPM_STATBIT_AUX_BATC       (0x0020): Battery charging
			TLPM_STATBIT_AUX_BATL       (0x0040): Battery low
			TLPM_STATBIT_AUX_IPS        (0x0080): Apple(tm) authentification supported.
			TLPM_STATBIT_AUX_IPF        (0x0100): Apple(tm) authentification failed.
			TLPM_STATBIT_AUX_9          (0x0200): Reserved
			TLPM_STATBIT_AUX_10         (0x0400): Reserved
			TLPM_STATBIT_AUX_11         (0x0800): Reserved
			TLPM_STATBIT_AUX_12         (0x1000): Reserved
			TLPM_STATBIT_AUX_13         (0x2000): Reserved
			TLPM_STATBIT_AUX_14         (0x4000): Reserved
			TLPM_STATBIT_AUX_15         (0x8000): Reserved
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_writeRegister(self.devSession, reg, value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def readRegister(self, reg, value):
		"""
		This function reads the content of any readable instrument register. Refer to your instrument's user's manual for more details on status structure registers.
		
		
		Args:
			reg(c_int16) : Specifies the register to be used for operation. This parameter can be any of the following constants:
			
			  TLPM_REG_STB         (0): Status Byte Register
			  TLPM_REG_SRE         (1): Service Request Enable
			  TLPM_REG_ESB         (2): Standard Event Status Register
			  TLPM_REG_ESE         (3): Standard Event Enable
			  TLPM_REG_OPER_COND   (4): Operation Condition Register
			  TLPM_REG_OPER_EVENT  (5): Operation Event Register
			  TLPM_REG_OPER_ENAB   (6): Operation Event Enable Register
			  TLPM_REG_OPER_PTR    (7): Operation Positive Transition
			  TLPM_REG_OPER_NTR    (8): Operation Negative Transition
			  TLPM_REG_QUES_COND   (9): Questionable Condition Register
			  TLPM_REG_QUES_EVENT (10): Questionable Event Register
			  TLPM_REG_QUES_ENAB  (11): Questionable Event Enable Reg.
			  TLPM_REG_QUES_PTR   (12): Questionable Positive Transition
			  TLPM_REG_QUES_NTR   (13): Questionable Negative Transition
			  TLPM_REG_MEAS_COND  (14): Measurement Condition Register
			  TLPM_REG_MEAS_EVENT (15): Measurement Event Register
			  TLPM_REG_MEAS_ENAB  (16): Measurement Event Enable Register
			  TLPM_REG_MEAS_PTR   (17): Measurement Positive Transition
			  TLPM_REG_MEAS_NTR   (18): Measurement Negative Transition
			  TLPM_REG_AUX_COND   (19): Auxiliary Condition Register
			  TLPM_REG_AUX_EVENT  (20): Auxiliary Event Register
			  TLPM_REG_AUX_ENAB   (21): Auxiliary Event Enable Register
			  TLPM_REG_AUX_PTR    (22): Auxiliary Positive Transition
			  TLPM_REG_AUX_NTR    (23): Auxiliary Negative Transition 
			
			value(c_int16 use with byref) : This parameter returns the value of the selected register.
			
			These register bits are defined:
			
			STATUS BYTE bits (see IEEE488.2-1992 §11.2)
			TLPM_STATBIT_STB_AUX        (0x01): Auxiliary summary
			TLPM_STATBIT_STB_MEAS       (0x02): Device Measurement Summary
			TLPM_STATBIT_STB_EAV        (0x04): Error available
			TLPM_STATBIT_STB_QUES       (0x08): Questionable Status Summary
			TLPM_STATBIT_STB_MAV        (0x10): Message available
			TLPM_STATBIT_STB_ESB        (0x20): Event Status Bit
			TLPM_STATBIT_STB_MSS        (0x40): Master summary status
			TLPM_STATBIT_STB_OPER       (0x80): Operation Status Summary
			
			STANDARD EVENT STATUS REGISTER bits (see IEEE488.2-1992 §11.5.1)
			TLPM_STATBIT_ESR_OPC        (0x01): Operation complete
			TLPM_STATBIT_ESR_RQC        (0x02): Request control
			TLPM_STATBIT_ESR_QYE        (0x04): Query error
			TLPM_STATBIT_ESR_DDE        (0x08): Device-Specific error
			TLPM_STATBIT_ESR_EXE        (0x10): Execution error
			TLPM_STATBIT_ESR_CME        (0x20): Command error
			TLPM_STATBIT_ESR_URQ        (0x40): User request
			TLPM_STATBIT_ESR_PON        (0x80): Power on
			
			QUESTIONABLE STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_QUES_VOLT      (0x0001): Questionable voltage measurement
			TLPM_STATBIT_QUES_CURR      (0x0002): Questionable current measurement
			TLPM_STATBIT_QUES_TIME      (0x0004): Questionable time measurement
			TLPM_STATBIT_QUES_POW       (0x0008): Questionable power measurement
			TLPM_STATBIT_QUES_TEMP      (0x0010): Questionable temperature measurement
			TLPM_STATBIT_QUES_FREQ      (0x0020): Questionable frequency measurement
			TLPM_STATBIT_QUES_PHAS      (0x0040): Questionable phase measurement
			TLPM_STATBIT_QUES_MOD       (0x0080): Questionable modulation measurement
			TLPM_STATBIT_QUES_CAL       (0x0100): Questionable calibration
			TLPM_STATBIT_QUES_ENER      (0x0200): Questionable energy measurement
			TLPM_STATBIT_QUES_10        (0x0400): Reserved
			TLPM_STATBIT_QUES_11        (0x0800): Reserved
			TLPM_STATBIT_QUES_12        (0x1000): Reserved
			TLPM_STATBIT_QUES_INST      (0x2000): Instrument summary
			TLPM_STATBIT_QUES_WARN      (0x4000): Command warning
			TLPM_STATBIT_QUES_15        (0x8000): Reserved
			
			OPERATION STATUS REGISTER bits (see SCPI 99.0 §9)
			TLPM_STATBIT_OPER_CAL       (0x0001): The instrument is currently performing a calibration.
			TLPM_STATBIT_OPER_SETT      (0x0002): The instrument is waiting for signals to stabilize for measurements.
			TLPM_STATBIT_OPER_RANG      (0x0004): The instrument is currently changing its range.
			TLPM_STATBIT_OPER_SWE       (0x0008): A sweep is in progress.
			TLPM_STATBIT_OPER_MEAS      (0x0010): The instrument is actively measuring.
			TLPM_STATBIT_OPER_TRIG      (0x0020): The instrument is in a “wait for trigger” state of the trigger model.
			TLPM_STATBIT_OPER_ARM       (0x0040): The instrument is in a “wait for arm” state of the trigger model.
			TLPM_STATBIT_OPER_CORR      (0x0080): The instrument is currently performing a correction (Auto-PID tune).
			TLPM_STATBIT_OPER_SENS      (0x0100): Optical powermeter sensor connected and operable.
			TLPM_STATBIT_OPER_DATA      (0x0200): Measurement data ready for fetch.
			TLPM_STATBIT_OPER_THAC      (0x0400): Thermopile accelerator active.
			TLPM_STATBIT_OPER_11        (0x0800): Reserved
			TLPM_STATBIT_OPER_12        (0x1000): Reserved
			TLPM_STATBIT_OPER_INST      (0x2000): One of n multiple logical instruments is reporting OPERational status.
			TLPM_STATBIT_OPER_PROG      (0x4000): A user-defined programming is currently in the run state.
			TLPM_STATBIT_OPER_15        (0x8000): Reserved
			
			Thorlabs defined MEASRUEMENT STATUS REGISTER bits
			TLPM_STATBIT_MEAS_0         (0x0001): Reserved
			TLPM_STATBIT_MEAS_1         (0x0002): Reserved
			TLPM_STATBIT_MEAS_2         (0x0004): Reserved
			TLPM_STATBIT_MEAS_3         (0x0008): Reserved
			TLPM_STATBIT_MEAS_4         (0x0010): Reserved
			TLPM_STATBIT_MEAS_5         (0x0020): Reserved
			TLPM_STATBIT_MEAS_6         (0x0040): Reserved
			TLPM_STATBIT_MEAS_7         (0x0080): Reserved
			TLPM_STATBIT_MEAS_8         (0x0100): Reserved
			TLPM_STATBIT_MEAS_9         (0x0200): Reserved
			TLPM_STATBIT_MEAS_10        (0x0400): Reserved
			TLPM_STATBIT_MEAS_11        (0x0800): Reserved
			TLPM_STATBIT_MEAS_12        (0x1000): Reserved
			TLPM_STATBIT_MEAS_13        (0x2000): Reserved
			TLPM_STATBIT_MEAS_14        (0x4000): Reserved
			TLPM_STATBIT_MEAS_15        (0x8000): Reserved
			
			Thorlabs defined Auxiliary STATUS REGISTER bits
			TLPM_STATBIT_AUX_NTC        (0x0001): Auxiliary NTC temperature sensor connected.
			TLPM_STATBIT_AUX_EMM        (0x0002): External measurement module connected.
			TLPM_STATBIT_AUX_2          (0x0004): Reserved
			TLPM_STATBIT_AUX_3          (0x0008): Reserved
			TLPM_STATBIT_AUX_EXPS       (0x0010): External power supply connected
			TLPM_STATBIT_AUX_BATC       (0x0020): Battery charging
			TLPM_STATBIT_AUX_BATL       (0x0040): Battery low
			TLPM_STATBIT_AUX_IPS        (0x0080): Apple(tm) authentification supported.
			TLPM_STATBIT_AUX_IPF        (0x0100): Apple(tm) authentification failed.
			TLPM_STATBIT_AUX_9          (0x0200): Reserved
			TLPM_STATBIT_AUX_10         (0x0400): Reserved
			TLPM_STATBIT_AUX_11         (0x0800): Reserved
			TLPM_STATBIT_AUX_12         (0x1000): Reserved
			TLPM_STATBIT_AUX_13         (0x2000): Reserved
			TLPM_STATBIT_AUX_14         (0x4000): Reserved
			TLPM_STATBIT_AUX_15         (0x8000): Reserved
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_readRegister(self.devSession, reg, value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def presetRegister(self):
		"""
		This function presets all status registers to default.
		
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_presetRegister(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setTime(self, year, month, day, hour, minute, second):
		"""
		This function sets the system date and time of the powermeter.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM100D, PM200, PM400.
		
		Args:
			year(c_int16) : This parameter specifies the actual year in the format yyyy e.g. 2009.
			month(c_int16) : This parameter specifies the actual month in the format mm e.g. 01.
			day(c_int16) : This parameter specifies the actual day in the format dd e.g. 15.
			
			hour(c_int16) : This parameter specifies the actual hour in the format hh e.g. 14.
			
			minute(c_int16) : This parameter specifies the actual minute in the format mm e.g. 43.
			
			second(c_int16) : This parameter specifies the actual second in the format ss e.g. 50.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setTime(self.devSession, year, month, day, hour, minute, second)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getTime(self, year, month, day, hour, minute, second):
		"""
		This function returns the system date and time of the powermeter.
		
		Notes:
		(1) Date and time are displayed on instruments screen and are used as timestamp for data saved to memory card.
		(2) The function is only available on PM100D, PM200, PM400.
		
		Args:
			year(c_int16 use with byref) : This parameter specifies the actual year in the format yyyy.
			month(c_int16 use with byref) : This parameter specifies the actual month in the format mm.
			day(c_int16 use with byref) : This parameter specifies the actual day in the format dd.
			hour(c_int16 use with byref) : This parameter specifies the actual hour in the format hh.
			minute(c_int16 use with byref) : This parameter specifies the actual minute in the format mm.
			second(c_int16 use with byref) : This parameter specifies the actual second in the format ss.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getTime(self.devSession, year, month, day, hour, minute, second)
		self.__testForError(pInvokeResult)
		return pInvokeResult


	def setWavelength(self, wavelength):
		"""
		This function sets the users wavelength in nanometer [nm].
		
		Remark:
		Wavelength set value is used for calculating power.
		
		
		Args:
			wavelength(c_double) : This parameter specifies the users wavelength in nanometer [nm].
			
			Remark:
			Wavelength set value is used for calculating power.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setWavelength(self.devSession, wavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getWavelength(self, attribute, wavelength):
		"""
		This function returns the users wavelength in nanometer [nm].
		
		Remark:
		Wavelength set value is used for calculating power.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			wavelength(c_double use with byref) : This parameter returns the specified wavelength in nanometer [nm].
			
			Remark:
			Wavelength set value is used for calculating power.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getWavelength(self.devSession, attribute, wavelength)
		self.__testForError(pInvokeResult)
		return pInvokeResult


	def setPowerAutoRange(self, powerAutorangeMode):
		"""
		This function sets the power auto range mode.
		
		
		Args:
			powerAutorangeMode(c_int16) : This parameter specifies the power auto range mode.
			
			Acceptable values:
			  TLPM_AUTORANGE_POWER_OFF (0): power auto range disabled
			  TLPM_AUTORANGE_POWER_ON  (1): power auto range enabled
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setPowerAutoRange(self.devSession, powerAutorangeMode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerAutorange(self, powerAutorangeMode):
		"""
		This function returns the power auto range mode.
		
		
		Args:
			powerAutorangeMode(c_int16 use with byref) : This parameter returns the power auto range mode.
			
			Return values:
			  TLPM_AUTORANGE_POWER_OFF (0): power auto range disabled
			  TLPM_AUTORANGE_POWER_ON  (0): power auto range enabled
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getPowerAutorange(self.devSession, powerAutorangeMode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerRange(self, power_to_Measure):
		"""
		This function sets the sensor's power range.
		
		
		Args:
			power_to_Measure(c_double) : This parameter specifies the most positive signal level expected for the sensor input in watt [W].
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setPowerRange(self.devSession, power_to_Measure)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerRange(self, attribute, powerValue):
		"""
		This function returns the actual power range value.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			
			powerValue(c_double use with byref) : This parameter returns the specified power range value in watt [W].
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getPowerRange(self.devSession, attribute, powerValue)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerRef(self, powerReferenceValue):
		"""
		This function sets the power reference value.
		
		
		Args:
			powerReferenceValue(c_double) : This parameter specifies the power reference value.
			
			Remark:
			(1) The power reference value has the unit specified with <Set Power Unit>.
			(2) This value is used for calculating differences between the actual power value and this power reference value if Power Reference State is ON.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setPowerRef(self.devSession, powerReferenceValue)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerRef(self, attribute, powerReferenceValue):
		"""
		This function returns the power reference value.
		
		
		Args:
			attribute(c_int16) : This parameter specifies the value to be queried.
			
			Acceptable values:
			  TLPM_ATTR_SET_VAL  (0): Set value
			  TLPM_ATTR_MIN_VAL  (1): Minimum value
			  TLPM_ATTR_MAX_VAL  (2): Maximum value
			  TLPM_ATTR_DFLT_VAL (3): Default value
			
			powerReferenceValue(c_double use with byref) : This parameter returns the specified power reference value.
			
			Remark:
			(1) The power reference value has the unit specified with <Set Power Unit>.
			(2) This value is used for calculating differences between the actual power value and this power reference value if Power Reference State is ON.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getPowerRef(self.devSession, attribute, powerReferenceValue)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerRefState(self, powerReferenceState):
		"""
		This function sets the power reference state.
		
		
		Args:
			powerReferenceState(c_int16) : This parameter specifies the power reference state.
			
			Acceptable values:
			  TLPM_POWER_REF_OFF (0): Power reference disabled. Absolute measurement.
			  TLPM_POWER_REF_ON  (1): Power reference enabled. Relative measurement.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setPowerRefState(self.devSession, powerReferenceState)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerRefState(self, powerReferenceState):
		"""
		This function returns the power reference state.
		
		
		Args:
			powerReferenceState(c_int16 use with byref) : This parameter returns the power reference state.
			
			Return values:
			  TLPM_POWER_REF_OFF (0): Power reference disabled. Absolute measurement.
			  TLPM_POWER_REF_ON  (1): Power reference enabled. Relative measurement.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getPowerRefState(self.devSession, powerReferenceState)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerUnit(self, powerUnit):
		"""
		This function sets the unit of the power value.
		
		
		Args:
			powerUnit(c_int16) : This parameter specifies the unit of the pover value.
			
			Acceptable values:
			  TLPM_POWER_UNIT_WATT (0): power in Watt
			  TLPM_POWER_UNIT_DBM  (1): power in dBm
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setPowerUnit(self.devSession, powerUnit)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerUnit(self, powerUnit):
		"""
		This function returns the unit of the power value.
		
		
		Args:
			powerUnit(c_int16 use with byref) : This parameter returns the unit of the power value.
			
			Return values:
			  TLPM_POWER_UNIT_WATT (0): power in Watt
			  TLPM_POWER_UNIT_DBM  (1): power in dBm
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getPowerUnit(self.devSession, powerUnit)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPointsInformation(self, index, serialNumber, calibrationDate, calibrationPointsCount, author, sensorPosition):
		"""
		Queries the customer adjustment header like serial nr, cal date, nr of points at given index
		
		
		Args:
			index(c_uint16) : Index of the power calibration (range 1...5)
			serialNumber(create_string_buffer(1024)) : Serial Number of the sensor.
			Please provide a buffer of 256 characters.
			calibrationDate(create_string_buffer(1024)) : Last calibration date of this sensor
			Please provide a buffer of 256 characters.
			calibrationPointsCount(ViPUInt16 use with byref) : Number of calibration points of the power calibration with this sensor
			author(create_string_buffer(1024))
			sensorPosition(ViPUInt16 use with byref) : The position of the sencor switch of a Thorlabs S130C
			1 = 5mW
			2 = 500mW
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getPowerCalibrationPointsInformation(self.devSession, index, serialNumber, calibrationDate, calibrationPointsCount, author, sensorPosition)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPointsState(self, index, state):
		"""
		Queries the state if the power calibration of this sensor is activated.
		
		
		Args:
			index(c_uint16)
			state(c_int16 use with byref) : State if the user power calibration is activated and used for the power measurements.
			
			VI_ON: The user power calibration is used
			VI_OFF: The user power calibration is ignored in the power measurements
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getPowerCalibrationPointsState(self.devSession, index, state)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerCalibrationPointsState(self, index, state):
		"""
		This function activates/inactivates the power calibration of this sensor.
		
		
		Args:
			index(c_uint16) : Index of the power calibration (range 1...5)
			state(c_int16) : State if the user power calibration is activated and used for the power measurements.
			
			VI_ON: The user power calibration is used
			VI_OFF: The user power calibration is ignored in the power measurements
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setPowerCalibrationPointsState(self.devSession, index, state)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getPowerCalibrationPoints(self, index, pointCounts, wavelengths, powerCorrectionFactors):
		"""
		Returns a list of wavelength and the corresponding power correction factor.
		
		
		Args:
			index(c_uint16)
			pointCounts(c_uint16) : Number of points that are submitted in the wavelength and power correction factors arrays.
			Maximum of 8 wavelength - power correction factors pairs can be calibrated for each sensor.
			wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order.
			The array must contain <points counts> entries.
			powerCorrectionFactors( (c_double * arrayLength)()) : Array of power correction factorw that correspond to the wavelength array. 
			The array must contain <points counts> entries, same as wavelenght to build wavelength - power correction factors pairs.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getPowerCalibrationPoints(self.devSession, index, pointCounts, wavelengths, powerCorrectionFactors)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setPowerCalibrationPoints(self, index, pointCounts, wavelengths, powerCorrectionFactors, author, sensorPosition):
		"""
		Sumbits a list of wavelength and the corresponding measured power correction factors to calibrate the power measurement.
		
		
		Args:
			index(c_uint16) : Index of the power calibration (range 1...5)
			pointCounts(c_uint16) : Number of points that are submitted in the wavelength and power correction factors arrays.
			Maximum of 8 wavelength - power correction factors  pairs can be calibrated for each sensor.
			wavelengths( (c_double * arrayLength)()) : Array of wavelengths in nm. Requires ascending wavelength order.
			The array must contain <points counts> entries.
			powerCorrectionFactors( (c_double * arrayLength)()) : Array of powers correction factors that correspond to the wavelength array. 
			The array must contain <points counts> entries, same as wavelenght to build wavelength - power correction factors  pairs.
			author(create_string_buffer(1024)) : Buffer that contains the name of the editor of the calibration.
			Name of Author limited to 19 chars + ''
			sensorPosition(c_uint16) : The position of the sencor switch of a Thorlabs S130C
			1 = 5mW
			2 = 500mW
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setPowerCalibrationPoints(self.devSession, index, pointCounts, wavelengths, powerCorrectionFactors, author, sensorPosition)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def reinitSensor(self):
		"""
		To use the user power calibration, the sensor has to be reconnected.
		Either manually remove and reconnect the sensor to the instrument or use this funtion.
		
		This function will wait 2 seconds until the sensor has been reinitialized.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_reinitSensor(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def measPower(self, power):
		"""
		This function is used to obtain power readings from the instrument. 
		
		Remark:
		This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
		
		Args:
			power(c_double use with byref) : This parameter returns the power in the selected unit.
			
			Remark:
			(1) This function starts a new measurement cycle and after finishing measurement the result is received. Subject to the actual Average Count this may take up to seconds. Refer to <Set/Get Average Count>. 
			(2) Select the unit with <Set Power Unit>.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_measPower(self.devSession, power)
		self.__testForError(pInvokeResult)
		return pInvokeResult


	def errorMessage(self, statusCode, description):
		"""
		This function takes the error code returned by the instrument driver functions interprets it and returns it as an user readable string. 
		
		Status/error codes and description:
		
		--- Instrument Driver Errors and Warnings ---
		Status      Description
		-------------------------------------------------
		         0  No error (the call was successful).
		0x3FFF0085  Unknown Status Code     - VI_WARN_UNKNOWN_STATUS
		0x3FFC0901  WARNING: Value overflow - VI_INSTR_WARN_OVERFLOW
		0x3FFC0902  WARNING: Value underrun - VI_INSTR_WARN_UNDERRUN
		0x3FFC0903  WARNING: Value is NaN   - VI_INSTR_WARN_NAN
		0xBFFC0001  Parameter 1 out of range. 
		0xBFFC0002  Parameter 2 out of range.
		0xBFFC0003  Parameter 3 out of range.
		0xBFFC0004  Parameter 4 out of range.
		0xBFFC0005  Parameter 5 out of range.
		0xBFFC0006  Parameter 6 out of range.
		0xBFFC0007  Parameter 7 out of range.
		0xBFFC0008  Parameter 8 out of range.
		0xBFFC0012  Error Interpreting instrument response.
		
		--- Instrument Errors --- 
		Range: 0xBFFC0700 .. 0xBFFC0CFF.
		Calculation: Device error code + 0xBFFC0900.
		Please see your device documentation for details.
		
		--- VISA Errors ---
		Please see your VISA documentation for details.
		
		
		Args:
			statusCode(ViStatus) : This parameter accepts the error codes returned from the instrument driver functions.
			
			Default Value: 0 - VI_SUCCESS
			description(create_string_buffer(1024)) : This parameter returns the interpreted code as an user readable message string.
			
			Notes:
			(1) The array must contain at least 512 elements ViChar[512].
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_errorMessage(self.devSession, statusCode, description)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def errorQuery(self, errorNumber, errorMessage):
		"""
		This function queries the instrument's error queue manually. 
		Use this function to query the instrument's error queue if the driver's error query mode is set to manual query. 
		
		Notes:
		(1) The returned values are stored in the drivers error store. You may use <Error Message> to get a descriptive text at a later point of time.
		
		Args:
			errorNumber(c_int use with byref) : This parameter returns the instrument error number.
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
			errorMessage(create_string_buffer(1024)) : This parameter returns the instrument error message.
			
			Notes:
			(1) The array must contain at least TLPM_ERR_DESCR_BUFFER_SIZE (512) elements ViChar[512].
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_errorQuery(self.devSession, errorNumber, errorMessage)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def errorQueryMode(self, mode):
		"""
		This function selects the driver's error query mode.
		
		Args:
			mode(c_int16) : This parameter specifies the driver's error query mode. 
			
			If set to Automatic each driver function queries the instrument's error queue and in case an error occured returns the error number.
			
			If set to Manual the driver does not query the instrument for errors and therefore a driver function does not return instrument errors. You should use <Error Query> to manually query the instrument's error queue.
			
			VI_OFF (0): Manual error query.
			VI_ON  (1): Automatic error query (default).
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_errorQueryMode(self.devSession, mode)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def reset(self):
		"""
		This function resets the device.
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_reset(self.devSession)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def selfTest(self, selfTestResult, description):
		"""
		This function runs the device self test routine and returns the test result.
		
		Args:
			selfTestResult(c_int16 use with byref) : This parameter contains the value returned from the device self test routine. A retured zero value indicates a successful run, a value other than zero indicates failure.
			description(create_string_buffer(1024)) : This parameter returns the interpreted code as an user readable message string.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_selfTest(self.devSession, selfTestResult, description)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def revisionQuery(self, instrumentDriverRevision, firmwareRevision):
		"""
		This function returns the revision numbers of the instrument driver and the device firmware.
		
		Args:
			instrumentDriverRevision(create_string_buffer(1024)) : This parameter returns the Instrument Driver revision.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			firmwareRevision(create_string_buffer(1024)) : This parameter returns the device firmware revision. 
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_revisionQuery(self.devSession, instrumentDriverRevision, firmwareRevision)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def identificationQuery(self, manufacturerName, deviceName, serialNumber, firmwareRevision):
		"""
		This function returns the device identification information.
		
		Args:
			manufacturerName(create_string_buffer(1024)) : This parameter returns the manufacturer name.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			deviceName(create_string_buffer(1024)) : This parameter returns the device name.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			serialNumber(create_string_buffer(1024)) : This parameter returns the device serial number.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
			firmwareRevision(create_string_buffer(1024)) : This parameter returns the device firmware revision.
			
			Notes:
			(1) The array must contain at least 256 elements ViChar[256].
			(2) You may pass VI_NULL if you do not need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_identificationQuery(self.devSession, manufacturerName, deviceName, serialNumber, firmwareRevision)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getCalibrationMsg(self, message):
		"""
		This function returns a human readable calibration message.
		
		
		Args:
			message(create_string_buffer(1024)) : This parameter returns the calibration message.
			
			Notes:
			(1) The array must contain at least TLPM_BUFFER_SIZE (256) elements ViChar[256].
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getCalibrationMsg(self.devSession, message)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getSensorInfo(self, name, snr, message, pType, pStype, pFlags):
		"""
		This function is used to obtain informations from the connected sensor like sensor name, serial number, calibration message, sensor type, sensor subtype and sensor flags.  
		
		Remark:
		The meanings of the obtained sensor type, subtype and flags are:
		
		Sensor Types:
		 SENSOR_TYPE_NONE               0x00 // No sensor
		 SENSOR_TYPE_PD_SINGLE          0x01 // Photodiode sensor
		 SENSOR_TYPE_THERMO             0x02 // Thermopile sensor
		 SENSOR_TYPE_PYRO               0x03 // Pyroelectric sensor
		
		Sensor Subtypes:
		 SENSOR_SUBTYPE_NONE            0x00 // No sensor
		 
		Sensor Subtypes Photodiode:
		 SENSOR_SUBTYPE_PD_ADAPTER      0x01 // Photodiode adapter
		 SENSOR_SUBTYPE_PD_SINGLE_STD   0x02 // Photodiode sensor
		 SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with 
		                                        integrated filter
		                                        identified by position 
		 SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with
		                                        temperature sensor
		Sensor Subtypes Thermopile:
		 SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter
		 SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor
		 SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with 
		                                        temperature sensor
		Sensor Subtypes Pyroelectric Sensor:
		 SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter
		 SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor
		 SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with
		                                        temperature sensor
		Sensor Flags:
		 TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor
		 TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor
		 TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable
		 TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable
		 TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable
		 TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor 
		
		Args:
			name(create_string_buffer(1024)) : This parameter returns the name of the connected sensor.
			
			snr(create_string_buffer(1024)) : This parameter returns the serial number of the connected sensor.
			message(create_string_buffer(1024)) : This parameter returns the calibration message of the connected sensor.
			
			pType(c_int16 use with byref) : This parameter returns the sensor type of the connected sensor.
			
			Remark:
			The meanings of the obtained sensor type are:
			
			Sensor Types:
			 SENSOR_TYPE_NONE               0x00 // No sensor
			 SENSOR_TYPE_PD_SINGLE          0x01 // Photodiode sensor
			 SENSOR_TYPE_THERMO             0x02 // Thermopile sensor
			 SENSOR_TYPE_PYRO               0x03 // Pyroelectric sensor
			pStype(c_int16 use with byref) : This parameter returns the subtype of the connected sensor.
			
			Remark:
			The meanings of the obtained sensor subtype are:
			
			Sensor Subtypes:
			 SENSOR_SUBTYPE_NONE            0x00 // No sensor
			 
			Sensor Subtypes Photodiode:
			 SENSOR_SUBTYPE_PD_ADAPTER      0x01 // Photodiode adapter
			 SENSOR_SUBTYPE_PD_SINGLE_STD   0x02 // Photodiode sensor
			 SENSOR_SUBTYPE_PD_SINGLE_FSR   0x03 // Photodiode sensor with 
			                                        integrated filter
			                                        identified by position 
			 SENSOR_SUBTYPE_PD_SINGLE_STD_T 0x12 // Photodiode sensor with
			                                        temperature sensor
			Sensor Subtypes Thermopile:
			 SENSOR_SUBTYPE_THERMO_ADAPTER  0x01 // Thermopile adapter
			 SENSOR_SUBTYPE_THERMO_STD      0x02 // Thermopile sensor
			 SENSOR_SUBTYPE_THERMO_STD_T    0x12 // Thermopile sensor with 
			                                        temperature sensor
			Sensor Subtypes Pyroelectric Sensor:
			 SENSOR_SUBTYPE_PYRO_ADAPTER    0x01 // Pyroelectric adapter
			 SENSOR_SUBTYPE_PYRO_STD        0x02 // Pyroelectric sensor
			 SENSOR_SUBTYPE_PYRO_STD_T      0x12 // Pyroelectric sensor with
			                                        temperature sensor
			pFlags(c_int16 use with byref) : This parameter returns the flags of the connected sensor.
			
			Remark:
			The meanings of the obtained sensor flags are:
			
			Sensor Flags:
			 TLPM_SENS_FLAG_IS_POWER     0x0001 // Power sensor
			 TLPM_SENS_FLAG_IS_ENERGY    0x0002 // Energy sensor
			 TLPM_SENS_FLAG_IS_RESP_SET  0x0010 // Responsivity settable
			 TLPM_SENS_FLAG_IS_WAVEL_SET 0x0020 // Wavelength settable
			 TLPM_SENS_FLAG_IS_TAU_SET   0x0040 // Time constant settable
			 TLPM_SENS_FLAG_HAS_TEMP     0x0100 // With Temperature sensor
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getSensorInfo(self.devSession, name, snr, message, pType, pStype, pFlags)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def writeRaw(self, command):
		"""
		This function writes directly to the instrument.
		
		Args:
			command(ViString) : Null terminated command string to send to the instrument.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_writeRaw(self.devSession, command)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def readRaw(self, buffer, size, returnCount):
		"""
		This function reads directly from the instrument.
		
		
		Args:
			buffer(create_string_buffer(1024)) : Byte buffer that receives the data read from the instrument.
			
			Notes:
			(1) If received data is less than buffer size, the buffer is additionaly terminated with a '' character.
			(2) If received data is same as buffer size no '' character is appended. Its the caller's responsibility to make sure a buffer is '' terminated if the caller wants to interprete the buffer as string.
			size(c_uint32) : This parameter specifies the buffer size.
			
			returnCount(c_uint32 use with byref) : Number of bytes actually transferred and filled into Buffer. This number doesn't count the additional termination '' character. If Return Count == size the buffer content will not be '' terminated.
			
			Notes:
			(1) You may pass VI_NULL if you don't need this value.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_readRaw(self.devSession, buffer, size, returnCount)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setTimeoutValue(self, value):
		"""
		This function sets the interface communication timeout value.
		
		Args:
			value(c_uint32) : This parameter specifies the communication timeout value in ms.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setTimeoutValue(self.devSession, value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getTimeoutValue(self, value):
		"""
		This function gets the interface communication timeout value.
		
		
		Args:
			value(c_uint32 use with byref) : This parameter returns the communication timeout value in ms.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getTimeoutValue(self.devSession, value)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDeviceBaudrate(self, baudrate):
		"""
		Tell the instrument which baudrate has to be used for the serial communication.
		This value is stored inside the instrument. 
		
		If the RS232 interface is currently used for the communication, call the function setDriverBaudrate to adapt to the new baudrate.
		
		Args:
			baudrate(c_uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setDeviceBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDeviceBaudrate(self, baudrate):
		"""
		This function returns the baudrate that is used for the serial communication inside the instrument
		
		
		Args:
			baudrate(c_uint32 use with byref) : This parameter returns the baudrate in bist/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getDeviceBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def setDriverBaudrate(self, baudrate):
		"""
		This function sets the baudrate for the serial interface on the PC side
		
		Args:
			baudrate(c_uint32) : This parameter specifies the baudrate in bits/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_setDriverBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

	def getDriverBaudrate(self, baudrate):
		"""
		This function returns the baudrate that is used for the serial communication on the PC side
		
		
		Args:
			baudrate(c_uint32 use with byref) : This parameter returns the baudrate in bist/sec.
			
		Returns:
			int: The return value, 0 is for success
		"""
		pInvokeResult = self.dll.TLPM_getDriverBaudrate(self.devSession, baudrate)
		self.__testForError(pInvokeResult)
		return pInvokeResult

