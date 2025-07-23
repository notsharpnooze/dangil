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
    print("3. Actualizar producto")
    print("4. Eliminar producto")
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

#OPTIONS
def add_product():
    
    while True:
        file = open('database/inventory.csv', 'a', newline='')
        clear()
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

        with open('database/inventory.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['ID','Nombre', 'Cantidad', 'Precio'])
            writer.writerow([p_id, name, quantity, price])
        clear()
        print("Producto agregado exitosamente.")
           
        cont = input("¿Desea agregar otro producto? (s/n): ").lower().strip()
        if cont not in {"s","n"}:
            print("\nEntrada no válida. Por favor ingrese 's' o 'n'.")
            continue
        if cont == "s":
            add_product()
        if cont == "n":
            return
        
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
    data = rows[1:]

    while True:
        clear()
        print("\nInventario actual:\n")
        # Print only first 4 columns for display
        print(f"{header[1]:<15} {header[2]:<15} {header[3]:<8}")
        print("-" * 50)
        for row in data:
            print(f"{row[1]:<15} {row[2]:<15} {row[3]:<8}")
        print()

        choice = input("Presiona 'x' para organizar, o 'b' para regresar al menu principal: ").strip().lower()
        if choice == "b":
            return
        elif choice == "x":
            data = sort_entries(data)
        else:
            print("Opcion no valida.")

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

def update_product():
    
        with open('database/inventory.csv', 'r') as file:
            rows = list(csv.reader(file))

        if len(rows) <= 1:
            print("\n No hay productos para actualizar. \n")
            return
        
        header = rows[0]
        data = rows[1:]

        filtered = data
        filtered = sort_entries(filtered)

        clear()
        print("\nProductos disponibles para actualizar:\n")
        print(f"{header[1]:<15} {header[2]:<8} {header[3]:<8}")
        print("-" * 50)
        for i, row in enumerate(filtered, start=1):
            print(f"{i:<5} {row[1]:<15} {row[2]:<8} {row[3]:<8}")
                  
        select = input('\nSeleccione el producto a actualizar (número) o "c" para cancelar: ').strip()
        if select.lower() == 'c':
            return

        try:   
            index = int(select) - 1
            if index < 0 or index >= len(filtered):
                print("Número de producto no válido.")
                return
            to_update = filtered[index]
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

    select = input('\nSeleccione el producto a eliminar (número) o "c" para cancelar: ').strip()
    if select.lower() == 'c':
        return

    try:
        index = int(select) - 1
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
            update_product()
        elif choice == 4:
            delete_product()
        elif choice == 5:
            return

if __name__ == "__main__":
    main()
     