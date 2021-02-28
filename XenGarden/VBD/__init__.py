from deprecated import deprecated
from XenAPI.XenAPI import Failure

from XenGarden.VDI import VDI
from XenGarden.VM import VM


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

    @staticmethod
    def create(
        session,
        vm: VM,
        vdi: VDI,
        userdevice="0",
        bootable=True,
        mode="RW",
        disk_type="Disk",
        empty=False,
        qos_algorithm_type="",
        qos_algorithm_params={},
        other_config={},
        **kwargs
    ):
        _vm = vm.vm
        _vdi = vdi.vdi

        _vbd = session.xenapi.VBD.create(
            {
                "VM": _vm,
                "VDI": _vdi,
                "userdevice": userdevice,
                "bootable": bootable,
                "mode": mode,
                "type": disk_type,
                "empty": empty,
                "qos_algorithm_type": qos_algorithm_type,
                "qos_algorithm_params": qos_algorithm_params,
                "other_config": other_config,
                **kwargs,
            }
        )

        return VBD(session, _vbd)

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

        try:
            from XenGarden.VM import VM

            vm = self.session.xenapi.VBD.get_VM(self.vbd)
            vm = VM(self.session, vm)

            vm.get_uuid()
            return vm
        except Failure as xenapi_error:
            if xenapi_error.details[0] == "HANDLE_INVALID":
                return None
            else:
                raise xenapi_error

    def get_VDI(self) -> VDI:
        """ get VDI attached to the specified VBD """
        try:
            vdi = self.session.xenapi.VBD.get_VDI(self.vbd)
            vdi = VDI(self.session, vdi)
            vdi.get_uuid()

            return vdi
        except Failure as xenapi_error:
            if xenapi_error.details[0] == "HANDLE_INVALID":
                return None
            else:
                raise xenapi_error

    def get_record(self):
        """ Returns Information of the VM """
        return self.session.xenapi.VBD.get_record(self.vbd)

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
