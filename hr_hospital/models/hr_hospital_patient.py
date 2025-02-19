import logging
from datetime import date
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hospital.patient'
    _inherit = 'hr.hospital.person'  # Наслідує баз.поля з hr.hospital.person
    _description = 'Пацієнт'

    # Специфічні поля для пацієнтів
    birth_date = fields.Date(
        string='Дата народження',
        required=True,  # Поле обов'язкове для заповнення
    )
    age = fields.Integer(
        string='Вік',
        compute='_compute_age',
        store=True,  # Значення зберігається у базі даних
    )
    passport_data = fields.Char(
        string='Паспортні дані',
        help="Дані паспорта або іншого ідентифікаційного документа."
    )

    # Поле для зв’язку з іншими пацієнтами
    related_contact = fields.Many2one(
        comodel_name='hospital.patient',
        string='Пов’язаний контакт',
        help="Виберіть пов’язаний контакт серед інших пацієнтів",
        domain="[('id', '!=', id)]",
        context={'no_create': True},  # Забороняє створення нового запису
    )

    # Поле для призначення лікаря пацієнту
    doctor = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Особистий лікар',
        help="Лікар, який відповідає за пацієнта.",
    )

    # Поле для вказання типу захворювання пацієнта
    disease_type_id = fields.Many2one(
        comodel_name='hospital.disease.type',
        string='Тип захворювання',
        help="Тип захворювання, яким страждає пацієнт.",
    )

    # Поле для історії діагнозів пацієнта
    diagnosis_ids = fields.One2many(
        comodel_name='hospital.diagnosis',
        inverse_name='patient_id',
        string="Історія діагнозів",
    )

    # Поле для історії візитів
    appointment_ids = fields.One2many(
        comodel_name='hospital.appointment',
        inverse_name='patient',
        string="Історія візитів",
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """Розрахувати вік пацієнта на основі його дати народження."""
        for record in self:
            try:
                if record.birth_date:
                    today = date.today()
                    birth_date = record.birth_date
                    record.age = (
                        today.year - birth_date.year
                        - ((today.month, today.day)
                           < (birth_date.month, birth_date.day))
                    )
                else:
                    record.age = 0  # Якщо дата народження не вказана
            except Exception as e:
                record.age = 0
                _logger.warning(
                    "Помилка при обчисленні віку для пацієнта "
                    "%(patient)s: %(error)s",
                    {'patient': record.name, 'error': str(e)}
                )

    @api.constrains('doctor', 'related_contact')
    def _check_related_doctor(self):
        """Перевірка, що пов’язаний пацієнт не має того ж лікаря."""
        for record in self:
            if (record.related_contact
                    and record.related_contact.doctor == record.doctor):
                raise models.ValidationError(
                    _("Пов'язаний пацієнт не може мати того ж лікаря.")
                )

    def action_open_appointment_history(self):
        """
        Метод для відкриття історії візитів поточного пацієнта.
        """
        return {
            'type': 'ir.actions.act_window',
            'name': 'Історія візитів',
            'res_model': 'hospital.appointment',
            'view_mode': 'tree,form',
            'domain': [('patient', '=', self.id)],
        }

    def action_create_appointment(self):
        """
        Метод для швидкого створення запису про візит.
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient': self.id,
                'default_doctor': self.doctor.id if self.doctor else False,
            },
        }
