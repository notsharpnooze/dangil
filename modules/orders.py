import os
import uuid
import datetime
import csv
import subprocess

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(r"""
   ____    ______   ______     _____     __      _  _____   _____  
  / __ \  (   __ \ (_  __ \   / ___/    /  \    / )/ ___/  / ____\ 
 / /  \ \  ) (__) )  ) ) \ \ ( (__     / /\ \  / /( (__   ( (___   
( ()  () )(    __/  ( (   ) ) ) __)    ) ) ) ) ) ) ) __)   \___ \  
( ()  () ) ) \ \  _  ) )  ) )( (      ( ( ( ( ( ( ( (          ) ) 
 \ \__/ / ( ( \ \_))/ /__/ /  \ \___  / /  \ \/ /  \ \___  ___/ /  
  \____/   )_) \__/(______/    \____\(_/    \__/    \____\/____/   
                                                                   
          """)
    
def show_menu():
    print("1. Agregar orden")
    print("2. Ver órdenes")
    print("3. Actualizar orden")
    print("4. Eliminar orden")
    print("5. Volver al menú principal")

def get_choice():
    while True:
        try:
            choice = int(input("Seleccione una opción: "))
            if choice in [1, 2, 3, 4, 5]:
                return choice
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor ingrese un número.")


#DATA
# GENERATE UNIQUE ORDER ID
customer_id = str(uuid.uuid4())[:5]

def sort_entries(data):
    sort_options = {
        "1": ("Nombre (A-Z)", lambda x: x[1].lower()),
        "2": ("Cantidad (Menor a Mayor)", lambda x: int(x[2])),
        "3": ("Precio (Menor a Mayor)", lambda x: int(x[3])),
        "4": ("Por orden de entrada", None)
}

    while True:
        clear()
        print("\nComo quieres ver los resultados?")
        for key, (desc, _) in sort_options.items():
            print(f"{key}. {desc}")

        option = input("Elige una opcion (1-4): ").strip()
        if option in sort_options:
            sort_key = sort_options[option][1]
            if sort_key:
                data = sorted(data, key=sort_key)
            break
        else:
            print("Opcion no valida.")
    return data
#OPTIONS

def write_csv_header_if_needed(writer, file_exists):
    header = ['id', 'customer', 'order_date', 'description']
    if not file_exists or os.path.getsize("database/orders/orders.csv") == 0:
        writer.writerow(header)

