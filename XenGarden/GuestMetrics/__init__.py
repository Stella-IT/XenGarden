from deprecated import deprecated


class GuestMetrics:
    def __init__(self, session, guest):
        self.session = session
        self.guest = guest

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns GuestMetrics object that has specific uuid """

        guest_metrics = session.xenapi.VM_guest_metrics.get_by_uuid(uuid)
        if guest_metrics is not None:
            return GuestMetrics(session, guest_metrics)
        else:
            return None

    def get_record(self):
        return self.session.xenapi.VM.get_record(self.guest)

    @deprecated
    def serialize(self):
        return {
            "uuid": self.get_uuid(),
            "os": self.get_os_version(),
            "networks": self.get_networks(),
        }

    def get_record(self):
        """ Returns Information of the Guest """
        return self.session.xenapi.VM_guest_metrics.get_record(self.guest)

    def get_uuid(self):
        """ Gets UUID of Guest Metrics """

        return self.session.xenapi.VM_guest_metrics.get_uuid(self.guest)

    def get_networks(self):
        """ Gets UUID of Guest Networks """

        return self.session.xenapi.VM_guest_metrics.get_networks(self.guest)

    def get_os_version(self):
        """ Gets OS Version of Guest """

        return self.session.xenapi.VM_guest_metrics.get_os_version(self.guest)

    def get_other(self):
        """ Gets "Other" of Guest """

        return self.session.xenapi.VM_guest_metrics.get_other(self.guest)
