# -*- coding: utf-8 -*-
{
    'name': "openacademy",

    'summary': """
        我的第一个模块""",

    'description': """
        我的第一个模块，用于学习自定义模块。
    """,

    'author': "KayeJing",
    'website': "http://www.linkloving.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    # 本模块的依赖关系，这里主要是指本模块对于Odoo框架内其他的模块的依赖。如果本模块实在没什么依赖，就把 base 模块填上去。
    'depends': ['base'],

    # always loaded

    # 本模块要加载的数据文件，别看是数据文件，似乎不怎么重要，其实Odoo里面视图，动作，工作流，
    # 模型具体对象等等几乎大部分内容都是通过数据文件定义的
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/openacademy.xml',  # 添加一个openacademy
        'views/partner.xml'  # 添加一个partner
    ],

    # only loaded in demonstration mode
    # 这里定义的数据文件正常情况下不会加载，只有在demonstration模式下才会加载，具体就是你新建某个数据库是勾选上了加载演示数据那个选项
    'demo': [
        'demo.xml',
    ],

    # installabel
    # 默认True，可设为False禁用该模块
    # auto_install
    # 默认False，如果设为True，则根据其依赖模块，如果依赖模块都安装了，那么这个模块将自动安装，这种模块通常作为胶合(glue)模块。
    # application
    # 默认False，如果设为True，则这个模块成为一个应用了。你的主要模块建议设置为True，这样进入Odoo后点击本地模块，然后默认的搜索过滤就是 应用 ，这样你的主模块会显示出来
}
