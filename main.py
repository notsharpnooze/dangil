import os

def clear():
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

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
    clear()
    show_banner()
    while True:
        show_menu()
        choice = get_choice()
        
        if choice == 1:
            import subprocess
            subprocess.run(["python", "modules/inventory.py"])
            break

        elif choice == 2:
            import subprocess
            subprocess.run(["python", "modules/orders.py"])
            break 

        elif choice == 3:
            import subprocess
            subprocess.run(["python", "modules/quotes.py"])
            break

        elif choice == 4:
            import subprocess
            subprocess.run(["python", "modules/reports.py"])
            break

        elif choice == 5:
            print("Saliendo del programa...")
            break

main()

