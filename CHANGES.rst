Changelog
=========

0.5 (2019-09-24)
----------------

- Skip empty scan_id in highest_scan_id method.
  [sgeulette]

0.4 (2018-01-22)
----------------

- Corrected unused parameters in consume function.
  [sgeulette]
- Corrected method not called => made a property.
  [sgeulette]
- Handle several portal types in search. Take the first one for creation
  [sgeulette]

0.3 (2017-12-18)
----------------

- Removed `commit` method that tried to manage retry of failing commits,
  queuing does not manage order, this will be managed another way when necessary.
  [gbastien]
- Added method `consume` that is the default method called by consumers to
  consume a message using the `create_or_update` method.
  [gbastien]

0.2 (2017-11-27)
----------------

- Added possibility to handle several portal_types in methods
  `utils.highest_scan_id`, `utils.next_scan_id` and
  `utils.scan_id_barcode`.
  [gbastien]
- In `utils.highest_scan_id`, do the portal_catalog search unrestricted so we
  are sure that every elements are found.
  [gbastien]
- Make it possible to use a different portal_type for query or creation.  This
  is useful if consumer.file_portal_type returns several portal_types, we need
  to know which of the returned portal_types we need to use for file creation.
  [gbastien]

0.1 (2017-06-01)
----------------
- Some improvements
  [sgeulette]
- Initial release, inspired from imio.dms.amqp.
  [gbastien]
