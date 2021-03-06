#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: check_lucit_collector.py
#
# Part of ‘check_lucit_collector’
# Project website: https://github.com/LUCIT-Development/check_lucit_collector.py
#
# Author: LUCIT
#         https://www.lucit.co
#
# Copyright (c) 2020, LUCIT
# All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from argparse import ArgumentParser
import argparse
import requests
import textwrap
import time
import urllib3

VERSION = "0.1.0"


def status_unkown():
    print("SERVICE STATUS - UNKNOWN: not connected!")
    exit(3)


parser = ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                        description=textwrap.dedent("ICINGA/Nagios compatible check_command to collect data from REST APIs"))
parser.add_argument('-H', '--hostname', dest='hostname', help='host name or ip address (default: 127.0.0.1)',
                    default="127.0.0.1")
parser.add_argument('-P', '--port', dest='port', help='port number (default: 64201)', default=64201)
parser.add_argument('-R', dest='req_cert', help='Require a valid certificate (use with -S)', action="store_true")
parser.add_argument('-S', '--ssl', dest='ssl', help='use https prefix instead of http', action="store_true")
parser.add_argument('-V', '--version', dest='version', help='print version information', action="store_true")
parsed_args = parser.parse_args()

if parsed_args.version is True:
    print("check_lucit_collector.py " + VERSION + " for ICINGA/Nagios by LUCIT 2020 - " +
          time.strftime("%Y"))
    exit(0)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if parsed_args.ssl is True:
    protocol = "https"
else:
    protocol = "http"

if parsed_args.req_cert is True:
    verify = True
else:
    verify = False

try:
    respond = requests.get(protocol + '://' + str(parsed_args.hostname) + ':' +
                           str(parsed_args.port) + '/status/icinga/' + str(VERSION), verify=verify)
    status = respond.json()
    if status['text']:
        print(status['text'])
        exit(status['return_code'])
    else:
        status_unkown()
except requests.exceptions.ConnectionError:
    status_unkown()
except KeyError:
    status_unkown()
