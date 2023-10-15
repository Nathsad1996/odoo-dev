from odoo import models, fields
import requests


class Transactions(models.Model):
    _name = 'transactions'
    _description = 'mobile money transactions tables'

    reference = fields.Char('Reference', required=True)
    amount = fields.Float('Montant', required=True)
    currency = fields.Selection([('usd', 'USD'), ('cdf', 'CDF')], string='Devise', default='cdf', required=True)
    customer_number = fields.Char('Numéro Client', required=True)
    method = fields.Selection([('debit', 'Debit'), ('credit', 'Credit')], string='Opération', default='debit',
                              required=True)
    operator = fields.Selection([('airtel', 'Airtel'), ('vodacom', 'Vodacom'), ('orange', 'Orange')],
                                string='Opérateur', default='vodacom',
                                required=True)
    status = fields.Char(string='Status', required=False, default='PENDING', readonly=True, invisible=True)

    def make_transaction(self):
        requestBody = {
            "merchantID": "bad9c0d8-bd1c-4095-a166-84872d811d46",
            "phoneNumber": f"+243{self.customer_number[1:]}",
            "key": "ops",
            "amount": self.amount,
            "currency": f"{self.currency}".upper(),
            "service": f"{self.operator}",
            "reference": f"{self.reference}",
            "action": f"{self.method}".upper(),
            "callback_url": "http://161.35.161.32:3500/"
        }

        url = "http://161.35.161.32:3000/api/verification"

        response = requests.post(url, json=requestBody)

        print(requestBody, response.json())

        return True
