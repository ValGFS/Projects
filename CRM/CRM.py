# Archivo JSON para lista de clientes
import json

# Archivo CSV para lista de clientes
import csv

# Asignación de fecha de registro
from datetime import datetime

#Lista para ir añadiendo los clientes con su respecto diccionario
clients = []

# Lista global para facturas
invoices = []

# Funcion para añadir clientes
def add_client():
    user_id = f"USR{len(clients) + 1:03}"
    print("\n=== Registro de nuevo usuario ===")
    first_name = input("Nombre: ")
    if not first_name:
        print("Ingresa nombre")
    last_name = input("Apellido: ")
    if not last_name:
        print("Ingresa apellido")
    email = input("Email: ")
    if not email:
        print("Ingresa email")
    # Validación de email correcto con @ y "."
    if "@" not in email or "." not in email.split("@")[-1]:
        print("Email inválido. Debe tener formato usuario@dominio.com")
        return
    # Validación de email duplicado
    for client in clients:
        if client["email"].lower() == email.lower():
            print("Ya existe un cliente registrado con ese email")
            return

    phone = input("Teléfono (opcional): ")

    # Validación de digitos al ingresar el telefono
    if phone and not phone.isdigit():
        print("El teléfono debe contener solo números.")
        return
    company = input("Empresa (opcional): ")
    address = input("Dirección (opcional): ")
    notes = input("Notas (opcional: \n")
    registration_date = datetime.now().strftime("%d/%m/%Y")

    client = {
        "id": user_id,
        "nombre": first_name,
        "apellido": last_name,
        "email": email,
        "telefono": phone,
        "empresa": company if company else "No especificado",
        "direccion": address if address else "No especificado",
        "notas": notes,
        "fecha de registro": registration_date
    }
    clients.append(client)
    print("Cliente registrado correctamente!.")
    print(f"ID asignado: {user_id}")
    print(f"Fecha de registro: {registration_date}")
    if len(clients) >= 100:
        print("Límite máximo de clientes alcanzado.")
        return
    save_clients_to_file()


# Función para enlistar todos los clientes
def list_clients():
    if not clients:
        print("No hay clientes registrados.")
    else:
        print("\n=== Lista de usuarios ===")
        for i, client in enumerate(clients, start=1):
            print(f"Usuario #{i}:")
            print(f"ID: {client.get('nombre', '')} {client.get('apellido', '')}")
            print(f"Email: {client.get('email', '')}")
            print(f"Telefono: {client.get('telefono', 'No Especificado')}")
            print(f"Empresa: {client.get('empresa', 'No Especificado')}")
            print(f"Direccion: {client.get('direccion', '')}")
            print(f"Fecha de registro: {client.get('fecha de registro', '')}")

        print(f"Total de usuarios registrados: {len(clients)}\n")

# Función para crear factura
def create_invoice():
    print("=== Crear Factura ===")
    user_email = input("Ingresa email del usuario: ").strip().lower()
    user = None
    for client in clients:
        if client["email"].lower() == user_email:
            user = client
            break
    if not user:
        print("Cliente no encontrado")
        return
    full_name = f"{client.get('nombre', '')} {client.get('apellido', '')}"
    print(f"\nUsuario encontrado: {full_name}\n")
    description = input("Ingrese descripción del servicio/producto: ").strip()
    if not description:
        print("La decripción no puede estar vacia")
        return
    try:
        amount = float(input("Ingresa el monto total: "))
        if amount <= 0:
            print("El monto debe ser mayor a 0")
            return
    except ValueError:
        print("Monto invalido. Ingrese un numero.")
        return

    print("Seleccione el estado de la factura.")
    print("1. Pendiente")
    print("2. Pagado")
    print("3. Cancelado")
    status_option = input("Ingrese el estado de la factura: ")
    states = {"1": "Pendiente", "2": "Pagado", "3": "Cancelado"}
    status = states.get(status_option)
    if not status:
        print("Estado inválido")
        return

    invoice_number = f"FAC{len(invoices) + 1:03}"
    emission_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    invoice = {
        "numero": invoice_number,
        "email_usuario": user_email,
        "fecha_emision": emission_date,
        "descripcion": description,
        "monto": amount,
        "estado": status
    }
    invoices.append(invoice)
    print("\nFactura creada exitosamente!.")
    print(f"Numero de factura: {invoice_number}")
    print(f"Fecha de emision: {emission_date}")
    print(f"Cliente: {client['nombre']} {client['apellido']}")
    print(f"Descripcion: {description}")
    print(f"Monto: {amount}")
    print(f"Estado: {status}")
    if len(invoices) >= 500:
        print("Límite máximo de facturas alcanzada.")
        return
    save_invoices_to_file()

