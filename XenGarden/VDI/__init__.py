from deprecated import deprecated

from XenGarden.Common import Common


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

    def get_record(self):
        return self.session.xenapi.VDI.get_record(self.vdi)

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

    def get_virtual_size(self) -> str:

        return self.session.xenapi.VDI.get_virtual_size(self.vdi)

    def destroy(self):

        return self.session.xenapi.VDI.destroy(self.vdi)

    def get_SR(self):
        from XenGarden.SR import SR

        data = self.session.xenapi.VDI.get_SR(self.vdi)
        sr = SR(self.session, data)

        return sr

    async def clone(self):

        task = self.session.xenapi.Async.VDI.clone(self.vdi)
        data = await Common.xenapi_task_handler(self.session, task, True)

        vdi = VDI(self.session, data)
        return vdi

    async def copy(self, sr):

        task = self.session.xenapi.Async.VDI.copy(self.vdi, sr.sr)
        data = await Common.xenapi_task_handler(self.session, task, True)

        vdi = VDI(self.session, data)
        return vdi

    async def resize(self, size: str):

        task = self.session.xenapi.Async.VDI.resize(self.vdi, size)
        await Common.xenapi_task_handler(self.session, task, True)

        return True
