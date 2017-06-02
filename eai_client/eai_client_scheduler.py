# eai_client_scheduler.py
# -*- coding: utf-8 -*-

from openerp import models
from fnmatch import fnmatch,fnmatchcase
from lxml import etree
import xmlrpclib

# EAI Client Scheduler
class eai_client_scheduler(models.Model):

    _name = 'eai_client.scheduler'
    _description = 'EAI Client Scheduler'

    def run_scheduler(self, cr, uid, context=None):
        # Step 1: Produkte ausspielen
        #product_ids = self.pool['product.template'].search(cr,uid, ['|',('company_id','=',company_id),('active','=','true'),('sale_ok','=','true')], context=context)
        message_name = 'TEST Produktmessage'
        document_name = 'TEST Produktdokument'
        document_text = 'TEST Dokumentinhalt'
        eai_server_messageid = self._message_create(cr, uid, context=context, message_name, document_name, document_text)
    
    def _message_create(self, cr, uid, context=None, message_name, document_name, document_text):
        # Configuration einlesen
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
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
            'sender_id': 'Sender',
            'receiver_id': 'Receiver',
            'state': 'created'
        }])
        eai_server_documentid = eai_server_models.execute_kw(eai_server_db, eai_server_uid, eai_server_password, 'eai_server.documents', 'create', [{
            'message_id': eai_server_messageid
            'name': document_name,
            'document_text': document_text'
        }])
        return eai_server_messageid
    
    def _export_xml(lines):
        document = etree.Element('openerp')
        data = etree.SubElement(document,'data')

        for line in lines:
            if line.id:
                k,id = line.get_external_id().items()[0] if line.get_external_id() else 0,"%s-%s" % (line._name,line.id)
                _logger.info("Reporting Block id = %s" % id)          
                record = etree.SubElement(data,'record',id=id,model=line._name)
                names = [name for name in line.fields_get().keys() if fnmatch(name,'in_group*')] + [name for name in line.fields_get().keys() if fnmatch(name,'sel_groups*')]
                for field,values in line.fields_get().items():
                    if not field in ['create_date','nessage_ids','id','write_date','create_uid','__last_update','write_uid',] + names:
                        if values.get('type') in ['boolean','char','text','float','integer','selection','date','datetime']:
                            _logger.info("Simple field %s field %s values %s" % (values.get('type'),field,values))
                            try:
                                etree.SubElement(record,'field',name = field).text = "%s" % eval('line.%s' % field)
                            except:
                                pass
                        elif values.get('type') in ['many2one']:
                            if eval('line.%s' % field):                                     
                                k,id = eval('line.%s.get_external_id().items()[0]' % field) if eval('line.%s.get_external_id()' % field) else (0,"%s-%s" % (eval('line.%s._name' % field),eval('line.%s.id' % field)))
                                if id == "":
                                    id = "%s-%s" % (eval('line.%s._name' % field),eval('line.%s.id' % field))
                                etree.SubElement(record,'field',name=field,ref="%s" % id)
                        elif values.get('type') in ['one2many']: 
                            pass
                        elif values.get('type') in ['many2many']:
                            m2mvalues = []
                            for val in line:
                                id,external_id = 0,'' if not val.get_external_id() else val.get_external_id().items()[0]
                                _logger.info("External id %s -> %s" % (id,external_id[1]))
                                if len(external_id)>0:
                                    m2mvalues.append("(4, ref('%s'))" % external_id[1])
                            if len(m2mvalues)>0:
                                etree.SubElement(record,'field',name=field,eval="[%s]" % (','.join(m2mvalues)))
        return document
