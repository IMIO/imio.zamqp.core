Changelog
=========

0.2 (unreleased)
----------------

- Added possibility to handle several portal_types in methods
  `utils.highest_scan_id`, `utils.next_scan_id` and
  `utils.scan_id_barcode`.
  [gbastien]
- In `utils.highest_scan_id`, do the portal_catalog search unrestricted so we
  are sure that every elements are found.
  [gbastien]

0.1 (2017-06-01)
----------------
- Some improvements
  [sgeulette]
- Initial release, inspired from imio.dms.amqp.
  [gbastien]
