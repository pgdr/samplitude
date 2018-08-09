import math

def sinegenerator(rate):
    num = 0
    while True:
        yield math.sin(num*rate)
        num += 1

def cosinegenerator(rate):
    num = 0
    while True:
        yield math.cos(num*rate)
        num += 1

def tangenerator(rate):
    num = 0
    while True:
        yield math.tan(num*rate)
        num += 1
