# eai_client_scheduler.py
# -*- coding: utf-8 -*-

from openerp import models
import gc

# Garbage Collector to release unreferenced memory
class garbage_collector(models.Model):

    _name = 'garbage.collector'
    _description = 'Garbage Collector'

    def run_collector(self, cr, uid, context=None):
gc.collect()
