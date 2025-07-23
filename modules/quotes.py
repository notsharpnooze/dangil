import csv
import os
import requests

#CALCULATIONS



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
    print("1. Calculadora de cotizaciones")
    print("2. Calcular precio de venta")
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

def main():
    while True:
        clear()
        show_banner()
        show_menu()
        choice = get_choice()
        
        if choice == 1:
            cal_selling_price()
        elif choice == 2:
            print("Calcular precio de venta (funcionalidad no implementada)")
            input("Presione Enter para continuar...")
        elif choice == 3:
            print("Registro de cotizaciones (funcionalidad no implementada)")
            input("Presione Enter para continuar...")
        elif choice == 4:
            return
        
if __name__ == "__main__":
    main() 