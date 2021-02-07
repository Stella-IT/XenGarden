from deprecated import deprecated

from XenGarden.Console import Console
from XenGarden.GuestMetrics import GuestMetrics


class VM:
    """ The Virtual Machine Object """

    def __init__(self, session, vm):
        self.session = session
        self.vm = vm

    @staticmethod
    def get_by_uuid(session, uuid):
        """ returns VM object that has specific uuid """

        vm = session.xenapi.VM.get_by_uuid(uuid)

        if vm is not None:
            return VM(session, vm)
        else:
            return None

    @staticmethod
    def list_templates(session):
        """gets Templates available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of VM object)"""

        allTemplates = []
        allVMs = session.xenapi.VM.get_all_records()

        for vmF in allVMs:
            template = VM(session, vmF)

            if template.is_template():
                allTemplates.append(template)

        return allTemplates

    @staticmethod
    def list_vm(session):
        """gets VMs available in specific XenServer
        session: the XenServer Connection Session
        Returns Available Templates (List of VM object)"""

        allVMList = []
        allVMs = session.xenapi.VM.get_all()

        for vmF in allVMs:
            vm = VM(session, vmF)
            if not vm.is_template():
                allVMList.append(vm)

        return allVMList

    def get_uuid(self):
        """ get UUID of VM """

        return self.session.xenapi.VM.get_uuid(self.vm)

    def is_template(self):
        """ Returns rather this _vm is template """

        return self.session.xenapi.VM.get_is_a_template(self.vm)

    @deprecated
    def serialize(self):
        """ Returns Info for of the VM """
        return {
            "name": self.get_name(),
            "bios": self.get_bios_strings(),
            "power": self.get_power_state(),
            "description": self.get_description(),
            "uuid": self.get_uuid(),
            "vCPUs": self.get_vCPUs(),
            "memory": self.get_memory(),
        }

    def get_power_state(self):
        """ Returns Power State of the VM """

        return self.session.xenapi.VM.get_power_state(self.vm)

    def get_consoles(self):
        """ Returns Consoles of the VM """

        consoles = self.session.xenapi.VM.get_consoles(self.vm)

        consoleList = []
        for console in consoles:
            consoleList.append(Console(self.session, console))
        return consoleList

    def get_guest_metrics(self):
        """ Returns Guest Metrics Object of the VM """

        return GuestMetrics(
            self.session, self.session.xenapi.VM.get_guest_metrics(self.vm)
        )

    def get_snapshots(self):
        """ Returns Available Snapshots (List of VM object) """

        allSnapshots = []
        snapshots = self.session.xenapi.VM.get_snapshots(self.vm)

        for snapshotNo in snapshots:
            allSnapshots.append(VM(self.session, snapshots[snapshotNo]))

        return allSnapshots

    def get_name(self):
        """ Returns VM's XenServer Name """

        return self.session.xenapi.VM.get_name_label(self.vm)
        #
        return True

    def get_description(self):
        """ Returns VM's XenServer Description """

        return self.session.xenapi.VM.get_name_description(self.vm)
        #
        return True

    def start(self):
        """ Starts VM (Returns Boolean, True: Success, False: Fail) """

        self.session.xenapi.VM.start(self.vm, False, False)

        return True

    def shutdown(self):
        """ Shutdowns VM (Returns Boolean, True: Success, False: Fail) """

        self.session.xenapi.VM.clean_shutdown(self.vm)

        return True

    def force_shutdown(self):
        """ Force Shutdown VM (Returns Boolean, True: Success, False: Fail) """

        self.session.xenapi.VM.hard_shutdown(self.vm)

        return True

    def reboot(self):
        """ Reboot VM (Returns Boolean, True: Success, False: Fail) """

        self.session.xenapi.VM.clean_reboot(self.vm)

        return True

    def force_reboot(self):
        """ Force Reboot VM (Returns Boolean, True: Success, False: Fail) """

        self.session.xenapi.VM.hard_reboot(self.vm)

        return True

    def snapshot(self, snapshot_name):
        """ Take a snapshot of current VM """

        self.session.xenapi.VM.snapshot(self.vm, snapshot_name)

        return True

    def suspend(self):

        self.session.xenapi.VM.suspend(self.vm)

        return True

    def resume(self):

        self.session.xenapi.VM.resume(self.vm, True, False)

        return True

    def pause(self):

        self.session.xenapi.VM.pause(self.vm)

        return True

    def unpause(self):

        self.session.xenapi.VM.unpause(self.vm)

        return True

    def clone(self, new_name):

        vm = self.session.xenapi.VM.clone(self.vm, new_name)
        self.session.xenapi.VM.set_is_a_template(vm, False)
        return VM(self.session, vm)

        return None

    def set_name(self, name):

        self.session.xenapi.VM.set_name_label(self.vm, name)
        #
        return True

    def set_description(self, description):

        self.session.xenapi.VM.set_name_description(self.vm, description)
        #
        return True

    def set_vCPUs(self, vCPUs):

        tmp_platform = self.session.xenapi.VM.get_platform(
            self.vm,
        )
        vCPU_platform = {"cores-per-socket": str(vCPUs)}

        platform = {**tmp_platform, **vCPU_platform}

        self.session.xenapi.VM.set_platform(self.vm, platform)
        self.session.xenapi.VM.set_VCPUs_max(self.vm, vCPUs)
        self.session.xenapi.VM.set_VCPUs_at_startup(self.vm, vCPUs)
        #
        return True

    def set_memory(self, memory):

        self.session.xenapi.VM.set_memory_limits(
            self.vm, memory, memory, memory, memory
        )
        #
        return True

    def get_platform(self):

        return self.session.xenapi.VM.get_platform(self.vm)
        #
        return None

    def set_platform(self, platform):

        return self.session.xenapi.VM.set_platform(self.vm, platform)
        #
        return None

    def get_vCPUs(self):

        return self.session.xenapi.VM.get_VCPUs_at_startup(self.vm)
        #
        return None

    def get_vCPU_params(self):

        return self.session.xenapi.VM.get_VCPUs_params(self.vm)
        #
        return None

    def get_bios_strings(self):

        return self.session.xenapi.VM.get_bios_strings(self.vm)
        #
        return None

    def set_bios_strings(self, input_bios_str):

        tmp_bios_str = self.session.xenapi.VM.get_bios_strings(self.vm)
        bios_str = {**tmp_bios_str, **input_bios_str}
        self.session.xenapi.VM.set_bios_strings(self.vm, bios_str)
        return True
        #
        return None

    def get_memory(self):

        return self.session.xenapi.VM.get_memory_static_max(self.vm)

    def delete(self):
        from XenGarden.VBD import VBD

        vbds = self.get_Disks()
        for vbd in vbds:
            vbd.destroy()

        self.session.xenapi.VM.destroy(self.vm)
        return True

    def destroy(self):
        return self.delete()

    def get_VBDs(self):
        from XenGarden.VBD import VBD

        vbds = self.session.xenapi.VM.get_VBDs(self.vm)

        vbd_list = []
        for vbd in vbds:
            vbd_list.append(VBD(self.session, vbd))

        return vbd_list

    def get_CDs(self):
        from XenGarden.VBD import VBD

        vbds = self.session.xenapi.VM.get_VBDs(self.vm)

        vbd_list = []
        for vbd in vbds:
            thisVBD = VBD(self.session, vbd)

            if thisVBD.get_type() == "CD":
                vbd_list.append(thisVBD)

        return vbd_list

    def get_VIFs(self):
        from XenGarden.VIF import VIF

        vifs = self.session.xenapi.VM.get_VIFs(self.vm)

        vif_list = []
        for vif in vifs:
            thisVIF = VIF(self.session, vif)
            vif_list.append(thisVIF)

        return vif_list

    def get_VIF(self):
        vifs = self.get_VIFs()
        if vifs is not None:
            return vifs[0]
        else:
            return None

    def get_CD(self):
        return self.get_CDs()[0]

    def get_Disks(self):
        from XenGarden.VBD import VBD

        vbds = self.session.xenapi.VM.get_VBDs(self.vm)

        vbd_list = []
        for vbd in vbds:
            thisVBD = VBD(self.session, vbd)

            if thisVBD.get_type() == "Disk":
                vbd_list.append(thisVBD)

        return vbd_list
