import os
import sys

from modules.inventory import main as inventory_main
from modules.orders import main as orders_main

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(r"""
 ______     ____       __      _   _____  _____  _____      
(_  __ \   (    )     /  \    / ) / ___ \(_   _)(_   _)     
  ) ) \ \  / /\ \    / /\ \  / / / /   \_) | |    | |       
 ( (   ) )( (__) )   ) ) ) ) ) )( (  ____  | |    | |       
  ) )  ) ) )    (   ( ( ( ( ( ( ( ( (__  ) | |    | |   __  
 / /__/ / /  /\  \  / /  \ \/ /  \ \__/ / _| |____| |___) ) 
(______/ /__(  )__\(_/    \__/    \____/ /_____(\________/  
            Gestor de inventario y Ventas
                    Version 1.0.0                                                           
          """)

def show_menu():
    print("1. Inventario de productos")
    print("2. Ordenes de productos")
    print("3. Presupuestos y cotizaciones")
    print("4. Reportes y estadísticas")
    print("5. Salir")

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

def main():
    while True:
        clear()
        show_banner()
        show_menu()
        choice = get_choice()
        
        if choice == 1:
            inventory_main()
        elif choice == 2:
            orders_main()
        elif choice == 3:
            import subprocess
            subprocess.run(["python", "modules/quotes.py"])
        elif choice == 4:
            import subprocess
            subprocess.run(["python", "modules/reports.py"])
        elif choice == 5:
            print("Saliendo del programa...")
            sys.exit()

if __name__ == "__main__":
    main()  