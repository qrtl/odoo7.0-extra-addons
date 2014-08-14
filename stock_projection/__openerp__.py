# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) Rooms For (Hong Kong) Limited T/A OSCG. All Rights Reserved.
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

{
    'name' : 'Stock Projection',
    'version' : '1.0',
    'author': 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website': 'http://www.openerp-asia.net',    
    'summary': 'Adds a menu item "Stock Projection"',
    'description': """
    
Features:
==========

* Adds a menu item "Stock Projection" which opens a wizard for user to select product and location.
* Opens a list view which is based on outstanding stock move records upon confirming the wizard input.
* The list view should show projected QOH as of the timing of future stock moves.
 
   
    """,
    'category': 'Warehouse Management',
    'sequence': 25,
    'website' : 'http://www.openerp-asia.net',
    'images' : [],
    'depends' : ['stock'],
    'demo' : [],
    'data' : [
              'stock_view.xml',
              'wizard/stock_projection_view.xml',
              ],
    'test' : [],
    'auto_install': False,
    'application': True,
    'installable': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
