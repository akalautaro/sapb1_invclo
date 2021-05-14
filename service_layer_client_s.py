import logging
import requests
import json
from datetime import datetime
from hana_client import HanaClient
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

hana = HanaClient('user', 'password', 'schema')
logging.basicConfig(filename='./log/logs_invclo.log',  level=logging.DEBUG)

facturas_pagas = []
importe_total = []


class ServiceLayer:
    """
    Conectarse y consumir la Service Layer de SAP B1
    """

    BASE_URL = 'url_base'
    username = 'user'
    password = 'password'
    companydb = 'schema'
    sesion = requests.Session()
    nextLink: str = None
    ObjectTypesUrlMapping = {13: '/Invoices'}

    def __init__(self, username, password, companydb):

        self.username = username
        self.password = password
        self.companydb = companydb

    def login(self):

        body = '{ "CompanyDB": "' + self.companydb + '", "UserName": "' + self.username + '", "Password": "' + \
               self.password + '" }'

        # No verificar certificados.
        self.sesion.verify = False

        url = self.BASE_URL + "/Login"
        req = requests.Request('POST', url, data=body)
        prepped = req.prepare()
        prepped.body = body

        # Enviar el requerimiento
        resp = self.sesion.send(prepped)

        # Verificar la respuesta
        if resp.status_code >= 400:
            print("Error de conexión")
            logging.error("Error de conexión")
        else:
            logging.debug("Conexión a ServiceLayer exitosa")

    def logout(self) -> bool:

        url = self.BASE_URL + "/Logout"
        req = self.sesion.post(url, cookies=self.sesion.cookies, verify=False)
        if req.status_code == 204:
            return True
        else:
            return False

    def post_incoming_payment(self, doc_entry, cardname, cardcode, importe_pago, doc_num):

        current_date = datetime.today().strftime('%Y-%m-%d')

        json_incpay = {
                        "DocType": "rCustomer",
                        "CardCode": f"{cardcode}",
                        "CashAccount": "cashaccount",
                        "CashSum": f"{importe_pago}",
                        "BPLID": bplid,  # bplid = int
                        "Reference1": f"{doc_num}",
                        "PaymentInvoices": [
                            {
                                "DocEntry": f"{doc_entry}",
                                "SumApplied": f"{importe_pago}"
                            }
                        ]
                    }
        url = self.BASE_URL + f"/IncomingPayments"
        self.login()
        req = self.sesion.post(url, data=json.dumps(json_incpay), cookies=self.sesion.cookies, verify=False)
        self.logout()
        if req.status_code >= 400:
            print(f"Cobro con error al insertar {req.json()}, \nitem: {json_incpay}")
        else:
            f = req.json()
            print(f"Cobro insertado DocNum: {['DocNum']} | {['CardName']}")
            return f
        return {}

    def post_incoming_payment_red(self, doc_entry):
        """Misma función que post_incoming_payment, pero hace nuevamente la consulta hana.busca_factura_abierta.
        Esto se soluciona en la próxima versión, trabajando con los checkbuttons como diccionarios y no como strings."""

        factura_abierta = hana.busca_factura_abierta(doc_entry)

        for f in factura_abierta:

            cardcode = f.get('CardCode')
            current_date = datetime.today().strftime('%Y-%m-%d')
            doc_num = f.get('DocNum')
            doc_entry = f.get('DocEntry')
            importe_pago = round(f.get('Diferencia'), 2)

            json_incpay = {
                        "DocType": "rCustomer",
                        "CardCode": f"{cardcode}",
                        "CashAccount": "cashaccount",
                        "CashSum": f"{importe_pago}",
                        "BPLID": bplid,  # bplid = int
                        "Reference1": f"{doc_num}",
                        "PaymentInvoices": [
                            {
                                "DocEntry": f"{doc_entry}",
                                "SumApplied": f"{importe_pago}"
                            }
                        ]
                    }
            url = self.BASE_URL + f"/IncomingPayments"
            self.login()
            req = self.sesion.post(url, data=json.dumps(json_incpay), cookies=self.sesion.cookies, verify=False)
            self.logout()
            if req.status_code >= 400:
                print(f"Cobro con error al insertar {req.json()}, \nitem: {json_incpay}")
                logging.error(f"Cobro con error al insertar {req.json()}, \nitem: {json_incpay}")
            else:
                f = req.json()
                print(f"Cobro insertado DocNum: {doc_num} | {f['CardName']}")
                logging.info(f"Cobro insertado DocNum: {doc_num} | {f['CardName']}")
                facturas_pagas.append(f)
                importe_total.append(f"{importe_pago}")
                return f
            logging.info(f"Cantidad de facturas cerradas {len(facturas_pagas)}")
            return {}
