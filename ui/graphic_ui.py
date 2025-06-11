import pygame
from game.pokemon import get_all_pokemon_names, get_pokemon
from game.battle import BattleSystem
from pathlib import Path

pygame.init()
FONT = pygame.font.SysFont("Arial", 20)
BIG_FONT = pygame.font.SysFont("Arial", 32, bold=True)
PIXEL_FONT = pygame.font.Font(str(Path(__file__).parent.parent / "data" / "fonts" / "pixel.ttf"), 16)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokeminmax - Selección de Pokémon")


def load_battle_bg():
    path = Path(__file__).parent.parent / "data" / "images" / "arena.png"
    if path.exists():
        return pygame.transform.scale(pygame.image.load(str(path)), (SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"[WARNING] Fondo no encontrado: {path}")
    return None


BATTLE_BG = load_battle_bg()

TYPE_COLORS = {
    'fire': (255, 100, 0), 'water': (0, 150, 255), 'electric': (255, 255, 0),
    'grass': (0, 200, 80), 'normal': (200, 200, 200), 'bug': (153, 204, 0),
    'poison': (160, 64, 160), 'ground': (210, 180, 140), 'rock': (184, 160, 56),
    'flying': (135, 206, 235), 'psychic': (255, 105, 180), 'ice': (150, 240, 255),
    'fighting': (192, 48, 40), 'ghost': (112, 88, 152), 'dragon': (100, 40, 255),
    'dark': (85, 85, 85)
}


def mostrar_carrusel(pokemons, ya_elegido=None, etapa="jugador"):
    index = 0
    total = len(pokemons)

    while True:
        screen.fill((240, 248, 255))

        titulo = "Selecciona tu Pokémon" if etapa == "jugador" else "Selecciona el Pokémon de la IA"
        title_surface = BIG_FONT.render(titulo, True, (0, 0, 0))
        screen.blit(title_surface, ((SCREEN_WIDTH - title_surface.get_width()) // 2, 30))

        p = pokemons[index]
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        if p.card_image:
            img = pygame.transform.scale(p.card_image, (200, 280))
            screen.blit(img, (center_x - 100, center_y - 140))

        name_text = BIG_FONT.render(p.name, True, (0, 0, 0))
        screen.blit(name_text, (center_x - name_text.get_width() // 2, center_y + 150))

        for i, tipo in enumerate(p.types):
            color = TYPE_COLORS.get(tipo, (150, 150, 150))
            pygame.draw.rect(screen, color, (center_x - 40, center_y + 190 + i * 32, 80, 24), border_radius=8)
            tipo_text = FONT.render(tipo.capitalize(), True, (0, 0, 0))
            screen.blit(tipo_text, (center_x - tipo_text.get_width() // 2, center_y + 192 + i * 32))

        btn_left = pygame.Rect(80, center_y - 40, 60, 60)
        btn_right = pygame.Rect(SCREEN_WIDTH - 140, center_y - 40, 60, 60)
        btn_select = pygame.Rect(center_x - 80, SCREEN_HEIGHT - 80, 160, 40)

        pygame.draw.polygon(screen, (100, 100, 100),
            [(btn_left.right, btn_left.top), (btn_left.right, btn_left.bottom), (btn_left.left, btn_left.centery)])
        pygame.draw.polygon(screen, (100, 100, 100),
            [(btn_right.left, btn_right.top), (btn_right.left, btn_right.bottom), (btn_right.right, btn_right.centery)])
        pygame.draw.rect(screen, (0, 120, 255), btn_select, border_radius=10)
        txt = FONT.render("Seleccionar", True, (255, 255, 255))
        screen.blit(txt, (btn_select.centerx - txt.get_width() // 2, btn_select.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_left.collidepoint(event.pos):
                    index = (index - 1) % total
                elif btn_right.collidepoint(event.pos):
                    index = (index + 1) % total
                elif btn_select.collidepoint(event.pos):
                    if etapa == "ia" and p == ya_elegido:
                        continue
                    return p


def render_battle(screen, battle: BattleSystem, anim_state: dict):
    screen.blit(BATTLE_BG if BATTLE_BG else pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

    _render_pokemon(screen, battle.state.player_pokemon, (100, 360), flip=True)
    _render_pokemon(screen, battle.state.ai_pokemon, (700, 120))

    _animate_hp(battle, anim_state)
    _render_hp_bar(screen, battle.state.player_pokemon, anim_state["player_hp"], (100, 320))
    _render_hp_bar(screen, battle.state.ai_pokemon, anim_state["ai_hp"], (700, 80))

    # Texto de turno
    turn = battle.state.current_turn
    turn_text = BIG_FONT.render(f"Turno: {'Jugador' if turn == 'player' else 'IA'}", True, (0, 0, 100))
    screen.blit(turn_text, (SCREEN_WIDTH // 2 - turn_text.get_width() // 2, 20))

    # Texto del daño con fuente pixelada en la parte superior
    if battle.state.last_move:
        move_text = PIXEL_FONT.render(battle.state.last_move, True, (255, 255, 0))
        screen.blit(move_text, (SCREEN_WIDTH // 2 - move_text.get_width() // 2, 70))

    if battle.state.game_over:
        win_text = BIG_FONT.render(f"¡Ganador: {battle.state.winner.upper()}!", True, (255, 0, 0))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 630))

    if not battle.state.game_over and turn == 'player':
        render_attack_buttons(screen, battle.get_available_attacks())


def _render_pokemon(screen, pokemon, pos, flip=False):
    if pokemon.image:
        img = pygame.transform.scale(pokemon.image, (180, 180))
        if flip:
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, pos)
        name = FONT.render(pokemon.name, True, (0, 0, 0))
        screen.blit(name, (pos[0] + 90 - name.get_width() // 2, pos[1] + 190))


def _render_hp_bar(screen, pokemon, display_hp, pos):
    bar_w = 200
    bar_h = 22
    x, y = pos
    ratio = max(0, display_hp / pokemon.max_hp)
    pygame.draw.rect(screen, (0, 0, 0), (x - 2, y - 2, bar_w + 4, bar_h + 4), 2)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, int(bar_w * ratio), bar_h))
    pygame.draw.rect(screen, (230, 230, 230), (x + int(bar_w * ratio), y, bar_w - int(bar_w * ratio), bar_h))

    ps_text = FONT.render(f"{pokemon.current_hp}/{pokemon.max_hp}", True, (0, 0, 0))
    screen.blit(ps_text, (x + bar_w // 2 - ps_text.get_width() // 2, y - 25))


def _animate_hp(battle: BattleSystem, anim_state):
    speed = 1.5
    if anim_state["player_hp"] > battle.state.player_pokemon.current_hp:
        anim_state["player_hp"] -= speed
        anim_state["player_hp"] = max(battle.state.player_pokemon.current_hp, anim_state["player_hp"])
    if anim_state["ai_hp"] > battle.state.ai_pokemon.current_hp:
        anim_state["ai_hp"] -= speed
        anim_state["ai_hp"] = max(battle.state.ai_pokemon.current_hp, anim_state["ai_hp"])


def render_attack_buttons(screen, attacks):
    btn_w, btn_h = 200, 40
    padding = 20
    start_x = SCREEN_WIDTH - btn_w * 2 - padding * 3
    start_y = SCREEN_HEIGHT - btn_h * 2 - padding * 2

    for i, atk in enumerate(attacks):
        col = i % 2
        row = i // 2
        x = start_x + col * (btn_w + padding)
        y = start_y + row * (btn_h + padding)
        rect = pygame.Rect(x, y, btn_w, btn_h)
        pygame.draw.rect(screen, (100, 200, 255), rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        text = FONT.render(atk.name, True, (0, 0, 0))
        screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))


def combate_grafico():
    pokemons = [get_pokemon(name) for name in get_all_pokemon_names()]
    jugador = mostrar_carrusel(pokemons, etapa="jugador")
    ia = mostrar_carrusel(pokemons, ya_elegido=jugador, etapa="ia")

    battle = BattleSystem(jugador.name, ia.name)
    anim_state = {
        "player_hp": jugador.current_hp,
        "ai_hp": ia.current_hp
    }

    IA_TURNO_EVENT = pygame.USEREVENT + 1
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((255, 255, 255))
        render_battle(screen, battle, anim_state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and battle.state.current_turn == 'player' and not battle.state.game_over:
                mx, my = pygame.mouse.get_pos()
                btn_w, btn_h = 200, 40
                padding = 20
                start_x = SCREEN_WIDTH - btn_w * 2 - padding * 3
                start_y = SCREEN_HEIGHT - btn_h * 2 - padding * 2

                for i, atk in enumerate(battle.get_available_attacks()):
                    col = i % 2
                    row = i // 2
                    x = start_x + col * (btn_w + padding)
                    y = start_y + row * (btn_h + padding)
                    rect = pygame.Rect(x, y, btn_w, btn_h)
                    if rect.collidepoint(mx, my):
                        battle.execute_move(i)
                        if not battle.state.game_over and battle.state.current_turn == 'ai':
                            pygame.time.set_timer(IA_TURNO_EVENT, 2000, loops=1)

            elif event.type == IA_TURNO_EVENT and not battle.state.game_over and battle.state.current_turn == 'ai':
                battle.execute_move(-1)
                pygame.time.set_timer(IA_TURNO_EVENT, 0)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
