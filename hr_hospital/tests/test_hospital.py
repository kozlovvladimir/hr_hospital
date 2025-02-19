from datetime import datetime, date
from odoo.tests.common import TransactionCase


class TestHospitalModels(TransactionCase):
    """Тести для перевірки основних функцій модуля hr_hospital1."""

    def setUp(self):
        """Підготовка тестових даних перед запуском тестів."""
        super(TestHospitalModels, self).setUp()

        # Створюємо тестового лікаря
        self.doctor = self.env['hospital.doctor'].create({
            'name': 'Dr. House',
            'surname': 'House',
            'specialization': 'general_practitioner',
            'is_intern': False
        })

        # Створюємо тестового пацієнта
        self.patient = self.env['hospital.patient'].create({
            'name': 'John Doe',
            'surname': 'Doe',
            'birth_date': '1990-05-15',  # Пацієнту 34 роки
            'doctor': self.doctor.id
        })

    def test_create_appointment_sequence(self):
        """Перевірка, чи створюється унікальний код прийому."""
        appointment = self.env['hospital.appointment'].create({
            'doctor': self.doctor.id,
            'patient': self.patient.id,
            'planned_date': datetime.now(),
        })

        self.assertNotEqual(appointment.name, 'New',
                            "Код прийому не було згенеровано.")
        self.assertTrue(appointment.name.startswith('APT'),
                        "Код прийому має невірний формат.")

    def test_doctor_intern_must_have_mentor(self):
        """Перевірка, що лікар-інтерн повинен мати ментора."""
        intern = self.env['hospital.doctor'].create({
            'name': 'Intern Smith',
            'surname': 'Smith',
            'specialization': 'surgeon',
            'is_intern': True
        })

        with self.assertRaises(Exception,
                               msg="Інтерн без ментора був створений!"):
            intern._check_mentor_and_intern()

    def test_patient_age_calculation(self):
        """Перевірка, чи правильно рахується вік пацієнта."""
        self.patient._compute_age()
        expected_age = (date.today().year - 1990
                        - ((date.today().month, date.today().day) < (5, 15)))
        self.assertEqual(self.patient.age, expected_age,
                         "Розрахунок віку невірний.")
