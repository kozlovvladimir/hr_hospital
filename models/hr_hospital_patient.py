from odoo import models, fields, api
from datetime import date

class Patient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'

    # Основна інформація про пацієнта
    name = fields.Char(string='Повне ім’я', required=True)  # Ім’я пацієнта
    birth_date = fields.Date(string='Дата народження', required=True)  # Дата народження
    gender = fields.Selection([
        ('male', 'Чоловік'),
        ('female', 'Жінка'),
        ('other', 'Інше')
    ], string='Стать', required=True)  # Стать пацієнта
    phone = fields.Char(string='Номер телефону')  # Номер телефону

    # Поле для віку, яке обчислюється автоматично
    age = fields.Integer(string='Вік', compute='_compute_age', store=True)

    # Паспортні дані пацієнта
    passport_data = fields.Char(string='Паспортні дані')

    # Пов'язаний контакт (інший пацієнт)
    related_contact = fields.Many2one(
        'hospital.patient',
        string='Пов’язаний контакт',
        help="Оберіть пов’язаний контакт з інших пацієнтів",
        domain="[('id', '!=', id)]",  # Не дозволяє обирати самого себе
        context={'no_create': True}   # Вимикає можливість створення нового запису
    )

    # Поле для лікаря, який відповідає за пацієнта
    doctor = fields.Many2one('hospital.doctor', string='Особистий лікар')

    # Вид захворювання пацієнта
    disease_type_id = fields.Many2one(
        'hospital.disease.type',
        string='Disease Type',
        help='Disease the patient is suffering from'
    )

    @api.depends('birth_date')
    def _compute_age(self):
        """Обчислення віку на основі дати народження."""
        for record in self:
            if record.birth_date:
                today = date.today()
                birth_date = record.birth_date
                record.age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month, birth_date.day)
                )
            else:
                record.age = 0
