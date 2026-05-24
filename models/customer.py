from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')
    vat = fields.Char(string='Tax ID')

    @api.constrains('vat')
    def _check_vat_mandatory(self):
        for record in self:
            if not record.vat:
                raise ValidationError("Tax ID field is mandatory for CRM Customers!")

    @api.constrains('email', 'related_patient_id')
    def _check_customer_email_in_patients(self):
        for record in self:
            if record.email:
                existing_patient = self.env['hms.patient'].search([('email', '=', record.email)], limit=1)
                if existing_patient:
                    raise ValidationError("This email already exists in the Patients model! You cannot use it for a customer.")

    def unlink(self):
        for record in self:
            if record.related_patient_id:
                raise ValidationError("You cannot delete this customer because they are linked to a patient profile!")
        return super().unlink()