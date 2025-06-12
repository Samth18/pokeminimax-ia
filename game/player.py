from typing import List
from .pokemon import Pokemon, Attack, calculate_damage
from .minimax import minimax_decision

class Player:
    def __init__(self, pokemon: Pokemon):
        self.pokemon = pokemon

    def choose_attack(self, opponent_pokemon: Pokemon) -> Attack:
        raise NotImplementedError("Este método debe ser implementado por las subclases.")

class HumanPlayer(Player):
    def choose_attack(self, opponent_pokemon: Pokemon) -> Attack:
        print("\nTus ataques disponibles:")
        for i, atk in enumerate(self.pokemon.attacks):
            print(f"{i + 1}. {atk.name} - Poder: {atk.power}, Tipo: {atk.type}")

        while True:
            try:
                seleccion = int(input("Selecciona un ataque (1-4): ")) - 1
                if 0 <= seleccion < len(self.pokemon.attacks):
                    return self.pokemon.attacks[seleccion]
                else:
                    print("Índice fuera de rango. Intenta de nuevo.")
            except ValueError:
                print("Entrada inválida. Ingresa un número.")

class AIPlayer(Player):
    def choose_attack(self, opponent_pokemon: Pokemon) -> Attack:
        index = minimax_decision(self.pokemon, opponent_pokemon)
        return self.pokemon.attacks[index]
