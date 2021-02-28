from deprecated import deprecated


class Host:
    """ The Host Object """

    def __init__(self, session, host):
        self.session = session
        self.host = host

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns Host object that has specific uuid """

        host = session.xenapi.host.get_by_uuid(uuid)

        if host is not None:
            return Host(session, host)
        else:
            return None

    @staticmethod
    def get_by_name(session, label):
        """ returns Host object that has specific name """

        host = session.xenapi.host.get_by_name_label(label)

        if host is not None:
            return Host(session, host)
        else:
            return None

    @staticmethod
    def list_host(session):
        """gets Hosts available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of Host object)"""

        allHostList = []
        allHosts = session.xenapi.host.get_all()

        for hostF in allHosts:
            host = Host(session, hostF)
            allHostList.append(host)

        return allHostList

    def get_record(self):
        return self.session.xenapi.host.get_record(self.host)

    @deprecated
    def serialize(self) -> dict:

        return {
            "uuid": self.get_uuid(),
            "name": self.get_name(),
            "description": self.get_description(),
            "enabled": self.get_enabled(),
            "memory": {
                "free": self.get_free_memory(),
                "total": self.get_total_memory(),
            },
            "cpu": self.get_cpu_info(),
            "bios": self.get_bios_strings(),
            "version": self.get_software_version(),
        }

    def get_uuid(self):
        """ get UUID of Host """

        return self.session.xenapi.host.get_uuid(self.host)

    def get_free_memory(self):
        """ get Free Memory of Host """

        return self.session.xenapi.host.compute_free_memory(self.host)

    def get_total_memory(self):
        """ get Total Memory of Host """

        metrics = self.session.xenapi.host.get_metrics(self.host)
        return self.session.xenapi.host_metrics.get_memory_total(metrics)

    def get_cpu_info(self):
        """ get CPU Info of Host """

        return self.session.xenapi.host.get_cpu_info(self.host)

    def get_software_version(self):
        """ get Software Version of Host """

        return self.session.xenapi.host.get_software_version(self.host)

    def disable(self):
        """ Disable Host """

        return self.session.xenapi.host.disable(self.host)

    def enable(self):
        """ Enable Host """

        return self.session.xenapi.host.enable(self.host)

    def get_enabled(self):
        """ Get Host is Enabled """

        return self.session.xenapi.host.get_enabled(self.host)

    def evacuate(self):
        """ Evacuate Host """

        return self.session.xenapi.host.evacuate(self.host)

    def get_address(self):
        """ Get Address of Host """

        return self.session.xenapi.host.evacuate(self.host)

    def get_bios_strings(self):
        """ Get BIOS Strings of Host """

        return self.session.xenapi.host.get_bios_strings(self.host)

    def get_capabilities(self):
        """ Get capabilities of Host """

        return self.session.xenapi.host.get_capabilites(self.host)

    def get_name(self):
        """ Get name of Host """

        return self.session.xenapi.host.get_name_label(self.host)
