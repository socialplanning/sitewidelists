This OpenCore plugin package lets you manage sitewide mailing lists, similar to
the per-project mailing lists provided by OpenCore itself.

It requires opencore>=0.18 (dev).

The package provides a zopectl script that will:
 * Create a sitewide `lists` folder
 * Create a sitewide Announce List synced to sitewide membership:
  * all new users will be auto-subscribed upon account confirmation
  * a user's subscription will be auto-removed upon account deletion

Additional sitewide lists can then be created through the standard web interface
by navigating to /siteroot/lists/ as a Site Manager.

Execute `zopectl run opencore_sitewidelists/zopectl_scripts.py` for usage information.
These management commands can be run against a live site if you are using ZEO (which
all Fassembled builds do by default, so if you aren't sure, you can probably assume
you are)
