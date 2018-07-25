# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from pygments.lexer import _inherit


class Exercicereport(models.Model):
    _name = "entretien.odoo"
    
    #Fonction par defaut pour chercher les ids de  account.invoice.line
    def get_default_invoice_line_ids(self):
        line_ids=[]
        active_id=self.env.context.get('active_ids')
        line_ids += [a.id for a in self.env['account.invoice.line'].search([('invoice_id', '=', active_id[0])])]
        return line_ids
    
    #Fonction pour modifier les comptes analytic dans  account.invoice.line
    @api.multi
    @api.depends('account_analytic_id')
    def update_account_all(self):
        for line in self.invoice_line_ids:
            line.account_analytic_id=self.account_analytic_id.id
        return {
        "type": "ir.actions.do_nothing",
                }
    
    #Fonction pour modifier les tags analytic dans  account.invoice.line
    @api.multi
    @api.depends('analytic_tag_ids')
    def update_tag_all(self):
        tag_ids=[]
        tag_ids += [a.id for a in self.tag_analytic_ids]
        for line in self.invoice_line_ids:
            if tag_ids:
                line.analytic_tag_ids=tag_ids
            else:
                line.analytic_tag_ids=False
        return {
        "type": "ir.actions.do_nothing",
                }
        
   

            
    account_analytic_id = fields.Many2one('account.analytic.account',"Analytic account")
    tag_analytic_ids = fields.Many2many('account.analytic.tag',string="Analytic tags")
    invoice_line_ids = fields.Many2many('account.invoice.line', string='Invoice Lines',default=get_default_invoice_line_ids)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
     
    #Fonction pour modifier les comptes analytic dans  account.move.line
    def update_analytic_move_line(self,invoice_id,invoice_line):
        account_move_line = self.env['account.move.line'].search([('move_id', '=',invoice_id.move_id.id),('product_id', '=',invoice_line.product_id.id),('analytic_account_id', '=',invoice_line.account_analytic_id.id)])
        account_move_line.write({'analytic_account_id':self.account_analytic_id.id})
    
    #Fonction pour modifier les comptes analytic dans  account.analytic.line
    def update_account_analytic_line(self,invoice_line):
        analytic_line = self.env['account.analytic.line'].search([('account_id', '=',invoice_line.account_analytic_id.id),('product_id', '=',invoice_line.product_id.id),('unit_amount', '=',invoice_line.quantity),('amount', '=',invoice_line.price_subtotal)])
        analytic_line.write({'account_id':self.account_analytic_id.id})
    
    #Fonction onchange pour modifier les comptes analytic dans  account.invoice.line
    #et fais appel a deux autre fonctions (update_analytic_move_line,update_account_analytic_line)
    @api.onchange('account_analytic_id') 
    def account_analytic_id_change(self):
        invoice_line=self.env['account.invoice.line'].browse(self._origin.id)
        if invoice_line:
            self.update_analytic_move_line(invoice_line.invoice_id,invoice_line)
            self.update_account_analytic_line(invoice_line)
            invoice_line.write({'account_analytic_id':self.account_analytic_id.id})
    
    #Fonction onchange pour modifier les tags analytic dans  account.move.line
    def update_analytic_tags_move_line(self,invoice_id,invoice_line,tag_ids):
        account_move_line = self.env['account.move.line'].search([('move_id', '=',invoice_id.move_id.id),('product_id', '=',invoice_line.product_id.id),('analytic_account_id', '=',invoice_line.account_analytic_id.id)])
        account_move_line.write({'analytic_tag_ids':[(6, 0, tag_ids)]})
    
    #Fonction onchange pour modifier les tags analytic dans  account.invoice.line
    #et fais appel a une seul fonction (update_analytic_tags_move_line)      
    @api.onchange('analytic_tag_ids') 
    def analytic_tag_ids_change(self):
        tag_ids=[]
        tag_ids += [a.id for a in self.analytic_tag_ids]
        invoice_line=self.env['account.invoice.line'].browse(self._origin.id)
        if invoice_line:
            self.update_analytic_tags_move_line(invoice_line.invoice_id,invoice_line,tag_ids)
            invoice_line.write({'analytic_tag_ids':[(6, 0, tag_ids)]})
        
    
    