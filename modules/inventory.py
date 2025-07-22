import csv
import os  


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

def add_product():
    
    while True:
        file = open('database/inventory.csv', 'a', newline='')
        clear()
        name = input("Ingrese el nombre del producto: ")
        quantity = input("Ingrese la cantidad del producto: ")
        price = input("Ingrese el precio de compra del producto: ")

        with open('database/inventory.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(['Nombre', 'Cantidad', 'Precio'])
            writer.writerow([name, quantity, price])
        clear()
        print("Producto agregado exitosamente.")
           
        cont = input("¿Desea agregar otro producto? (s/n): ").lower().strip()
        if cont not in {"s","n"}:
            print("\nEntrada no válida. Por favor ingrese 's' o 'n'.")
            continue
        if cont == "s":
            add_product()
        if cont == "n":
            main()
            break
        

def main():
    clear()
    show_banner()
    while True:
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
            break
                                                        
main()
            