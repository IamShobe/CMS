#!/usr/bin/python

from __future__ import print_function, unicode_literals

from optparse import OptionParser
import sys
import dbus
import dbus.service
import dbus.mainloop.glib

try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

import bluezutils

BUS_NAME = 'org.bluez'
AGENT_INTERFACE = 'org.bluez.Agent1'
AGENT_PATH = "/test/agent"

bus = None
device_obj = None
dev_path = None



if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    capability = "KeyboardDisplay"

    parser = OptionParser()
    parser.add_option("-i", "--adapter", action="store",
                      type="string",
                      dest="adapter_pattern",
                      default=None)
    parser.add_option("-c", "--capability", action="store",
                      type="string", dest="capability")
    parser.add_option("-t", "--timeout", action="store",
                      type="int", dest="timeout",
                      default=60000)
    (options, args) = parser.parse_args()
    if options.capability:
        capability = options.capability

    path = "/test/agent"
    agent = Agent(bus, path)

    obj = bus.get_object(BUS_NAME, "/org/bluez")
    manager = dbus.Interface(obj, "org.bluez.AgentManager1")
    manager.RegisterAgent(path, "KeyboardDisplay")

    print("Agent registered")

    device = bluezutils.find_device("C0:EE:FB:D5:FC:A2")
    dev_path = device.object_path
    agent.set_exit_on_release(False)
    device.Pair(reply_handler=pair_reply, error_handler=pair_error,
                timeout=60000)
    device_obj = device

    mainloop.run()

# adapter.UnregisterAgent(path)
# print("Agent unregistered")
