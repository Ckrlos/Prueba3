
import os
import datetime
import json


Pizzas = [ 
    ["Margarita", {'pequeña': 5500, 'mediana': 8500, 'familiar': 11000 }],
    ["Mexicana", {'pequeña': 7000, 'mediana': 10000, 'familiar': 13000 }],
    ["Barbacoa", {'pequeña': 6500, 'mediana': 9500, 'familiar': 12500 }],   
    ["Vegetariana", {'pequeña': 5000, 'mediana': 8000, 'familiar': 10500 }]   
]

descuentos = { 
    'Estudiante diurno' : 0.15,
    'Estudiante vespertino' : 0.18,
    'Administrativo' : 0.11,
}

ventasCollection = []
ventasId = 1

directory = os.getcwd()
dbpath = os.path.join(directory, 'Pizzas.json')


def verificarEnteros(opciones=None):
    while True:
        try:
            num = int(input(": "))
            if num > 0 and (opciones is None or num in opciones):
                return num
            else:
                print("Por favor ingrese una opción válida.")
        except ValueError:
            print("Por favor ingrese un número entero.")


def menu():
        os.system('cls')
        print(f"==== PIZZERIA DUOC ==== \n" 
            "1. Venta \n"
            "2. Mostrar todas las ventas \n"
            "3. Buscar ventas por clientes \n"
            "4. Guardar las ventas en un archivo \n"
            "5. Cargar las ventas desde un archivo \n"
            "6. Generar Boleta \n"
            "7. Anular venta. \n"
            "8. Salir")
        return verificarEnteros([1,2,3,4,5,6,7,8])
    
def tamaños():{
      print("Ingrese el tamaño que desea comprar: \n"
              "1. Pequeña \n"
              "2. Mediana \n"
              "3. Familiar")
}
def opt1(): 
        global ventasId, ventasCollection
        os.system('cls')
        cliente = input("Ingrese el nombre del cliente:\n: ")
        os.system('cls')

        print("Ingrese el tipo de pizza que desea comprar:\n")
        for idx, producto in enumerate(Pizzas, start=1):
            print(f" {idx}. {producto[0]}")
        eleccion = verificarEnteros(range(1, len(Pizzas) + 1))
        producto = Pizzas[eleccion - 1]
        os.system('cls')
        tamaños()
        eleccion = verificarEnteros([1,2,3])
        tamaño = list(producto[1].items())[eleccion-1]
        os.system('cls')

        print("Ingrese unidades que desea comprar:")
        cantidad = verificarEnteros()
        os.system('cls')

        print("Ingrese el descuento que desea aplicar:\n")
        for idx, (nombre, valor) in enumerate(descuentos.items(), start=1):
            print(f" {idx}. {nombre} / {valor * 100}%")
        eleccion = verificarEnteros(range(1, len(descuentos) + 1))
        dcto = list(descuentos.items())[eleccion - 1]
        subtotal = tamaño[1] * cantidad
        dcto_monto = round(subtotal * dcto[1])
        total = subtotal - dcto_monto
        ventaData = {   
        'id' : ventasId,
        'fecha' : datetime.datetime.now().strftime("%d/%m/%Y - %H:%M"),
        'cliente' : cliente,
        'producto' : producto[0],
        'tamaño' : tamaño,
        'cantidad' : cantidad,
        'dcto_data' : dcto,
        'dcto_monto': dcto_monto,
        'subtotal' : subtotal,
        'total' : total,
        }       

        ventasCollection.append({'detalle': ventaData})
        ventasId += 1



def mostrarVentas(filter=None):
    ventas = [venta for venta in ventasCollection if filter is None or venta['detalle']['cliente'] == filter]
    if not ventas:
        print("No hay ventas registradas.")
    else:
        for venta in ventas:
            print("=====================================")
            for key, value in venta['detalle'].items():
                print(f"{key}: {value}")
            print("\n")

def opt2():
    mostrarVentas()


def obtenerClientes():
    return list({venta['detalle']['cliente'] for venta in ventasCollection})


def opt3(): 
    clients = obtenerClientes()
    if not clients:
        print("No hay ventas registradas.")
        input()
    else:
        while True:
            print("Clientes registrados: \n")
            for name in clients:
                print(name)
            client = input("\nIngrese el nombre del cliente que desea buscar:\n: ")
            if client in clients:
                os.system('cls')
                print(f"=====================================\nVentas de {client}:\n")
                mostrarVentas(client)
                input()
                break
            else:
                print("Cliente no encontrado.")
                input()
                os.system('cls')

  
def opt4():
    if not ventasCollection:
        print("No hay ventas registradas.")
    else:
        with open(dbpath, 'w') as f:
            json.dump(ventasCollection, f)
        print(f"{len(ventasCollection)} ventas guardadas en con éxito en {dbpath}")
  

def cargarVentas():
    try:
        with open(dbpath, 'r') as f:
            ventas = json.load(f)
            print(f"{ventas[-1]['detalle']['id']} ventas cargadas con éxito desde {dbpath}." )
            return ventas, ventas[-1]['detalle']['id'] + 1 if ventas else 1
    except FileNotFoundError:
        print(f"No se ha encontrado archivo .json que contenga las ventas.")
        return [], 1
    
def opt5(): 
    global ventasCollection, ventasId
    ventasCollection, ventasId = cargarVentas()


def generarBoleta(detalleVenta):
    formatted_now = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    boleta = (f"==== BOLETA DE VENTA ====\n"
              f"ID: {detalleVenta['id']}\n"
              f"Cliente: {detalleVenta['cliente']}\n"
              f"{detalleVenta['cantidad']} Pizza {detalleVenta['producto']} {detalleVenta['tamaño'][0]} \n"
              f"--------------------------------\n"
              f"SUBTOTAL: {detalleVenta['subtotal']}\n"
              f"DESCUENTO: -{detalleVenta['dcto_monto']}\n"
              f"TOTAL: {detalleVenta['total']}\n"
              f"--------------------------------\n"
              f"Gracias por su compra! \t\t {formatted_now}")
    return boleta

def opt6(): 
    if not ventasCollection:
        print("No hay ventas registradas.")
    else:
        mostrarVentas()
        print("\n Ingrese el ID de la venta que desea generar la boleta: ")
        ventaId= verificarEnteros(range(1, ventasCollection[-1]['detalle']['id']+1))
        detalleVenta = ventasCollection[ventaId-1]['detalle']
        os.system('cls')
        print(generarBoleta(detalleVenta))

def opt7():
    global ventasCollection, ventasId
    ventasCollection = []
    ventasId = 1
    print("Ventas anuladas con éxito.")


while True:
    choice = menu()
    if choice == 1: #Ingresar venta
        opt1() #Ingresa venta y guarda en diccionario
        os.system('cls')
        print("Venta registrada con éxito.")
        input()
    elif choice == 2: #Muestra las ventas
        os.system('cls')
        opt2() 
        input()
    elif choice == 3:#Buscar ventas por cliente
        os.system('cls')
        opt3()
    elif choice == 4: #Guarda las ventas
        os.system('cls')
        opt4()
        input()
    elif choice == 5: #Carga las ventas
        os.system('cls')
        opt5()
        input()
    elif choice == 6: #Imprime las boletas
        os.system('cls')
        opt6()
        input()
    elif choice == 7:
        os.system('cls')
        opt7()
        input()
    elif choice == 8:
        break