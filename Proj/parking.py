#!/usr/bin/env python

import sys
import time
from tinyos import tos

AM_OSCILLOSCOPE = 0x93

class OscilloscopeMsg(tos.Packet):
    def __init__(self, packet = None):
        tos.Packet.__init__(self,
                            [('version',  'int', 2),
                             ('interval', 'int', 2),
                             ('id',       'int', 2),
                             ('count',    'int', 2),
                             ('readings', 'blob', None)],
                            packet)
if '-h' in sys.argv:
    print "Usage:", sys.argv[0], "serial@/dev/ttyUSB0:57600"
    sys.exit()

am = tos.AM()
threshold = 550
occupied = dict()
prevReading = dict()
cnt = dict()

start = time.time()

while True:
    p = am.read()
    if p and p.type == AM_OSCILLOSCOPE:
        msg = OscilloscopeMsg(p.data)

        nodeID = msg.id
        count = msg.count
        readings = [i<<8 | j for (i,j) in zip(msg.readings[::2], msg.readings[1::2])]

        print nodeID, count, readings

        if nodeID not in occupied:
            occupied[nodeID] = False
            prevReading[nodeID] = 0
            cnt[nodeID] = 0

        maxReading = max(readings)

        print maxReading, prevReading[nodeID]

        if not occupied[nodeID]:
            if (maxReading > threshold) and (prevReading[nodeID] < threshold):
                occupied[nodeID] = True
        else :
            if (maxReading > threshold) and (prevReading[nodeID] < threshold):
                occupied[nodeID] = False

        prevReading[nodeID]=maxReading

        print (time.time()-start)
        for i, k in occupied.items():
            print i, k
