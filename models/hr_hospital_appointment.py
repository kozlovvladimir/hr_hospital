from odoo import models, fields, api, exceptions


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Doctor Appointment'

    doctor = fields.Many2one('hospital.doctor', string='Doctor', required=True)
    patient = fields.Many2one('hospital.patient', string='Patient', required=True)
    appointment_date = fields.Datetime(string='Appointment Date and Time', required=True)
    diagnosis = fields.Many2one('hospital.disease.type', string='Diagnosis')  # Вид захворювання
    recommendations = fields.Text(string='Recommendations')
    is_done = fields.Boolean(string='Is Appointment Done', default=False)

    @api.constrains('doctor', 'appointment_date')
    def _check_duplicate_appointment(self):
        """Ensure there are no duplicate appointments for the same doctor at the same time."""
        for record in self:
            domain = [
                ('doctor', '=', record.doctor.id),
                ('appointment_date', '=', record.appointment_date),
                ('id', '!=', record.id)
            ]
            if self.search_count(domain) > 0:
                raise exceptions.ValidationError('An appointment with the same doctor at this time already exists.')
