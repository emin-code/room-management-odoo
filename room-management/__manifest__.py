# -*- coding: utf-8 -*-
{
    'name': "Rooms",

    'summary': """
        Conversation rooms management """,

    'description': """
        Allows to create and manage rooms for different needs, usually conversations
    """,

    'author': "Emin Nazarov",
    'website': "vk.com/em_naz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '0.1',
    'license': 'GNU GPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/reservation.xml',
        'views/room.xml',
        'data/cron_rooms_event.xml',
        'data/cron_reservation_event.xml',
        'wizard/create_reservation.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}