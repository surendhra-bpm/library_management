# Copyright (c) 2022, surendhranath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryTransaction(Document):
	def before_submit(self):
		if self.type == "Issue":
			self.validate_issue()
			# Set the articles status to be Issued
			articles = frappe.get_doc("Articles", self.articles)
			articles.status = "Issued"
			articles.save()

		elif self.type == "Return":
			self.validate_retun()
			# Set the Articles status to be Available
			articles = frappe.get_doc("Articles", self.artilces)
			articles.status = "Available"
			articles.save()
	def validate_issue(self):
		self.validate_membership()
		articles = frappe.get_doc("Articles", self.articles)
		# Articles cannot be issued it it is already Issued
		if articles.status == "Issued":
			frappe.throw("Article is already issued by another member")
	def validate_return(self):
		articles = frappe.get_doc("Articles", self.articles)
		# Articles cannot be retunedif it is not issued first
		if articles.status == "Available":
			frappe.throw("Article cannot be returned without being issued first")
	def validate_membership(self):
		# Check if a valid membership exist for this library member
		valid_membership == frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": DocStatus.submitted(),
				"from_date": ("<", self.date),
				"to_date": (">", self.date),
			},
		)
		if not valid_membership:
			frappe.throw("The member does not have a valid membership")
