from opencore.listen.interfaces import IListenFeatureletInstalled
from opencore.listen.events import _perform_listen_action
from zope.app.component.hooks import getSite 

def member_left_site(event):
    mem = event.member

    try:
        portal = IListenFeatureletInstalled(getSite())
    except TypeError:
        return

    _perform_listen_action(
        portal.lists,
        mem.getId(),
        'unsubscribe'
        )
    
def member_joined_site(event):
    mem = event.member

    try:
        portal = IListenFeatureletInstalled(getSite())
    except TypeError:
        return

    _perform_listen_action(
        portal.lists,
        mem.getId(),
        'subscribe'
        )