# Función para mostrar resumen financiero
def show_financial_summary():
    if not invoices:
        print("No hay facturas registradas")
        return
    print("\n === Resumen Financiero ===\n")
    total_invoices = 0
    total_amount = 0
    total_paid = 0
    total_pending = 0
    total_cancelled = 0
    for client in clients:
        email = client.get("email", "")
        full_name = f"{client.get('nombre', '')} {client.get('apellido', '')}"
        client_invoices = [inv for inv in invoices if inv["email_usuario"].lower() == email.lower()]
        amount_total = sum(inv["monto"] for inv in client_invoices)
        amount_paid = sum(inv["monto"] for inv in client_invoices if inv["estado"] == "Pagado")
        amount_pending =  sum(inv["monto"] for inv in client_invoices if inv["estado"] == "Pendiente")

        print("\n=== Resumen Financiero ===\n")
        print(f"Usuario: {full_name} ({email})")
        print(f"- Total facturas: {len(client_invoices):,}")
        print(f"- Monto total: {amount_total:.2f} €")
        print(f"- Facturas pagadas: {amount_paid:.2f} €")
        print(f"- Facturas pendientes: {amount_pending:.2f} €\n")

        total_invoices+= len(client_invoices)
        total_amount += amount_total
        total_paid += amount_paid
        total_pending += amount_pending
        total_cancelled = sum(inv["monto"] for inv in client_invoices if inv["estado"] == "Cancelado")

    print("--- Resumen Financiero General ---")
    print(f"Total de usuarios: {len(clients)}")
    print(f"Total de facturas registradas: {total_invoices}")
    print(f"Monto total acumulado: {total_amount:.2f} €")
    print(f"Facturas pagadas: {total_paid:.2f} €")
    print(f"Facturas pendientes: {total_pending:.2f} €")
    print(f"Facturas canceladas: {total_cancelled:.2f} €\n")

# Función para buscar un cliente por su ID
def search_client():
    print("\n=== Buscar Usuario ===")
    print("1. Buscar por email.")
    print("2. Buscar por nombre.")
    search_option = input("\n Seleccione metodo de Busqueda: ")

    if search_option == "1":
        email_csearch = input("Ingresa el email:\n").strip().lower()
        client = next((client for client in clients if client["email"].lower() == email_csearch), None)

    elif search_option == "2":
        name_csearch = input("Ingresa el nombre:\n").strip().lower()
        client = next((client for client in clients if client["nombre"].lower() == name_csearch), None)

    else:
        print("Opcion invalida")

    if client:
        full_name = f"{client.get('nombre', '')} {client.get('apellido', '')}"
        print("---Usuario Encontrado ---")
        print(f"ID: {client.get('id','')}")
        print(f"Nombre: {full_name}")
        print(f"Email: {client.get('email', '')}")
        print(f"Telefono: {client.get('telefono', 'No Especificado')}")
        print(f"Empresa: {client.get('empresa', 'No Especificado')}")
        print(f"Direccion: {client.get('direccion', 'No Especificado')}")
        print(f"Fecha de registro: {client.get('fecha de registro', 'No Disponible')}")
        print(f"Notas: {client.get('notas', '')}\n")
    else:
        print("Cliente no encontrado.")

