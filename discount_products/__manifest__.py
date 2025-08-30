{
    'name':'Discounted Products',
    'summary':'Add discouts to products and filter discounted products',
    'version':'18.0',
    'author':'Nadim',
    'catagory':'Website',
    'depends':['base','website'],
    'data':[
        'views/product_views.xml',
        'views/website_menu_views.xml',
        'views/website_sale_inherit_template.xml',
    ],
    'installable':True,
    'application':False,
}