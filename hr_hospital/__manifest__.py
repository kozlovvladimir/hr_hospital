# -*- coding: utf-8 -*-
{
    'name': "hr_hospital",
    'version': '17.0.1.0.1',
    'summary': "Hospital management module for training purposes",
    'author': "Odoo School",
    'website': "https://odoo.school/",
    'category': 'Education',
    'license': 'OPL-1',

    # Dependencies (модулі, необхідні для роботи цього модуля)
    'depends': ['base'],

    # Файли даних, які завантажуються завжди
    'data': [
        'security/hr_hospital_security.xml',
        'security/ir.model.access.csv',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'wizard/hr_hospital_change_doctor_wizard_views.xml',
        'wizard/hr_hospital_diagnosis_report_wizard_views.xml',
        'views/hr_hospital_disease_type_views.xml',
        'views/hr_hospital_appointment_views.xml',
        'views/hr_hospital_diagnosis_views.xml',
        'views/hr_hospital_menus.xml',
        'report/hr_hospital_doctor_report.xml',
        'report/hr_hospital_doctor_report_templates.xml',
    ],

    # Демонстраційні дані (тільки в режимі демонстрації)
    'demo': [
        'demo/disease_type_demo.xml',
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
        'demo/hospital_appointment_demo.xml',
        'demo/hospital_diagnosis_demo.xml',
    ],

    # Додаткові параметри
    'installable': True,  # Модуль можна встановити
    'application': True,  # Відображати модуль як додаток
    'auto_install': False,  # Модуль не встановлюється автоматично з іншими

    # Зображення для сторінки програми
    'images': [
        'static/description/icon.png'
    ],
}