def add_order():
    clear()

    id = customer_id
    customer = input("Ingrese el nombre del cliente: ")
    order_date = datetime.date.today().strftime("%d/%m/%Y")
    description = input("Ingrese una descripcion sencilla de la orden: ")

    #Adds entry to orders.csv
    os.makedirs("database/orders", exist_ok=True)
    file_exists = os.path.exists("database/orders/orders.csv")
    with open("database/orders/orders.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        write_csv_header_if_needed(writer, file_exists)
        writer.writerow([id, customer, order_date, description])
    print(f"Orden agregada con éxito. ID de la orden: {id}")

    #Creates csv with order data
    os.makedirs("database/orders/ind_orders", exist_ok=True)
    filename = f"{id}_order.csv"
    filepath = os.path.join("database/orders/ind_orders", filename)

    #Adds data to individual order csv
    with open(filepath, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["nombre", "cantidad", "precio"])

         # Load inventory data
        with open("database/inventory.csv", "r") as inv_file:
            inv_rows = list(csv.reader(inv_file))
        if len(inv_rows) <= 1:
            print("\nNo hay productos en el inventario.\n")
        else:
            inv_header = inv_rows[0]
            inv_data = inv_rows[1:]
            while True:
                clear()
                print("\nProductos disponibles para agregar a la orden:\n")
                print(f"{inv_header[1]:<15} {inv_header[2]:<8} {inv_header[3]:<8}")
                print("-" * 50)
                for i, row in enumerate(inv_data, start=1):
                    print(f"{i:<5} {row[1]:<15} {row[2]:<8} {row[3]:<8}")
                print()

                choice = input("Presiona 'x' para organizar, elige producto (número), o 'c' para cancelar: ").strip().lower()
                if choice == "c":
                    break
                elif choice == "x":
                    inv_data = sort_entries(inv_data)
                    continue
                try:
                    index = int(choice) - 1
                    if index < 0 or index >= len(inv_data):
                        print("Número de producto no válido.")
                        input("Presiona Enter para continuar...")
                        continue
                    selected = inv_data[index]
                except ValueError:
                    print("Entrada no válida. Por favor ingrese un número.")
                    input("Presiona Enter para continuar...")
                    continue

                cantidad = input(f"Ingrese la cantidad para '{selected[1]}' (disponible: {selected[2]}): ").strip()
                if not cantidad.isdigit() or int(cantidad) <= 0:
                    print("Cantidad no válida.")
                    input("Presiona Enter para continuar...")
                    continue

                writer.writerow([selected[1], cantidad, selected[3]])
                print(f"Producto '{selected[1]}' agregado a la orden.")
                otro = input("¿Desea agregar otro producto? (s/n): ").strip().lower()
                if otro != "s":
                    break

    #Update inventory
    with open(filepath, "r") as order_file:
        order_reader = csv.reader(order_file)
        next(order_reader)  # Skip header
        ordered_products = list(order_reader)

    # Load inventory again to update quantities
    with open("database/inventory.csv", "r") as inv_file:
        inv_rows = list(csv.reader(inv_file))
    inv_header = inv_rows[0]
    inv_data = inv_rows[1:]

    for order_row in ordered_products:
            if not order_row or len(order_row) < 2:
                continue  # Skip empty or incomplete rows
            nombre = order_row[0]
            cantidad = int(order_row[1])
            for inv_row in inv_data:
                if inv_row[1] == nombre:
                    inv_row[2] = str(max(0, int(inv_row[2]) - cantidad))

    with open("database/inventory.csv", "w", newline='') as inv_file:
        writer = csv.writer(inv_file)
        writer.writerow(inv_header)
        writer.writerows(inv_data)    


    #Creates txt with order details
    os.makedirs("database/orders/ind_desc", exist_ok=True)
    filename = f"{id}_order.txt"
    filepath = os.path.join("database/orders/ind_desc", filename)

    #TXT template and details
    with open(filepath, "w") as f:
        f.write("\n =========== Detalles de la orden: ==============\n")
        detalles = input("\nIngrese los detalles de la orden: \n")
        f.write(detalles + "\n")

    print(f"\nOrden creada, la puedes visualizar en Ver ordenes/{filename}\n")
    input("Presiona cualquier tecla para continuar...")
    main()

#END OF THE ENTRY LOOP
def end_of_data_entry():
    while True:
        add_order()
        response = input("Tienes otra orden? (s/n): ").strip().lower()
        while response not in {"s", "n"}:
            print("Escribe (s) o (n): ")
            response = input("Tienes otra orden? (s/n): ").strip().lower()
        if response == "n":
            print("Regresando al menu...")
            main()
            break

def view_orders():
    # Load orders
    orders_path = "database/orders/orders.csv"
    if not os.path.exists(orders_path):
        print("\nNo hay ordenes registradas.\n")
        return

    with open(orders_path, "r") as file:
        rows = list(csv.reader(file))
    if len(rows) <= 1:
        print("\nNo hay ordenes registradas.\n")
        return

    header = rows[0]
    data = rows[1:]

    # Show orders list
    clear()
    print("\nOrdenes registradas:\n")
    print(f"{'N°':<5} {'ID':<8} {'Cliente':<15} {'Fecha':<12} {'Descripcion':<20}")
    print("-" * 60)
    for i, row in enumerate(data, start=1):
        print(f"{i:<5} {row[0]:<8} {row[1]:<15} {row[2]:<12} {row[3]:<20}")

    select = input('\nSeleccione la orden a ver (número) o "c" para cancelar: ').strip()
    if select.lower() == "c":
        return

    try:
        index = int(select) - 1
        if index < 0 or index >= len(data):
            print("Número de orden no válido.")
            return
        order_id = data[index][0]
    except ValueError:
        print("Entrada no válida.")
        return

    #Header for order details
    #Here add the client name and order date

    
    # Show CSV order details
    order_csv_path = f"database/orders/ind_orders/{order_id}_order.csv"
    print("\n========= Productos en la orden ============")
    if os.path.exists(order_csv_path):
        with open(order_csv_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            if rows:
                header = rows[0]
                data = rows[1:]
                print(f"{header[0]:<15} {header[1]:<10} {header[2]:<8}")
                print("-" * 40)
            for row in data:
                if not row or len(row) < 3:
                    continue  # Skip empty or incomplete rows
                print(f"{row[0]:<15} {row[1]:<10} {row[2]:<8}")
    else:
        print("No se encontró el archivo de productos para esta orden.")

    # Show TXT order details
    order_txt_path = f"database/orders/ind_desc/{order_id}_order.txt"
    if os.path.exists(order_txt_path):
        with open(order_txt_path, "r") as f:
            for line in f:
                print(line.strip())
    else:
        print("No se encontró el archivo de detalles para esta orden.")

    input("\nPresiona Enter para continuar...")
    main()

def main():
    clear()
    show_banner()
    while True:
        show_menu()
        choice = get_choice()
        
        if choice == 1:
            add_order()
            break

        elif choice == 2:
            view_orders()
            break 

        elif choice == 3:
            update_order()
            break

        elif choice == 4:
            delete_order()
            break

        elif choice == 5:
            subprocess.run(["python","main.py"])
            break

main()
