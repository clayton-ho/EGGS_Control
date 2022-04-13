"""
Measure a value from the oscope.
"""

import labrad
from time import time, sleep
from datetime import datetime
import pyvisa

# get device
rm = pyvisa.ResourceManager()
lr = rm.list_resources()
oscope = rm.open_resource(lr[0])
oscope.write(":MEAS:ITEM VAMP,CHAN1")

# connect to eggs labrad
cxn_eggs = labrad.connect('localhost', password='lab')
dv = cxn_eggs.data_vault
cr_dv = cxn_eggs.context()

# create dataset
date = datetime.now()
year = str(date.year)
month = '{:02d}'.format(date.month)
trunk1 = '{0:s}_{1:s}_{2:02d}'.format(year, month, date.day)
trunk2 = '{0:s}_{1:02d}:{2:02d}'.format('397 Measure', date.hour, date.minute)
dv.cd(['', year, month, trunk1, trunk2], True, context=cr_dv)
dv.new('Rigol Can - tmp', [('Elapsed time', 's')], [('Channel 1', 'Signal Amplitude', 'V')], context=cr_dv)

# start recording
starttime = time()
while True:
    vamp = oscope.query(":MEAS:ITEM? VAMP,CHAN1")
    elapsedtime = time() - starttime
    dv.add(elapsedtime, vamp, context=cr_dv)
    sleep(5)
