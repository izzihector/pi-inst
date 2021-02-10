# from backend_theme_v13.controllers import DasboardBackground
from odoo.addons.backend_theme_v13.controllers.main import DasboardBackground
from odoo.http import Controller, request, route
from werkzeug.utils import redirect

PIVOTINO_BACKGROUND = '/pivotino_web_responsive/static/src/img/pivo-bg.png'


class DashboardBackGround(DasboardBackground):
    # inherit and change the background for dashboard
    @route(['/dashboard'], type='http', auth='user', website=False)
    def dashboard(self, **post):
        company = request.env.user.company_id
        if company.dashboard_background:
            return super(DashboardBackGround, self).dashboard(post)
        else:
            return redirect(PIVOTINO_BACKGROUND)
