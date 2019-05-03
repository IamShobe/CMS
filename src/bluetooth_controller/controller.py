import time
import logging
from logging import getLogger

import bluetooth
from backports.functools_lru_cache import lru_cache
from bluetool import Bluetooth
from cached_property import cached_property

from logger.logger import paint_logger

from .utils import fix_keys
from .protocols.hfp.controller import HFPController
from .protocols.pbap.controller import PBAPController
from .protocols.avctp.controller import AVCTPController

logger = getLogger("Bluetooth")
logger.setLevel(logging.DEBUG)


class Service(object):
    def __init__(self, protocol, name, service_id, profiles,
                 service_classes, host, provider, port,
                 description):
        self.protocol = protocol
        self.name = name
        self.service_id = service_id
        self.profiles = profiles
        self.service_classes = service_classes
        self.host = host
        self.provider = provider
        self.port = port
        self.description = description

    def to_dict(self):
        return {
            "protocol": self.protocol,
            "name": self.name,
            "service_id": self.service_id,
            "profiles": self.profiles,
            "service_classes": self.service_classes,
            "host": self.host,
            "provider": self.provider,
            "port": self.port,
            "description": self.description,
        }

    def __repr__(self):
        return "{}(name={!r}, protocol={!r}, port={}, classes={!r})".format(
            self.__class__.__name__, self.name, self.protocol, self.port,
            self.service_classes)


class BTDevice(object):
    SERVICES_SCAN_TRIES = 3

    def __init__(self, address, adapter):
        self.address = address
        self.adapter = adapter

        self.pbap = PBAPController(self.address)
        self.hfp = HFPController(self.address)
        self.avctp = AVCTPController(self.address)

    def is_alive(self):
        name = bluetooth.lookup_name(self.address)
        return name is not None

    @cached_property
    def services(self):
        logger.info("Fetching device services...")
        for try_index in xrange(self.SERVICES_SCAN_TRIES):
            logger.debug(
                "Scan try number: {}/{}".format(try_index,
                                                self.SERVICES_SCAN_TRIES))
            services = bluetooth.find_service(address=self.address)
            if len(services) == 0:
                logger.warning("No services could be found!")
                time.sleep(1)
                continue

            to_ret = {}
            for raw_service in services:
                service = Service(**fix_keys(raw_service))
                logger.debug("Service found: {!r}".format(service))
                for service_class in service.service_classes:
                    to_ret[service_class] = service

            return to_ret

        else:
            logger.error("Device doesn't seemed to have bluetooth services")
            raise RuntimeError(
                "Device doesn't seemed to have bluetooth services")

    def pair_and_trust(self):
        logger.info("Pairing and trusting device...")
        success = self.adapter.pair(self.address)
        if not success:
            logger.error("Could not pair with device")
            raise RuntimeError("Could not pair with device")

        success = self.adapter.trust(self.address)
        if not success:
            logger.error("Could not trust device")
            raise RuntimeError("Could not trust device")

        logger.info("Paired and trusted successfully")

    def get_service_port(self, service):
        try:
            return self.services[service.SERVICE_CLASS].port

        except:
            logger.warning("default port chosen!")
            return service.DEFAULT_PORT

    def connect(self):
        logger.info("Connecting to all available services...")
        self.pair_and_trust()

        self.pbap.connect(self.get_service_port(self.pbap))
        logger.info("Service pbap connected!")
        self.hfp.connect(self.get_service_port(self.hfp))
        logger.info("Service hfp connected!")
        self.avctp.connect(self.get_service_port(self.avctp))
        logger.info("Service avctp connected!")

        logger.info("All services connected!")

    def remove(self):
        success = self.adapter.remove(self.address)
        if not success:
            logger.error("Could not pair remove device")
            raise RuntimeError("Could not remove with device")

    def close(self):
        logger.info("Closing all available services connections...")
        self.pbap.close()
        logger.info("Service pbap disconnected!")
        self.hfp.close()
        logger.info("Service hfp disconnected!")
        self.avctp.close()
        logger.info("Service avctp disconnected!")

        logger.info("All services disconnected!")

        logger.info("Disconnecting from agent...")
        self.adapter.disconnect(self.address)


class BTController(object):
    FINDING_TRIES = 3

    def __init__(self):
        self.adapter = Bluetooth()

    @classmethod
    def edit_devices_data(cls, devices):
        actual_devices = bluetooth.discover_devices(duration=1)
        for device in devices:
            device["alive"] = device["mac_address"] in actual_devices

        return devices

    @property
    def available_devices(self):
        return self.edit_devices_data(self.adapter.get_available_devices())

    @property
    def connected_devices(self):
        return self.adapter.get_connected_devices()

    @property
    def paired_devices(self):
        return self.adapter.get_paired_devices()

    @property
    def devices_to_pair(self):
        return self.adapter.get_devices_to_pair()

    def probe_devices(self):
        logger.info("Probing for nearby devices...")
        self.adapter.scan()
        return self.available_devices

    def get_address_from_cache(self, name):
        cached = self.available_devices
        if name.lower() not in cached:
            return None

        address = cached[name.lower()]
        logger.debug(
            "Device `{}` located in scans cache: {}".format(
                name, address))
        return address

    def find_address_of(self, name):
        logger.info("Locating device by name: {}".format(name))
        cached_address = self.get_address_from_cache(name)
        if cached_address is not None:
            return cached_address

        logger.warning("Device `{}` is not in scans cache".format(name))
        for try_index in xrange(self.FINDING_TRIES):
            logger.debug(
                "Scan try number: {}/{}".format(try_index, self.FINDING_TRIES))
            self.probe_devices()
            cached_address = self.get_address_from_cache(name)
            if cached_address is not None:
                return cached_address

        else:
            logger.error("Device `{}` couldn't be found".format(name))
            raise RuntimeError("Device `{}` couldn't be found!".format(name))

    @lru_cache()
    def get_client(self, address):
        return BTDevice(address, self.adapter)


if __name__ == '__main__':
    paint_logger(logger)
    controller = BTController()
    controller.probe_devices()
    address = controller.find_address_of("OnePlus 3")
    device = controller.get_client(address)
    device.services
    device.connect()

    a = device.avctp.connection.play()
    time.sleep(10)

    # phone_book = device.get_history()
    # phone_book = device.pbap.get_phonebook()
    #
    # with open('phonebook.json', "wb") as f:
    #     json.dump([contact.to_dict() for contact in phone_book], f)

    device.close()

    # controller.get_phonebook()
    # controller.close()
