# player.py

from abc import ABC, abstractmethod
from typing import List
from .pokemon import Pokemon, Attack
from .minimax import minimax_decision  # Asumimos que existe esta función

class Player(ABC):
    def __init__(self, pokemon: Pokemon):
        self.pokemon = pokemon

    @abstractmethod
    def choose_attack(self, opponent_pokemon: Pokemon) -> Attack:
        pass

    def is_defeated(self) -> bool:
        return self.pokemon.current_hp <= 0

class HumanPlayer(Player):
    def choose_attack(self, opponent_pokemon: Pokemon) -> Attack:
        print(f"\nTu Pokémon: {self.pokemon.name} (PS: {self.pokemon.current_hp}/{self.pokemon.max_hp})")
        print("Elige un ataque:")
        for idx, atk in enumerate(self.pokemon.attacks):
            print(f"{idx + 1}. {atk.name} ({atk.type}, Poder: {atk.power})")

        while True:
            try:
                choice = int(input("Ataque (1-4): ")) - 1
                if 0 <= choice < len(self.pokemon.attacks):
                    return self.pokemon.attacks[choice]
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Ingresa un número válido.")

class AIPlayer(Player):
    def choose_attack(self, opponent_pokemon: Pokemon) -> Attack:
        index = minimax_decision(self.pokemon, opponent_pokemon)
        return self.pokemon.attacks[index]