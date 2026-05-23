from odoo import models, fields,api

class HmsDoctors(models.Model):
    _name = 'hms.doctors'
    _description = 'Hospital Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Full Name', compute='_compute_full_name')

    image = fields.Image(string='Image')

    @api.depends('first_name', 'last_name')
    def _compute_full_name(self):
        for rec in self:
            if rec.first_name and rec.last_name:
                rec.name = f"{rec.first_name} {rec.last_name}"
            else:
                rec.name = rec.first_name or rec.last_name or ""