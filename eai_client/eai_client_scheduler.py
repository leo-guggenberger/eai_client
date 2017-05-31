# eai_client_scheduler.py
# -*- coding: utf-8 -*-

from openerp import models

# EAI Client Scheduler
class eai_client_scheduler(models.Model):

    _name = 'eai_client.scheduler'
    _description = 'EAI Client Scheduler'

    def run_scheduler(self, cr, uid, context=None):
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        
        # Step 1: Produkte ausspielen
        product_ids = self.pool['product.template'].search(cr,uid, ['|',('company_id','=',company_id),('active','=','true'),('sale_ok','=','true')], context=context)
