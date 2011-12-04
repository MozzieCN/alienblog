#!/usr/bin/env python

# -*- coding: utf-8 -*-
# Name:     qrcode.py
# Author:   xiooli <xioooli[at]yahoo.com.cn>
# Site:     http://joolix.com
# Licence:  GPLv3
# Version:  100104
import PyQrcodec as pqr
import sys
def gen_qrpic(text, file):
    print dir(pqr)
    stat, img = pqr.encode(text,image_width=200,version=5)
    if stat:
        img.save(file)
        return file
    else:
        print "failed to generate qrcode picture."
def qrdecode(file):
    stat, text = pqr.decode(file)
    if stat:
        return text
    else:
        print "failed to decode the qrcode picture."
if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1 :
        print "encode: " + args[0] + " -e [text] [image file]"
        print "decode: " + args[0] + " -d [imgae file]"
    elif args[1] == '-e':
        try:
            print "generated file: " + gen_qrpic(args[2],args[3])
        except :
            pass
    elif args[1] == '-d':
        try:
            print "get text: " + qrdecode(args[2])
        except:
            pass
    else:
        print 'unrecoded arguments'
