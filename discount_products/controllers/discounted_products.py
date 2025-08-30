from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

_logger = logging.getLogger(__name__)

class DiscountedProductsController(WebsiteSale):

    @http.route(['/shop/discounted'], type='http', auth='public', website=True)
    def shop_discounted(self, **kwargs):
        products = http.request.env['product.template'].sudo().search([
            ('discount', '>', 0), ('website_published', '=', True)
        ])
        _logger.info("DISCOUNTED PRODUCTS FOUND: %s", products.mapped('name'))

        return http.request.render('discount_products.products_discounted', {
            'products': products,
        })

