from twisted.internet.defer import inlineCallbacks
from EGGS_labrad.clients.SLS_client.SLS_gui import SLS_gui

_TIME_STR = '{0:d}:{1:d}:{2:d}'


class SLS_client(SLS_gui):

    name = 'SLS Client'
    AUTOLOCKID = 295372


    def __init__(self, reactor, cxn=None, parent=None):
        super().__init__()
        self.cxn = cxn
        self.gui = self
        self.gui.setupUi()
        self.reactor = reactor
        self.servo_target = None
        self.servers = ['SLS Server', 'Data Vault']
        # initialization sequence
        d = self.connect()
        d.addCallback(self.initData)
        d.addCallback(self.initializeGUI)


    # SETUP
    @inlineCallbacks
    def connect(self):
        """
        Creates an asynchronous connection to labrad.
        """
        # create connection to labrad manager
        if not self.cxn:
            import os
            LABRADHOST = os.environ['LABRADHOST']
            from labrad.wrappers import connectAsync
            self.cxn = yield connectAsync(LABRADHOST, name=self.name)

        # get servers
        try:
            self.dv = self.cxn.data_vault
            self.reg = self.cxn.registry
            self.sls = self.cxn.sls_server
        except Exception as e:
            print('Required servers not connected, disabling widget.')
            self.setEnabled(False)

        # connect to signals
            # device parameters
        yield self.sls.signal__autolock_update(self.AUTOLOCKID)
        yield self.sls.addListener(listener=self.updateAutolock, source=None, ID=self.AUTOLOCKID)
            # server connections
        yield self.cxn.manager.subscribe_to_named_message('Server Connect', 9898989, True)
        yield self.cxn.manager.addListener(listener=self.on_connect, source=None, ID=9898989)
        yield self.cxn.manager.subscribe_to_named_message('Server Disconnect', 9898989 + 1, True)
        yield self.cxn.manager.addListener(listener=self.on_disconnect, source=None, ID=9898989 + 1)

        # start device polling
        poll_params = yield self.sls.polling()
        # only start polling if not started
        if not poll_params[0]:
            yield self.sls.polling(True, 5.0)
        return self.cxn

    @inlineCallbacks
    def initData(self, cxn):
        """
        Get startup data from servers and show on GUI.
        """
        # lockswitches
        self.gui.autolock_lockswitch.setChecked(True)
        self.gui.off_lockswitch.setChecked(True)
        self.gui.PDH_lockswitch.setChecked(True)
        self.gui.servo_lockswitch.setChecked(True)
        # get all values
        values_tmp = yield self.sls.get_values()
        init_values = dict(zip(values_tmp[0], values_tmp[1]))
        # autolock
        self.gui.autolock_param.setCurrentIndex(int(init_values['SweepType']))
        self.gui.autolock_toggle.setChecked(bool(init_values['AutoLockEnable']))
        self.gui.autolock_attempts.setText(str(init_values['LockCount']))
        autolock_time = float(init_values['LockTime'])
        autolock_time_formatted = self._dateFormat(autolock_time)
        self.gui.autolock_time.setText(autolock_time_formatted)
        # offset
        self.gui.off_freq.setValue(float(init_values['OffsetFrequency']))
        self.gui.off_lockpoint.setCurrentIndex(int(init_values['LockPoint']))
        # PDH
        self.gui.PDH_freq.setValue(float(init_values['PDHFrequency']))
        self.gui.PDH_phasemodulation.setValue(float(init_values['PDHPMIndex']))
        self.gui.PDH_phaseoffset.setValue(float(init_values['PDHPhaseOffset']))
        self.gui.PDH_filter.setCurrentIndex(int(init_values['PDHDemodFilter']))
        # Servo
        self.gui.servo_param.setCurrentIndex(0)
        self.gui.servo_set.setValue(float(init_values['CurrentServoSetpoint']))
        self.gui.servo_p.setValue(float(init_values['CurrentServoPropGain']))
        self.gui.servo_i.setValue(float(init_values['CurrentServoIntGain']))
        self.gui.servo_d.setValue(float(init_values['CurrentServoDiffGain']))
        self.gui.servo_filter.setCurrentIndex(int(init_values['CurrentServoOutputFilter']))
        return cxn

    def initializeGUI(self, cxn):
        """
        Connect signals to slots and other initializations.
        """
        # autolock
        self.gui.autolock_toggle.toggled.connect(lambda status: self.sls.autolock_toggle(status))
        self.gui.autolock_param.currentTextChanged.connect(lambda param: self.sls.autolock_parameter(param.upper()))
        # pdh
        self.gui.PDH_freq.valueChanged.connect(lambda value: self.changePDHValue('frequency', value))
        self.gui.PDH_phasemodulation.valueChanged.connect(lambda value: self.changePDHValue('index', value))
        self.gui.PDH_phaseoffset.valueChanged.connect(lambda value: self.changePDHValue('phase', value))
        self.gui.PDH_filter.currentIndexChanged.connect(lambda value: self.changePDHValue('filter', value))
        # servo
        self.gui.servo_param.currentTextChanged.connect(lambda target: self.changeServoTarget(target))
        self.gui.servo_set.valueChanged.connect(lambda value: self.changeServoValue('set', value))
        self.gui.servo_filter.currentIndexChanged.connect(lambda value: self.changeServoValue('filter', value))
        self.gui.servo_p.valueChanged.connect(lambda value: self.changeServoValue('p', value))
        self.gui.servo_i.valueChanged.connect(lambda value: self.changeServoValue('i', value))
        self.gui.servo_d.valueChanged.connect(lambda value: self.changeServoValue('d', value))
        return cxn


    # SIGNALS
    @inlineCallbacks
    def on_connect(self, c, message):
        server_name = message[1]
        if server_name in self.servers:
            print(server_name + ' reconnected, enabling widget.')
            yield self.initData(self.cxn)
            self.setEnabled(True)

    def on_disconnect(self, c, message):
        server_name = message[1]
        if server_name in self.servers:
            print(server_name + ' disconnected, disabling widget.')
            self.setEnabled(False)

    def updateAutolock(self, c, lockstatus):
        """
        Updates GUI when values are received from server.
        """
        autolock_time = lockstatus[1]
        autolock_time_formatted = self._dateFormat(autolock_time)
        self.gui.autolock_attempts.setText(str(lockstatus[0]))
        self.gui.autolock_time.setText(autolock_time_formatted)


    # SLOTS
    @inlineCallbacks
    def changePDHValue(self, param_name, param_value):
        yield self.sls.PDH(param_name, param_value)

    @inlineCallbacks
    def changeServoTarget(self, target):
        print('target: ' + target)
        self.servo_target = target.lower()
        servo_params = {'p': self.gui.servo_p, 'i': self.gui.servo_i,
                  'd': self.gui.servo_d, 'set': self.gui.servo_set}
        for param_name, gui_element in servo_params.items():
            val = yield self.sls.servo(self.servo_target, param_name)
            gui_element.setValue(val)
        index = yield self.sls.servo(self.servo_target, 'filter')
        self.gui.servo_filter.setCurrentIndex(index)

    @inlineCallbacks
    def changeServoValue(self, param_name, param_value):
        print('servo: ' + str(param_name) + ': ' + str(param_value))
        yield self.sls.servo(self.servo_target, param_name, param_value)

    def closeEvent(self, event):
        self.cxn.disconnect()
        if self.reactor.running:
            self.reactor.stop()


    # HELPER
    def _dateFormat(self, _seconds):
        days = _seconds / 86400
        hours = (days % 1) * 24
        minutes = int((hours % 1) * 60)
        time_str = _TIME_STR.format(int(days), int(hours), minutes)
        return time_str


if __name__ == "__main__":
    from EGGS_labrad.clients import runClient
    runClient(SLS_client)
