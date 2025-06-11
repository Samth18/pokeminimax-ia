# main.py

def menu():
    print("===== Pokeminmax =====")
    print("1. Jugar en consola")
    print("2. Jugar con interfaz gráfica")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        from ui.console_ui import combate
        combate()
    elif opcion == "2":
        from ui.graphic_ui import combate_grafico
        combate_grafico()
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    menu()

