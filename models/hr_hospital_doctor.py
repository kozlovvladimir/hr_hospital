from odoo import models, fields, api, exceptions


class Doctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Doctor'

    # Основна інформація про лікаря
    name = fields.Char(string='Повне ім’я', required=True)  # Ім’я лікаря (обов’язкове поле)
    date_of_birth = fields.Date(string='Дата народження')  # Дата народження
    gender = fields.Selection([
        ('male', 'Чоловік'),
        ('female', 'Жінка'),
        ('other', 'Інше')
    ], string='Стать')  # Стать лікаря
    phone = fields.Char(string='Номер телефону')  # Номер телефону

    # Спеціалізація лікаря
    specialization = fields.Char(string='Спеціалізація', required=True)  # Спеціалізація лікаря (обов’язкове поле)

    # Поле для зв’язку з інтерном (учнем лікаря)
    intern = fields.Many2one('hospital.doctor', string="Інтерн")  # Інтерн (пов'язаний запис)

    # Поле для зв’язку з ментором (наставником лікаря)
    mentor = fields.Many2one('hospital.doctor', string="Ментор")  # Ментор (пов'язаний запис)

    @api.constrains('intern', 'mentor')
    def _check_mentor_intern(self):
        """Перевірка, щоб інтерн і ментор не були однією й тією самою особою."""
        for record in self:
            if record.intern and record.intern == record.mentor:
                # Якщо інтерн і ментор одна й та сама особа, підняти помилку
                raise exceptions.ValidationError("Інтерн не може бути своїм власним наставником.")

    @api.model
    def create(self, vals):
        """Метод створення запису."""
        return super(Doctor, self).create(vals)

    def write(self, vals):
        """Метод редагування запису."""
        return super(Doctor, self).write(vals)

