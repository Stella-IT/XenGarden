from deprecated import deprecated
from XenGarden.Common import Common


class Console:
    """ The Virtual Console """

    def __init__(self, session, console):
        self.session = session
        self.console = console

    @deprecated
    async def serialize(self) -> dict:
        (location, protocol, uuid) = asyncio.gather(
            self.get_location(), self.get_protocol(), self.get_uuid()
        )
        
        return {
            "location": location,
            "protocol": protocol,
            "uuid": uuid,
        }

    @staticmethod
    async def get_by_uuid(session, uuid):
        """ returns Console object that has specific uuid """

        console = session.xenapi.console.get_by_uuid(uuid)
        if console is not None:
            return Console(session, console)
        else:
            return None

    async def get_location(self):
        """ The Location for Console """

        return self.session.xenapi.console.get_location(self.console)

    async def get_uuid(self):
        """ Returns UUID of Console """

        return self.session.xenapi.console.get_uuid(self.console)

    async def get_protocol(self):
        """ Returns Protocol of Console """
        return self.session.xenapi.console.get_protocol(self.console)

    async def get_VM(self):
        """ Returns which VM is this console attached to """

        return self.session.xenapi.Async.console.get_VM(self.console)
