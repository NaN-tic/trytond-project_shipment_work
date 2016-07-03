# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, If, Bool
from trytond import backend

__all__ = ['Project', 'ShipmentWork']


class ShipmentWork:
    __name__ = 'shipment.work'
    __metaclass__ = PoolMeta

    #TODO: Change for origin
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

    @classmethod
    def __setup__(cls):
        super(ShipmentWork, cls).__setup__()
        if hasattr(cls, 'asset'):
            if 'asset' not in cls.project.depends:
                cls.project.domain.append(If(Bool(Eval('asset')),
                    ('asset', '=', Eval('asset')), ()))
                cls.project.depends.append('asset')


class Project:
    'Work Project'
    __name__ = 'project.work'
    __metaclass__ = PoolMeta

    shipments = fields.One2Many('shipment.work', 'project', 'Shipment Works')

    @classmethod
    def _get_cost(cls, works):
        costs = super(Project, cls)._get_cost(works)
        for work in works:
            for shipment in work.shipments:
                if shipment.state != 'done':
                    continue
                costs[work.id] += shipment.cost
        return costs

    @classmethod
    def _get_revenue(cls, works):
        revenues = super(Project, cls)._get_revenue(works)
        for work in works:
            for shipment in work.shipments:
                if shipment.state != 'done':
                    continue
                revenues[work.id] += shipment.revenue
        return revenues