from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'create.reservation'
    _inherit = 'rooms.reservation'

    @api.multi
    def action_create(self):
        vals = {
            'room_id': self.room_id.id,
            'name': self.name,
            'start_date': self.start_date,
            'duration': self.duration,
            'end_date': self.end_date,
            'person_in_charge': self.person_in_charge.id,
            'reason': self.reason
        }
        self.env['rooms.reservation'].create(vals)