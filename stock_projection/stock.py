# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

import openerp.addons.decimal_precision as dp
from osv import osv, fields
from tools.translate import _


class stock_move(osv.osv):

    def _get_prod_loc_qoh(self, cr, uid, ids, product, location, context=None):
        res = 0
        
        results = []
        results2 = []

        states = ('done',)
        what = ('in','out',)
        where = [(location,), (location,), (product,), tuple(states)]

        if 'in' in what:
            cr.execute(
                'select sum(product_qty), product_id, product_uom '\
                'from stock_move '\
                'where location_id NOT IN %s '\
                'and location_dest_id IN %s '\
                'and product_id IN %s '\
                'and state IN %s '\
                'group by product_id, product_uom',tuple(where))
            results = cr.dictfetchone()
            if results:
                res = results['sum']
        if 'out' in what:
            cr.execute(
                'select sum(product_qty), product_id, product_uom '\
                'from stock_move '\
                'where location_id IN %s '\
                'and location_dest_id NOT IN %s '\
                'and product_id IN %s '\
                'and state IN %s '\
                'group by product_id, product_uom',tuple(where))
            results2 = cr.dictfetchone()
            if results2:
                res -= results2['sum']
          
        return res


    def _projected_qty(self, cr, uid, ids, field_names, args, context=None):
        res = {}

#        if context.get('active_model') == 'stock.projection':
        location = context.get('location_id')        
        if location == None:
            raise osv.except_osv(_('Error!'),_("Please run a query through the menu item again."))

        red_true = []
        red_false = []

        first_line = True
        begin_qty = 0
        
        for move in self.browse(cr, uid, ids, context=context):
            res[move.id] = {
                'begin_qty': 0.0,
                'move_qty': 0.0,
                'projected_qty': 0.0,
            }

            if first_line == True:
                product = move.product_id.id
                begin_qty = self._get_prod_loc_qoh(cr, uid, ids, product, location, context=context)
                first_line = False               

            if move.location_id.id == location:
                move_qty = move.product_qty * -1
            else:
                move_qty = move.product_qty

            res[move.id]['begin_qty'] = begin_qty
            res[move.id]['move_qty'] = move_qty
            end_qty = begin_qty + move_qty
            res[move.id]['projected_qty'] = end_qty

            if end_qty < 0:
                red_true += [move.id]
            else:
                red_false += [move.id]
            
            begin_qty = end_qty

        self.pool.get('stock.move').write(cr, uid, red_true, {'is_red': True}, context=context)        
        self.pool.get('stock.move').write(cr, uid, red_false, {'is_red': False}, context=context)

        return res


    _inherit = 'stock.move'
    _order = 'date_expected, id'
    _columns = {
        'is_stock_projection': fields.boolean('Is Stock Projection'),
        'qty_available': fields.related('product_id', 'qty_available', type="float", relation="product.product", string="Total QOH"),
        'begin_qty': fields.function(_projected_qty, type='float', digits_compute=dp.get_precision('Product Unit of Measure'), string='Begin Qty', multi="move"),
        'move_qty': fields.function(_projected_qty, type='float', digits_compute=dp.get_precision('Product Unit of Measure'), string='Move Qty', multi="move"),
        'projected_qty': fields.function(_projected_qty, type='float', digits_compute=dp.get_precision('Product Unit of Measure'), string='Projected Qty', multi="move"),
        'is_red': fields.boolean('Is Red')
    }
    _defaults = {
    }
stock_move()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
