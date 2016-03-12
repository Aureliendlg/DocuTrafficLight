#!/usr/bin/python2

import argparse
import os
import time
import RPi.GPIO as GPIO

if os.getuid() != 0:
    raise SystemExit('Expecting root privileges. Root privileges needed for GPIO pin usage.')

parser = argparse.ArgumentParser(description = 'Control Traffic Signal State')
parser.add_argument('color', choices = ['RED', 'YLLW', 'GRN'], help = 'Color of light')
parser.add_argument('state', choices = ['on', 'off', 'blink'], help = 'State of light')
parser.add_argument('--verbose', '-v', action = 'store_true')
args = parser.parse_args()

if args.verbose:
    print('Setting ' + args.color + " light to " + args.state + ".")

# Determine the GPIO pin
if args.color == 'RED':
    pin = 25
elif args.color == 'YLLW':
    pin = 24
elif args.color == 'GRN':
    pin = 18
else:
    raise SystemExit('Bad color specified.')

# Determine the state
if args.state == 'on':
    state = 1
elif args.state == 'off':
    state = 0
else:
    raise SystemExit('Bad state specified.')

# Set up the GPIO interface
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Trigger the GPIO output
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, state)
