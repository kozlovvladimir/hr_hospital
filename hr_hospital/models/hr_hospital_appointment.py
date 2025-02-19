from odoo import models, fields, api, exceptions, _


class Appointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Doctor Appointment'

    # Основні поля
    doctor = fields.Many2one(
        comodel_name='hospital.doctor',
        required=True,
        help="The doctor assigned to this appointment."
    )
    patient = fields.Many2one(
        comodel_name='hospital.patient',
        required=True,
        help="The patient for whom this appointment is scheduled."
    )
    planned_date = fields.Datetime(
        string='Planned Appointment Date and Time',
        required=True,
        help="Date and time when the appointment is scheduled."
    )
    actual_date = fields.Datetime(
        string='Actual Appointment Date and Time',
        help="Date and time when the appointment actually occurred."
    )
    status = fields.Selection(
        [
            ('planned', 'Planned'),
            ('done', 'Completed'),
            ('cancelled', 'Cancelled')
        ],
        default='planned',
        required=True,
        help="The current status of the appointment."
    )
    diagnosis_ids = fields.One2many(
        comodel_name='hospital.diagnosis',
        inverse_name='appointment_id',
        string='Diagnoses',
        help="List of diagnoses associated with this appointment."
    )
    recommendations = fields.Text(
        help="Recommendations provided to the patient during "
             "or after the appointment."
    )
    is_done = fields.Boolean(
        string='Is Appointment Done',
        default=False,
        help="Indicates whether the appointment has been marked as completed."
    )

    # Додаткове поле для унікальності прийому
    name = fields.Char(
        string="Appointment Reference",
        readonly=True,
        default=lambda self: _('New'),
        copy=False
    )

    # Автоматичне встановлення імені запису
    @api.model
    def create(self, vals):
        """Генерація унікального посилання (імені) для запису."""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = (self.env['ir.sequence'].
                            next_by_code('hospital.appointment') or _('New'))
        return super(Appointment, self).create(vals)

    # Обмеження на дублювання записів для лікаря на одну дату
    @api.constrains('doctor', 'planned_date')
    def _check_duplicate_appointment(self):
        """Забезпечення, що один лікар не має більше одного прийому
        на ту саму дату і час."""
        for record in self:
            domain = [
                ('doctor', '=', record.doctor.id),
                ('planned_date', '=', record.planned_date),
                ('id', '!=', record.id)
            ]
            if self.search_count(domain) > 0:
                raise exceptions.ValidationError(_(
                    'An appointment with the same doctor '
                    'at this planned time already exists.'))

    # Захист від зміни ключових полів для завершених прийомів
    @api.constrains('status', 'actual_date', 'planned_date', 'doctor')
    def _check_immutable_fields(self):
        """Забороняється редагувати ключові поля у завершених прийомах."""
        for record in self:
            if record.status == 'done':
                if self.env.context.get('force_edit', False):
                    continue  # Дозволити зміни в особливих випадках
                if any(
                    record[field] != self[field]
                    for field in ['doctor', 'planned_date']
                ):
                    raise exceptions.ValidationError(_(
                        'You cannot change the doctor '
                        'or planned date for an appointment '
                        'that has already been completed.'))

    # Заборона видалення прийомів з діагнозами
    @api.ondelete(at_uninstall=False)
    def _check_delete(self):
        """Не дозволяти видалення прийомів, до яких прив’язані діагнози."""
        for record in self:
            if record.diagnosis_ids:
                raise exceptions.UserError(_(
                    'You cannot delete appointments with linked diagnoses.'
                ))
