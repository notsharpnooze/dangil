import csv
import os  
import uuid
import sys

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')    

def show_banner():
    print(r""""
  _                           _                _        
 (_) _ __ __   __ ___  _ __  | |_  __ _  _ __ (_)  ___  
 | || '_ \\ \ / // _ \| '_ \ | __|/ _` || '__|| | / _ \ 
 | || | | |\ V /|  __/| | | || |_| (_| || |   | || (_) |
 |_||_| |_| \_/  \___||_| |_| \__|\__,_||_|   |_| \___/ 
                                                        """)

def show_menu():
    print("1. Agregar producto")
    print("2. Ver inventario")

    print("\n3. Volver al menú principal\n")

def get_choice():
    while True:
        try:
            choice = int(input("Seleccione una opción: "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Opción no válida. Intente de nuevo.")
        except ValueError:
            print("Entrada no válida. Por favor ingrese un número.")

#OPTIONS
def add_product():
    
    def write_header_if_needed(writer, file_exists):
        header = ['ID', 'Nombre', 'Cantidad', 'Precio']
        if not file_exists or os.path.getsize('database/inventory.csv') == 0:
            writer.writerow(header)
    clear()

    while True:
        #file = open('database/inventory.csv', 'a', newline='')
        #clear()
        print("\n=== Agregar Producto ===\n")
        print("Agregar producto (escribe 'c' en cualquier campo para cancelar y volver al menú)")
        p_id = str(uuid.uuid4())[:4]
        name = input("Ingrese el nombre del producto: ")
        if name.lower() == 'c':
            return 
        quantity = input("Ingrese la cantidad del producto: ")
        if quantity.lower() == 'c':
            return
        price = input("Ingrese el precio de compra del producto: ")
        if price.lower() == 'c':
            return

        # Write to CSV file
        os.makedirs('database', exist_ok=True)
        file_exists = os.path.exists('database/inventory.csv')
        with open('database/inventory.csv', 'a', newline='') as file:
            writer = csv.writer(file)

            #if file.tell() == 0:
            write_header_if_needed(writer, file_exists)
            writer.writerow([p_id, name, quantity, price])
        clear()
        print(f"{name} agregado exitosamente.")
           
        cont = input("¿Desea agregar otro producto? (s/n): ").lower().strip()
        if cont not in {"s","n"}:
            print("\nEntrada no válida. Por favor ingrese 's' o 'n'.")
            continue
        if cont == "s":
            add_product()
        if cont == "n":
            return
        
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

def search_product(data, header):
    clear()
    print("\nBuscar producto:")
    print("¿Buscar por?")
    print("1. Nombre")
    print("2. Cantidad")
    print("3. Precio")
    option = input("Seleccione una opción (1-3): ").strip()
    query = input("Ingrese el valor a buscar: ").strip().lower()
    results = filter_data(data, option, query)

    if not results:
        print("\nNo se encontro algun producto.")
        input("Presiona enter para continuar...")
        return None

    clear()
    print(f"\nHay {len(results)} resultado(s):\n")
    print(f"{header[0]:<15} {header[1]:<15} {header[2]:<8} {header[3]:<8}")
    print("-" * 50)
    for row in results:
        print(f"{row[0]:<15} {row[1]:<15} {row[2]:<8} {row[3]:<8}")

    input("\nPress Enter to continue...")
    return results
        
def filter_data(data, option, query):
    if option == "1": #nombre
        return [row for row in data if query in row[1].lower()]
    elif option == "2": #cantidad
        return [row for row in data if query in row[2].lower()]
    elif option == "3": #precio
        return [row for row in data if query in row[3].lower()]
    else:
        print("Opción no válida.")
        return []

def view_inventory():
    if not os.path.exists("database/inventory.csv"):
        print("\n No hay datos... \n")
        return

    with open("database/inventory.csv", "r") as file:
        rows = list(csv.reader(file))

    if len(rows) <= 1:
        print("\n El archivo esta vacio. \n")
        return

    header = rows[0]
    full_data = rows[1:]
    current_data = full_data

    while True:
        clear()
        print("\nInventario actual:\n")

        print(f"{'No.':<5}{header[1]:<15} {header[2]:<15} {header[3]:<8}")
        print("-" * 50)
        for i, row in enumerate(current_data, start=1):
            print(f"{i:<5} {row[1]:<15} {row[2]:<15} {row[3]:<8}")

        choice = input(
            "\nSeleccione una opción: \n"
            "\n'f' para buscar producto \n"
            "'x' para ordenar productos \n"  
            "'d' para eliminar producto \n"
            "'a' para actualizar producto \n"
            "\n'b' para volver al menú principal \n"
            ).strip().lower()
        
        if choice == 'b':
            return
        
        elif choice == 'f':
            filtered = search_product(current_data, header)
            if filtered is not None:
                current_data = filtered

        elif choice == 'x':
            current_data = sort_entries(current_data)

        #FIXME:
        elif choice == 'd':
            current_data = delete_product(current_data)

        else:
            print("Opción no válida. Por favor, intente de nuevo.")
            continue
        
        #choice = input("Presiona 'x' para organizar, o 'b' para regresar al menu principal: ").strip().lower()
        #if choice == "b":
        #    return
        #elif choice == "x":
        #    data = sort_entries(data)
        #else:
        #    print("Opcion no valida.")


def update_product():
    
        with open('database/inventory.csv', 'r') as file:
            rows = list(csv.reader(file))

        if len(rows) <= 1:
            print("\n No hay productos para actualizar. \n")
            return
        
        header = rows[0]
        data = rows[1:]        

        while True:
            clear()
            print("\nProductos disponibles para actualizar:\n")
            
            print(f"{header[1]:<15} {header[2]:<8} {header[3]:<8}")
            print("-" * 50)
            for i, row in enumerate(data, start=1):
                print(f"{i:<5} {row[1]:<15} {row[2]:<8} {row[3]:<8}")

            choice = input('\nSeleccione el producto a actualizar (número)\n "x" para ordenar, "c" para cancelar: ').strip()
            if choice.lower() == 'c':
                return
            elif choice == "x":
                data = sort_entries(data)
                continue 
            try:   
                index = int(choice) - 1
                if index < 0 or index >= len(data):
                    print("Número de producto no válido.")
                    return
                to_update = data[index]
            except ValueError:
                print("Entrada no válida. Por favor ingrese un número.")
                return
            
            #Confirmación de actualización
            print(f"\nQuieres actualizar {to_update[1]}? ")
            confirm = input("Presiona 's' para confirmar o cualquier otra tecla para cancelar: ").strip().lower()
            if confirm != 's':
                print("Actualización cancelada.")
                return
            
            # Solicitar nuevos datos
            nuevo_nombre = input(f"Nuevo nombre [{to_update[1]}]: ").strip() or to_update[1]
            nueva_cantidad = input(f"Nueva cantidad [{to_update[2]}]: ").strip() or to_update[2]
            nuevo_precio = input(f"Nuevo precio [{to_update[3]}]: ").strip() or to_update[3]
    
            # Buscar el índice real en data
            real_index = data.index(to_update)
            data[real_index] = [nuevo_nombre, nueva_cantidad, nuevo_precio]

            # Guardar cambios en el archivo
            with open('database/inventory.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(data)

            print("\nProducto actualizado exitosamente.\n")
            input("Presiona Enter para continuar...")
            return

def delete_product():
    with open('database/inventory.csv', 'r') as file:
        rows = list(csv.reader(file))

    if len(rows) <= 1:
        print("\n No hay productos para eliminar. \n")
        return

    header = rows[0]
    data = rows[1:]

    filtered = data
    filtered = sort_entries(filtered)

    clear()
    print("\nProductos disponibles para eliminar:\n")
    print(f"{header[1]:<15} {header[2]:<8} {header[3]:<8}")
    print("-" * 50)
    for i, row in enumerate(filtered, start=1):
        print(f"{i:<5} {row[1]:<15} {row[2]:<8} {row[3]:<8}")
    print()

    choice = input('\nSeleccione el producto a eliminar (número) o "c" para cancelar: ').strip()
    if choice.lower() == 'c':
        return
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(filtered):
            print("Número de producto no válido.")
            return
        to_delete = filtered[index]
    except ValueError:
        print("Entrada no válida. Por favor ingrese un número.")
        return

    # Confirmación de eliminación
    print(f"\n¿Seguro que quieres eliminar {to_delete[1]}? ")
    confirm = input("Presiona 's' para confirmar o cualquier otra tecla para cancelar: ").strip().lower()
    if confirm != 's':
        print("Eliminación cancelada.")
        clear()
        return


    # Eliminar el producto
    data.remove(to_delete)

    # Guardar cambios en el archivo
    with open('database/inventory.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)

    print("\nProducto eliminado exitosamente.\n")
    input("Presiona Enter para continuar...")
    return

def main():
    while True:
        clear()
        show_banner()
        show_menu()
        choice = get_choice()
        
        if choice == 1:
            add_product()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            return

if __name__ == "__main__":
    main()
     