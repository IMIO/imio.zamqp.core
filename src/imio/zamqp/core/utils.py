# encoding: utf-8

from Acquisition import aq_base
from imio.helpers.barcode import generate_barcode
from imio.zamqp.core import base
from plone import api


def highest_scan_id(file_portal_type='dmsmainfile'):
    """Returns the highest scan_id found for given p_portal_type.
       If no scan_id found, None is returned."""
    catalog = api.portal.get_tool('portal_catalog')
    brains = catalog(portal_type=file_portal_type,
                     sort_on='scan_id',
                     sort_order='descending',
                     sort_limit=1)
    if brains:
        return brains[0].scan_id
    else:
        return None


def next_scan_id(file_portal_type='dmsmainfile', cliend_id_var='client_id', scan_type='3'):
    highest_id = highest_scan_id(file_portal_type=file_portal_type)
    if not highest_id:
        # generate first scan_id, concatenate client_id and first number
        client_id = base.get_config(cliend_id_var)
        highest_id = '%s%s%s00000000' % (client_id[0:2], scan_type, client_id[2:6])
    client_id, unique_id = highest_id[0:7], highest_id[7:15]
    # increment unique_id
    unique_id = "%08d" % (int(unique_id) + 1)
    return client_id + unique_id


def scan_id_barcode(obj, file_portal_type='dmsmainfile', cliend_id_var='client_id', barcode_format='IMIO{0}',
                    scan_type='3', barcode_options={}):
    """Generate the barcode with scan_id for given p_obj :
       - set the scan_id attribute on given p_obj if it does not exist yet;
       - return the data of the generated barcode.
       Some options may be used when generating the barcode, check the
       generate_barcode method to get available options."""
    scan_id = getattr(aq_base(obj), 'scan_id', None)
    if not scan_id:
        scan_id = next_scan_id(file_portal_type=file_portal_type, cliend_id_var=cliend_id_var, scan_type=scan_type)
        obj.scan_id = scan_id
        obj.reindexObject(idxs=['scan_id'])
    barcode = generate_barcode(barcode_format.format(scan_id), **barcode_options)
    return barcode
