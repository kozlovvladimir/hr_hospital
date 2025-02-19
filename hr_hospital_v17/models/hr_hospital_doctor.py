from odoo import models, fields, api, exceptions, _


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    # Спеціалізація лікаря
    specialization = fields.Selection(
        selection=[
            ('cardiologist', 'Cardiologist'),
            ('neurologist', 'Neurologist'),
            ('pediatrician', 'Pediatrician'),
            ('general_practitioner', 'General Practitioner'),
            ('surgeon', 'Surgeon'),
        ],
        required=True,
        help='Specialization of the doctor'
    )

    # Поле, яке визначає, чи є лікар інтерном
    is_intern = fields.Boolean(
        string='Intern',
        default=False,
        help='Indicates whether the doctor is an intern.'
    )

    appointment_ids = fields.One2many(
        comodel_name='hospital.appointment',
        inverse_name='doctor'
    )

    patient_ids = fields.One2many(
        comodel_name='hospital.patient',
        inverse_name='doctor'
    )

    # Поле для вказання ментора для інтерна
    mentor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Mentor',
        help='Mentor for the intern.',
        domain="[('is_intern', '=', False)]"
    )

    # Список інтернів, які підпорядковуються цьому ментору
    intern_ids = fields.One2many(
        comodel_name='hospital.doctor',
        inverse_name='mentor_id',
        string='Interns',
        help='List of interns under this mentor.'
    )

    # Метод для перевірки, що інтерн має ментора
    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor_and_intern(self):
        """Ensure the intern is not their own mentor
        and has a mentor assigned."""
        for record in self:
            if record.is_intern and not record.mentor_id:
                raise exceptions.ValidationError(
                    _("An intern must have a mentor assigned.")
                )
            if record.mentor_id == record:
                raise exceptions.ValidationError(
                    _("An intern cannot be their own mentor.")
                )

    # Метод для перевірки, що ментор не є інтерном
    @api.constrains('mentor_id')
    def _check_mentor_not_intern(self):
        """Ensure the mentor is not an intern."""
        for record in self:
            if record.mentor_id and record.mentor_id.is_intern:
                raise exceptions.ValidationError(
                    _("A mentor cannot be an intern.")
                )

    # Метод для створення швидкого запису до лікаря
    def action_create_appointment(self):
        """
        Метод для створення швидкого запису до лікаря.
        Повертає форму для створення нового візиту.
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor': self.id,
            },
        }

    # Додаткове поле для підрахунку кількості інтернів
    intern_count = fields.Integer(
        compute='_compute_intern_count',
        help='Shows the total number of interns under this mentor.'
    )

    @api.depends('intern_ids')
    def _compute_intern_count(self):
        """Обчислює кількість інтернів для кожного ментора."""
        for record in self:
            record.intern_count = len(record.intern_ids)

    # Додатковий метод для відкриття списку інтернів
    def action_view_interns(self):
        """
        Відкриває список інтернів, підпорядкованих цьому ментору.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': _('Interns'),
            'res_model': 'hospital.doctor',
            'view_mode': 'tree,form',
            'domain': [('mentor_id', '=', self.id)],
        }

    # Додатковий метод для перегляду записів пацієнтів лікаря
    def action_view_patients(self):
        """
        Метод для відкриття списку пацієнтів, закріплених за цим лікарем.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': _('Patients'),
            'res_model': 'hospital.patient',
            'view_mode': 'tree,form',
            'domain': [('doctor', '=', self.id)],
        }

    def action_print_report(self):
        """Функція для виклику друкованого звіту"""
        return self.env.ref(
            'hr_hospital1.report_hospital_doctor').report_action(self)
