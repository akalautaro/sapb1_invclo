# SAP-B1 InvClo

GUI que conecta a la base de datos SAP Hana y cierra (paga saldo vencido) de las facturas que estén en estado 'abierto' en SAP B1 con el monto máximo que le indiquemos, mediante el consumo de la API Service Layer. Todo esto lo va guardando en un log para chequear en caso de que la factura no se pague o haya algún error.
Esta versión es para usuario final y tiene ciertos parámetros hardcodeados, como por ejemplo el importe máximo vencido (es alto para traer todas las facturas abiertas de X día) y quita la posibilidad de elegir qué facturas pagar.

Ya estoy trabajando en la próxima versión, la cual permite:
* Ingresar rango de fechas
* Importe máximo de saldo vencido
* Tipo de cliente (Consumidor final, responsable inscripto)
* Elegir qué facturas pagar
* Logging mejorado
* Exportar un resumen a PDF

![](Animation.gif)

## Comenzando 🚀

_Las siguientes instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas.

### Pre-requisitos 📋

_Para que este script funcione vas a necesitar de:

* [SAP Business One](https://www.sap.com/latinamerica/products/business-one.html) - Es de donde saldrán los informes con los que se generará el archivo
* [HanaDB Client](https://www.sap.com/latinamerica/products/hana.html) - Cliente/tecnología de la base de datos.
#### Recomendado
* [Gestor de base de datos](http://squirrel-sql.sourceforge.net/) - En mi caso utilicé SquirrelSQL

### Instalación 🔧

_Las mayores complicaciones pueden surgir a la hora de instalar las librerías, ya que las demás cosas necesarias poseen interfaces gráficas para realizar cada instalación.
Si sos un usuario que ya tiene experiencia con la programación e instalación de librerías, podés avanzar con el resto del readme._

* Librerías de Python

```
pip install hdbcli
pip install requests
pip install mechanize
```

## Construido con 🛠️

_Lo utilizado para construir esta pequeña interfaz_

* [Python 3.9](https://www.python.org/)

## Contribuyendo 🖇️

_Si querés contribuir con este proyecto, no dudes en hacer una ```pull request```. Todas las ideas y sugerencias son bienvenidas!_

---
💻 En Twitter soy [akalautaro](www.twitter.com/akalautaro)
