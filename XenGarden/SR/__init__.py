from deprecated import deprecated

from XenGarden.VDI import VDI


class SR:
    """ The Storage Repository Object """

    def __init__(self, session, sr):
        self.session = session
        self.sr = sr

    @staticmethod
    def get_all(session):
        """ get all SR object available """

        srs = session.xenapi.SR.get_all()

        sr_list = []
        for sr in srs:
            sr_list.append(SR(session, sr))

        return sr_list

    @staticmethod
    def get_by_name(session, name):
        """ returns SR object that has specific name"""

        srs = session.xenapi.SR.get_by_name_label(name)

        srs_list = []
        for sr in srs:
            srs_list.append(SR(session, sr))

        return srs_list

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns SR object that has specific uuid """

        sr = session.xenapi.SR.get_by_uuid(uuid)

        if sr is not None:
            return SR(session, sr)
        else:
            return None

    def get_record(self):
        return self.session.xenapi.SR.get_record(self.sr)

    @deprecated
    def serialize(self) -> dict:
        """ Returns Info of this SR """
        vdis = self.get_VDIs()
        vdi_list = []

        if vdis is not None:
            for vdi in vdis:
                vdi_list.append(vdi.serialize())
        else:
            vdi_list = None

        return {
            "name": self.get_name(),
            "description": self.get_description(),
            "size": self.get_physical_size(),
            "uuid": self.get_uuid(),
            "content_type": self.get_content_type(),
            "type": self.get_type(),
            "vdis": vdi_list,
        }

    def get_VDIs(self):

        vdis = self.session.xenapi.SR.get_VDIs(self.sr)

        vdi_list = []
        for vdi in vdis:
            vdi_list.append(VDI(self.session, vdi))

        return vdi_list

    def get_name(self):

        return self.session.xenapi.SR.get_name_label(self.sr)

    def get_description(self):

        return self.session.xenapi.SR.get_name_description(self.sr)

    def get_physical_size(self):

        return self.session.xenapi.SR.get_physical_size(self.sr)

    def get_physical_utilisation(self):

        return self.session.xenapi.SR.get_physical_utilisation(self.sr)

    def get_uuid(self):

        return self.session.xenapi.SR.get_uuid(self.sr)

    def get_content_type(self):

        return self.session.xenapi.SR.get_content_type(self.sr)

    def get_type(self):

        return self.session.xenapi.SR.get_type(self.sr)

    def scan(self):

        self.session.xenapi.SR.scan(self.sr)
