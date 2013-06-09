UsbIOCard-WoodChipBurnerSoftware
================================

Wood chip burner controller software. Originally meant to use with RaspBerry-Pi, but is usable with any Windows/Linux machine.

In dev enviroment there were major issues with gevent/greenlet. They were fixed by updating Python to version 2.7.5.

In pycharm, change:
SUPPORT_GEVENT = True