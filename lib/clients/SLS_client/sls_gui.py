# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sls_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets


class SLS_gui(QWidget):
    def setupUi(self):
        SLS_gui = self
        SLS_gui.setObjectName("SLS_gui")
        SLS_gui.resize(595, 515)
        self.PDH_label = QtWidgets.QLabel(SLS_gui)
        self.PDH_label.setGeometry(QtCore.QRect(270, 140, 41, 31))
        self.PDH_label.setObjectName("PDH_label")
        self.servo_label = QtWidgets.QLabel(SLS_gui)
        self.servo_label.setGeometry(QtCore.QRect(440, 140, 101, 31))
        self.servo_label.setObjectName("servo_label")
        self.autolock_label = QtWidgets.QLabel(SLS_gui)
        self.autolock_label.setGeometry(QtCore.QRect(60, 140, 81, 31))
        self.autolock_label.setObjectName("autolock_label")
        self.sls_label = QtWidgets.QLabel(SLS_gui)
        self.sls_label.setGeometry(QtCore.QRect(170, 10, 271, 41))
        self.sls_label.setObjectName("sls_label")
        self.frequency = QtWidgets.QLabel(SLS_gui)
        self.frequency.setGeometry(QtCore.QRect(130, 60, 321, 71))
        self.frequency.setObjectName("frequency")
        self.lockswitch = QtWidgets.QPushButton(SLS_gui)
        self.lockswitch.setGeometry(QtCore.QRect(220, 430, 151, 23))
        self.lockswitch.setObjectName("lockswitch")
        self.widget = QtWidgets.QWidget(SLS_gui)
        self.widget.setGeometry(QtCore.QRect(220, 180, 151, 234))
        self.widget.setObjectName("widget")
        self.PDH_layout = QtWidgets.QGridLayout(self.widget)
        self.PDH_layout.setContentsMargins(0, 0, 0, 0)
        self.PDH_layout.setObjectName("PDH_layout")
        self.PDH_phaseoffset = QtWidgets.QDoubleSpinBox(self.widget)
        self.PDH_phaseoffset.setMaximum(360.0)
        self.PDH_phaseoffset.setSingleStep(0.1)
        self.PDH_phaseoffset.setObjectName("PDH_phaseoffset")
        self.PDH_layout.addWidget(self.PDH_phaseoffset, 5, 1, 1, 1)
        self.PDH_filter = QtWidgets.QComboBox(self.widget)
        self.PDH_filter.setObjectName("PDH_filter")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_filter.addItem("")
        self.PDH_layout.addWidget(self.PDH_filter, 7, 1, 1, 1)
        self.PDH_phasemodulation = QtWidgets.QDoubleSpinBox(self.widget)
        self.PDH_phasemodulation.setMaximum(3.0)
        self.PDH_phasemodulation.setSingleStep(0.1)
        self.PDH_phasemodulation.setObjectName("PDH_phasemodulation")
        self.PDH_layout.addWidget(self.PDH_phasemodulation, 3, 1, 1, 1)
        self.autolock_toggle_2 = QtWidgets.QPushButton(self.widget)
        self.autolock_toggle_2.setObjectName("autolock_toggle_2")
        self.PDH_layout.addWidget(self.autolock_toggle_2, 8, 1, 1, 1)
        self.PDH_phasemodulation_label = QtWidgets.QLabel(self.widget)
        self.PDH_phasemodulation_label.setObjectName("PDH_phasemodulation_label")
        self.PDH_layout.addWidget(self.PDH_phasemodulation_label, 2, 1, 1, 1)
        self.PDH_freq_label = QtWidgets.QLabel(self.widget)
        self.PDH_freq_label.setObjectName("PDH_freq_label")
        self.PDH_layout.addWidget(self.PDH_freq_label, 0, 1, 1, 1)
        self.PDH_phaseoffset_label = QtWidgets.QLabel(self.widget)
        self.PDH_phaseoffset_label.setObjectName("PDH_phaseoffset_label")
        self.PDH_layout.addWidget(self.PDH_phaseoffset_label, 4, 1, 1, 1)
        self.PDH_filter_label = QtWidgets.QLabel(self.widget)
        self.PDH_filter_label.setObjectName("PDH_filter_label")
        self.PDH_layout.addWidget(self.PDH_filter_label, 6, 1, 1, 1)
        self.PDH_freq = QtWidgets.QDoubleSpinBox(self.widget)
        self.PDH_freq.setMinimum(10.0)
        self.PDH_freq.setMaximum(35.0)
        self.PDH_freq.setSingleStep(0.1)
        self.PDH_freq.setObjectName("PDH_freq")
        self.PDH_layout.addWidget(self.PDH_freq, 1, 1, 1, 1)
        self.widget1 = QtWidgets.QWidget(SLS_gui)
        self.widget1.setGeometry(QtCore.QRect(420, 180, 150, 311))
        self.widget1.setObjectName("widget1")
        self.servo_layout = QtWidgets.QGridLayout(self.widget1)
        self.servo_layout.setContentsMargins(0, 0, 0, 0)
        self.servo_layout.setObjectName("servo_layout")
        self.servo_p = QtWidgets.QDoubleSpinBox(self.widget1)
        self.servo_p.setMaximum(10000.0)
        self.servo_p.setObjectName("servo_p")
        self.servo_layout.addWidget(self.servo_p, 3, 1, 1, 1)
        self.servo_d = QtWidgets.QDoubleSpinBox(self.widget1)
        self.servo_d.setMaximum(1000.0)
        self.servo_d.setObjectName("servo_d")
        self.servo_layout.addWidget(self.servo_d, 7, 1, 1, 1)
        self.servo_filter = QtWidgets.QComboBox(self.widget1)
        self.servo_filter.setObjectName("servo_filter")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_filter.addItem("")
        self.servo_layout.addWidget(self.servo_filter, 11, 1, 1, 1)
        self.servo_i = QtWidgets.QDoubleSpinBox(self.widget1)
        self.servo_i.setMaximum(1.0)
        self.servo_i.setSingleStep(0.01)
        self.servo_i.setObjectName("servo_i")
        self.servo_layout.addWidget(self.servo_i, 5, 1, 1, 1)
        self.servo_set = QtWidgets.QDoubleSpinBox(self.widget1)
        self.servo_set.setMinimum(-1000000.0)
        self.servo_set.setMaximum(1000000.0)
        self.servo_set.setObjectName("servo_set")
        self.servo_layout.addWidget(self.servo_set, 9, 1, 1, 1)
        self.servo_param = QtWidgets.QComboBox(self.widget1)
        self.servo_param.setObjectName("servo_param")
        self.servo_param.addItem("")
        self.servo_param.addItem("")
        self.servo_param.addItem("")
        self.servo_layout.addWidget(self.servo_param, 1, 1, 1, 1)
        self.autolock_toggle_3 = QtWidgets.QPushButton(self.widget1)
        self.autolock_toggle_3.setObjectName("autolock_toggle_3")
        self.servo_layout.addWidget(self.autolock_toggle_3, 13, 1, 1, 1)
        self.servo_param_label = QtWidgets.QLabel(self.widget1)
        self.servo_param_label.setObjectName("servo_param_label")
        self.servo_layout.addWidget(self.servo_param_label, 0, 1, 1, 1)
        self.servo_p_label = QtWidgets.QLabel(self.widget1)
        self.servo_p_label.setObjectName("servo_p_label")
        self.servo_layout.addWidget(self.servo_p_label, 2, 1, 1, 1)
        self.servo_i_label = QtWidgets.QLabel(self.widget1)
        self.servo_i_label.setObjectName("servo_i_label")
        self.servo_layout.addWidget(self.servo_i_label, 4, 1, 1, 1)
        self.servo_d_label = QtWidgets.QLabel(self.widget1)
        self.servo_d_label.setObjectName("servo_d_label")
        self.servo_layout.addWidget(self.servo_d_label, 6, 1, 1, 1)
        self.servo_set_label = QtWidgets.QLabel(self.widget1)
        self.servo_set_label.setObjectName("servo_set_label")
        self.servo_layout.addWidget(self.servo_set_label, 8, 1, 1, 1)
        self.servo_filter_label = QtWidgets.QLabel(self.widget1)
        self.servo_filter_label.setObjectName("servo_filter_label")
        self.servo_layout.addWidget(self.servo_filter_label, 10, 1, 1, 1)
        self.widget2 = QtWidgets.QWidget(SLS_gui)
        self.widget2.setGeometry(QtCore.QRect(20, 180, 151, 251))
        self.widget2.setObjectName("widget2")
        self.autolock_layout = QtWidgets.QGridLayout(self.widget2)
        self.autolock_layout.setContentsMargins(0, 0, 0, 0)
        self.autolock_layout.setObjectName("autolock_layout")
        self.autolock_toggle = QtWidgets.QPushButton(self.widget2)
        self.autolock_toggle.setObjectName("autolock_toggle")
        self.autolock_layout.addWidget(self.autolock_toggle, 6, 1, 1, 1)
        self.autolock_param = QtWidgets.QComboBox(self.widget2)
        self.autolock_param.setObjectName("autolock_param")
        self.autolock_param.addItem("")
        self.autolock_param.addItem("")
        self.autolock_param.addItem("")
        self.autolock_layout.addWidget(self.autolock_param, 8, 1, 1, 1)
        self.autolock_attempts = QtWidgets.QLabel(self.widget2)
        self.autolock_attempts.setObjectName("autolock_attempts")
        self.autolock_layout.addWidget(self.autolock_attempts, 4, 1, 1, 1)
        self.autolock_attempts_label = QtWidgets.QLabel(self.widget2)
        self.autolock_attempts_label.setObjectName("autolock_attempts_label")
        self.autolock_layout.addWidget(self.autolock_attempts_label, 3, 1, 1, 1)
        self.autolock_toggle_label = QtWidgets.QLabel(self.widget2)
        self.autolock_toggle_label.setObjectName("autolock_toggle_label")
        self.autolock_layout.addWidget(self.autolock_toggle_label, 5, 1, 1, 1)
        self.autolock_time_label = QtWidgets.QLabel(self.widget2)
        self.autolock_time_label.setObjectName("autolock_time_label")
        self.autolock_layout.addWidget(self.autolock_time_label, 0, 1, 1, 1)
        self.autolock_time = QtWidgets.QLabel(self.widget2)
        self.autolock_time.setObjectName("autolock_time")
        self.autolock_layout.addWidget(self.autolock_time, 1, 1, 2, 1)
        self.PDH_phasemodulation_label_4 = QtWidgets.QLabel(self.widget2)
        self.PDH_phasemodulation_label_4.setObjectName("PDH_phasemodulation_label_4")
        self.autolock_layout.addWidget(self.PDH_phasemodulation_label_4, 7, 1, 1, 1)

        self.retranslateUi(SLS_gui)
        QtCore.QMetaObject.connectSlotsByName(SLS_gui)

    def retranslateUi(self, SLS_gui):
        _translate = QtCore.QCoreApplication.translate
        SLS_gui.setWindowTitle(_translate("SLS_gui", "Form"))
        self.PDH_label.setText(_translate("SLS_gui", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">PDH</span></p></body></html>"))
        self.servo_label.setText(_translate("SLS_gui", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Servo PID</span></p></body></html>"))
        self.autolock_label.setText(_translate("SLS_gui", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Autolock</span></p></body></html>"))
        self.sls_label.setText(_translate("SLS_gui", "<html><head/><body><p align=\"center\"><span style=\" font-size:26pt;\">SLS Laser Client</span></p></body></html>"))
        self.frequency.setText(_translate("SLS_gui", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#ff0000;\">Frequency</span></p></body></html>"))
        self.lockswitch.setText(_translate("SLS_gui", "Lock"))
        self.PDH_filter.setItemText(0, _translate("SLS_gui", "None"))
        self.PDH_filter.setItemText(1, _translate("SLS_gui", "1"))
        self.PDH_filter.setItemText(2, _translate("SLS_gui", "2"))
        self.PDH_filter.setItemText(3, _translate("SLS_gui", "3"))
        self.PDH_filter.setItemText(4, _translate("SLS_gui", "4"))
        self.PDH_filter.setItemText(5, _translate("SLS_gui", "5"))
        self.PDH_filter.setItemText(6, _translate("SLS_gui", "6"))
        self.PDH_filter.setItemText(7, _translate("SLS_gui", "7"))
        self.PDH_filter.setItemText(8, _translate("SLS_gui", "8"))
        self.PDH_filter.setItemText(9, _translate("SLS_gui", "9"))
        self.PDH_filter.setItemText(10, _translate("SLS_gui", "10"))
        self.PDH_filter.setItemText(11, _translate("SLS_gui", "11"))
        self.PDH_filter.setItemText(12, _translate("SLS_gui", "12"))
        self.PDH_filter.setItemText(13, _translate("SLS_gui", "13"))
        self.PDH_filter.setItemText(14, _translate("SLS_gui", "14"))
        self.PDH_filter.setItemText(15, _translate("SLS_gui", "15"))
        self.PDH_filter.setItemText(16, _translate("SLS_gui", "16"))
        self.autolock_toggle_2.setText(_translate("SLS_gui", "Update"))
        self.PDH_phasemodulation_label.setText(_translate("SLS_gui", "Phase modulation (rad)"))
        self.PDH_freq_label.setText(_translate("SLS_gui", "Frequency (MHz)"))
        self.PDH_phaseoffset_label.setText(_translate("SLS_gui", "Reference phase (deg)"))
        self.PDH_filter_label.setText(_translate("SLS_gui", "Filter Index"))
        self.servo_filter.setItemText(0, _translate("SLS_gui", "None"))
        self.servo_filter.setItemText(1, _translate("SLS_gui", "1"))
        self.servo_filter.setItemText(2, _translate("SLS_gui", "2"))
        self.servo_filter.setItemText(3, _translate("SLS_gui", "3"))
        self.servo_filter.setItemText(4, _translate("SLS_gui", "4"))
        self.servo_filter.setItemText(5, _translate("SLS_gui", "5"))
        self.servo_filter.setItemText(6, _translate("SLS_gui", "6"))
        self.servo_filter.setItemText(7, _translate("SLS_gui", "7"))
        self.servo_filter.setItemText(8, _translate("SLS_gui", "8"))
        self.servo_filter.setItemText(9, _translate("SLS_gui", "9"))
        self.servo_filter.setItemText(10, _translate("SLS_gui", "10"))
        self.servo_filter.setItemText(11, _translate("SLS_gui", "11"))
        self.servo_filter.setItemText(12, _translate("SLS_gui", "12"))
        self.servo_filter.setItemText(13, _translate("SLS_gui", "13"))
        self.servo_filter.setItemText(14, _translate("SLS_gui", "14"))
        self.servo_filter.setItemText(15, _translate("SLS_gui", "15"))
        self.servo_filter.setItemText(16, _translate("SLS_gui", "16"))
        self.servo_param.setItemText(0, _translate("SLS_gui", "Current"))
        self.servo_param.setItemText(1, _translate("SLS_gui", "PZT"))
        self.servo_param.setItemText(2, _translate("SLS_gui", "TX"))
        self.autolock_toggle_3.setText(_translate("SLS_gui", "Update"))
        self.servo_param_label.setText(_translate("SLS_gui", "Parameter"))
        self.servo_p_label.setText(_translate("SLS_gui", "Proportional"))
        self.servo_i_label.setText(_translate("SLS_gui", "Integral"))
        self.servo_d_label.setText(_translate("SLS_gui", "Differential"))
        self.servo_set_label.setText(_translate("SLS_gui", "Setpoint"))
        self.servo_filter_label.setText(_translate("SLS_gui", "Filter Index"))
        self.autolock_toggle.setText(_translate("SLS_gui", "On"))
        self.autolock_param.setItemText(0, _translate("SLS_gui", "Current"))
        self.autolock_param.setItemText(1, _translate("SLS_gui", "PZT"))
        self.autolock_param.setItemText(2, _translate("SLS_gui", "TX"))
        self.autolock_attempts.setText(_translate("SLS_gui", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; color:#0055ff;\">Attempts</span></p></body></html>"))
        self.autolock_attempts_label.setText(_translate("SLS_gui", "Lock Attempts"))
        self.autolock_toggle_label.setText(_translate("SLS_gui", "Autolock"))
        self.autolock_time_label.setText(_translate("SLS_gui", "Lock Time"))
        self.autolock_time.setText(_translate("SLS_gui", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; color:#0055ff;\">Time</span></p></body></html>"))
        self.PDH_phasemodulation_label_4.setText(_translate("SLS_gui", "Sweep Parameter"))

if __name__=="__main__":
    from EGGS_labrad.lib.clients import runGUI
    runGUI(SLS_gui)