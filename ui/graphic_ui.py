import pygame
from game.pokemon import get_all_pokemon_names, get_pokemon
from game.battle import BattleSystem
from game.player import AIPlayer  # ← Importa la IA real con Minimax
from pathlib import Path

pygame.init()

PIXEL_FONT = pygame.font.Font(str(Path(__file__).parent.parent / "data" / "fonts" / "pixel.ttf"), 16)
BIG_FONT = pygame.font.Font(str(Path(__file__).parent.parent / "data" / "fonts" / "pixel.ttf"), 28)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pokeminmax - Batalla Pokémon")

def load_battle_bg():
    path = Path(__file__).parent.parent / "data" / "images" / "arena.png"
    if path.exists():
        img = pygame.image.load(str(path))
        return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
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
        screen.fill((204, 238, 255))
        titulo = "ELIGE TU POKÉMON" if etapa == "jugador" else "ELIGE EL POKÉMON DE LA IA"
        title_surface = BIG_FONT.render(titulo, True, (0, 0, 0))
        screen.blit(title_surface, ((SCREEN_WIDTH - title_surface.get_width()) // 2, 30))

        p = pokemons[index]
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

        if p.card_image:
            img = pygame.transform.scale(p.card_image, (200, 280))
            screen.blit(img, (center_x - 100, center_y - 140))

        name_text = BIG_FONT.render(p.name.upper(), True, (0, 0, 0))
        screen.blit(name_text, (center_x - name_text.get_width() // 2, center_y + 160))

        for i, tipo in enumerate(p.types):
            color = TYPE_COLORS.get(tipo, (150, 150, 150))
            tipo_text = PIXEL_FONT.render(tipo.upper(), True, color)
            screen.blit(tipo_text, (center_x - tipo_text.get_width() // 2, center_y + 190 + i * 32))

        btn_left = pygame.Rect(80, center_y - 40, 60, 60)
        btn_right = pygame.Rect(SCREEN_WIDTH - 140, center_y - 40, 60, 60)
        btn_select = pygame.Rect(center_x - 100, SCREEN_HEIGHT - 90, 200, 40)

        pygame.draw.polygon(screen, (100, 100, 100),
            [(btn_left.right, btn_left.top), (btn_left.right, btn_left.bottom), (btn_left.left, btn_left.centery)])
        pygame.draw.polygon(screen, (100, 100, 100),
            [(btn_right.left, btn_right.top), (btn_right.left, btn_right.bottom), (btn_right.right, btn_right.centery)])
        pygame.draw.rect(screen, (0, 120, 255), btn_select, border_radius=10)
        txt = PIXEL_FONT.render("SELECCIONAR", True, (255, 255, 255))
        screen.blit(txt, (btn_select.centerx - txt.get_width() // 2, btn_select.y + 10))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
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
    screen.blit(BATTLE_BG, (0, 0))
    _render_pokemon(screen, battle.state.player_pokemon, (120, 320), flip=False)
    _render_pokemon(screen, battle.state.ai_pokemon, (660, 320), flip=True)

    _animate_hp(battle, anim_state)
    _render_hp_bar(screen, battle.state.player_pokemon, anim_state["player_hp"], (120, 290))
    _render_hp_bar(screen, battle.state.ai_pokemon, anim_state["ai_hp"], (660, 290))

    if battle.state.last_move:
        move_text = PIXEL_FONT.render(battle.state.last_move, True, (255, 255, 0))
        screen.blit(move_text, (SCREEN_WIDTH // 2 - move_text.get_width() // 2, 20))

    if battle.state.game_over:
        win_text = BIG_FONT.render(f"¡GANADOR: {battle.state.winner.upper()}!", True, (255, 0, 0))
        screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 650))

    if not battle.state.game_over and battle.state.current_turn == 'player':
        render_attack_buttons(screen, battle.get_available_attacks())

def _render_pokemon(screen, pokemon, pos, flip=False):
    if pokemon.image:
        img = pygame.transform.scale(pokemon.image, (180, 180))
        if flip:
            img = pygame.transform.flip(img, True, False)
        screen.blit(img, pos)
        name = PIXEL_FONT.render(pokemon.name.upper(), True, (0, 0, 0))
        screen.blit(name, (pos[0] + 90 - name.get_width() // 2, pos[1] + 190))

def _render_hp_bar(screen, pokemon, display_hp, pos):
    x, y = pos
    bar_w = 180
    bar_h = 18
    ratio = max(0, display_hp / pokemon.max_hp)
    pygame.draw.rect(screen, (0, 0, 0), (x-2, y-2, bar_w+4, bar_h+4), 2)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, int(bar_w * ratio), bar_h))
    pygame.draw.rect(screen, (230, 230, 230), (x + int(bar_w * ratio), y, bar_w - int(bar_w * ratio), bar_h))
    ps_text = PIXEL_FONT.render(f"{pokemon.current_hp}/{pokemon.max_hp}", True, (255, 255, 255))
    screen.blit(ps_text, (x + bar_w // 2 - ps_text.get_width() // 2, y - 20))

def _animate_hp(battle: BattleSystem, anim_state):
    speed = 2
    if anim_state["player_hp"] > battle.state.player_pokemon.current_hp:
        anim_state["player_hp"] -= speed
        anim_state["player_hp"] = max(battle.state.player_pokemon.current_hp, anim_state["player_hp"])
    if anim_state["ai_hp"] > battle.state.ai_pokemon.current_hp:
        anim_state["ai_hp"] -= speed
        anim_state["ai_hp"] = max(battle.state.ai_pokemon.current_hp, anim_state["ai_hp"])

def render_attack_buttons(screen, attacks):
    padding = 18
    btn_h = 36
    start_x = SCREEN_WIDTH - 300
    y_start = SCREEN_HEIGHT - (len(attacks) * (btn_h + padding)) - 30

    for i, atk in enumerate(attacks):
        text_surface = PIXEL_FONT.render(atk.name.upper(), True, (0, 0, 0))
        text_width = text_surface.get_width()
        btn_w = text_width + 30
        rect = pygame.Rect(start_x, y_start + i * (btn_h + padding), btn_w, btn_h)
        pygame.draw.rect(screen, (100, 200, 255), rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), rect, 2)
        screen.blit(text_surface, (rect.centerx - text_width // 2, rect.centery - text_surface.get_height() // 2))

def combate_grafico():
    pokemons = [get_pokemon(name) for name in get_all_pokemon_names()]
    jugador = mostrar_carrusel(pokemons, etapa="jugador")
    ia = mostrar_carrusel(pokemons, ya_elegido=jugador, etapa="ia")

    battle = BattleSystem(jugador.name, ia.name)
    anim_state = {"player_hp": jugador.current_hp, "ai_hp": ia.current_hp}

    clock = pygame.time.Clock()
    IA_TURNO_EVENT = pygame.USEREVENT + 1
    running = True

    while running:
        screen.fill((255, 255, 255))
        render_battle(screen, battle, anim_state)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and battle.state.current_turn == 'player' and not battle.state.game_over:
                mx, my = pygame.mouse.get_pos()
                btn_w, btn_h = 180, 36
                padding = 18
                start_x = SCREEN_WIDTH - btn_w - 60
                y_start = SCREEN_HEIGHT - (len(battle.get_available_attacks()) * (btn_h + padding)) - 30
                for i in range(len(battle.get_available_attacks())):
                    rect = pygame.Rect(start_x, y_start + i * (btn_h + padding), btn_w, btn_h)
                    if rect.collidepoint(mx, my):
                        battle.execute_move(i)
                        if not battle.state.game_over and battle.state.current_turn == 'ai':
                            pygame.time.set_timer(IA_TURNO_EVENT, 1500, loops=1)

            elif event.type == IA_TURNO_EVENT and not battle.state.game_over and battle.state.current_turn == 'ai':
                ai_player = AIPlayer(battle.ai_pokemon)
                attack = ai_player.choose_attack(battle.player_pokemon)
                index = battle.ai_pokemon.attacks.index(attack)
                battle.execute_move(index)
                pygame.time.set_timer(IA_TURNO_EVENT, 0)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
