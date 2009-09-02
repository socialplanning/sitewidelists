__doc__ = """
usage:

zopectl run zopectl_scripts.py add [username]
   * adds a sitewide `lists` folder (with a default ISyncWithProjectMembership 
     mailing list, just like a new project) to your OpenCore site.  This list
     will be a Post-Moderated List, instead of a project's default Discussion
     List.

zopectl run zopectl_scripts.py remove [username]
   * removes the sitewide `lists` folder, and all its contents, from your OpenCore
     site. THIS ACTION WILL PERMANENTLY DELETE DATA FROM YOUR SITE IF YOU HAVE A
     LISTS FOLDER INSTALLED; you may prefer to just set its permissions to private
     or otherwise archive it (which this script won't help you with)

zopectl run zopectl_scripts.py sync [username]
   * re-syncs membership/subscriptions for all ISyncWithProjectMembership-marked
     lists in the sitewide `lists` folder (assuming you've already added one) so
     that all existing, confirmed site members are automatically subscribed to
     the sitewide list(s). Warning: this may take a while.

All operations will be performed as user `admin` unless otherwise specified with
the optional [username] argument. 'username' must refer to a user with site manager
permissions findable by acl_users.getUser() [i think this means he can't be a
remember-based user?]  This is useful if you use a particular admin account for
user-facing administrative actions (remember that this will show up in places like
Creator and lastModifiedAuthor metadata) but most likely you can ignore this option.

"""


def setup(app, username='admin', site='openplans'):
    from AccessControl.SecurityManagement import newSecurityManager
    from Testing.makerequest import makerequest

    user = app.acl_users.getUser(username)

    assert user is not None, \
        "Could not find user `%s`; maybe it's a remember-based user?" % username

    user = user.__of__(app.acl_users)
    newSecurityManager(app, user)

    app = makerequest(app)
    
    from zope.app.component.hooks import setSite
    setSite(app[site])

    return app

import sys
try:
    username = sys.argv[2]
except IndexError:
    username = 'admin'

app = setup(app, username=username)

portal = app.openplans

from Products.CMFCore.utils import getToolByName
from Products.listen.interfaces import IWriteMembershipList
from opencore.listen.interfaces import IListenContainer, IListenFeatureletInstalled, ISyncWithProjectMembership
from topp.featurelets.interfaces import IFeatureletSupporter

before = IFeatureletSupporter(portal).getInstalledFeatureletIds()

from Products.listen.interfaces.list_types import PostModeratedListTypeDefinition as PostModerated
from Products.listen.content import ListTypeChanged
from zope.event import notify

if sys.argv[1] == 'add':
    IFeatureletSupporter(portal).installFeaturelet('listen')
    lists_folder = IListenContainer(IListenFeatureletInstalled(portal).lists)
    for mlist in lists_folder.objectValues(spec='OpenMailingList'):
        # what a silly API :-(
        notify(ListTypeChanged(mlist,
                               mlist.list_type.list_marker,
                               PostModerated.list_marker))
            
elif sys.argv[1] == 'remove':
    IFeatureletSupporter(portal).removeFeaturelet('listen')

elif sys.argv[1] == 'sync':
    lists_folder = IListenContainer(IListenFeatureletInstalled(portal).lists)

    mlists = []
    for mlist in lists_folder.objectValues(spec='OpenMailingList'):
        if ISyncWithProjectMembership.providedBy(mlist):
            mlists.append(mlist)

    site_users = getToolByName(portal, 'membrane_tool'
                               ).unrestrictedSearchResults(review_state='public')

    for user in site_users:
        for mlist in mlists:
            IWriteMembershipList(mlist).subscribe(user.getId)

else:
    print __doc__

after = IFeatureletSupporter(portal).getInstalledFeatureletIds()

import transaction
transaction.commit()
