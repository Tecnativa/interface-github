# Copyright 2020 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, tools


class GithubRepositoryBranchRuleInfoReport(models.Model):
    _inherit = "github.analysis.rule"
    _name = "github.repository.branch.rule.info.report"
    _description = "Github Repository Branch Rule Info Report"
    _auto = False

    analysis_rule_id = fields.Many2one(
        string="Analysis Rule", comodel_name="github.analysis.rule",
    )
    group_id = fields.Many2one(
        string="Group", related="analysis_rule_id.group_id", readonly=True
    )
    repository_branch_id = fields.Many2one(
        string="Repository Branch", comodel_name="github.repository.branch",
    )
    repository_id = fields.Many2one(
        string="Repository", comodel_name="github.repository",
    )
    organization_serie_id = fields.Many2one(
        string="Organization serie", comodel_name="github.organization.serie",
    )
    code_count = fields.Integer(string="# Code")
    documentation_count = fields.Integer(string="# Documentation")
    empty_count = fields.Integer(string="# Empty")
    string_count = fields.Integer(string="# String")
    total_count = fields.Integer(string="# Total")
    scanned_files = fields.Integer(string="Scanned files")

    def init(self):
        tools.drop_view_if_exists(self._cr, "github_repository_branch_rule_info_report")
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW github_repository_branch_rule_info_report AS (
                SELECT
                MIN(grbri.id) AS id,
                gar.id AS analysis_rule_id,
                garg.id AS group_id,
                grb.id AS repository_branch_id,
                gr.id AS repository_id,
                gos.id AS organization_serie_id,
                SUM(grbri.code_count) AS code_count,
                SUM(grbri.documentation_count) AS documentation_count,
                SUM(grbri.string_count) AS string_count,
                SUM(grbri.empty_count) AS empty_count,
                SUM(grbri.total_count) AS total_count,
                SUM(grbri.scanned_files) AS scanned_files
                FROM github_repository_branch_rule_info AS grbri
                LEFT JOIN github_analysis_rule AS gar ON grbri.analysis_rule_id = gar.id
                LEFT JOIN github_analysis_rule_group AS garg ON gar.group_id = garg.id
                LEFT JOIN github_repository_branch AS grb
                ON grbri.repository_branch_id = grb.id
                LEFT JOIN github_organization_serie AS gos
                ON grb.organization_serie_id = gos.id
                LEFT JOIN github_repository AS gr ON grb.repository_id = gr.id
                WHERE grbri.id > 0
                GROUP BY gar.id, garg.id, grb.id, gr.id, gos.id
        )"""
        )
