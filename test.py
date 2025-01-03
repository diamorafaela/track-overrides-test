import frappe


def validate_pos_paid_amount(self):
	"""
	HASH: 4f29908aa94c9cc4d189c38bb73b30c16b894f05
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/accounts/doctype/sales_invoice/sales_invoice.py
	METHOD: validate_pos_paid_amount
	"""
	if len(self.payments) == 0 and self.is_pos:
		frappe.throw(_("At least one mode of payment is required for POS invoice."))


def add_remarks(self):
	"""
	HASH: 6b1acc3283aaa647786f588965e0b7db14dfccd8
	REPO: https://github.com/frappe/erpnext/
	PATH: erpnext/accounts/doctype/sales_invoice/sales_invoice.py
	METHOD: add_remarks
	"""
	if not self.remarks:
		if self.po_no and self.po_date:
			self.remarks = _("Against Customer Order {0} dated {1}").format(
				self.po_no, formatdate(self.po_date)
			)
		else:
			self.remarks = _("No Remarks")