# Función para editar clientes
def edit_client():
    id_edit = input("Ingrese el ID del cliente a modificar: ")
    for client in clients:
        if client["id"] == id_edit:
            print("ID:", client["id"], "- Nombre:", client["nombre"])
            new_first_name = input(f"Nuevo nombre (actual: {client['nombre']}): ") or client['nombre']
            new_last_name = input(f"Nuevo apellido (actual: {client['apellido']}): ") or client['apellido']
            new_email = input(f"Nuevo email (actual: {client['email']}): ") or client['email']
            new_phone = input(f"Nuevo telefono (actual: {client['telefono']}): ") or client['telefono']
            new_company = input(f"Nueva empresa (actual: {client['empresa']}): ") or client['empresa']
            new_notes = input(f"Nuevas notas (actual: {client['notas']}): ") or client['notas']

            client["nombre"] = new_first_name
            client["apellido"] = new_last_name
            client["email"] = new_email
            client["telefono"] = new_phone
            client["empresa"] = new_company
            client["notas"] = new_notes

            print("Cliente modificado correctamente.")
            save_clients_to_file()
            return
    print("Cliente no encontrado.")

# Función para eliminar cliente
def delete_client():
    id_delete = input("Ingrese el ID del cliente a eliminar: ")
    for client in clients:
        if client["id"] == id_delete:
            confirm = input("Seguro que desea eliminar este cliente? (y/n): ")
            if confirm.lower() == "y":
                clients.remove(client)
                print("Cliente eliminado correctamente.")
                save_clients_to_file()
                return
    print("Cliente no encontrado.")

# Función para guardar clientes en archivo JSON
def save_clients_to_file():
    with open("data.json", "w") as file:
        json.dump(clients, file, indent=4)
    if not clients:
        print("No hay clientes registrados.")
        return

# Función para guardar facturas en JSON
def save_invoices_to_file():
    with open("invoices.json", "w") as file:
        json.dump(invoices, file, indent=4)
    if not invoices:
        print("No hay facturas registradas.")
        return

# Función para cargar clientes a partir del archivo JSON con validación de archivo faltante/corrupto
def load_clients_from_file():
    global clients
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            if isinstance (data, list):
                clients = data
            else:
                print("El archivo no contiene una lista válida. Se usará una lista vacía.")
                clients = []
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("El archivo no existe o esta dañado. Se empezará con una lista vacía.")
        clients = []

# Función para cargar facturas a partir del archivo JSON con validación de archivo faltante/corrupto
def load_invoices_from_file():
    global invoices
    try:
        with open("invoices.json", "r") as file:
            invoice_data = json.load(file)
            if isinstance(invoice_data, list):
                invoices = invoice_data
            else:
                print("El archivo no contiene facturas validas. Se usara una lista vacia")
                invoices = []
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("El archivo no existe o esta dañado. Se empezará con una lista vacía.")
        invoices = []


# Función para exportar lista de clientes a CSV
def export_clients_to_csv():
    with open("clientes_exportados.csv", mode= "w", newline= "") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "nombre", "apellido", "email", "telefono", "empresa", "notas"])
        writer.writeheader()
        writer.writerows(clients)
    print("Lista de clientes exportado correctamente.")

# Función para importar lista de cliente por CSV con validación de archivo faltante/corrupto
def import_clients_from_csv():
    try:
        with open("clientes_importados.csv", mode = "r", newline= "") as file:
            reader = csv.DictReader(file)
            new_clients = []
            existent_ids = {nclient["id"] for nclient in clients}
            for row in reader:
                new_id = (row["id"])
                if new_id in existent_ids:
                    print("El cliente ya existe en la lista actual.")
                    continue
                nclient = {
                    "id": new_id,
                    "nombre": row["nombre"],
                    "apellido": row["apellido"],
                    "email": row["email"],
                    "telefono": row["telefono"],
                    "empresa": row["empresa"],
                    "notas": row["notas"]
                }
                new_clients.append(nclient)
            clients.extend(new_clients)
            save_clients_to_file()
            print(f"Se importaron {len(new_clients)} clientes correctamente.")
            return new_clients
    except FileNotFoundError:
        print("Archivo 'clientes_importados.csv' no encontrado.")
        return []

