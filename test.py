import asyncio
import sys
from argparse import ArgumentParser

import XenAPI

from XenGarden.VM import VM

parser = ArgumentParser(
    description="XenGarden Test Script",
)
parser.add_argument(
    "--host",
    dest="host",
    type=str,
    default="127.0.0.1",
    help="The Destination Xenhost (default: 127.0.0.1)",
)
parser.add_argument(
    "--username",
    dest="username",
    type=str,
    default="root",
    help="Username of Xenhost (default: root)",
)
parser.add_argument(
    "--password",
    dest="password",
    default=None,
    help="Password of Xen host",
)


async def main(url="http://127.0.0.1/", username="root", password=""):
    print("XenGarden: ./test.py")
    print("Copyright (c) 2021 Stella IT Inc.")

    # First acquire a valid session by logging in:
    session = XenAPI.Session(url)
    try:
        session.xenapi.login_with_password(username, password)

        print("login successful")
        await test(session)

    except XenAPI.Failure as f:
        print("Failed to acquire a session: %s" % f.details)
        sys.exit(1)
    finally:
        session.xenapi.session.logout()
        print("Test Complete")


async def test(session):
    uuid = "2988e088-ff23-f543-334e-454352a6024a"

    vm = VM.get_by_uuid(session, uuid)
    print(await vm.get_record())

    """
  
  vm = session.xenapi.VM.get_by_uuid(uuid)
  task = session.xenapi.Async.VM.start(vm, False, False)
  data = await Common.xenapi_task_handler(session, task)
  print("started!")
  task = session.xenapi.Async.VM.shutdown(vm)
  data = await Common.xenapi_task_handler(session, task)
  print("shutdown!")
  """


if __name__ == "__main__":
    args = parser.parse_args()
    password = args.password

    if password is None:
        password = input("Enter your password:")

    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main(args.host, args.username, password), loop=loop)
    loop.run_forever()
