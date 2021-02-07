from deprecated import deprecated


class VDI:
    """ The Virtual Disk Image Object """

    def __init__(self, session, vdi):
        self.session = session
        self.vdi = vdi

    @staticmethod
    def get_by_name(session, name):
        """ returns SR object that has specific name """

        vdis = session.xenapi.VDI.get_by_name_label(name)

        vdi_list = []
        for vdi in vdis:
            vdi_list.append(VDI(session, vdi))

        return vdi_list

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns SR object that has specific uuid """

        vdi = session.xenapi.VDI.get_by_uuid(uuid)

        if vdi is not None:
            return VDI(session, vdi)
        else:
            return None

    @staticmethod
    def get_all(session):
        """ returns SR object that exists on _host """

        vdis = session.xenapi.VDI.get_all()

        vdi_list = []
        for vdi in vdis:
            vdi_list.append(VDI(session, vdi))

        return vdi_list

    @deprecated
    def serialize(self) -> dict:
        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "uuid": self.get_uuid(),
            "location": self.get_location(),
            "type": self.get_type(),
        }

    def get_name(self):

        return self.session.xenapi.VDI.get_name_label(self.vdi)

    def get_description(self):

        return self.session.xenapi.VDI.get_name_description(self.vdi)

    def get_uuid(self):

        return self.session.xenapi.VDI.get_uuid(self.vdi)

    def get_type(self):

        return self.session.xenapi.VDI.get_type(self.vdi)

    def get_location(self):

        return self.session.xenapi.VDI.get_location(self.vdi)

    def destroy(self):

        return self.session.xenapi.VDI.destroy(self.vdi)
