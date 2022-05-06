from enum import Enum

from XenAPI.XenAPI import Failure

from XenGarden import VM


class PIFIPv4ConfigurationMode(Enum):
    NONE = "None"
    STATIC = "Static"


class PIFIPv6ConfigurationMode(Enum):
    NONE = "None"
    STATIC = "Static"


class PIF:
    """The Physical Interface"""

    def __init__(self, session, pif):
        self.session = session
        self.pif = pif

    @staticmethod
    def get_by_uuid(session, uuid):
        """returns VIF object that has specific uuid"""

        pif = session.xenapi.PIF.get_by_uuid(uuid)

        if pif is not None:
            return PIF(session, pif)
        else:
            return None

    @staticmethod
    def get_all(session):
        """gets PIFs available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of PIF object)"""

        allPIFList = []
        allPIFs = session.xenapi.PIF.get_all()

        for pif in allPIFs:
            thisPIF = PIF(session, pif)
            allPIFList.append(thisPIF)

        return allPIFList

    def get_device(self):
        return self.session.xenapi.PIF.get_device(self.pif)

    def get_uuid(self):
        return self.session.xenapi.PIF.get_uuid(self.pif)

    def get_record(self):
        """Returns Information of the PIF"""
        return self.session.xenapi.PIF.get_record(self.pif)

    def get_attached(self):
        return self.session.xenapi.PIF.get_currently_attached(self.pif)

    def plug(self):
        self.session.xenapi.PIF.plug(self.pif)
        return True

    def unplug(self):
        self.session.xenapi.PIF.unplug(self.pif)
        return True

    def unplug_force(self):
        self.session.xenapi.PIF.unplug_force(self.pif)
        return True

    def get_mac(self):
        mac = self.session.xenapi.PIF.get_MAC(self.pif)
        return mac

    def get_mtu(self):
        return self.session.xenapi.PIF.get_MTU(self.pif)

    def config_ipv4(
        self,
        ipv4_config_mode: PIFIPv4ConfigurationMode,
        ip: str,
        netmask: str,
        gateway: str,
        dns: str,
    ):
        self.session.xenapi.PIF.configure_ipv4(
            self.pif, ipv4_config_mode, ip, netmask, gateway, dns
        )
        return True

    def get_address_v4(self):
        return self.session.xenapi.PIF.get_IP(self.pif)

    def get_address_v6(self):
        return self.session.xenapi.PIF.get_IPv6(self.pif)

    def get_gateway_v4(self):
        return self.session.xenapi.PIF.get_gateway(self.pif)
