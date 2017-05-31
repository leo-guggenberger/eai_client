# eai_client_scheduler.py
# -*- coding: utf-8 -*-

from openerp import models
import xmlrpclib

# EAI Client Scheduler
class eai_client_scheduler(models.Model):

    _name = 'eai_client.scheduler'
    _description = 'EAI Client Scheduler'

    def run_scheduler(self, cr, uid, context=None):
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        eai_server_url = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_server_url
        eai_server_db = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_server_db
        eai_server_user = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_server_user
        eai_server_password = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_server_password
        
        # Step 1: Produkte ausspielen
        #product_ids = self.pool['product.template'].search(cr,uid, ['|',('company_id','=',company_id),('active','=','true'),('sale_ok','=','true')], context=context)
        eai_server_models = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(eai_server_url))
        eai_server_uid = eai_server_models.authenticate(eai_server_db, eai_server_user, eai_server_password, {})
        eai_server_models.execute_kw(eai_server_db, eai_server_uid, eai_server_password,'eai_server.messages', 'check_access_rights', ['create'], {'raise_exception': False})
        eai_serverid = eai_server_models.execute_kw(eai_server_db, eai_server_uid, eai_server_password, 'eai_server.messages', 'create', [{
            'name': 'Test',
            'direction': 'outgoing',
            'sender_id': 'Sender',
            'receiver_id': 'Receiver',
            'state': 'created',
        }])
