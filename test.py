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

def validate_job_card(self):
	"""
	HASH: 4d34b1ead73baf4c5430a2ecbe44b9e8468d7626
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/manufacturing/doctype/job_card/job_card.py
	METHOD: validate_job_card
	"""
	return

def make_work_order(self):
	"""
	HASH: b087fb3d549462ea8c9d1e65e8622e952d4039f6
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/manufacturing/doctype/production_plan/production_plan.py
	METHOD: make_work_order
	"""
	return

def make_work_order_for_subassembly_items(self, wo_list, subcontracted_po, default_warehouses):
	"""
	HASH: b087fb3d549462ea8c9d1e65e8622e952d4039f6
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/manufacturing/doctype/production_plan/production_plan.py
	METHOD: make_work_order_for_subassembly_items
	"""
	return

def validate_with_previous_doc(self):
	"""
	HASH: e7432fc60d4b5b82363212ae003cb7d2d4e8f294
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/accounts/doctype/purchase_invoice/purchase_invoice.py
	METHOD: validate_with_previous_doc
	"""
	return


def validate_item_details(args, item):
	"""
	HASH: 5c5349ed16680a22a8fd16a1f6f9ed16957069b4
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/stock/get_item_details.py
	METHOD: validate_item_details
	"""
	return

def check_if_operations_completed(self):
	"""
	HASH: 153e0ba81b62acc170a951a289363fff5579edc7
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/stock/doctype/stock_entry/stock_entry.py
	METHOD: check_if_operations_completed

	Original code checks that the stock entry amount plus what's already produced in the WO
	is not larger than any operation's completed quantity (plus the overallowance amount).
	Since customized code rewires so stock entries happen via a Job Card, the function now
	checks that the stock entry amount plus what's already been produced in the WO is not
	greater than the amount to be manufactured plus the overallowance amount.
	"""
	return

def validate_finished_goods(self):
	"""
	HASH: 153e0ba81b62acc170a951a289363fff5579edc7
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/stock/doctype/stock_entry/stock_entry.py
	METHOD: validate_finished_goods

	1. Check if FG exists (mfg, repack)
	2. Check if Multiple FG Items are present (mfg)
	3. Check FG Item and Qty against WO if present (mfg)
	"""
	return


def get_pending_raw_materials(self, backflush_based_on=None):
	"""
	HASH: 153e0ba81b62acc170a951a289363fff5579edc7
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/stock/doctype/stock_entry/stock_entry.py
	METHOD: get_pending_raw_materials

	issue (item quantity) that is pending to issue or desire to transfer,
	whichever is less
	"""
	return