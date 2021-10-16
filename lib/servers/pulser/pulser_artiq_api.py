from labrad import util

from artiq.experiment import *
from pulser_artiq import Pulser_artiq
from devices import Devices

import numpy as np

class api(EnvExperiment):
    kernel_invariants = {}

    def build(self):
        #get core
        self.setattr_device("core")
        self.setattr_device("core_dma")
        self.setattr_device("scheduler")

        #get device names
        self.device_db = self.get_device_db()
            #get ttl names
        ttl_names = [key for key, val in self.device_db if val['class'] == 'TTLOut']
            #get ttl names
        ttlin_names = [key for key, val in self.device_db if val['class'] == 'TTLInOut']
            #get dds names
        dds_names = [key for key, val in self.device_db if val['class'] == 'AD9910' or 'AD9912']
            #get urukul names
        urukul_names = [key for key, val in self.device_db if val['class'] == 'CPLD']

        #todo: do DAC and ADC
        #todo: do PMT via TTL
        #todo: linetrigger via TTL

        #set device attributes
        for name in ttl_names + ttlin_names + dds_names + urukul_names:
            self.setattr_device(name)

        #get devices
        self.ttl_list = [self.get_device(name) for name in ttl_names]
        self.ttlin_list = [self.get_device(name) for name in ttlin_names]
        self.dds_list = [self.get_device(name) for name in dds_names]
        self.urukul_list = [self.get_device(name) for name in urukul_names]
        #todo: convert to dictionary so we can take names

        #setup variables
        self.numRuns = 0
        self.maxRuns = 0
        self.linetrigger_delay = 0
        self.linetrigger_active = False

    @kernel
    def prepare(self):
        #initialize devices
            #set ttlinout devices to be input
        for device in self.ttlin_list:
            device.input()
            #initialize DDSs
        for device in self.dds_list + self.urukul_list:
            device.init()

    #Pulse sequencer functions
    @kernel(flags = {"fast-math"})
    def programSequence(self, ttl_sequence, dds_single_sequence, dds_ramp_sequence):
        #record pulse sequence in memory
        with self.core_dma.record("pulse_sequence"):
            #add ttl sequence
            for timestamp, ttlCommandArr in ttl_sequence:
                at_mu(timestamp)
                with parallel:
                    for i in range(ttl_sequence.channelTotal):
                        if ttlCommandArr[i] == 1:
                            self.ttl_list[i].on()
                        elif ttlCommandArr[i] == -1:
                            self.ttl_list[i].off()

    @kernel
    def runSequence(self):
        #get sequence handle to minimize overhead
        sequence_handle = self.core_dma.get_handle("pulse_sequence")

        #wait until line trigger receives input or we disable the line trigger
        while self.linetrigger_active:
            #wait in blocks of 10ms
            time_gate = self.ttlin_list['LineTrigger'].gate_rising(10 * ms)
            time_trig = self.ttlin_list['LineTrigger'].timestamp_mu(time_gate)
            #time_trig returns -1 if we dont receive a signal
            if time_trig > 0:
                #set time to now and do an offset delay
                at_mu(time_trig)
                delay(self.linetrigger_delay * us)
                break

        #start running
        while self.numRuns < self.maxRuns:
            self.core.reset()
            self.core_dma.playback_handle(sequence_handle)
            self.numRuns += 1

    @kernel
    def eraseSequence(self):
        '''
        Removes the pulse sequence from memory
        '''
        self.core_dma.erase("pulse_sequence")

    def resetFIFONormal(self):
        '''
        Reset the FIFO on the FPGA for the normal PMT counting
        '''

    def resetFIFOResolved(self):
        '''
        Reset the FIFO on the FPGA for the time-tagged photon counting
        '''

    def resetFIFOReadout(self):
        '''
        Reset the FIFO on the FPGA for the read-out count.
        '''

    def setModeNormal(self):
        """
        user selects PMT counting rate
        """


    def setModeDifferential(self):
        """
        pulse sequence controls the PMT counting rate
        """


    @kernel
    def isSeqDone(self):
        '''
        check if the pulse sequence is done executing or not
        '''
        return self.numRuns

    def getResolvedTotal(self):
        '''
        Get the number of photons counted in the FIFO for the time-resolved photon counter.
        '''


    def getResolvedCounts(self, number):
        '''
        Get the time-tagged photon data.
        '''


    def getNormalTotal(self):
        '''
        Get the number of normal PMT counts. (How many data in the FIFO)
        '''


    def getNormalCounts(self, number):
        '''
        Get the normal PMT counts from the FIFO.
        '''


    def getReadoutTotal(self):
        '''
        Get the number of readout count.
        '''


    def getReadoutCounts(self, number):
        '''
        Get the readout count data.
        '''


    def setPMTCountRate(self, time):
        '''

        '''


    def setAuto(self, channel, inversion):
        '''
        Set the logic of the TTL to be auto or not
        '''


    def setManual(self, channel, state):
        '''
        Set the logic of the TTL to be manual or not
        '''


    @kernel
    def resetAllDDS(self):
        '''
        Reset the ram position of all dds chips to 0
        '''
        #not easily possible since FPGA RAM isn't exposed as part of artiq API
        pass

    @kernel
    def advanceAllDDS(self):
        '''
        Advance the ram position of all dds chips
        '''
        # not easily possible since FPGA RAM isn't exposed as part of artiq API
        pass

    @kernel
    def initializeDDS(self):
        '''
        Force reprogram of all dds chips during initialization
        '''
        self.core.reset()
        for device in self.dds_list + self.urukul_list:
            try:
                device.init()
            except RTIOUnderflow:
                self.core.break_realtime()
                device.init()

    @kernel
    def setDDSParam(self, chan, _asf, _ftw, **kwargs):
        self.dds_list[chan].set_mu(ftw = _ftw, asf = _asf)
        if kwargs is not None:
            self.dds_list[chan].set_mu(kwargs)

    def enableLineTrigger(self, delay = 0):
        '''
        Enable line trigger with some delay (in microseconds)
        '''
        self.linetrigger_active = True
        self.linetrigger_delay =

    def disableLineTrigger(self):
        '''
        Disable the line trigger
        '''

    def run(self):
        #run the labrad server and expose class methods to the server
        util.runServer(Pulser_artiq(self))
