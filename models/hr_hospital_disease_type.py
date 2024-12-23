from odoo import models, fields


class DiseaseType(models.Model):
    _name = 'hospital.disease.type'
    _description = 'Disease Type'

    name = fields.Char(
        string='Disease Type Name', required=True
    )  # Назва захворювання
    description = fields.Text(string='Description')  # Опис захворювання
    symptoms = fields.Text(string='Symptoms')  # Симптоми
    treatment = fields.Text(string='Treatment')  # Рекомендації з лікування
    severity = fields.Selection(selection=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Severity Level', default='low')  # Рівень тяжкості
