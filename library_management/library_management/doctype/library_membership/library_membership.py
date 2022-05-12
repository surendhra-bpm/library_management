# Copyright (c) 2022, surendhranath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryMembership(Document):
	#check before submitting this document
	def before_submit(self):
		exists = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": DocStatus.submitted(),
				# Check if the membership's end date is later than this membership's start date
				"to_date": (">", self.from_date),
			},
		)
		if exists:
			frappe.throw("There is an active membership for this member")

		# get Loan Peroid and comput e to_date by adding loan_period to from_date
		loan_period = frappe.db.get_single_value("Library Settings", "loan_peroid")
		self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)	
		