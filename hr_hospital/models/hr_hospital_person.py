from odoo import models, fields


class HrHospitalPerson(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Abstract Person Model'

    # Поля для базової інформації
    surname = fields.Char(string="Прізвище", required=True, default='N/A')
    name = fields.Char(string="Ім'я", required=True)
    phone = fields.Char(string="Телефон")
    photo = fields.Binary(string="Фото")
    gender = fields.Selection(
        selection=[
            ('male', 'Чоловік'),
            ('female', 'Жінка'),
            ('other', 'Інше')
        ],
        string="Стать"
    )

    # Нові поля
    birth_date = fields.Date(
        string="Дата народження",
        help="Дата народження цієї особи."
    )
    passport_data = fields.Char(
        string="Паспортні дані",
        help="Дані паспорта або іншого ідентифікаційного документа."
    )
