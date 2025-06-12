# minimax.py
from typing import Tuple
from .pokemon import Pokemon, Attack, calculate_damage, is_fainted
import copy

MAX_DEPTH = 2

def evaluate_state(ai_pokemon: Pokemon, player_pokemon: Pokemon) -> int:
    if is_fainted(player_pokemon):
        return 9999
    if is_fainted(ai_pokemon):
        return -9999
    return ai_pokemon.current_hp - player_pokemon.current_hp

def minimax(ai_pokemon: Pokemon, player_pokemon: Pokemon, depth: int, is_maximizing: bool, alpha: int, beta: int) -> int:
    if depth == 0 or is_fainted(ai_pokemon) or is_fainted(player_pokemon):
        return evaluate_state(ai_pokemon, player_pokemon)

    if is_maximizing:
        max_eval = -float('inf')
        for attack in ai_pokemon.attacks:
            new_player = copy.deepcopy(player_pokemon)
            damage = calculate_damage(ai_pokemon, new_player, attack)
            new_player.current_hp -= damage
            eval = minimax(ai_pokemon, new_player, depth - 1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for attack in player_pokemon.attacks:
            new_ai = copy.deepcopy(ai_pokemon)
            damage = calculate_damage(player_pokemon, new_ai, attack)
            new_ai.current_hp -= damage
            eval = minimax(new_ai, player_pokemon, depth - 1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def minimax_decision(ai_pokemon: Pokemon, player_pokemon: Pokemon) -> int:
    best_score = -float('inf')
    best_index = 0
    for i, attack in enumerate(ai_pokemon.attacks):
        simulated_player = copy.deepcopy(player_pokemon)
        damage = calculate_damage(ai_pokemon, simulated_player, attack)
        simulated_player.current_hp -= damage
        score = minimax(ai_pokemon, simulated_player, MAX_DEPTH - 1, False, -float('inf'), float('inf'))
        if score > best_score:
            best_score = score
            best_index = i
    return best_index
