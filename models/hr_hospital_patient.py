import logging
from datetime import date
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class Patient(models.Model):
    _name = 'hospital.patient'
    _inherit = 'hr.hospital.person'  # Наслідує поля
    # та поведінку від абстрактної моделі
    _description = 'Пацієнт'

    # Специфічні поля для пацієнтів
    birth_date = fields.Date(
        string='Дата народження',
        required=True,  # Поле обов'язкове для заповнення
    )
    age = fields.Integer(
        string='Вік',
        compute='_compute_age',
        store=True,  # Зберігати значення у базі даних
    )
    passport_data = fields.Char(
        string='Паспортні дані',
        # Дані паспорта або ідентифікаційного документа
    )

    # Поле для зв’язку з іншими пацієнтами
    related_contact = fields.Many2one(
        comodel_name='hospital.patient',
        string='Пов’язаний контакт',
        help="Виберіть пов’язаний контакт серед інших пацієнтів",
        domain="[('id', '!=', id)]",
        # Унеможливлює вибір самого себе як пов'язаного контакту
        context={'no_create': True},
        # Забороняє створення нового пацієнта через це поле
    )

    # Поле для призначення лікаря пацієнту
    doctor = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Особистий лікар',  # Лікар, який відповідає за пацієнта
    )

    # Поле для вказання типу захворювання пацієнта
    disease_type_id = fields.Many2one(
        comodel_name='hospital.disease.type',
        string='Тип захворювання',
        help='Захворювання, на яке страждає пацієнт',
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """Розрахувати вік пацієнта на основі його дати народження."""
        for record in self:
            try:
                if record.birth_date:
                    today = date.today()
                    birth_date = record.birth_date
                    record.age = today.year - birth_date.year - (
                        (today.month, today.day) <
                        (birth_date.month, birth_date.day)
                    )
                else:
                    record.age = 0  # Якщо дата народження не вказана,
                    # вік дорівнює 0
            except Exception as e:
                record.age = 0
                _logger.warning(
                    "Помилка при обчисленні віку для пацієнта "
                    "%(patient)s: %(error)s") % {
                    'patient': record.name,
                    'error': str(e)
                }

    @api.constrains('doctor', 'related_contact')
    def _check_related_doctor(self):
        """Перевірка, що пов’язаний пацієнт не має того ж лікаря."""
        for record in self:
            if (record.related_contact
                    and record.related_contact.doctor == record.doctor):
                raise models.ValidationError(
                    _("Пов'язаний пацієнт не може мати того ж лікаря.")
                )

    @api.model
    def action_open_change_doctor_wizard(self):
        """
        Метод для відкриття візарда зміни лікаря для вибраних пацієнтів.
        """
        active_ids = self.env.context.get('active_ids', [])
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.change.doctor.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_ids': active_ids},  # Передаємо вибрані записи
        }
