from odoo import models, fields


class DiseaseType(models.Model):
    _name = 'hospital.disease.type'
    _description = 'Disease Type'
    _parent_store = True  # Активує ієрархічне збереження
    _parent_name = 'parent_id'  # Використовується для ієрархії

    name = fields.Char(
        string='Disease Type Name', required=True
    )  # Назва захворювання
    description = fields.Text()  # Опис захворювання
    symptoms = fields.Text()  # Симптоми
    treatment = fields.Text()  # Рекомендації з лікування
    severity = fields.Selection(selection=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Severity Level', default='low')  # Рівень важкості

    # Поля для ієрархічної структури
    parent_id = fields.Many2one(
        comodel_name='hospital.disease.type',
        string='Parent Disease',
        help='Parent disease type in the hierarchy',
        index=True,
        ondelete='cascade'
    )  # Посилання на батьківську хворобу
    parent_path = fields.Char(index=True, unaccent=False)  # Поле для ієрархії
    child_ids = fields.One2many(
        comodel_name='hospital.disease.type',
        inverse_name='parent_id',
        string='Child Diseases'
    )  # Список дочірніх хвороб
