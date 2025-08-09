import os
import uuid
import datetime
import csv

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
    print("3. Despacho")
    print("4. Salir")

def get_choice():
    while True:
        try:
            choice = int(input("Seleccione una opcion: "))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print("Opcion no válida. Intente de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor ingrese un número.")

#GENERATE UNIQUE ORDER ID
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

def write_csv_header_if_needed(writer, file_exists):
    header = ['id', 'customer', 'order_date', 'description']
    if not file_exists or os.path.getsize("database/orders/orders.csv") == 0:
        writer.writerow(header)

def add_order():
    clear()

    id = str(uuid.uuid4())[:5]
    print("Presiona 'c' en cualquier campo para cancelar y volver al menú")
    customer = input("Ingrese el nombre del cliente: ")
    if customer.lower() == 'c':
        return
    order_date = datetime.date.today().strftime("%d/%m/%Y")
    description = input("Ingrese una descripcion sencilla de la orden: ")
    if description.lower() == 'c':
        return

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

                choice = input("\nElige producto (número) \nPresiona 'x' para organizar, \n'c' para cancelar: ").strip().lower()
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

                amount = input(f"Ingrese la cantidad de '{selected[1]}' (disponible: {selected[2]}) o 'c' para cancelar': ").strip()
                if amount.lower() == 'c':
                    return
                if not amount.isdigit() or int(amount) <= 0:
                    print("Cantidad no válida.")
                    input("Presiona Enter para continuar...")
                    continue

                writer.writerow([selected[1], amount, selected[3]])
                print(f"Producto '{selected[1]}' agregado a la orden.")
                otro = input("¿Desea agregar otro producto? (s/n): "),
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
            amount = int(order_row[1])
            for inv_row in inv_data:
                if inv_row[1] == nombre:
                    inv_row[2] = str(max(0, int(inv_row[2]) - amount))

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
        f.write("\n =========== Detalles de la orden: ============\n")
        detalles = input("\nIngrese los detalles de la orden: \n")
        f.write(detalles + "\n")

    print(f"\nOrden creada, la puedes visualizar en \"Ver ordenes\"\n")
    input("Presiona cualquier tecla para continuar...")
    return

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
            return
            break

