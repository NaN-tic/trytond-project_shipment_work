# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Project', 'ShipmentWork']


class ShipmentWork:
    __name__ = 'shipment.work'
    __metaclass__ = PoolMeta

    @classmethod
    def _get_origin(cls):
        return super(ShipmentWork, cls)._get_origin() + ['project.work']


class Project:
    'Work Project'
    __name__ = 'project.work'
    __metaclass__ = PoolMeta

    shipments = fields.One2Many('shipment.work', 'origin', 'Shipment Works')

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
