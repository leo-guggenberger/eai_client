# res_config.py
# -*- coding: utf-8 -*-

from openerp import models, fields

# Table inherit config
class eai_client_config_settings(models.Model):
    _name = 'eai_client.config.settings'
    _inherit = 'res.config.settings'
    
    eai_client_name = fields.Char('EAI Client Name')
    eai_server_url = fields.Char('EAI Server Url')
    eai_server_db = fields.Char('EAI Server Database')
    eai_server_username = fields.Char('EAI Server User'), default='admin'
    eai_server_password = fields.Char('EAI Server Password'), default='admin', password=true