def update_order(order_id):

    # Paths
    order_csv_path = f"database/orders/ind_orders/{order_id}_order.csv"
    order_txt_path = f"database/orders/ind_desc/{order_id}_order.txt"   

    # Edit products and quantities
    if os.path.exists(order_csv_path):
        with open(order_csv_path, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
        if rows:
            header = rows[0]
            data = rows[1:]
            valid_rows = [row for row in data if row and len(row) >= 3]
            clear()
            print(f"{'N°':<5} {header[0]:<15} {header[1]:<10} {header[2]:<8}")
            print("-" * 40)
            for i, row in enumerate(valid_rows, start=1):
                print(f"{i:<5} {row[0]:<15} {row[1]:<10} {row[2]:<8}")
                continue

            print("\nOpciones:")
            print("1. Editar producto/cantidad")
            print("2. Eliminar producto")
            print("3. Terminar edicion")
            choice = input("Seleccione una opcion: ").strip()
            if choice == "1":
                while True:
                    # Show inventory for product selection
                    clear()
                    print("\nSeleccione el producto a editar o 'c' para cancelar:")
                    print(f"{'N°':<5} {header[0]:<15} {header[1]:<10} {header[2]:<8}")
                    print("-" * 40)

                    for i, row in enumerate(valid_rows, start=1):
                        print(f"{i:<5} {row[0]:<15} {row[1]:<10} {row[2]:<8}")
                    prod_num = input("Número de producto a editar: ").strip()
                    if prod_num.lower() == 'c':
                        return
                    try:
                        idx = int(prod_num) - 1
                        if idx < 0 or idx >= len(valid_rows):
                            print("Número inválido.")
                            input("Presiona Enter para continuar...")
                            continue
                        selected_row = valid_rows[idx]
                        data_idx = data.index(selected_row)
                    except ValueError:
                        print("Entrada inválida.")
                        input("Presiona Enter para continuar...")
                        continue

                    # Show inventory for product selection
                    with open("database/inventory.csv", "r") as inv_file:
                        inv_rows = list(csv.reader(inv_file))
                    inv_header = inv_rows[0]
                    inv_data = inv_rows[1:]
                    print("\nProductos en inventario:")
                    print(f"{inv_header[1]:<15} {inv_header[2]:<8} {inv_header[3]:<8}")
                    print("-" * 40)
                    for i, row in enumerate(inv_data, start=1):
                        if not row or len(row) < 4:
                            continue
                        print(f"{i:<5} {row[1]:<15} {row[2]:<8} {row[3]:<8}")
                    prod_select = input("Elige el producto por número o deja vacío para mantener el actual: \no presiona 'c' para cancelar: ").strip()
                    if prod_select.lower() == 'c':
                        return
                    if prod_select:
                        inv_idx = int(prod_select) - 1
                        if inv_idx < 0 or inv_idx >= len(inv_data):
                            print("Número de producto no válido.\n")
                            input("Presiona Enter para continuar...")
                            continue
                        name = inv_data[inv_idx][1]
                    else:
                        name = data[data_idx][0]

                    # Calculate inventory adjustment
                    old_quantity = int(data[data_idx][1])
                    quantity = input(f"Nueva cantidad [{data[data_idx][1]}]: ").strip() or data[data_idx][1]
                    new_quantity = int(quantity)
                    difference = new_quantity - old_quantity
                    price = input(f"Nuevo precio [{data[data_idx][2]}]: ").strip() or data[data_idx][2]
                    data[data_idx] = [name, quantity, price]

                    other = input("¿Desea editar otro producto? (s/n): ").strip().lower()
                    if other != "s":
                        # Update inventory
                        for inv_row in inv_data:
                            if inv_row[1] == name:
                                inv_row[2] = str(max(0, int(inv_row[2]) - difference))

                            # Save inventory changes
                        with open("database/inventory.csv", "w", newline='') as inv_file:
                            writer = csv.writer(inv_file)
                            writer.writerow(inv_header)
                            writer.writerows(inv_data)
                        break

            elif choice == "2":
                while True:
                    print("\nSeleccione el producto a eliminar:")
                    print(f"{'N°':<5} {header[0]:<15} {header[1]:<10} {header[2]:<8}")
                    print("-" * 40)
                    for i, row in enumerate(valid_rows, start=1):
                        print(f"{i:<5} {row[0]:<15} {row[1]:<10} {row[2]:<8}")
                    prod_num = input("Número de producto a eliminar o 'c' para cancelar: ").strip()
                    if prod_num.lower() == 'c':
                        return
                    try:
                        idx = int(prod_num) - 1
                        if idx < 0 or idx >= len(valid_rows):
                            print("Número inválido.\n")
                            input("Presiona Enter para continuar...")
                            continue
                        selected_row = valid_rows[idx]
                        data_idx = data.index(selected_row)
                        data.pop(data_idx)
                        break
                    except ValueError:
                        print("Entrada inválida.\n")
                        input("Presiona Enter para continuar...")
                        continue
            elif choice == "3":
                return
        # Save changes
        with open(order_csv_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)
        print("Productos actualizados.")

    # Edit description/details
    if os.path.exists(order_txt_path):
        with open(order_txt_path, "r") as f:
            lines = f.readlines()
        print("\nDescripcion actual:")
        for line in lines:
            print(line.strip())
        nueva_desc = input("\nNueva descripcion (deja vacío para no cambiar) o 'c' para cancelar:\n").strip()
        if nueva_desc.lower() == 'c':
            return
        if nueva_desc:
            with open(order_txt_path, "w") as f:
                f.write(nueva_desc + "\n")
            print("Descripcion actualizada.")
        else:
            print("Descripcion no modificada.")
    else:
        print("No se encontró el archivo de descripcion.")

    input("\nEdicion terminada. Presiona Enter para continuar...")
    return

def delete_order(order_id):
    
    # Confirm deletion
    confirm = input("¿Estás seguro que deseas eliminar esta orden? (s/n): ").strip().lower()
    if confirm != "s":
        print("Eliminación cancelada.\n")
        input("Presiona Enter para continuar...")
        return

    # Paths
    order_csv_path = f"database/orders/ind_orders/{order_id}_order.csv"
    order_txt_path = f"database/orders/ind_desc/{order_id}_order.txt"
    orders_path = "database/orders/orders.csv"
    inventory_path = "database/inventory.csv"

    # Return products to inventory (only if there are product rows)
    if os.path.exists(order_csv_path) and os.path.getsize(order_csv_path) > 0:
        with open(order_csv_path, "r", newline='') as f:
            rows = [r for r in csv.reader(f) if r]
        if rows:  # rows[0] is header for items
            item_header = rows[0]
            item_data = rows[1:]
            # Load inventory
            if os.path.exists(inventory_path):
                with open(inventory_path, "r", newline='') as inv_file:
                    inv_rows = [r for r in csv.reader(inv_file) if r]
                if inv_rows:
                    inv_header = inv_rows[0]
                    inv_data = inv_rows[1:]
                    for row in item_data:
                        if len(row) < 2:
                            continue
                        nombre = row[0]
                        try:
                            cantidad = int(row[1])
                        except ValueError:
                            continue
                        for inv_row in inv_data:
                            if inv_row[1] == nombre:
                                try:
                                    inv_row[2] = str(int(inv_row[2]) + cantidad)
                                except ValueError:
                                    pass
                    with open(inventory_path, "w", newline='') as inv_file:
                        w = csv.writer(inv_file)
                        w.writerow(inv_header)
                        w.writerows(inv_data)

    # Delete individual order files
    if os.path.exists(order_csv_path):
        os.remove(order_csv_path)
    if os.path.exists(order_txt_path):
        os.remove(order_txt_path)

    # Remove order entry from orders.csv (single safe pass)
    if os.path.exists(orders_path):
        with open(orders_path, "r", newline='') as f:
            rows = [r for r in csv.reader(f) if r]
        if rows:
            orders_header = rows[0]
            # Ensure header looks correct; recreate if malformed
            if orders_header and orders_header[0] != 'id':
                orders_header = ['id', 'customer', 'order_date', 'description']
                orders_data = []
            else:
                orders_data = [r for r in rows[1:] if r and r[0] != order_id]
            with open(orders_path, "w", newline='') as f:
                w = csv.writer(f)
                w.writerow(orders_header)
                w.writerows(orders_data)
        else:
            # Recreate with header if totally empty
            with open(orders_path, "w", newline='') as f:
                w = csv.writer(f)
                w.writerow(['id', 'customer', 'order_date', 'description'])

    print("Orden eliminada y productos devueltos (si correspondía) al inventario.\n")
    input("Presiona Enter para continuar...")
    return

def view_orders():
    # Load orders
    orders_path = "database/orders/orders.csv"
    if not os.path.exists(orders_path):
        print("\nNo hay ordenes registradas.\n")
        input("Presiona Enter para continuar...")
        return

    with open(orders_path, "r") as file:
        rows = [r for r in csv.reader(file) if r]
    if not rows or len(rows) == 1:
        clear()
        print("\nNo hay ordenes registradas.\n")
        input("Presiona Enter para continuar...")
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
        customer = data[index][1]
        order_date = data[index][2]
        description = data[index][3]
        clear()
    except ValueError:
        print("Entrada no válida.")
        return

    # Print order header details
    
    print("\n========= Detalles del cliente =========")
    print(f"Cliente: {customer}")
    print(f"Fecha: {order_date}")
    print(f"Descripcion: {description}")
    print("=" * 40)

    # Show TXT order details
    order_txt_path = f"database/orders/ind_desc/{order_id}_order.txt"
    if os.path.exists(order_txt_path):
        with open(order_txt_path, "r") as f:
            for line in f:
                print(line.strip())
    else:
        print("No se encontró el archivo de detalles para esta orden.")

    # Show CSV order details
    order_csv_path = f"database/orders/ind_orders/{order_id}_order.csv"
    print("\n======== Productos en la orden =========")
    total = 0.0  # <-- Agrega esta línea
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
                    try:
                        cantidad = float(row[1])
                        precio = float(str(row[2]).replace(',', '.'))
                        subtotal = cantidad * precio
                        total += subtotal
                    except (ValueError, IndexError):
                        continue
                print("-" * 40)
                print(f"{'TOTAL':<25}{total:<8.2f}")  # <-- Muestra el total
    else:
        print("No se encontró el archivo de productos para esta orden.")

    #Total goes here
    #Other Options
    
    print("\nOpciones:")
    print("a. Editar orden")
    print("d. Eliminar orden")
    print("c. Exportar como PDF")

    print("\nb. Volver al menú \n")

    choice = input("Seleccione una opcion: ").strip()
    if choice == "a":
        update_order(order_id)  # To do
        return
    elif choice == "d":
        delete_order(order_id)  # To do
        return
    #elif choice == "c":
     #   export_order_pdf(order_id, customer, order_date, description, order_csv_path, order_txt_path)
      #  print("Orden exportada como PDF.")
       # input("Presiona Enter para continuar...")
        #return
    elif choice == "b":
        return

def sell():
    clear()
    orders_path = "database/orders/orders.csv"
    sold_path = "database/orders/sold.csv"

    if not os.path.exists(orders_path):
        print("No hay órdenes registradas.\n")
        input("Presiona Enter para continuar...")
        return
    
        # List orders
    with open(orders_path, "r") as f:
        rows = list(csv.reader(f))
    if len(rows) <= 1:
        print("No hay órdenes registradas.\n")
        input("Presiona Enter para continuar...")
        return

    header = rows[0]
    data = rows[1:]

    print("\nÓrdenes registradas:")
    print(f"{'N°':<5} {'ID':<8} {'Cliente':<15} {'Fecha':<12} {'Descripcion':<20}")
    print("-" * 60)
    for i, row in enumerate(data, start=1):
        print(f"{i:<5} {row[0]:<8} {row[1]:<15} {row[2]:<12} {row[3]:<20}")

    select = input('\nSeleccione la orden (número) o "c" para cancelar: ').strip()
    if select.lower() == "c":
        return
    try:
        idx = int(select) - 1
        if idx < 0 or idx >= len(data):
            print("Número de orden no válido.\n")
            input("Presiona Enter para continuar...")
            return
        order = data[idx]
        order_id = order[0]

        # Show order details before selling/cancelling
        customer = order[1]
        order_date = order[2]
        description = order[3]
        clear()
        print("\n========= Detalles del cliente =========")
        print(f"Cliente: {customer}")
        print(f"Fecha: {order_date}")
        print(f"Descripcion: {description}")
        print("=" * 40)

        # Show TXT order details
        order_txt_path = f"database/orders/ind_desc/{order_id}_order.txt"
        if os.path.exists(order_txt_path):
            with open(order_txt_path, "r") as f:
                for line in f:
                    print(line.strip())
        else:
            print("No se encontró el archivo de detalles para esta orden.")

        # Show CSV order details
        order_csv_path = f"database/orders/ind_orders/{order_id}_order.csv"
        print("\n======== Productos en la orden =========")
        if os.path.exists(order_csv_path):
            with open(order_csv_path, "r") as f:
                reader = csv.reader(f)
                rows = list(reader)
                if rows:
                    header = rows[0]
                    data_products = rows[1:]
                    print(f"{header[0]:<15} {header[1]:<10} {header[2]:<8}")
                    print("-" * 40)
                    for row in data_products:
                        if not row or len(row) < 3:
                            continue
                        print(f"{row[0]:<15} {row[1]:<10} {row[2]:<8}")
        else:
            print("No se encontró el archivo de productos para esta orden.")

    except ValueError:
        print("Entrada no válida.")
        return
    
    choice = input("¿La orden fue vendida (v) o cancelada (c)? ").strip().lower()
    if choice == "v":
        selling_price = input("Ingrese el precio de venta total: ").strip()

        # Save to sold.csv
        sold_exists = os.path.exists(sold_path)
        with open(sold_path, "a", newline='') as f:
            writer = csv.writer(f)
            if not sold_exists or os.path.getsize(sold_path) == 0:
                writer.writerow(header + ["PrecioVenta"])
            writer.writerow(order + [selling_price])
        print("Orden marcada como vendida y registrada en sold.csv.")
    elif choice == "c":

        # Return products to inventory
        order_csv_path = f"database/orders/ind_orders/{order_id}_order.csv"
        inventory_path = "database/inventory.csv"
        if os.path.exists(order_csv_path):
            with open(order_csv_path, "r") as f:
                order_rows = list(csv.reader(f))
            order_data = order_rows[1:]  
            with open(inventory_path, "r") as f:
                inv_rows = list(csv.reader(f))
            inv_header = inv_rows[0]
            inv_data = inv_rows[1:]
            for prod in order_data:
                if not prod or len(prod) < 3:
                    continue
                nombre, cantidad = prod[0], int(prod[1])
                for inv_row in inv_data:
                    if inv_row[1] == nombre:
                        inv_row[2] = str(int(inv_row[2]) + cantidad)
            with open(inventory_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(inv_header)
                writer.writerows(inv_data)
            print("Productos devueltos al inventario.")
        print("Orden cancelada y eliminada.")
    else:
        print("Opcion no válida.")
        return   

    # Remove order from orders.csv
    data.pop(idx)
    with open(orders_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    # Delete order files
    order_csv_path = f"database/orders/ind_orders/{order_id}_order.csv"
    order_txt_path = f"database/orders/ind_desc/{order_id}_order.txt"
    for path in [order_csv_path, order_txt_path]:
        if os.path.exists(path):
            os.remove(path)

    input("Presiona Enter para continuar...")

def save_order(order_id, customer, order_date, description, products):
    # Guarda en orders.csv
    os.makedirs("database/orders", exist_ok=True)
    orders_path = "database/orders/orders.csv"
    file_exists = os.path.exists(orders_path)
    with open(orders_path, "a", newline='') as file:
        writer = csv.writer(file)
        if not file_exists or os.path.getsize(orders_path) == 0:
            writer.writerow(['id', 'customer', 'order_date', 'description'])
        writer.writerow([order_id, customer, order_date, description])

    # Guarda productos en ind_orders
    os.makedirs("database/orders/ind_orders", exist_ok=True)
    order_csv_path = f"database/orders/ind_orders/{order_id}_order.csv"
    with open(order_csv_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["nombre", "cantidad", "precio"])
        for prod in products:
            writer.writerow(prod)

def main():
    while True:
        clear()
        show_banner()
        show_menu()
        choice = get_choice()
        
        if choice == 1:
            add_order()
        elif choice == 2:
            view_orders()
        elif choice == 3:
            sell()
        elif choice == 4:
            return

if __name__ == "__main__":
    main()
