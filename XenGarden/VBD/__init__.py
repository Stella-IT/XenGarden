from deprecated import deprecated

from XenGarden.VDI import VDI


class VBD:
    """ The Virtual Block Device Object """

    def __init__(self, session, vbd):
        self.session = session
        self.vbd = vbd

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns SR object that has specific uuid """

        vbd = session.xenapi.VBD.get_by_uuid(uuid)

        if vbd is not None:
            return VBD(session, vbd)
        else:
            return None

    @staticmethod
    def get_all(session):
        """ returns VBDs existing on this _host """

        vbds = session.xenapi.VBD.get_all()
        vbd_list = []

        for vbd in vbds:
            vbd_list.append(VBD(session, vbd))

        return vbd_list

    @deprecated
    def serialize(self) -> dict:
        vm = self.get_VM()
        vdi = self.get_VDI()

        if vm is not None:
            vm = vm.serialize()

        if vdi is not None:
            vdi = vdi.serialize()

        return {
            "_vm": vm,
            "vdi": vdi,
            "bootable": self.get_bootable(),
            "attached": self.get_currently_attached(),
            "unpluggable": self.get_unpluggable(),
            "device": self.get_device(),
            "type": self.get_type(),
            "uuid": self.get_uuid(),
            "mode": self.get_mode(),
        }

    def get_VM(self):
        """ get VM attached to the specified VBD """
        from XenGarden.VM import VM

        vm = self.session.xenapi.VBD.get_VM(self.vbd)

        if vm is not None:
            return VM(self.session, vm)
        else:
            return None

    def get_VDI(self) -> VDI:
        """ get VDI attached to the specified VBD """

        vdi = self.session.xenapi.VBD.get_VDI(self.vbd)

        if vdi is not None:
            return VDI(self.session, vdi)
        else:
            return None

    def get_uuid(self) -> str:
        """ get UUID of VBD """

        return self.session.xenapi.VBD.get_uuid(self.vbd)

    def get_mode(self) -> str:
        """ get mode of VBD """

        return self.session.xenapi.VBD.get_mode(self.vbd)

    def get_type(self) -> str:
        """ get type of VBD """

        return self.session.xenapi.VBD.get_type(self.vbd)

    def get_bootable(self) -> bool:
        """ get VBD is bootable """

        return self.session.xenapi.VBD.get_bootable(self.vbd)

    def get_currently_attached(self) -> bool:
        """ get VBD is currently attached """

        return self.session.xenapi.VBD.get_currently_attached(self.vbd)

    def get_unpluggable(self) -> bool:
        """ get VBD is unpluggable """

        return self.session.xenapi.VBD.get_unpluggable(self.vbd)

    def get_device(self) -> str:
        """ get VBD device """

        return self.session.xenapi.VBD.get_device(self.vbd)

    def destroy(self) -> bool:
        """ eject VDI from VBD """

        self.session.xenapi.VBD.destroy(self.vbd)
        return True

    def insert(self, vdi: VDI) -> bool:
        """ insert VDI to VBD """

        self.session.xenapi.VBD.insert(self.vbd, vdi.vdi)
        return True

    def eject(self) -> bool:
        """ eject VDI from VBD """

        self.session.xenapi.VBD.eject(self.vbd)
        return True

    def plug(self) -> bool:
        """ plug specified VBD """

        self.session.xenapi.VBD.plug(self.vbd)
        return True

    def unplug(self) -> bool:
        """ unplug VBD """

        self.session.xenapi.VBD.unplug(self.vbd)
        return True

    def unplug_force(self) -> bool:
        """ unplug VBD """

        self.session.xenapi.VBD.unplug_force(self.vbd)
        return True
