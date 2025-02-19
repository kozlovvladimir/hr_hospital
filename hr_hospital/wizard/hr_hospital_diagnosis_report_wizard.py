from odoo import models, fields


class DiagnosisReportWizard(models.TransientModel):
    _name = 'hospital.diagnosis.report.wizard'
    _description = 'Візард для створення звіту по діагнозам'

    # Поле для вибору одного або декількох лікарів
    doctor_ids = fields.Many2many(
        comodel_name='hospital.doctor',
        string='Лікарі',
        help='Оберіть одного або декількох лікарів для звіту. '
             'Якщо поле порожнє, буде використано всіх лікарів.'
    )

    # Поле для вибору однієї або декількох хвороб
    disease_ids = fields.Many2many(
        comodel_name='hospital.disease.type',
        string='Хвороби',
        help='Оберіть одну або декілька хвороб для звіту. '
             'Якщо поле порожнє, буде використано всі хвороби.'
    )

    # Поля для вказання періоду
    date_from = fields.Date(
        string='З дати',
        required=True,
        help='Початкова дата для формування звіту.'
    )
    date_to = fields.Date(
        string='По дату',
        required=True,
        help='Кінцева дата для формування звіту.'
    )

    def action_generate_report(self):
        """Метод для фільтрації діагнозів на основі вказаних критеріїв."""
        domain = []

        # Фільтр за лікарями (якщо вибрано)
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        # Фільтр за хворобами (якщо вибрано)
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        # Фільтр за періодом
        domain.append(('appointment_id.actual_date', '>=', self.date_from))
        domain.append(('appointment_id.actual_date', '<=', self.date_to))

        # Отримання записів моделі "Діагноз"
        # diagnoses = self.env['hospital.diagnosis'].search(domain)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Pivot Report',
            'res_model': 'hospital.diagnosis',
            'view_mode': 'list',
            'target': 'inline',
            'domain': domain
        }