# Función para buscar por criterio
def search_by_field():
    valid_fields = ["id", "nombre", "apellido", "email", "telefono", "empresa", "notas"]
    field = input("Buscar por campo (Nombre/Apellido/Email/Telefono/Empresa/Notas): ").strip().lower()
    if field not in valid_fields:
        print("El campo no es valido.")
        return

    value = input(f"Ingrese el valor a buscar en ({field}): ").strip().lower()
    matches = []
    for client in clients:
        if value in client[field].lower():
            matches.append(client)
    if matches:
        print(f"\n Se encontraron {len(matches)} clientes(s):\n")
        for match in matches:
            print("-" * 30)
            print(f"ID: {match['id']}")
            print(f"Nombre: {match['nombre']}")
            print(f"Apellido: {match['apellido']}")
            print(f"Email: {match['email']}")
            print(f"Telefono: {match['telefono']}")
            print(f"Empresa: {match['empresa']}")
            print(f"Notas: {match['notas']}\n")
    else:
        print("No se encontraron coincidencias")

# Función para mostrar todas las facturas asociadas a un cliente
def show_client_invoices():
    print("\n=== Facturas por Usuario ===")
    email_search = input("Ingrese el email para buscar facturas: ").strip().lower()
    client_data = next((c for c in clients if c["email"].lower() == email_search), None)
    if not client_data:
        print("No se encontro cliente con ese email.")
        return

    client_invoices = [inv for inv in invoices if inv ["email_usuario"].lower() == email_search]
    if not client_invoices:
        print("Este cliente no tiene facturas registradas.")
    else:
        print(f"\n Se encontraron {len(client_invoices)} factura(s) para {email_search}:\n")
        full_name = f"{client_data.get('nombre', '')} {client_data.get('apellido', '')}"
        print(f"--- Facturas de {full_name}---\n")

        total_camount = 0
        total_cpending = 0

        for i, inv in enumerate(client_invoices, start=1):
            print(f"Factura #{i}:")
            print(f"Número de factura: {inv['numero']}")
            print(f"Fecha de emisión: {inv['fecha_emision']}")
            print(f"Descripcion: {inv['descripcion']}")
            print(f"Monto: {inv['monto']:.2f} €")
            print(f"Estado: {inv['estado']}\n")

            total_camount += inv["monto"]
            if inv["estado"] == "Pendiente":
                total_cpending += inv["monto"]

            print(f"Total de facturas: {len(client_invoices)}")
            print(f"Monto total facturado: {total_camount: .2f} €")
            print(f"Monto total pendiente: {total_cpending: .2f} €\n")




# Menú principal
def main_menu():
    while True:
        print("\n=== CRM ===")
        print("1. Registrar nuevo usuario")
        print("2. Buscar usuario")
        print("3. Crear factura para usuario")
        print("4. Mostrar todos los usuarios")
        print("5. Mostrar facturas de un usuario")
        print("6. Resumen financiero por usuario")
        print("7. Editar cliente")
        print("8. Eliminar cliente")
        print("9. Buscar usuario por cualquier campo")
        print("10. Exportar a CSV")
        print("11. Importar desde CSV")
        print("0. Salir")

        option = input("Seleccione una opción: ")

        if option == "1":
            add_client()
        elif option == "2":
            search_client()
        elif option == "3":
            create_invoice()
        elif option == "4":
            list_clients()
        elif option == "5":
            show_client_invoices()
        elif option == "6":
            show_financial_summary()
        elif option == "7":
            edit_client()
        elif option == "8":
            delete_client()
        elif option == "9":
            search_by_field()
        elif option == "10":
            export_clients_to_csv()
        elif option == "11":
            import_clients_from_csv()
        elif option == "0":
            print("Saliendo del CRM...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

load_clients_from_file()
load_invoices_from_file()
main_menu()