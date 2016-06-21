# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .work import *

def register():
    Pool.register(
        Project,
        ShipmentWork,
        module='project_shipment_work', type_='model')
