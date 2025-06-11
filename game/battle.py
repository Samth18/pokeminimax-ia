from dataclasses import dataclass
from typing import Optional, List
from .pokemon import Pokemon, Attack, calculate_damage, is_fainted, get_pokemon

@dataclass
class BattleState:
    player_pokemon: Pokemon
    ai_pokemon: Pokemon
    current_turn: str  # 'player' o 'ai'
    game_over: bool = False
    winner: Optional[str] = None
    last_move: Optional[str] = None

class BattleSystem:
    def __init__(self, player_name: str, ai_name: str):
        self.player_pokemon = get_pokemon(player_name)
        self.ai_pokemon = get_pokemon(ai_name)

        self.state = BattleState(
            player_pokemon=self.player_pokemon,
            ai_pokemon=self.ai_pokemon,
            current_turn='player'
        )

    def execute_move(self, attack_index: int) -> bool:
        if self.state.game_over:
            return True

        # 🧑 Turno del jugador
        if self.state.current_turn == 'player':
            if 0 <= attack_index < len(self.player_pokemon.attacks):
                attack = self.player_pokemon.attacks[attack_index]
                damage = calculate_damage(self.player_pokemon, self.ai_pokemon, attack)
                self.ai_pokemon.current_hp -= damage
                self.state.last_move = f"{self.player_pokemon.name} usó {attack.name} ({damage} de daño)"
                if is_fainted(self.ai_pokemon):
                    self.state.game_over = True
                    self.state.winner = "player"
                else:
                    self.state.current_turn = 'ai'

        # 🤖 Turno de la IA
        elif self.state.current_turn == 'ai':
            if attack_index == -1:
                attack = self._select_best_ai_attack()
            else:
                attack = self.ai_pokemon.attacks[attack_index]

            damage = calculate_damage(self.ai_pokemon, self.player_pokemon, attack)
            self.player_pokemon.current_hp -= damage
            self.state.last_move = f"{self.ai_pokemon.name} usó {attack.name} ({damage} de daño)"
            if is_fainted(self.player_pokemon):
                self.state.game_over = True
                self.state.winner = "ai"
            else:
                self.state.current_turn = 'player'

        return self.state.game_over

    def _select_best_ai_attack(self) -> Attack:
        return max(
            self.ai_pokemon.attacks,
            key=lambda atk: calculate_damage(self.ai_pokemon, self.player_pokemon, atk)
        )

    def get_available_attacks(self) -> List[Attack]:
        return self.player_pokemon.attacks
