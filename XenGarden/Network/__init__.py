from enum import Enum

from XenAPI.XenAPI import Failure


class PIFIPv4ConfigurationMode(Enum):
    NONE = "None"
    STATIC = "Static"


class PIFIPv6ConfigurationMode(Enum):
    NONE = "None"
    STATIC = "Static"


class Network:
    """Virtual Network in Xen Hypervisor"""

    def __init__(self, session, network):
        self.session = session
        self.network = network

    @staticmethod
    def get_by_uuid(session, uuid):
        """returns VIF object that has specific uuid"""

        network = session.xenapi.network.get_by_uuid(uuid)

        if network is not None:
            return Network(session, network)
        else:
            return None

    @staticmethod
    def get_all(session):
        """gets Virtual Networks available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of Network object)"""

        allNetworkList = []
        allNetworks = session.xenapi.network.get_all()

        for network in allNetworks:
            thisNetwork = Network(session, network)
            allNetworkList.append(thisNetwork)

        return allNetworkList

    def get_uuid(self):
        return self.session.xenapi.network.get_uuid(self.network)

    def get_record(self):
        """Returns Information of the PIF"""
        return self.session.xenapi.network.get_record(self.network)

    def get_mtu(self):
        return self.session.xenapi.network.get_MTU(self.network)

    def get_name(self):
        return self.session.xenapi.network.get_name_label(self.network)

    def get_description(self):
        return self.session.xenapi.network.get_name_description(self.network)
