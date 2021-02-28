import math

from XenAPI.XenAPI import Failure

from XenGarden.Common import Common
from XenGarden.Console import Console
from XenGarden.GuestMetrics import GuestMetrics
from XenGarden.SR import SR


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

    def get_record(self):
        """ Returns Information of the VM """
        return self.session.xenapi.VM.get_record(self.vm)

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
        try:
            guest_metrics = self.session.xenapi.VM.get_guest_metrics(self.vm)
            guest_metrics = GuestMetrics(self.session, guest_metrics)
            guest_metrics.get_uuid()

            return guest_metrics
        except Failure as xenapi_error:
            if xenapi_error.details[0] == "HANDLE_INVALID":
                return None
            else:
                raise xenapi_error

    def get_snapshots(self):
        """ Returns Available Snapshots (List of VM object) """

        allSnapshots = []
        snapshots = self.session.xenapi.VM.get_snapshots(self.vm)

        for snapshotNo in snapshots:
            try:
                vm = VM(self.session, snapshots[snapshotNo])
                vm.uuid()

                allSnapshots.append(vm)
            except:
                pass

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

    async def start(self):
        """ Starts VM (Returns Boolean, True: Success, False: Fail) """

        task = self.session.xenapi.Async.VM.start(self.vm, False, False)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def shutdown(self):
        """ Shutdowns VM (Returns Boolean, True: Success, False: Fail) """

        task = self.session.xenapi.Async.VM.clean_shutdown(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def force_shutdown(self):
        """ Force Shutdown VM (Returns Boolean, True: Success, False: Fail) """

        task = self.session.xenapi.Async.VM.hard_shutdown(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def reboot(self):
        """ Reboot VM (Returns Boolean, True: Success, False: Fail) """

        task = self.session.xenapi.Async.VM.clean_reboot(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def force_reboot(self):
        """ Force Reboot VM (Returns Boolean, True: Success, False: Fail) """

        task = self.session.xenapi.Async.VM.hard_reboot(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def snapshot(self, snapshot_name):
        """ Take a snapshot of current VM """

        task = self.session.xenapi.Async.VM.snapshot(self.vm, snapshot_name)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def suspend(self):
        """ Suspend VM """
        task = self.session.xenapi.Async.VM.suspend(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def resume(self):
        task = self.session.xenapi.VM.resume(self.vm, True, False)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def pause(self):
        task = self.session.xenapi.Async.VM.pause(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def unpause(self):
        task = self.session.xenapi.Async.VM.unpause(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def provision(self):
        task = self.session.xenapi.Async.VM.provision(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def clone(self, new_name):
        task = self.session.xenapi.Async.VM.clone(self.vm, new_name)
        data = await Common.xenapi_task_handler(self.session, task, True)
        vm = VM(self.session, data)

        return vm

    async def copy(self, new_name, sr: SR):
        task = self.session.xenapi.Async.VM.copy(self.vm, new_name, sr.sr)
        data = await Common.xenapi_task_handler(self.session, task, True)
        vm = VM(self.session, data)

        return vm

    def set_name(self, name):
        self.session.xenapi.VM.set_name_label(self.vm, name)
        return True

    def set_description(self, description):
        self.session.xenapi.VM.set_name_description(self.vm, description)
        return True

    def set_vCPUs(self, vCPUs, sockets=1):
        tmp_platform = self.session.xenapi.VM.get_platform(
            self.vm,
        )
        vCPU_platform = {"cores-per-socket": str(math.floor(vCPUs / sockets))}

        platform = {**tmp_platform, **vCPU_platform}

        self.session.xenapi.VM.set_platform(self.vm, platform)
        self.session.xenapi.VM.set_VCPUs_max(self.vm, vCPUs)
        self.session.xenapi.VM.set_VCPUs_at_startup(self.vm, vCPUs)

        return True

    def set_memory(self, memory):
        self.session.xenapi.VM.set_memory_limits(
            self.vm, memory, memory, memory, memory
        )
        return True

    def get_platform(self):
        return self.session.xenapi.VM.get_platform(self.vm)

    def set_platform(self, platform):
        return self.session.xenapi.VM.set_platform(self.vm, platform)

    def get_vCPUs(self):
        return self.session.xenapi.VM.get_VCPUs_at_startup(self.vm)

    def get_vCPU_params(self):
        return self.session.xenapi.VM.get_VCPUs_params(self.vm)

    def get_bios_strings(self):
        return self.session.xenapi.VM.get_bios_strings(self.vm)

    def set_bios_strings(self, input_bios_str):

        tmp_bios_str = self.session.xenapi.VM.get_bios_strings(self.vm)
        bios_str = {**tmp_bios_str, **input_bios_str}
        self.session.xenapi.VM.set_bios_strings(self.vm, bios_str)
        return True

    def get_memory(self):

        return self.session.xenapi.VM.get_memory_static_max(self.vm)

    async def delete(self):
        from XenGarden.VBD import VBD

        vbds = self.get_Disks()
        for vbd in vbds:
            vbd.destroy()

        task = self.session.xenapi.Async.VM.destroy(self.vm)
        await Common.xenapi_task_handler(self.session, task, True)

        return True

    async def destroy(self):
        return await self.delete()

    def get_VBDs(self, vbd_type=None):
        from XenGarden.VBD import VBD

        vbds = self.session.xenapi.VM.get_VBDs(self.vm)

        vbd_list = []
        for vbd in vbds:
            try:
                vbd_obj = VBD(self.session, vbd)
                vbd_obj.get_uuid()

                if vbd_type is not None:
                    if vbd_type == vbd_obj.get_type():
                        vbd_list.append(vbd_obj)
                else:
                    vbd_list.append(vbd_obj)
            except:
                pass

        return vbd_list

    def get_VIFs(self):
        from XenGarden.VIF import VIF

        vifs = self.session.xenapi.VM.get_VIFs(self.vm)

        vif_list = []
        for vif in vifs:
            try:
                thisVIF = VIF(self.session, vif)
                thisVIF.get_uuid()
                vif_list.append(thisVIF)
            except:
                pass

        return vif_list

    def get_VIF(self):
        vifs = self.get_VIFs()
        if vifs is not None and len(vifs) > 0:
            return vifs[0]
        else:
            return None

    def get_CD(self):
        return self.get_CDs()[0]

    def get_CDs(self):
        return self.get_VBDs("CD")

    def get_Disks(self):
        return self.get_VBDs("Disk")
