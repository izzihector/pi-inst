# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Meeting(models.Model):
    _inherit = 'calendar.event'

    def _get_ics_file(self):
        """ Inherit this function to change Odoo to Pivotino in alarm
        """
        res = super(Meeting, self)._get_ics_file()
        for meeting, ics_file in res.items():
            ics_string = ics_file.decode('UTF-8')
            new_ics_string = ics_string.replace('DESCRIPTION:Odoo',
                                                'DESCRIPTION:Pivotino')
            res[meeting] = new_ics_string.encode('UTF-8')
        return res
