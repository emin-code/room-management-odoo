from typing import Any, Union

from odoo import models, fields, api, exceptions
import datetime as dt


class room(models.Model):
    _name = 'rooms.room'

    res_events = fields.One2many('rooms.reservation', string="Event", inverse_name='room_id')
    name = fields.Char(string='Room Name', required=True)
    # TODO: make number get correct id when created
    number = fields.Integer(string='Number', required=True)
    description = fields.Text(string='Description', required=True)
    color = fields.Integer('Color Index', compute='_set_color', default=10)
    status = fields.Selection([
        ('free', 'Available'),
        ('busy', 'Modifying Right Now'),
        ('soon', 'Will be reserved in'),
        ('reserved', 'Reserved')
    ], string='Availability', default='free', compute='compute_status', store=True)
    is_show_events = fields.Boolean(default=True, compute='is_events_visible')

    @api.depends('res_events')
    def is_events_visible(self):
        for rec in self:
            if not rec.res_events:
                rec.is_show_events = False
            else:
                rec.is_show_events = True

    @api.depends('status')
    def _set_color(self):
        for rec in self:
            if rec.status == 'free':
                rec.color = 10
            elif rec.status == 'busy':
                rec.color = 3
            elif rec.status == 'reserved':
                rec.color = 1

    @api.constrains('name', 'description')
    def _check_description(self):
        self.ensure_one()
        if self.name == self.description:
            raise exceptions.ValidationError("Fields name and description must be different")

    def action_reserve(self):
        # TODO: Wizard should be here
        pass

    @api.model
    def create(self, vals):
        # TODO: ???
        res = super(room, self).create(vals)
        # print('override create function')
        return res

    @api.multi
    def write(self, vals):
        # TODO: ???
        # print('override write function')
        res = super(room, self).write(vals)
        return res

    # Runs every 2 minutes via cron
    @api.model
    @api.multi
    def compute_status(self):
        if self.res_events:
            try:
                for rec in self:
                    current = fields.Datetime().from_string(fields.Datetime().now())
                    start = fields.Datetime().from_string(rec.res_events.start_date)
                    time_to_start = (current - start).seconds / 60
                    if time_to_start < 30:
                        self.write({'status': 'soon'})
                    elif time_to_start < 5:
                        self.write({'status': 'reserved'})
                    elif self._is_dirty():
                        self.write({'status': 'busy'})
            except exceptions.MissingError as ex:
                print('Exception info:', ex)
        else:
            print('Computing status is working')
            res = self.search([
                ('status', '!=', 'free'),
            ])
            for r in res:
                r.status = 'free'


class Reservation(models.Model):
    _name = 'rooms.reservation'


    room_id = fields.Many2one('rooms.room', string='Room', required=True)
    name = fields.Char(string='Name', compute='_set_name', default=_name)
    start_date = fields.Datetime(string='Occupied From', default=fields.Datetime().now(), required=True)
    duration = fields.Float(digits=(2, 1), help="Duration in hours", required=True)
    end_date = fields.Datetime(string='Occupied To', store=True,
                               compute='_get_end_date', inverse='_set_end_date', readonly=True)
    person_in_charge = fields.Many2one('hr.employee', string='Person In Charge', required=True)
    reason = fields.Char(string='Reason To Reserve', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
    ], required=True, default='draft', store=True)

    @api.onchange('room_id')
    def _set_name(self):
        self.name = f"{self.room_id.name} reservation"

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.duration):
                rec.end_date = rec.start_date
                continue
            start = fields.Datetime().from_string(rec.start_date)
            duration = dt.timedelta(hours=rec.duration)
            rec.end_date = start + duration

    def _set_end_date(self):
        for rec in self:
            if not (rec.start_date and rec.duration):
                rec.end_date = rec.start_date
                continue
            start_date = fields.Datetime().from_string(rec.start_date)
            end_date = fields.Datetime().from_string(rec.end_date)
            rec.duration = (end_date - start_date).seconds / 3600

    def set_state_confirm(self):
        for r in self:
            r.write({'state': 'confirm'})

    def set_state_done(self):
        for r in self:
            r.write({'state': 'done'})

    def set_state_draft(self):
        for r in self:
            r.write({'state': 'draft'})

    @api.constrains('duration')
    def check_duration(self):
        self.ensure_one()
        if self.duration <= 0.0:
            raise exceptions.ValidationError("Duration must be positive")

    @api.constrains('start_date', 'end_date')
    def check_date(self):
        self.ensure_one()
        if self.start_date < fields.Datetime().now():
            raise exceptions.ValidationError("Start date must be greater than now")
        elif self.start_date == self.end_date:
            raise exceptions.ValidationError("Start/end dates must be different")

    def action_update(self):
        self.update_state_cron()

    # Runs every 2 minutes via cron
    @api.model
    def update_state_cron(self):
        current_datetime = fields.Datetime().now()
        try:
            res = self.search([
                ('end_date', '<=', current_datetime)
            ])
            for r in res:
                r.unlink()
            res = self.search([
                ('state', '!=', 'done'),
            ])
            for r in res:
                r.unlink()
        except exceptions.MissingError as ex:
            print("Exception info:", ex)
