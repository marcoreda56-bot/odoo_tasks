from odoo import models, fields,api
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'hms.patient'           
    _description = 'HMS Patient'    

    first_name = fields.Char(string='First Name', required=True)
    last_name  = fields.Char(string='Last Name',  required=True)
    birth_date = fields.Date(string='Birth Date')
    age        = fields.Integer(string='Age')
    address    = fields.Text(string='Address')

    history    = fields.Html(string='Medical History')
    cr_ratio   = fields.Float(string='CR Ratio')
    pcr        = fields.Boolean(string='PCR')
    blood_type = fields.Selection(
        selection=[
            ('A+',  'A+'),
            ('A-',  'A-'),
            ('B+',  'B+'),
            ('B-',  'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+',  'O+'),
            ('O-',  'O-'),
        ],
        string='Blood Type'
    )
    image = fields.Image(string='Patient Image')

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')
    department_id = fields.Many2one('hms.department', string='Department')
    department_capacity = fields.Integer(related='department_id.capacity', string='Department Capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctors', string='Doctors')
    log_ids = fields.One2many('hms.patient.log', 'patient_id', string='Log History')

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id and not self.department_id.is_opened:
            raise ValidationError("You cannot select a closed department!")
        return {'domain': {'department_id': [('is_opened', '=', True)]}}
    

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_mandatory(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio field is mandatory when PCR is checked!")
            

    @api.onchange('age')
    def _onchange_age_pcr_warning(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "Age Notice",
                    'message': "PCR has been automatically checked because the patient's age is lower than 30.",
                }
            }
        
    
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            self.env['hms.patient.log'].create({
                'patient_id': record.id,
                'description': f"Patient record created with state: {dict(record._fields['state'].selection).get(record.state)}"
            })
        return records

    def write(self, vals):
        if 'state' in vals:
            for record in self:
                if record.state != vals['state']:
                    new_state_label = dict(record._fields['state'].selection).get(vals['state'])
                    self.env['hms.patient.log'].create({
                        'patient_id': record.id,
                        'description': f"State changed to {new_state_label}"
                    })
        return super().write(vals)
    
class HmsPatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient State Log History'
    _order = 'date desc'

    patient_id = fields.Many2one('hms.patient', string='Patient', ondelete='cascade')
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, readonly=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, readonly=True)
    description = fields.Text(string='Description', readonly=True)