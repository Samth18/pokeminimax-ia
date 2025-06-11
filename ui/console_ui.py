# console_ui.py

from game.player import HumanPlayer, AIPlayer
from game.pokemon import get_pokemon, is_fainted
from game.battle import calculate_damage

def mostrar_estado(jugador: HumanPlayer, ia: AIPlayer):
    print("\n================ ESTADO DEL COMBATE ================\n")
    print(f"Tu Pokémon: {jugador.pokemon.name} (PS: {jugador.pokemon.current_hp}/{jugador.pokemon.max_hp})")
    print(f"Pokémon IA: {ia.pokemon.name} (PS: {ia.pokemon.current_hp}/{ia.pokemon.max_hp})\n")

def combate():
    print("¡Bienvenido a Pokeminmax!\n")

    # Selección de Pokémon
    nombre_jugador = input("Elige tu Pokémon (por ejemplo: Pikachu): ").strip().lower()
    nombre_ia = input("Elige el Pokémon de la IA (por ejemplo: Charizard): ").strip().lower()

    try:
        jugador = HumanPlayer(get_pokemon(nombre_jugador))
        ia = AIPlayer(get_pokemon(nombre_ia))
    except Exception as e:
        print(f"Error: {e}")
        return

    turno = "jugador"

    while not is_fainted(jugador.pokemon) and not is_fainted(ia.pokemon):
        mostrar_estado(jugador, ia)

        if turno == "jugador":
            ataque = jugador.choose_attack(ia.pokemon)
            daño = calculate_damage(jugador.pokemon, ia.pokemon, ataque)
            ia.pokemon.current_hp -= daño
            print(f"\n👉 {jugador.pokemon.name} usó {ataque.name}! Causó {daño} de daño.")
            turno = "ia"
        else:
            ataque = ia.choose_attack(jugador.pokemon)
            daño = calculate_damage(ia.pokemon, jugador.pokemon, ataque)
            jugador.pokemon.current_hp -= daño
            print(f"\n🤖 {ia.pokemon.name} usó {ataque.name}! Causó {daño} de daño.")
            turno = "jugador"

    mostrar_estado(jugador, ia)
    if is_fainted(ia.pokemon):
        print("🎉 ¡Has ganado el combate!")
    else:
        print("💀 La IA ha ganado el combate.")

if __name__ == "__main__":
    combate()
