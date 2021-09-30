"""
### BEGIN NODE INFO
[info]
name = Temperature Controller Server
version = 1.0.0
description = Talks to the Lakeshore 336 Temperature Controller
instancename = Lakeshore336Server

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20

[shutdown]
message = 987654321
timeout = 20
### END NODE INFO
"""

from __future__ import absolute_import
from twisted.internet.defer import inlineCallbacks, returnValue
from EGGs_Control.lib.servers.serial.serialdeviceserver import SerialDeviceServer, setting, inlineCallbacks, SerialDeviceError, SerialConnectionError, PortRegError
from labrad.server import setting
from labrad.support import getNodeName
from serial import PARITY_ODD
import time

import numpy as np

SERVERNAME = 'lakeshore336Server'
TIMEOUT = 1.0
BAUDRATE = 57600
BYTESIZE = 7
PARITY = PARITY_ODD #0 is odd parity
STOPBITS = 1
INPUT_CHANNELS = ['A', 'B', 'C', 'D', '0']
OUTPUT_CHANNELS = [1, 2, 3, 4]
TERMINATOR = '\r\n'

class Lakeshore336Server(SerialDeviceServer):
    name = 'Lakeshore336Server'
    regKey = 'Lakeshore336Server'
    serNode = getNodeName()
    OUTPUT_MODES = [0, 1, 2, 3, 4, 5]

    # def initServer(self):
    #     #temp workaround since serial server is a pos
    #     self.ser = Serial(port = 'COM24', baudrate = BAUDRATE, bytesize = BYTESIZE, parity = PARITY, stopbits = STOPBITS)
    #     self.ser.timeout = TIMEOUT

    @inlineCallbacks
    def initServer( self ):
        # if not self.regKey or not self.serNode: raise SerialDeviceError( 'Must define regKey and serNode attributes' )
        # port = yield self.getPortFromReg( self.regKey )
        port = 'COM24'
        self.port = port
        #self.timeout = TIMEOUT
        try:
            serStr = yield self.findSerial( self.serNode )
            print(serStr)
            self.initSerial( serStr, port, baudrate = BAUDRATE, bytesize = BYTESIZE, parity = PARITY, stopbits = STOPBITS)
        except SerialConnectionError, e:
            self.ser = None
            if e.code == 0:
                print 'Could not find serial server for node: %s' % self.serNode
                print 'Please start correct serial server'
            elif e.code == 1:
                print 'Error opening serial connection'
                print 'Check set up and restart serial server'
            else: raise

    @inlineCallbacks
    def _check_errors(self, ):
        """
        Checks user input for errors
        """
        if output_channel not in OUTPUT_CHANNELS:
            raise Exception('Channel must be one of: ' + str(OUTPUT_CHANNELS))
        if input_channel not in INPUT_CHANNELS:
            raise Exception('Channel must be one of: ' + str(INPUT_CHANNELS))
        # if mode is not None and not in OUTPUT_MODES:
        #     raise Exception ('Mode must be one of: ' + str(self.OUTPUT_MODES))

    # TEMPERATURE DIODES
    @setting(111,'Read Temperature', output_channel = 's', returns='*1v')
    def temperature_read(self, c, output_channel):
        """
        Get sensor temperature
        Args:
            channel (str): sensor channel to measure
        Returns:
            (*float): sensor temperature in Kelvin
        """
        if output_channel not in INPUT_CHANNELS:
            raise Exception('Channel must be one of: ' + str(INPUT_CHANNELS))
        yield self.ser.write('KRDG? ' + str(output_channel) + TERMINATOR)
        time.sleep(0.1)
        resp = yield self.ser.read()
        resp = np.array(resp.split(','), dtype=float)
        returnValue(resp)

    # HEATER
    @setting(211, 'Configure Heater', output_channel = 'i', mode = 'i', input_channel = 'i', returns = '*1v')
    def heater_configure_output(self, c, output_channel, mode = None, input_channel = None):
        """
        Configure or query the desired heater
        Args:
            output_channel  (int): the heater channel
            mode            (int): heater operation mode (0 = off, 1 = PID, 2 = zone,
                                                        3  = open loop, 4 = monitor out, 5 = warmup)
            input_channel   (int): the temperature diode channel to control the output
        Returns:
            ***                  : fd
        """
        chString = 'OUTMODE'

        #check for errors

        #send message if not querying
        if mode is not None:
            output_msg = ' ' + str(output_channel) + ',' + str(mode) + ',' + str(input_channel) + ',0' + TERMINATOR
            yield self.write(chString + output_msg)

        #issue query
        resp = yield self.query(chString + '?' + TERMINATOR)
        #*** process result
        returnValue(resp)

    @setting(212, 'Setup Heater', output_channel = 'i', resistance = 'i', max_current = 'v', returns = '*1v')
    def heater_setup(self, c, output_channel, resistance = None, max_current = None):
        """
        Set up or query the desired heater
        Args:
            output_channel  (int): the heater channel
            mode            (int): heater operation mode (0 = off, 1 = PID, 2 = zone,
                                                        3  = open loop, 4 = monitor out, 5 = warmup)
            input_channel   (int): the temperature diode channel to control the output
        Returns:
            ***                  : fd
        """
        chString = 'HTRSET'

        #check for errors***

        #send message if not querying
        if mode is not None:
            output_msg = ' ' + str(output_channel) + ',' + str(resistance) + ',0,' + str(max_current) + ',2' + TERMINATOR
            yield self.write(chString + output_msg)

        #issue query
        resp = yield self.query(chString + '? ' + str(output_channel) + TERMINATOR)
        #*** process result
        returnValue(resp)

    @setting(213, 'Set Heater Range', output_channel = 'i', range = 'i', returns = 'i')
    def heater_range(self, c, output_channel, range = None):
        """
        Set or query heater range.
        Args:
            output_channel (int): the heater channel
            range (int): the heater range (0 = off, 1 = Low, 2 = Medium, 3 = High)
        Returns:
            (int): the heater range
        """
        chString = 'RANGE'

        #check for errors ***

        if range is not None:
            output_msg = ' ' + str(output_channel) + ',' + str(range) + TERMINATOR
            yield self.write(chString + output_msg)

        #issue query
        resp = yield self.query(chString + '? ' + str(output_channel) + TERMINATOR)
        resp = int(resp)
        returnValue(resp)

    @setting(214, 'Set Heater Power', output_channel = 'i', power = 'v', returns = 'v')
    def heater_power(self, c, output_channel, power = None):
        """
        Set or query heater power.
        Args:
            output_channel (int): the heater channel
            power (float): the heater power as aa percentage of max amount
        Returns:
            (float): the heater power
        """
        chString = 'MOUT'

        #check for errors ***

        if power is not None:
            output_msg = ' ' + str(output_channel) + ',' + str(power) + TERMINATOR
            yield self.write(chString + output_msg)

        #issue query
        resp = yield self.query(chString + '? ' + str(output_channel) + TERMINATOR)
        resp = float(resp)
        returnValue(resp)

if __name__ == '__main__':
    from labrad import util
    util.runServer(Lakeshore336Server())