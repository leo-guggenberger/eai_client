# eai_client_scheduler.py
# -*- coding: utf-8 -*-

from openerp import models
import xmlrpclib

# EAI Client Scheduler
class eai_client_scheduler(models.Model):

    _name = 'eai_client.scheduler'
    _description = 'EAI Client Scheduler'

    def run_scheduler(self, cr, uid, context=None):
        # Step 1: Produkte ausspielen
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        product_ids = self.pool['product.template'].search(cr,uid, ['|',('company_id','=',company_id),('active','=','true'),('sale_ok','=','true')], context=context)
        message_name = 'TEST Produktmessage'
        document_name = 'Product External IDs'
        document_type = 'external_id'
        document_text = get_external_id( cr , uid , product_ids , *args , **kwargs ) 
        eai_server_messageid = self._message_create(cr, uid, context=context, message_name, document_name, document_text)
    
    def _message_create(self, cr, uid, context=None, message_name, document_name, document_text):
        # Configuration einlesen
        eai_client_name = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_client_name
        eai_server_url = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_server_url
        eai_server_db = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_server_db
        eai_server_user = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_server_user
        eai_server_password = self.pool.get('eai_client.config.settings').browse(cr, uid, uid, context=context).eai_server_password
        
        # Message am EAI-Server erzeugen
        eai_server_models = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(eai_server_url))
        eai_server_uid = eai_server_models.authenticate(eai_server_db, eai_server_user, eai_server_password, {})
        eai_server_models.execute_kw(eai_server_db, eai_server_uid, eai_server_password,'eai_server.messages', 'check_access_rights', ['create'], {'raise_exception': False})
        eai_server_messageid = eai_server_models.execute_kw(eai_server_db, eai_server_uid, eai_server_password, 'eai_server.messages', 'create', [{
            'name': message_name,
            'direction': 'outgoing',
            'sender_id': eai_client_name,
            'receiver_id': 'Receiver',
            'state': 'created'
        }])
        eai_server_documentid = eai_server_models.execute_kw(eai_server_db, eai_server_uid, eai_server_password, 'eai_server.documents', 'create', [{
            'message_id': eai_server_messageid
            'name': document_name,
            'type': document_type,
            'document_text': document_text'
        }])
        return eai_server_messageid
    
