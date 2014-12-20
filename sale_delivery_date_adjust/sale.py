# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) Rooms For (Hong Kong) Limited T/A OSCG
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta


class sale_order(osv.osv):
    _inherit = 'sale.order'

    def _get_date_planned(self, cr, uid, order, line, start_date, context=None):
        categ_lt = 0
        #categ_id = order.partner_id.category_id[0].id
        #categ = self.pool.get('res.partner.category').browse(cr, uid, categ_id)
        categ_obj = self.pool.get('res.partner.category')
        categ_ids = categ_obj.search(cr, uid, [])
        for categ in categ_obj.browse(cr, uid, categ_ids):
            if not categ.cutoff:
                categ_lt = categ.days_added
            else:
                date_order = datetime.strptime(order.date_order, '%Y-%m-%d')
                if date_order.weekday() <= categ.cutoff_day:
                    categ_lt = categ.cutoff_day - date_order.weekday() + categ.days_added
                else:
                    categ_lt = categ.cutoff_day - date_order.weekday() + 7 + categ.days_added
        return datetime.strftime(date_order + relativedelta(days=categ_lt), '%Y-%m-%d')

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
