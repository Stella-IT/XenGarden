from enum import Enum

from XenAPI.XenAPI import Failure


class VIFLockingMode(Enum):
    DEFAULT = "network_default"
    LOCKED = "locked"
    UNLOCKED = "unlocked"
    DISABLED = "disabled"


class VIFIPv4ConfigurationMode(Enum):
    NONE = "None"
    STATIC = "Static"


class VIFIPv6ConfigurationMode(Enum):
    NONE = "None"
    STATIC = "Static"


class VIF:
    """ The Virtual Interface """

    def __init__(self, session, vif):
        self.session = session
        self.vif = vif

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns VIF object that has specific uuid """

        vif = session.xenapi.VIF.get_by_uuid(uuid)

        if vif is not None:
            return VIF(session, vif)
        else:
            return None

    @staticmethod
    def get_all(session):
        """gets VIFs available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of VIF object)"""

        allVIFList = []
        allVIFs = session.xenapi.VIF.get_all()

        for vif in allVIFs:
            thisVif = VIF(session, vif)
            allVIFList.append(thisVif)

        return allVIFList

    def get_uuid(self):
        return self.session.xenapi.VIF.get_uuid(self.vif)

    def get_record(self):
        """ Returns Information of the VIF """
        return self.session.xenapi.VIF.get_record(self.vif)

    def get_attached(self):
        return self.session.xenapi.VIF.get_currently_attached(self.vif)

    def plug(self):
        self.session.xenapi.VIF.plug(self.vif)
        return True

    def unplug(self):
        self.session.xenapi.VIF.unplug(self.vif)
        return True

    def unplug_force(self):
        self.session.xenapi.VIF.unplug_force(self.vif)
        return True

    def get_locking_mode(self):
        return self.session.xenapi.VIF.get_locking_mode(self.vif)

    def set_locking_mode(self, locking_mode: VIFLockingMode):
        self.session.xenapi.VIF.set_locking_mode(self.vif, locking_mode)
        return True

    def set_locking_mode(self, locking_mode: VIFLockingMode):
        self.session.xenapi.VIF.set_locking_mode(self.vif, locking_mode)
        return True

    def lock(self, locking_mode):
        self.set_locking_mode("locked")
        return True

    def unlock(self, locking_mode):
        self.set_locking_mode("unlocked")
        return True

    def get_vm(self):
        from XenGarden.VM import VM

        try:
            vm = self.session.xenapi.VIF.get_VM(self.vif)
            vm = VM(self.session, vm)
            vm.get_uuid()

            return vm
        except Failure as xenapi_error:
            if xenapi_error.details[0] == "HANDLE_INVALID":
                return None
            else:
                raise xenapi_error

    def get_mac(self):
        mac = self.session.xenapi.VIF.get_MAC(self.vif)
        return mac

    def get_mtu(self):
        return self.session.xenapi.VIF.get_MTU(self.vif)

    def get_qos_type(self):
        return self.session.xenapi.VIF.get_qos_algorithm_type(self.vif)

    def set_qos_type(self, qos_type):
        return self.session.xenapi.VIF.get_qos_algorithm_type(self.vif, qos_type)

    def get_qos_info(self):
        return self.session.xenapi.VIF.get_qos_algorithm_params(self.vif)

    def set_qos_info(self, qos_params):
        self.session.xenapi.VIF.set_qos_algorithm_params(self.vif, qos_params)
        return True

    def supported_qos_types(self):
        return self.session.xenapi.VIF.get_qos_supported_algorithms(self.vif)

    def config_ipv4(
        self, ipv4_config_mode: VIFIPv4ConfigurationMode, ip: str, gateway: str
    ):
        self.session.xenapi.VIF.configure_ipv4(self.vif, ipv4_config_mode, ip, gateway)
        return True

    def get_address_v4(self):
        return self.session.xenapi.VIF.get_ipv4_addresses(self.vif)

    def get_gateway_v4(self):
        return self.session.xenapi.VIF.get_ipv4_gateway(self.vif)

    def get_allowed_address_v4(self):
        return self.session.xenapi.VIF.get_ipv4_allowed(self.vif)

    def set_allowed_address_v4(self, ips):
        self.session.xenapi.VIF.set_ipv4_allowed(self.vif, ips)
        return True

    def add_allowed_address_v4(self, ip):
        self.session.xenapi.VIF.add_ipv4_allowed(self.vif, ip)
        return True

    def remove_allowed_address_v4(self, ip):
        self.session.xenapi.VIF.remove_ipv4_allowed(self.vif, ip)
        return True

    def config_ipv6(
        self, ipv6_config_mode: VIFIPv6ConfigurationMode, ip: str, gateway: str
    ):
        self.session.xenapi.VIF.configure_ipv4(self.vif, ipv6_config_mode, ip, gateway)
        return True

    def get_address_v6(self):
        return self.session.xenapi.VIF.get_ipv6_addresses(self.vif)

    def get_gateway_v6(self):
        return self.session.xenapi.VIF.get_ipv6_gateway(self.vif)

    def get_allowed_address_v6(self):
        return self.session.xenapi.VIF.get_ipv6_allowed(self.vif)

    def set_allowed_address_v6(self, ips):
        self.session.xenapi.VIF.set_ipv6_allowed(self.vif, ips)
        return True

    def add_allowed_address_v6(self, ip):
        self.session.xenapi.VIF.add_ipv6_allowed(self.vif, ip)
        return True

    def remove_allowed_address_v6(self, ip):
        self.session.xenapi.VIF.remove_ipv6_allowed(self.vif, ip)
        return True
