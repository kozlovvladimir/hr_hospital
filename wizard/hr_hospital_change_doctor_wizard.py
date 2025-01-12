from odoo import models, fields, api, exceptions, _


class ChangeDoctorWizard(models.TransientModel):
    _name = 'hospital.change.doctor.wizard'
    _description = 'Change Doctor Wizard'

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='New Doctor',
        required=True,
        help='Select the new personal doctor for the selected patients.'
    )
    patient_ids = fields.Many2many(
        comodel_name='hospital.patient',
        string='Selected Patients',
        readonly=True,
        help='Patients selected for reassignment to a new doctor.'
    )

    @api.model
    def default_get(self, fields_list):
        """Set the default patients from the context."""
        res = super(ChangeDoctorWizard, self).default_get(fields_list)
        active_ids = self.env.context.get('active_ids', [])
        if active_ids:
            res['patient_ids'] = [(6, 0, active_ids)]
        return res

    def action_apply_change(self):
        """Assign the selected doctor to the selected patients."""
        if not self.patient_ids:
            raise exceptions.UserError(_("No patients selected."))
        if not self.doctor_id:
            raise exceptions.UserError(_("Please select a doctor."))

        self.patient_ids.write({'doctor': self.doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
