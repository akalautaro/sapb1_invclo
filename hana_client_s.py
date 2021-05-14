from hdbcli import dbapi


class HanaClient:
    """Conexión y consultas a base de datos SAP Hana"""

    conn = dbapi.Connection
    user = 'user'
    passwd = 'password'
    schema = 'schema'
    host = 'host'
    port = port

    def __init__(self, user, passwd, schema):

        self.user = user
        self.passwd = passwd
        self.schema = schema
        self.conn = dbapi.connect(address=self.host, port=self.port, user=self.user, password=self.passwd)

        sql = f'set schema {self.schema}'
        cursor = self.conn.cursor()
        cursor.execute(sql)

    @staticmethod
    def list_to_dict(cursor: dbapi.Connection.cursor):
        dict_rows = [dict(zip(list(zip(*cursor.description))[0], row)) for row in cursor.fetchall()]
        return dict_rows

    def busca_facturas_abiertas(self, fecha_desde, diferencia=10000000.00):

        sql = (f"""
                select "DocEntry", "DocNum", "CardCode", "CardName", "DocTotal", "PaidToDate", 
                TO_VARCHAR (TO_DATE("DocDate"), 'yyyy-mm-dd') as "DocDate",
                cast(("DocTotal" - "PaidToDate")as float(2)) as "Diferencia"
                from {self.schema}.oinv where "PTICode" = 0016 
                and "DocDate" = '{fecha_desde}' and "DocStatus" = 'O' 
                and (cast(("DocTotal" - "PaidToDate")as float(2)) < {diferencia})
                """)

        cur = self.conn.cursor()
        cur.execute(sql)
        fact_abiertas = self.list_to_dict(cur)
        return fact_abiertas

    def busca_factura_abierta(self, doc_entry):

        sql = (f"""
                select "DocEntry", "DocNum", "CardCode", "CardName", "DocTotal", "PaidToDate", 
                cast(("DocTotal" - "PaidToDate")as float(2)) as "Diferencia"
                from {self.schema}.oinv where "PTICode" = 0016 and "DocEntry" = {doc_entry}
                """)

        cur = self.conn.cursor()
        cur.execute(sql)
        fact_abierta = self.list_to_dict(cur)
        return fact_abierta
