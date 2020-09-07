import XenAPI


def create_session(_id, get_xen_clusters: dict):
    xen_clusters = get_xen_clusters
    cred = xen_clusters[_id]
    session = XenAPI.Session(cred["host"])
    session.xenapi.login_with_password(cred["username"], cred["password"])
    return session
