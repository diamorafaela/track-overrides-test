import frappe

@frappe.whitelist()
def get_item_details(args, doc=None, for_validate=False, overwrite_warehouse=True):
	"""
	HASH: 5c5349ed16680a22a8fd16a1f6f9ed16957069b4
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/stock/get_item_details.py
	METHOD: get_item_details
	"""
	import erpnext.stock.get_item_details

	erpnext.stock.get_item_details.validate_item_details = validate_item_details
	out = erpnext.stock.get_item_details.get_item_details(
		args, doc, for_validate, overwrite_warehouse
	)
	return out