@ECHO OFF

start "GPIB Bus Server" /min cmd "/k activate labart && python %HOME%/Code/EGGS_labrad/lib/servers/gpib/gpib_bus_server.py"
start "GPIB Device Manager" /min cmd "/k activate labart && python %HOME%/Code/EGGS_labrad/lib/servers/gpib/gpib_device_manager.py"
start "Serial Server" /min cmd "/k activate labart && python %HOME%/Code/EGGS_labrad/lib/servers/serial/serial_server.py"