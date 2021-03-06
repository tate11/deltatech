# coding=utf-8

from odoo import api, fields, models, tools, registry
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_round
import threading

class MrpCheckAvailability(models.TransientModel):
    _name = 'mrp.check.availability'
    _description = 'Check Availability'

    background = fields.Boolean('Run in background', default=True)

    @api.multi
    def do_check_availability(self):
        if self.background:
            threaded_calculation = threading.Thread(target=self._do_check_availability, args=())
            threaded_calculation.start()
        else:
            active_ids = self.env.context.get('active_ids', False)
            productions = self.env['mrp.production'].browse(active_ids)
            productions.action_assign()
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def _do_check_availability(self):
        active_ids = self.env.context.get('active_ids', False)
        print active_ids
        with api.Environment.manage():
            new_cr = registry(self._cr.dbname).cursor()
            self = self.with_env(self.env(cr=new_cr))
            productions = self.env['mrp.production'].browse(active_ids)
            productions.action_assign()
            new_cr.commit()
            new_cr.close()

