# Copyright 2025 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.mail.tools.discuss import Store

original_get_id = Store.One._get_id


def extended_get_id(self):
    result = original_get_id(self)
    # This patch is applied at import time, so it is shared by every registry
    # served by the process, while ``gateway_channel_ids`` only exists in the
    # registries where this module is installed. Check the actual registry.
    if (
        self.records
        and self.records._name == "res.partner"
        and "gateway_channel_ids" in self.records._fields
    ):
        if isinstance(result, int):
            result = {"id": result}
        result["gateway_channels"] = (
            self.records.sudo().gateway_channel_ids.mail_format()
        )
    return result


Store.One._get_id = extended_get_id
