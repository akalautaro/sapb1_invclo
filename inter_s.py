import tkinter as tk
from tkinter import ttk, DISABLED, Checkbutton
from tkinter import messagebox as mb
from datetime import datetime
import logging
from typing import List

from hana_client_s import HanaClient
from service_layer_client_s import ServiceLayer, facturas_pagas, importe_total

hana = HanaClient('user', 'password', 'schema')
sl = ServiceLayer(username="user", password="password", companydb='schema')
logging.basicConfig(filename='./log/logs_invclo.log',  level=logging.DEBUG)


class ProgramaMain:

    checkbuttons: List[Checkbutton]
    vars: List[vars]

    def __init__(self):

        self.factura1 = hana
        self.ventana1 = tk.Tk()
        self.ventana1.title('SWEET S.A.')
        self.ventana1.resizable(1, 1)
        self.ventana1.resizable(0, 0)
        self.ventana1.geometry('415x590')
        self.cuaderno1 = ttk.Notebook(self.ventana1)
        self.consulta()
        self.listado_completo()
        self.cuaderno1.grid(column=0, row=0, padx=10, pady=10)
        self.ventana1.mainloop()

    def consulta(self):

        self.ventana1.bind('<Return>', self.consulta_facturas)
        self.pagina1 = ttk.Frame(self.cuaderno1)
        self.cuaderno1.add(self.pagina1, text='Busca facturas abiertas')
        self.labelframe1 = ttk.LabelFrame(self.pagina1, height=125, width=385, text='Parámetros')
        self.labelframe1.grid_propagate(False)
        self.labelframe1.grid(column=0, row=0, padx=5, pady=10, sticky="NSW")

        # self.fecha = str(datetime.today().strftime('%Y-%m-%d'))  # se puede hardcodear a la fecha del día
        self.label1 = ttk.Label(self.labelframe1, text=f'{self.fecha}')
        self.label1.grid(column=0, row=1, padx=4, pady=4)
        self.fecha = tk.StringVar()
        self.fecha.set(str(datetime.today().strftime('%Y-%m-%d')))
        self.entry_fecha = ttk.Entry(self.labelframe1, textvariable=self.fecha)
        self.entry_fecha.grid(column=1, row=1, padx=4, pady=4)

        self.boton1 = ttk.Button(self.labelframe1, text='Buscar facturas', command=self.consulta_facturas)
        self.boton1.grid(column=1, row=1, padx=4, pady=4)
        self.boton2 = tk.Button(self.labelframe1, text="Cerrar facturas", command=self.cerrar_facturas)
        self.boton2.grid(column=1, row=2, padx=4, pady=4)
        self.boton1.focus_set()

    def consulta_facturas(self):

        text = tk.Text(self.labelframe2, cursor="arrow", height=50, width=385)
        vsb = tk.Scrollbar(self.labelframe2, command=text.yview)
        text.configure(yscrollcommand=vsb.set)
        text.grid(column=0, row=0, padx=5, pady=10, sticky="NSW")

        fecha_desde = self.fecha

        busca_facturas_abiertas = hana.busca_facturas_abiertas(fecha_desde)

        self.checkbuttons = []
        self.vars = []

        logging.info(f'Busca facturas para fecha {self.fecha}')
        for i in busca_facturas_abiertas:
            cardname = i.get('CardName')
            doc_num = i.get('DocNum')
            doc_entry = i.get('DocEntry')
            importe_pago = round(i.get('Diferencia'), 2)

            var = tk.IntVar(value=1)
            cb = tk.Checkbutton(self.labelframe2,
                                text=f'Fact: {doc_num} | {cardname}\n${importe_pago:<10}\t({doc_entry})',
                                variable=var, onvalue=1, offvalue=0, state=DISABLED)

            text.window_create("end", window=cb)
            text.insert("end", "\n")
            self.checkbuttons.append(cb)
            self.vars.append(var)

        self.boton1.focus_set()

    def listado_completo(self):

        self.labelframe2 = ttk.LabelFrame(self.pagina1, height=380, width=385, text="Listado completo")
        self.labelframe2.grid(column=0, row=1, padx=5, pady=5, sticky="NSW")
        self.labelframe2.grid_propagate(False)

    def cerrar_facturas(self):

        for cb, var in zip(self.checkbuttons, self.vars):
            value = var.get()
            if value:
                text = cb.cget("text")[-6:]
                doc_ent = int(text[0:-1])
                print(doc_ent)
                sl.post_incoming_payment_red(doc_ent)

        cant_facturas = len(facturas_pagas)
        importe_pagado = round(sum(map(float, importe_total)), 2)

        mb.showinfo(message=f'Cantidad de facturas cerradas: {cant_facturas}\nImporte pago: ${importe_pagado}',
                    title='Resumen')
        logging.info(f'Fin facturas cerradas')
        self.consulta_facturas()


if __name__ == "__main__":
    ProgramaMain()
