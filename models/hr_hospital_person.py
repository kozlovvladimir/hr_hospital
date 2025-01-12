from odoo import models, fields


class HrHospitalPerson(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Abstract Person Model'

    surname = fields.Char(required=True, default='N/A')
    name = fields.Char(required=True)
    phone = fields.Char()
    photo = fields.Binary()
    gender = fields.Selection(selection=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ])
