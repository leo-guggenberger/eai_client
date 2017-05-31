# eai_client_scheduler.py
# -*- coding: utf-8 -*-

from openerp import models

# EAI Client Scheduler
class eai_client_scheduler(models.Model):

    _name = 'eai_client.scheduler'
    _description = 'EAI Client Scheduler'

    def run_scheduler(self, cr, uid, context=None):

