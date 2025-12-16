Changelog
=========

0.11 (2025-12-16)
-----------------

- Removed `to_sign` and `signed` fields from the scanbehavior.
  [chris-adam]
- Corrected `collective.dms.scanbehavior.behaviors.IScanFields` usage
  [sgeulette]

0.10 (2025-11-05)
-----------------

- Commented unneeded code.
  [sgeulette]
- In `utils.highest_scan_id`, get `scan_id` from `brain` index instead metadata
  in case there is a desynchronization between index and metadata and we are
  sure we are re-using the same value as the one used to get
  the highest index value.
  [gbastien]

0.9 (2024-02-12)
----------------

- Raised a ValueError in `utils.next_scan_id` when found highest id doesn't start with scan_type parameter.
  [sgeulette]

0.8 (2024-02-12)
----------------

- Improved `utils.next_scan_id` to check if found highest id starts well with scan_type parameter.
  [sgeulette]
- Added gh actions for tests.
  [sgeulette]

0.7 (2022-10-28)
----------------

- Corrected parameter typo in `utils.next_scan_id` and `utils.scan_id_barcode`.
  Added sphinx compliant doc strings.
  [sgeulette]

0.6 (2021-04-21)
----------------

- In `utils.highest_scan_id`, avoid 2 `return` for lisibility.
  [gbastien]

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
