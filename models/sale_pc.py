from flectra import models, fields, api, _
from flectra.exceptions import ValidationError
from datetime import datetime


class salecp(models.Model):
    _name = 'sale.change.price'
    

    product_cat = fields.Many2one('product.category', string = 'Product Category')
    percentage_type = fields.Selection([
        ('a', 'Increase'),
        ('b','Decrease'),
    ], string = 'Price Increase/Decrease')
    percentage = fields.Float('Percentage %')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approve','Approved'),
    ], string = 'State',default = 'draft')
    date = fields.Date('Date',default=datetime.today())



    def approve(self):
        self.state = 'approve'
        percentageR = 0.0
        if self.percentage_type == 'a':
            percentageR = self.percentage
        elif self.percentage_type =='b':
            percentageR = self.percentage * -1
        else:
            raise ValidationError("Please Enter Price Increase/Decrease")
        
        products = self.env['product.template'].search([('categ_id', '=', self.product_cat.id)])
        for p in products:
            p.lst_price = p.lst_price* (1+percentageR/100)
