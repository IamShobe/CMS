import logging
from collections import namedtuple

import bluetooth
from cached_property import cached_property

from car.bt.protocols.avctp.controller import AVCTPController
from utils import fix_keys
from protocols.hfp.controller import HFPController
from protocols.pbap.controller import PBAPController

logger = logging.getLogger("Bluetooth")

# Create handlers
c_handler = logging.StreamHandler()

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)

logger.addHandler(c_handler)
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

    def __repr__(self):
        return "{}(name={!r}, protocol={!r}, port={}, classes={!r})".format(
            self.__class__.__name__, self.name, self.protocol, self.port,
            self.service_classes)


class BTDevice(object):
    SERVICES_SCAN_TRIES = 3

    def __init__(self, address):
        self.address = address
        self.pbap = PBAPController(self.address)
        self.hfp = HFPController(self.address)
        self.avctp = AVCTPController(self.address)

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

    def connect(self):
        logger.debug("Connecting to all available services...")
        self.pbap.connect(self.services[self.pbap.SERVICE_CLASS].port)
        self.hfp.connect(self.services[self.hfp.SERVICE_CLASS].port)
        self.avctp.connect(self.services[self.avctp.SERVICE_CLASS].port)

    def close(self):
        logger.debug("Closing all available services connections...")
        self.pbap.close()
        self.hfp.close()
        self.avctp.close()


class BTController(object):
    FINDING_TRIES = 3

    def __init__(self):
        self.cached_addresses = {}

    def probe_devices(self):
        logger.info("Probing for nearby devices...")
        near_devices = bluetooth.discover_devices(lookup_names=True)
        for device_address, device_name in near_devices:
            self.cached_addresses[device_name.lower()] = device_address
            logger.debug("Discovered device: {} - {}".format(device_name,
                                                             device_address))

        return near_devices

    def get_address_from_cache(self, name):
        if name.lower() not in self.cached_addresses:
            return None

        address = self.cached_addresses[name.lower()]
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


if __name__ == '__main__':
    controller = BTController()
    controller.probe_devices()
    controller.find_address_of("OnePlus 3")
    device = BTDevice(controller.find_address_of("OnePlus 3"))
    device.services
    device.connect()

    # phone_book = device.get_history()
    # phone_book = device.pbap.get_phonebook()
    #
    # with open('phonebook.json', "wb") as f:
    #     json.dump([contact.to_dict() for contact in phone_book], f)


    device.close()

    # controller.get_phonebook()
    # controller.close()
