import signal

import dbus
import waiting
from functools import partial
from waiting import TimeoutExpired

from bluetool.agent import Client, _bluetooth, Agent
from bluetool.utils import print_error
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
from socketIO_client import SocketIO, BaseNamespace


class partialmethod(partial):
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return partial(self.func, instance,
                       *(self.args or ()), **(self.keywords or {}))


def partialclass(cls, *args, **kwds):
    class NewCls(cls):
        __init__ = partialmethod(cls.__init__, *args, **kwds)

    return NewCls


class ParingNamespace(BaseNamespace):
    def __init__(self, var, *args, **kwargs):
        self.var = var
        super(ParingNamespace, self).__init__(*args, **kwargs)

    def on_pair_response(self, *data):
        print "callback received!"
        print data
        self.var["accepted"] = data[0]["accepted"]


class MyClient(Client):
    def __init__(self, *args, **kwargs):
        super(MyClient, self).__init__(*args, **kwargs)
        print("print running")

    def request_pin_code(self, dev_info):
        print(dev_info)
        return raw_input("Input pin code:")

    def request_passkey(self, dev_info):
        print(dev_info)
        return raw_input("Input passkey:")

    def request_confirmation(self, dev_info, *args):
        print "new request received! {}".format(dev_info)
        address = dev_info["mac_address"]
        data = {
            "mac_address": address,
            "name": dev_info["name"],
            "pin_code": args
        }
        var = {
            "accepted": None
        }
        socketIO = SocketIO("localhost", 8080)
        try:

            def wait_for_response():
                socketIO.wait(1)
                return var["accepted"] is not None

            pair_namespace = socketIO.define(partialclass(ParingNamespace, var),
                                             "/pair")
            pair_namespace.emit("pair", data)
            waiting.wait(wait_for_response, timeout_seconds=30)
            return var["accepted"]

        except TimeoutExpired:
            return False

        finally:
            print "stopped waiting!"
            socketIO.disconnect()

    def request_authorization(self, dev_info):
        print(dev_info)
        return raw_input("Input 'yes' to accept request:") == "yes"


class AgentSvr(object):

    def __init__(
            self, client_class, timeout=180, capability="KeyboardDisplay",
            path="/org/bluez/my_bluetooth_agent"):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        self.client_class = client_class
        self.timeout = timeout
        self.capability = capability
        self.path = path
        self._bus = dbus.SystemBus()
        self._mainloop = GObject.MainLoop()
        _bluetooth.make_discoverable(False)

    def run(self):
        # _bluetooth.make_discoverable(True, self.timeout)
        _bluetooth.set_adapter_property("Pairable", dbus.Boolean(1))
        _bluetooth.set_adapter_property("PairableTimeout", dbus.UInt32(0))
        self.agent = Agent(self.client_class, self.timeout, self.path)

        if not self._register():
            self.shutdown()
            return

        self._mainloop.run()

    def _register(self):
        try:
            manager = dbus.Interface(
                self._bus.get_object("org.bluez", "/org/bluez"),
                "org.bluez.AgentManager1")
            manager.RegisterAgent(self.path, self.capability)
            manager.RequestDefaultAgent(self.path)
        except dbus.exceptions.DBusException as error:
            print_error(str(error) + "\n")
            return False

        return True

    def shutdown(self):
        # _bluetooth.make_discoverable(False)
        self._mainloop.quit()
        self._unregister()

        try:
            self.agent.remove_from_connection()
            del self.agent
        except AttributeError:
            pass

    def _unregister(self):
        try:
            manager = dbus.Interface(
                self._bus.get_object("org.bluez", "/org/bluez"),
                "org.bluez.AgentManager1")
            manager.UnregisterAgent(self.path)
        except dbus.exceptions.DBusException:
            pass


def handler(svr, signum, frame):
    svr.shutdown()


def run_agent():
    svr = AgentSvr(client_class=MyClient)

    signal.signal(signal.SIGINT, partial(handler, svr))
    signal.signal(signal.SIGTERM, partial(handler, svr))

    svr.run()


if __name__ == '__main__':
    run_agent()
