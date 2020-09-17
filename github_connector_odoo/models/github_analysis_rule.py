# Copyright (C) 2016-Today: Odoo Community Association (OCA)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class GithubAnalysisRule(models.Model):
    _inherit = "github.analysis.rule"

    has_odoo_addons = fields.Boolean(string="Has odoo addons?")
