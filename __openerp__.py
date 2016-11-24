{
# The human-readable name of your module, displayed in the interface
        'name' : "Human_resource_cost" ,
# A more extensive description
        'description' : """
        """ ,
# Which modules must be installed for this one to work
        'depends' : ['base'],
        'category': 'human_resource cost',
# data files which are always installed
        'data': [
                'views/resource_cost_view.xml',
                'views/resource_cost_menu.xml',
                'views/resource_cost_cron.xml',
                "security/resource_security.xml",
                "security/ir.model.access.csv",
                ],
# data files which are only installed in "demonstration mode"
        'demo': [
                'demo.xml',
        ],

}
