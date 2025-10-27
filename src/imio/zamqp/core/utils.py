# encoding: utf-8

from Acquisition import aq_base
from imio.helpers.barcode import generate_barcode
from imio.zamqp.core import base
from plone import api


def highest_scan_id(file_portal_types=['dmsmainfile']):
    """Returns the highest scan_id found for given types

    :param file_portal_types: searched portal types
    :return: found scan_id, or None if nothing is found
    """
    catalog = api.portal.get_tool('portal_catalog')
    # do the search unrestricted so we are sure to get every elements
    brains = catalog.unrestrictedSearchResults(
        portal_type=file_portal_types,
        sort_on='scan_id',
        sort_order='descending',
        sort_limit=1)
    # highest_id = None
    if brains:
        # we use the index value so we are sure it is the same value
        # used in the previous catalog.unrestrictedSearchResults query
        return catalog.getIndexDataForRID(brains[0].getRID())['scan_id']
        # for brain in brains:  # no idea why this code was added in place of brains[0]
        #     if brain.scan_id != 'None':
        #         highest_id = brain.scan_id
    # return highest_id
    return None


def next_scan_id(file_portal_types=['dmsmainfile'], client_id_var='client_id', scan_type='3'):
    """Get next scan id to use following highest scan_id found on given types

    :param file_portal_types: types to search on highest used scan_id
    :param client_id_var: client id variable name in config
    :param scan_type: scan type number, used as third number in scan code
    :return: new full scan_id
    """
    highest_id = highest_scan_id(file_portal_types=file_portal_types)
    client_id = base.get_config(client_id_var)
    prefix = '{}{}{}'.format(client_id[0:2], scan_type, client_id[2:6])
    # limitation: doesn't check if the generated id already exists in catalog
    if not highest_id:
        # generate first scan_id, concatenate client_id and first number
        highest_id = '{}00000000'.format(prefix)
    elif not highest_id.startswith(prefix):
        raise ValueError("highest_id '{}' doesn't start with prefix '{}'".format(highest_id, prefix))
    # increment unique_id
    unique_id = "{:08d}".format(int(highest_id[7:15]) + 1)
    return prefix + unique_id


def scan_id_barcode(obj, file_portal_types=['dmsmainfile'],
                    client_id_var='client_id', barcode_format='IMIO{0}',
                    scan_type='3', barcode_options={}, scan_id=None):
    """Generate the barcode with scan_id for given p_obj (and set the scan_id attribute on given p_obj
    if it does not exist yet).

    :param obj: object to get scan_id on
    :param file_portal_types: types to search on highest used scan_id
    :param client_id_var: client id variable name in config
    :param barcode_format: string pattern used when formatting string
    :param scan_type: scan type number, used as third number in scan code
    :param barcode_options: barcode options dict, passed to imio.helpers.barcode.generate_barcode function
    :param scan_id: optional scan_id to use
    :return: new full barcode
    """
    scan_id = scan_id or getattr(aq_base(obj), 'scan_id', None)
    if not scan_id:
        scan_id = next_scan_id(file_portal_types=file_portal_types,
                               client_id_var=client_id_var,
                               scan_type=scan_type)
        obj.scan_id = scan_id
        obj.reindexObject(idxs=['scan_id'])
    barcode = generate_barcode(barcode_format.format(scan_id), **barcode_options)
    return barcode
