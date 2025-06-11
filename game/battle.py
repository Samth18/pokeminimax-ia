import pygame
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from .pokemon import Pokemon, Attack, calculate_damage, is_fainted, get_pokemon

# --------------------------
# Estructuras de Datos del Combate
# --------------------------
@dataclass
class BattleState:
    player_pokemon: Pokemon
    ai_pokemon: Pokemon
    current_turn: str  # 'player' o 'ai'
    game_over: bool = False
    winner: Optional[str] = None  # 'player' o 'ai'
    last_move: Optional[str] = None  # Para mostrar el último movimiento

# --------------------------
# Sistema de Combate
# --------------------------
class BattleSystem:
    def __init__(self, player_pokemon_name: str, ai_pokemon_name: str):
        pygame.init()  # Inicializar Pygame para sonidos/gráficos
        
        # Cargar Pokémon
        self.player_pokemon = get_pokemon(player_pokemon_name)
        self.ai_pokemon = get_pokemon(ai_pokemon_name)
        
        # Estado inicial
        self.state = BattleState(
            player_pokemon=self.player_pokemon,
            ai_pokemon=self.ai_pokemon,
            current_turn='player'  # El jugador comienza primero
        )
        
        # Recursos gráficos
        self.font = pygame.font.SysFont('Arial', 24)
        self.battle_bg = self._load_image("battle_bg.png")
        
    def _load_image(self, image_name: str) -> Optional[pygame.Surface]:
        """Carga una imagen desde la carpeta de assets"""
        try:
            image_path = Path(__file__).parent.parent / "images" / image_name
            if image_path.exists():
                return pygame.image.load(str(image_path)).convert()
            return None
        except pygame.error as e:
            print(f"Error cargando imagen {image_name}: {e}")
            return None

    def execute_move(self, attack_index: int) -> bool:
        """
        Ejecuta un movimiento del jugador y la respuesta de la IA.
        Devuelve True si el combate ha terminado.
        """
        if self.state.game_over:
            return True
            
        # Turno del jugador
        if self.state.current_turn == 'player':
            if 0 <= attack_index < len(self.state.player_pokemon.attacks):
                attack = self.state.player_pokemon.attacks[attack_index]
                damage = calculate_damage(
                    self.state.player_pokemon,
                    self.state.ai_pokemon,
                    attack
                )
                self.state.ai_pokemon.current_hp -= damage
                self.state.last_move = f"{self.state.player_pokemon.name} usó {attack.name} ({damage} de daño)"
                
                if is_fainted(self.state.ai_pokemon):
                    self.state.game_over = True
                    self.state.winner = 'player'
                    return True
                    
                self.state.current_turn = 'ai'
        
        # Turno de la IA (respuesta automática)
        if self.state.current_turn == 'ai' and not self.state.game_over:
            best_attack = self._select_best_ai_attack()
            damage = calculate_damage(
                self.state.ai_pokemon,
                self.state.player_pokemon,
                best_attack
            )
            self.state.player_pokemon.current_hp -= damage
            self.state.last_move = f"{self.state.ai_pokemon.name} usó {best_attack.name} ({damage} de daño)"
            
            if is_fainted(self.state.player_pokemon):
                self.state.game_over = True
                self.state.winner = 'ai'
                return True
                
            self.state.current_turn = 'player'
            
        return self.state.game_over

    def _select_best_ai_attack(self) -> Attack:
        """
        Selecciona el mejor ataque para la IA (versión simplificada).
        Más adelante se integrará con Minimax.
        """
        # Estrategia simple: elegir el ataque más poderoso efectivo
        best_attack = None
        max_damage = -1
        
        for attack in self.state.ai_pokemon.attacks:
            damage = calculate_damage(
                self.state.ai_pokemon,
                self.state.player_pokemon,
                attack
            )
            if damage > max_damage:
                max_damage = damage
                best_attack = attack
                
        return best_attack

    def render(self, screen: pygame.Surface):
        """Renderiza el estado del combate en Pygame"""
        # Fondo
        if self.battle_bg:
            screen.blit(self.battle_bg, (0, 0))
        else:
            screen.fill((240, 240, 240))
        
        # Dibujar Pokémon
        self._render_pokemon(screen, self.state.player_pokemon, (100, 300))
        self._render_pokemon(screen, self.state.ai_pokemon, (500, 100))
        
        # Mostrar información
        self._render_hp_bars(screen)
        self._render_text_info(screen)
        
        # Mostrar mensaje del último movimiento
        if self.state.last_move:
            move_text = self.font.render(self.state.last_move, True, (0, 0, 0))
            screen.blit(move_text, (50, 500))
        
        # Mostrar mensaje de fin de juego
        if self.state.game_over:
            result_text = f"¡Combate terminado! Ganador: {self.state.winner}"
            text_surface = self.font.render(result_text, True, (255, 0, 0))
            screen.blit(text_surface, (250, 550))

    def _render_pokemon(self, screen: pygame.Surface, pokemon: Pokemon, pos: Tuple[int, int]):
        """Renderiza un Pokémon en la posición especificada"""
        try:
            image_path = Path(__file__).parent.parent / "data" / "images" / pokemon.image_path
            if image_path.exists():
                img = pygame.image.load(str(image_path)).convert_alpha()
                screen.blit(img, pos)
            else:
                # Dibujar placeholder si no hay imagen
                pygame.draw.rect(screen, (200, 200, 200), (*pos, 100, 100))
                name_text = self.font.render(pokemon.name, True, (0, 0, 0))
                screen.blit(name_text, pos)
        except Exception as e:
            print(f"Error renderizando Pokémon: {e}")

    def _render_hp_bars(self, screen: pygame.Surface):
        """Dibuja las barras de HP"""
        # Jugador
        player_hp_ratio = self.state.player_pokemon.current_hp / self.state.player_pokemon.max_hp
        pygame.draw.rect(screen, (255, 0, 0), (50, 250, 200 * player_hp_ratio, 20))
        pygame.draw.rect(screen, (0, 0, 0), (50, 250, 200, 20), 2)
        
        # IA
        ai_hp_ratio = self.state.ai_pokemon.current_hp / self.state.ai_pokemon.max_hp
        pygame.draw.rect(screen, (255, 0, 0), (550, 50, 200 * ai_hp_ratio, 20))
        pygame.draw.rect(screen, (0, 0, 0), (550, 50, 200, 20), 2)

    def _render_text_info(self, screen: pygame.Surface):
        """Muestra información de texto"""
        # Jugador
        player_text = self.font.render(
            f"{self.state.player_pokemon.name} PS: {self.state.player_pokemon.current_hp}/{self.state.player_pokemon.max_hp}",
            True, (0, 0, 0)
        )
        screen.blit(player_text, (50, 220))
        
        # IA
        ai_text = self.font.render(
            f"{self.state.ai_pokemon.name} PS: {self.state.ai_pokemon.current_hp}/{self.state.ai_pokemon.max_hp}",
            True, (0, 0, 0)
        )
        screen.blit(ai_text, (550, 20))
        
        # Turno actual
        turn_text = self.font.render(
            f"Turno: {'Jugador' if self.state.current_turn == 'player' else 'IA'}",
            True, (0, 0, 255)
        )
        screen.blit(turn_text, (350, 550))

    def get_available_attacks(self) -> List[Attack]:
        """Devuelve los ataques disponibles del Pokémon del jugador"""
        return self.state.player_pokemon.attacks

# --------------------------
# Ejemplo de Uso
# --------------------------
if __name__ == "__main__":
    # Configuración inicial
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pokeminmax Battle")
    clock = pygame.time.Clock()
    
    # Crear sistema de combate
    battle = BattleSystem("Pikachu", "Charizard")
    running = True
    
    # Bucle principal
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not battle.state.game_over and battle.state.current_turn == 'player':
                    if pygame.K_1 <= event.key <= pygame.K_4:  # Teclas 1-4
                        attack_index = event.key - pygame.K_1
                        if attack_index < len(battle.get_available_attacks()):
                            battle.execute_move(attack_index)
        
        # Renderizado
        screen.fill((255, 255, 255))
        battle.render(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()