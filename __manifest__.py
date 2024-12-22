# -*- coding: utf-8 -*-
{
    'name': "HR Hospital",
    'version': '17.0.1.0.1',
    'summary': "Hospital management module for training purposes",
    'description': """
This is an exclusively free module created for educational purposes. 
It provides a hospital management system, including doctors, patients, disease types, and appointments.
    """,
    'author': "Odoo School",
    'website': "https://odoo.school/",
    'category': 'Education',
    'license': 'OPL-1',

    # Dependencies (модулі, необхідні для роботи цього модуля)
    'depends': ['base'],

    # Файли даних, які завантажуються завжди
    'data': [
        'security/ir.model.access.csv',  # Права доступу
        'views/hr_hospital_doctor_views.xml',  # Представлення для Doctor
        'views/hr_hospital_patient_views.xml',  # Представлення для Patient
        'views/hr_hospital_disease_type_views.xml',  # Представлення для Disease Type
        'views/hr_hospital_appointment_views.xml',  # Представлення для Appointment
        'views/hr_hospital_menus.xml',  # Меню
    ],

    # Демонстраційні дані (тільки в режимі демонстрації)
    'demo': [
        'demo/disease_type_demo.xml',
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',

    ],

    # Додаткові параметри
    'installable': True,  # Модуль можна встановити
    'application': True,  # Відображати модуль як додаток
    'auto_install': False,  # Модуль не встановлюється автоматично з іншими модулями

    # Зображення для сторінки програми
    'images': [
        'static/description/icon.png'
    ],
}
