#!/usr/bin/env python
with open('road-segments.txt', 'r') as f:
    speed = 0.0
    distance = 0.0
    count_s, count_d = 0, 0
    for line in f:
        val = line.split(' ')
        if val[3] is not None and val[3] is not "":
            speed += float(val[3])
            count_s += 1.0
        if val[2] is not None and val[2] is not "":
            distance += float(val[2])
            count_d += 1.0
    print "avg speed", speed / count_s
    print "avg miles on road", distance / count_d
        

