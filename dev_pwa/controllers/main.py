import urllib3

from odoo import http
from odoo.http import request


class PwaProxy(http.Controller):

    @http.route('/pwa_sw.js', type='http', auth='public', website=True)
    def load_pwa_sw(self, **kwargs):
        mimetype = "text/javascript"
        http = urllib3.PoolManager()
        base_url = request.env['ir.config_parameter'].sudo().\
            get_param('web.base.url')
        url = base_url + '/dev_pwa/static/src/js/pwa_sw.js'
        response = http.request('GET', url)
        return request.make_response(response.data,
                                     [('Content-Type', mimetype)])
