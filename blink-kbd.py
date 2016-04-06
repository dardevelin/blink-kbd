#!/bin/env python

#### yes python is supreme and comes first
# blink-kbd.py
# This file is a plugin for the irc hexchat client that makes the keyboard
# backlight blink once it has received a notification/highlight
# Copyright (C) 2015  Darcy Bras da Silva
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/


from __future__ import print_function

import os
from time import sleep
import hexchat
try:
    import thread
except ImportError:
    # we are probably using python 3 only
    import _thread as thread

__module_name__ = "kbd notify"
__module_version__ = "1.1"
__module_description__ = "Blinks the keyboard backlight on notifications"
__module_author__ = "Darcy 'dardevelin' Bras da Silva"

#None, True, False
kbd_status = None
kbd_light = False
configdir = hexchat.get_info('configdir')
thread_active = False

def on():
    global kbd_light
    if False == kbd_light:
        os.system('{}/addons/blink-kbd/lightcontroler.sh up'.format(configdir))
        kbd_light = True
    
def off():
    global kbd_light
    if True == kbd_light:
        os.system('{}/addons/blink-kbd/lightcontroler.sh down'.format(configdir))
        kbd_light = False


def blink(n, state=False):
    global thread_active
    global kbd_light
    
    idx = 0
    while idx < n:
        on()
        sleep(1)
        off()
        sleep(1)
        idx = idx + 1

    if True == state:
        on()

    thread_active = False

def dispatcher(word, word_eol, userdata):
    global thread_active
    global kbd_status

    # surpress any action if the plugin is suspended
    if False == kbd_status:
        return

    # don't blink the keyboard if we are looking at the client
    w_status = hexchat.get_info("win_status")
    if 'active' == str(w_status).lower():
        return
    
    if not thread_active:
        thread_active = True
        # we spawn a thread to not lock the client waiting
        # the blinking effect to finish
        thread.start_new_thread(blink, (3, True,))

    return hexchat.EAT_NONE

def consume_notification(i, ii):
    global thread_active

    # run endlessly until an opportunity is found to turn it off
    while True:
        if False == thread_active:
            sleep(1)
            off()
            break
        sleep(1)

def notification_checked(word, word_eol, userdata):
    global thread_active
    global kbd_status
    
    # surpress any action if the plugin is suspended
    if False == kbd_status:
        return
    
    # this tells that we have seen the notification and turns
    # off the light, however  we need to wait until
    # it finishes blinking, otherwise it will just be an off()
    # out of 'the blink set'
    if False == thread_active:
        # already stopped, just turn it off
        off()
    else:
        # don't lock the client for this. make a worker
        thread.start_new_thread(consume_notification, (None,None))

def unload_cb(userdata):
    print("\0034 {} {} {}".format(__module_name__, __module_version__, "has been unloaded\003"))

def toggle_kbd(word, word_eol, userdata):
    global kbd_status
    
    if kbd_status == True:
        kbd_status = False
    else:
        kbd_status = True

    if kbd_status == True:
        hexchat.prnt("kbd-light is now at full speed")
    else:
        hexchat.prnt("kbd-light is now suspended")

def on_init_cb():
    global kbd_status
    kbd_status = True
    hexchat.hook_print("Channel Msg Hilight", dispatcher, None, hexchat.PRI_LOWEST)
    hexchat.hook_print("Focus Window", notification_checked, None, hexchat.PRI_LOWEST)
    hexchat.hook_unload(unload_cb)
    hexchat.hook_command("kbdlight", toggle_kbd)
    print("\0034 {} {} {}".format(__module_name__, __module_version__,"has been loaded\003"))

on_init_cb()
