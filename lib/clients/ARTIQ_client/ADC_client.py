import os
import sys

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QDoubleSpinBox, QLabel, QGridLayout, QFrame, QSizePolicy

from twisted.internet.task import LoopingCall
from twisted.internet.defer import inlineCallbacks

from EGGS_labrad.lib.clients.Widgets import TextChangingButton
from EGGS_labrad.lib.servers.ARTIQ.device_db import device_db

class ADC_channel(QFrame):
    """
    GUI for a single TTL channel.
    """
    def __init__(self, name=None, parent=None):
        QWidget.__init__(self, parent)
        self.name = name
        self.setFrameStyle(0x0001 | 0x0010)
        # self.setLineWidth(2)
        self.makeLayout(name)
        self.setFixedSize(150, 75)

    def makeLayout(self, title):
        layout = QGridLayout()
        # labels
        title = QLabel(title)
        title.setFont(QFont('MS Shell Dlg 2', pointSize=10))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)
        # buttons
        self.toggle = TextChangingButton(("ON", "OFF"))
        self.lockswitch = TextChangingButton(("Unlocked", "Locked"))
        self.lockswitch.setFont(QFont('MS Shell Dlg 2', pointSize=8))
        self.lockswitch.setChecked(True)
        # set layout
        layout.addWidget(title, 0, 0, 1, 2)
        layout.addWidget(self.toggle, 1, 0, 1, 1)
        layout.addWidget(self.lockswitch, 1, 1, 1, 1)
        self.setLayout(layout)

        #connect signal to slot
        self.lockswitch.toggled.connect(lambda status=self.lockswitch.isChecked(): self.lock(status))

    @inlineCallbacks
    def lock(self, status):
        yield self.toggle.setEnabled(status)


class TTL_client(QWidget):
    """
    Client for all TTL channels.
    """
    name = "ARTIQ TTL Client"
    row_length = 10

    TTLID = 888999

    def __init__(self, reactor, cxn=None, parent=None):
        super(TTL_client, self).__init__()
        self.reactor = reactor
        self.cxn = cxn
        self.ttl_clients = {}
        #start connections
        d = self.connect()
        d.addCallback(self.getServers)
        d.addCallback(self.getDevices)
        d.addCallback(self.initializeGUI)

    @inlineCallbacks
    def connect(self):
        if not self.cxn:
            import os
            LABRADHOST = os.environ['LABRADHOST']
            from labrad.wrappers import connectAsync
            self.cxn = yield connectAsync(LABRADHOST, name=self.name)
        return self.cxn

    @inlineCallbacks
    def getServers(self, cxn):
        """
        Get required labrad servers.
        """
        try:
            self.reg = self.cxn.registry
            self.dv = self.cxn.data_vault
            self.artiq = self.cxn.artiq_server
        except Exception as e:
            print(e)
            raise

        #add listener to moninj
        yield self.artiq.signal__ttl_changed(self.TTLID)
        yield self.artiq.addListener(listener=self.updateTTLDisplay, source=None, ID=self.TTLID)
        return self.cxn

    def updateTTLDisplay(self, c, ttl_name, probe, status):
        print('yzde: ' + ttl_name + ', ' + str(probe))
        if probe == 0:
            self.ttl_clients[ttl_name].lockswitch.setText('scde')

    def getDevices(self, cxn):
        """
        Get devices from ARTIQ server and organize them.
        """
        # create holding lists
        self.ttlin_list = []
        self.ttlout_list = []
        self.ttlurukul_list = []
        self.ttlother_list = []
        for name, params in device_db.items():
            # only get devices with named class
            if 'class' not in params:
                continue
            # set device as attribute
            devicetype = params['class']
            if devicetype == 'TTLInOut':
                self.ttlin_list.append(name)
            elif devicetype == 'TTLOut':
                other_names = ['zotino', 'led', 'sampler']
                if 'urukul' in name:
                    self.ttlurukul_list.append(name)
                elif any(string in name for string in other_names):
                    self.ttlother_list.append(name)
                else:
                    self.ttlout_list.append(name)
        return self.cxn

    def initializeGUI(self, cxn):
        layout = QGridLayout()
        # set title
        title = QLabel(self.name)
        title.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setMargin(4)
        layout.addWidget(title, 0, 0, 1, 10)
        # create and layout widgets
        in_ttls = self._makeTTLGroup(self.ttlin_list, "Input")
        layout.addWidget(in_ttls, 2, 0, 2, 4)
        out_ttls = self._makeTTLGroup(self.ttlout_list, "Output")
        layout.addWidget(out_ttls, 5, 0, 3, 10)
        urukul_ttls = self._makeTTLGroup(self.ttlurukul_list, "Urukul")
        layout.addWidget(urukul_ttls, 9, 0, 3, 10)
        other_ttls = self._makeTTLGroup(self.ttlother_list, "Other")
        layout.addWidget(other_ttls, 13, 0, 2, 5)
        self.setLayout(layout)

    def _makeTTLGroup(self, ttl_list, name):
        """
        Creates a group of TTLs as a widget.
        """
        #create widget
        ttl_group = QFrame()
        ttl_group.setFrameStyle(0x0001 | 0x0010)
        ttl_group.setLineWidth(2)
        layout = QGridLayout()
        #set title
        title = QLabel(name)
        title.setFont(QFont('MS Shell Dlg 2', pointSize=13))
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title, 0, 0)
        #layout individual ttls on group
        for i in range(len(ttl_list)):
            # initialize GUIs for each channel
            channel_name = ttl_list[i]
            channel_gui = TTL_channel(channel_name)
            # layout channel GUI
            row = int(i / (self.row_length)) + 2
            column = i % (self.row_length)
            # connect signals to slots
            channel_gui.toggle.toggled.connect(lambda status, chan=channel_name: self.toggleSwitch(chan, status))
            # add widget to client list and layout
            self.ttl_clients[channel_name] = channel_gui
            layout.addWidget(channel_gui, row, column)
            #print(name + ' - row:' + str(row) + ', column: ' + str(column))
        ttl_group.setLayout(layout)
        return ttl_group

    @inlineCallbacks
    def toggleSwitch(self, channel_name, status):
        yield self.artiq.ttl_set(channel_name, status)

    def closeEvent(self, x):
        self.cxn.disconnect()
        if self.reactor.running:
            self.reactor.stop()

if __name__ == "__main__":
    #run channel GUI
    # from EGGS_labrad.lib.clients import runGUI
    # runGUI(TTL_channel, name='TTL Channel')

    #run TTL GUI
    from EGGS_labrad.lib.clients import runClient
    runClient(TTL_client)