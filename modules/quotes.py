import csv
import os
import glob
import shutil
import uuid
import datetime

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(r"""
 _____  ______    _____   _____       ____  ____  ________   
(  __ \(   __ \  / ___/  / ____\     / ___)/ __ \(___  ___)  
 ) )_) )) (__) )( (__   ( (___      / /   / /  \ \   ) )     
(  ___/(    __/  ) __)   \___ \    ( (   ( ()  () ) ( (      
 ) )    ) \ \  _( (          ) )   ( (   ( ()  () )  ) )     
( (    ( ( \ \_))\ \___  ___/ /__   \ \___\ \__/ /  ( (  __  
/__\    )_) \__/  \____\/____/(__)   \____)\____/   /__\(__) 
                                                             
    """)

def show_menu():
    print("1. Calculadora de precio de venta")
    print("2. Calculadora de cotizaciones")
    print("3. Registro de cotizaciones")
    print("4. Volver al menú principal")

def get_choice():
    while True:
        try:
            choice = int(input("Seleccione una opción: "))
            if choice in [1, 2, 3, 4]:
                return choice
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor ingrese un número.")

def cal_selling_price():
    clear()
    print("\nCalculadora de precios de venta")
    print("\nIngrese los datos del producto para calcular el precio de venta recomendado.\nPresione 'c' en cualquier campo para cancelar y volver al menú principal.\n")
    
    price = input("Ingrese el precio de compra del producto: ")
    if price.lower() == 'c':
        return
    price = float(price)

    print("El precio de compra es:\n 1. DOP\n 2. USD")
    currency_choice = input("Seleccione la moneda (1 o 2): ")
    if currency_choice == '1':
        price = price
    elif currency_choice == '2':
        interbank_rate = input("Ingrese la tasa de cambio interbancaria (USD a DOP): ")
        if interbank_rate.lower() == 'c':
            return
        price = price * float(interbank_rate)

    amount = input("Ingrese la cantidad de producto comprada (Unidades): ")
    if amount.lower() == 'c':
        return
    amount = float(amount)

    shipping_cost = input("Ingrese el costo de envío del producto: ")
    if shipping_cost.lower() == 'c':
        return
    shipping_cost = float(shipping_cost)

    shipping = (shipping_cost + price) / amount
    suggestion = shipping / (1 - 0.30)

    print(f"\nEl costo de envio por unidad es: {shipping:.2f}")
    print(f"\nEl precio de venta recomendado por unidad (30% de ganacia) es: {suggestion:.2f}")

    sell_price = float(input(f"\nCual precio de venta desea establecer? "))
    win_rate = ((sell_price - shipping) / shipping) * 100
    print(f"\nEl margen de ganancia es: {win_rate:.2f}%")

    # Save to CSV
    os.makedirs("database", exist_ok=True)
    csv_path = "database/quotes.csv"
    file_exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize(csv_path) == 0:
            writer.writerow(["VPU.", "Precio+(30%)", "Venta", "Ganacia(%)"])
        writer.writerow([
            f"{shipping:.2f}",
            f"{suggestion:.2f}",
            f"{sell_price:.2f}",
            f"{win_rate:.2f}"
        ])

    # Show all results as a table
    with open(csv_path, "r") as file:
        rows = list(csv.reader(file))

    if len(rows) <= 1:
        print("\n No hay cotizaciones registradas. \n")
    else:
        header = rows[0]
        data = rows[1:]
        clear()
        print("\nCotizaciones registradas:\n")
        print(f"{'N°':<5} {header[0]:<8} {header[1]:<18} {header[2]:<18} {header[3]:<18}")
        print("-" * 80)
        for i, row in enumerate(data, start=1):
            if len(row) < 4:
                continue  # Skip incomplete or empty rows
            print(f"{i:<5} {row[0]:<8} {row[1]:<18} {row[2]:<18} {row[3]:<18}")
        print()

    input("\nPresione Enter para continuar...")

    with open(csv_path, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["VPU.", "Precio+(30%)", "Venta", "Ganacia(%)"])

    # Ask if user wants to calculate another price
    while True:
        choice = input("\nDesea calcular otro precio de venta? (s/n): ").strip().lower()
        if choice == 's':
            cal_selling_price()
            break
        elif choice == 'n':
            print("Saliendo de la calculadora de precios de venta.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def quote_calculator():
    clear()
    print("1. Crear nueva cotización")
    print("2. Ver cotizaciones guardadas")
    print("3. Volver al menú principal")
    
    choice = input("\nseleccione una opcion: ")
    if choice == '1':
        create_quote()
    elif choice == '2':
        view_quotes()
    elif choice == '3':
        return
    else:
        print("Opción no válida. Intente de nuevo.")


def create_quote():
    clear()
    if not os.path.exists("database/inventory.csv"):
        print("\n No hay datos... \n")
        return

    with open("database/inventory.csv", "r") as file:
        rows = list(csv.reader(file))

    if len(rows) <= 1:
        print("\n El archivo esta vacio. \n")
        return

    header = rows[0]
    data = rows[1:]

    filtered = data

    quote_items = []

    while True:
        while True:
            #Start loop to select a product 

            clear()
            print("Inventario disponible:\n")
            # Print only first 4 columns for display
            print(f"No. {header[1]:^15} {header[2]:^8} {header[3]:^8}")
            print("-" * 50)
            for i, row in enumerate(filtered, start=1):
                print(f"{i:^5} {row[1]:<15} {row[2]:^8} {row[3]:<8}")
                
        
            select = input("\nPresiona el número del producto para seleccionar, \n'x' para organizar, o 'c' para regresar al menu principal: ").strip().lower()
            if select == "c":
                return
            elif select == "x":
                filtered = sort_entries(filtered)
                continue
            elif select.isdigit():
                    idx = int(select) - 1
                    if idx < 0 or idx >= len(filtered):
                        print("Producto no válido. Intente de nuevo.")
                        input("Presione Enter para continuar...")
                        continue

                    selected_row = filtered[idx]
                    max_qty = int(selected_row[2])
                    print(f"\nSeleccionaste: {selected_row[1]} (Disponible: {max_qty})")
                    qty = input(f"Ingrese la cantidad a cotizar (1-{max_qty}): ").strip()
                    if not qty.isdigit() or int(qty) < 1 or int(qty) > max_qty:
                        print("Cantidad inválida.")
                        input("Presiona Enter para continuar...")
                        continue

                    qty = int(qty)
                    quote_items.append([selected_row[1], qty, selected_row[3]])
                    print(f"Producto '{selected_row[1]}' con cantidad {qty} agregado a la cotización.\n")
                    input("Presiona Enter para continuar...") 
                    
                    clear()
                    add_more = input("¿Desea agregar otro producto a la cotización? (s/n): ").strip().lower()
                    if add_more != "s":
                        break
                       
                    #end loop
        clear()
        print("\nResumen de la cotización:\n")
        print(f"{'Producto':<20} {'Cantidad':<10} {'Precio':<10}")
        print("-" * 45)
        for item in quote_items:
            print(f"{item[0]:<20} {item[1]:<10} {item[2]:<10}")
        print()
        input("Presiona Enter para continuar...")

        # ask to save the quote
        save = input("¿Desea guardar esta cotización? (s/n): ").strip().lower()
        if save == "s":
            description = input("Agrega una descripción para esta cotización (sin caracteres especiales): ").strip()
            # Sanitize filename (remove problematic characters)
            safe_desc = "".join(c for c in description if c.isalnum() or c in (' ', '_', '-')).rstrip()
            if not safe_desc:
                safe_desc = "cotizacion"
            filename = f"database/quotes_saved/{safe_desc}.csv"
            os.makedirs("database/quotes_saved", exist_ok=True)
            with open(filename, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Producto", "Cantidad", "Precio"])
                for item in quote_items:
                    writer.writerow(item)
            clear()
            print(f"Cotización guardada exitosamente como '{filename}'.")
        else:
            clear()
            print("Cotización no guardada.")

        input("Presiona Enter para continuar...")

def view_quotes():

    quotes_dir = "database/quotes_saved"
    os.makedirs(quotes_dir, exist_ok=True)
    quote_files = sorted(glob.glob(os.path.join(quotes_dir, "*.csv")))

    if not quote_files:
        print("\nNo hay cotizaciones guardadas.\n")
        input("Presiona Enter para continuar...")
        return

    while True:
        clear()
        print("\nCotizaciones guardadas:\n")
        for i, file in enumerate(quote_files, start=1):
            print(f"{i}. {os.path.basename(file)}")
        print()
        select = input("Selecciona el número de la cotización para ver, o 'c' para regresar: ").strip().lower()
        if select == 'c':
            return
        if not select.isdigit() or int(select) < 1 or int(select) > len(quote_files):
            print("Selección inválida.")
            input("Presiona Enter para continuar...")
            continue

        idx = int(select) - 1
        filename = quote_files[idx]

        # Show quote content
        clear()
        print(f"\nCotización: {os.path.basename(filename)}\n")
        with open(filename, "r") as f:
            rows = list(csv.reader(f))
        if len(rows) > 1:
            header = rows[0]
            data = rows[1:]
            print(f"{'Producto':<20} {'Cantidad':<10} {'Precio':<10}")
            print("-" * 45)
            for item in data:
                print(f"{item[0]:<20} {item[1]:<10} {item[2]:<10}")
            print()
        else:
            print("Cotización vacía.\n")

        print("Opciones:")
        print("1. Eliminar cotización")
        print("2. Editar descripción")
        print("3. Convertir en orden")
        print("4. Volver al listado")
        action = input("Selecciona una opción: ").strip()
        if action == "1":
            os.remove(filename)
            print("Cotización eliminada.")
            input("Presiona Enter para continuar...")
            quote_files.pop(idx)
            if not quote_files:
                return
        elif action == "2":
            new_desc = input("Nueva descripción (sin caracteres especiales): ").strip()
            safe_desc = "".join(c for c in new_desc if c.isalnum() or c in (' ', '_', '-')).rstrip()
            if not safe_desc:
                safe_desc = "cotizacion"
            new_filename = os.path.join(quotes_dir, f"{safe_desc}.csv")
            shutil.move(filename, new_filename)
            print("Descripción actualizada.")
            input("Presiona Enter para continuar...")
            quote_files[idx] = new_filename
        elif action == "3":

            quote_id = f"Q{uuid.uuid4().hex[:6].upper()}"
            client = input("Nombre del cliente: ")
            date = datetime.date.today().strftime("%d/%m/%Y")
            description = input("Descripción de la cotización: ")

            # Save order (you can adapt this to your order structure)
            orders_dir = "database/orders"
            os.makedirs(orders_dir, exist_ok=True)
            filename = f"database/quotes_saved/{quote_id}_{client.replace(' ', '_')}.csv"
            with open(filename, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "cliente", "fecha", "descripcion"])
                writer.writerow([quote_id, client, date, description])
                writer.writerow([])  # Empty row for separation
                writer.writerow(["producto", "cantidad", "precio"])
                # Read items from the selected quote file and write them to the new order file
                with open(filename.replace(f"{quote_id}_{client.replace(' ', '_')}.csv", os.path.basename(filename)), "r") as quote_file:
                    quote_rows = list(csv.reader(quote_file))
                    # Find the start of the items (skip header)
                    for row in quote_rows[1:]:
                        if len(row) == 3:
                            writer.writerow(row)
            print(f"Orden creada exitosamente como '{filename}'.")
            input("Presiona Enter para continuar...")
        elif action == "4":
            continue
        else:
            print("Opción no válida.")
            input("Presiona Enter para continuar...")   

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

def main():
    while True:
        clear()
        show_banner()
        show_menu()
        choice = get_choice()
        
        if choice == 1:
            cal_selling_price()
        elif choice == 2:
            quote_calculator()
        elif choice == 3:
            input("Presione Enter para continuar...")
        elif choice == 4:
            return
        
if __name__ == "__main__":
    main() 