# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Project', 'ShipmentWork']


class ShipmentWork:
    __name__ = 'shipment.work'
    __metaclass__ = PoolMeta

    @classmethod
    def _get_origin(cls):
        return super(ShipmentWork, cls)._get_origin() + ['project.work']

    @classmethod
    def __setup__(cls):
        super(ShipmentWork, cls).__setup__()

        if hasattr(cls, 'asset'):
            cls.origin.domain = [('asset', '=', Eval('asset'))]



class Project:
    'Work Project'
    __name__ = 'project.work'
    __metaclass__ = PoolMeta
    project_party = fields.Function(fields.Many2One('party.party',
            'Project Party'),
        'on_change_with_project_party')
    shipments = fields.One2Many('shipment.work', 'origin', 'Shipment Works',
        domain=[
            ('party', '=', Eval('project_party', -1)),
            ], depends=['project_party'])

    @fields.depends('type', 'party', 'parent')
    def on_change_with_project_party(self, name=None):
        if self.type == 'project':
            return self.party.id if self.party else None
        elif self.parent:
            return self.parent.on_change_with_project_party(name=name)

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
