# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime
from decimal import Decimal
from itertools import izip, chain
from sql.aggregate import Sum

from trytond.model import Workflow, ModelSQL, ModelView, fields, Unique
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, If, Bool
from trytond.transaction import Transaction
from trytond.tools import grouped_slice, reduce_ids
from trytond import backend

__all__ = ['Project', 'ShipmentWork']

class ShipmentWork:
    __name__ = 'shipment.work'
    __metaclass__ = PoolMeta

    project = fields.Many2One('project.work', 'Project',
        domain=[
            ('party', '=', Eval('party')),
            ],
        states={
            'readonly': Eval('state').in_(['checked', 'cancel']),
            },
        depends=['state', 'party'])

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        table = TableHandler(cls, module_name)

        # migration from v3.4
        if table.column_exist('project'):
            table.column_rename('project', 'work_project')

        super(ShipmentWork, cls).__register__(module_name)

class Project:
    'Work Project'
    __name__ = 'work.project'
    __metaclass__ = PoolMeta

    shipments = fields.One2Many('shipment.work', 'project', 'Shipment Works')


    @classmethod
    def _get_cost(cls, works):
        pass


    #TODO: modify function to add cost, and invoiced amount.

