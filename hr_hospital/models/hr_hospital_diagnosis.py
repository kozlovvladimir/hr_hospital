from odoo import models, fields, api, exceptions, _


class Diagnosis(models.Model):
    _name = 'hospital.diagnosis'
    _description = 'Patient Diagnosis'

    # Поле для зв'язку з прийомом (Appointment)
    appointment_id = fields.Many2one(
        comodel_name='hospital.appointment',
        string='Appointment',
        required=True,
        ondelete='cascade'
    )

    # Поле для зв'язку з захворюванням (Disease Type)
    disease_id = fields.Many2one(
        comodel_name='hospital.disease.type',
        string='Disease',
        required=True
    )

    # Поле для зв'язку з пацієнтом (Patient)
    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        required=True,
        help='The patient for whom this diagnosis is recorded.'
    )

    # Поле для опису лікування
    description = fields.Text(string='Treatment Description')

    # Поле для статусу затвердження діагнозу
    approved = fields.Boolean(
        default=False,
        help='Indicates if this diagnosis has been reviewed '
             'and approved by the mentor doctor.'
    )

    # Поле для зв'язку з лікарем (Doctor)
    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Diagnosing Doctor',
        required=True,
        help='The doctor who made the diagnosis.'
    )

    @api.constrains('doctor_id', 'approved')
    def _check_mentor_approval(self):
        """Ensure that intern diagnoses are approved by their mentor."""
        for record in self:
            if (record.doctor_id.is_intern and record.approved
                    and not record.doctor_id.mentor_id):
                raise exceptions.ValidationError(_(
                    "Intern's diagnosis cannot be approved "
                    "without a mentor's review."
                ))
