import csv
import pygame
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple
from dataclasses import dataclass

# --------------------------
# Definición de Tipos (1era Generación)
# --------------------------
PokemonType = Literal[
    'normal', 'fire', 'water', 'electric', 'grass', 
    'ice', 'fighting', 'poison', 'ground', 'flying',
    'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark'
]

# --------------------------
# Estructuras de Datos
# --------------------------
@dataclass
class Attack:
    name: str
    type: PokemonType
    power: int

@dataclass
class Pokemon:
    name: str
    types: List[PokemonType]
    max_hp: int
    current_hp: int
    attacks: List[Attack]
    image: Optional[pygame.Surface] = None
    sprite_pos: Tuple[int, int] = (0, 0)
    card_image: Optional[pygame.Surface] = None  # NUEVO

# --------------------------
# Tabla de Efectividad Simplificada
# --------------------------
EFFECTIVITY_TABLE: Dict[PokemonType, Dict[PokemonType, float]] = {
    'normal': {'rock': 0.5, 'ghost': 0},
    'fire': {'fire': 0.5, 'water': 0.5, 'grass': 2, 'ice': 2, 'bug': 2, 'rock': 0.5},
    'water': {'fire': 2, 'water': 0.5, 'grass': 0.5, 'ground': 2, 'rock': 2},
    'electric': {'water': 2, 'electric': 0.5, 'grass': 0.5, 'ground': 0, 'flying': 2},
    'grass': {'fire': 0.5, 'water': 2, 'grass': 0.5, 'poison': 0.5, 'ground': 2, 'flying': 0.5, 'bug': 0.5},
    'ice': {'water': 0.5, 'grass': 2, 'ice': 0.5, 'ground': 2, 'flying': 2},
    'fighting': {'normal': 2, 'ice': 2, 'poison': 0.5, 'flying': 0.5, 'psychic': 0.5, 'bug': 0.5, 'rock': 2, 'ghost': 0},
    'poison': {'grass': 2, 'poison': 0.5, 'ground': 0.5, 'bug': 2},
    'ground': {'fire': 2, 'electric': 2, 'grass': 0.5, 'poison': 2, 'flying': 0, 'bug': 0.5, 'rock': 2},
    'flying': {'electric': 0.5, 'grass': 2, 'fighting': 2, 'bug': 2, 'rock': 0.5},
    'psychic': {'fighting': 2, 'poison': 2, 'psychic': 0.5},
    'bug': {'fire': 0.5, 'grass': 2, 'fighting': 0.5, 'poison': 2, 'flying': 0.5, 'psychic': 2},
    'rock': {'fire': 2, 'ice': 2, 'fighting': 0.5, 'ground': 0.5, 'flying': 2},
    'ghost': {'normal': 0, 'psychic': 0, 'ghost': 2},
    'dragon': {'dragon': 2},
    'dark': {'psychic': 2, 'ghost': 2, 'fighting': 0.5, 'dark': 0.5}
}

# --------------------------
# Cargador de Pokémon
# --------------------------
class PokemonLoader:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.data_dir = self.base_dir / "data"
        self.images_dir = self.data_dir / "images"
        self.csv_path = self.data_dir / "pokemon.csv"
        
        self._ensure_directories()
        self.pokemon_db: Dict[str, Pokemon] = self._load_db()

    def _ensure_directories(self):
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def _load_image(self, image_name: str) -> Optional[pygame.Surface]:
        try:
            image_path = self.images_dir / image_name
            if image_path.exists():
                return pygame.image.load(str(image_path))
            return None
        except (pygame.error, FileNotFoundError) as e:
            print(f"[WARNING] No se pudo cargar imagen {image_name}: {e}")
            return None

    def _load_image_from_subdir(self, subfolder: str, image_name: str) -> Optional[pygame.Surface]:
        try:
            image_path = self.images_dir / subfolder / image_name
            if image_path.exists():
                return pygame.image.load(str(image_path))
            return None
        except (pygame.error, FileNotFoundError) as e:
            print(f"[WARNING] No se pudo cargar imagen {image_name}: {e}")
            return None

    def _load_db(self) -> Dict[str, Pokemon]:
        pokemon_db = {}
        
        try:
            with open(self.csv_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row in reader:
                    if int(row.get('generation', '1')) != 1:
                        continue
                    
                    types = [row['type1'].lower()]
                    if row.get('type2'):
                        types.append(row['type2'].lower())

                    # Carga imágenes principales y de tarjeta
                    main_image_name = row.get('image', f"{row['name'].lower()}.png")
                    card_image_name = row.get('card_image', f"{row['name'].lower()}_card.png")
                    
                    pokemon_db[row['name'].lower()] = Pokemon(
                        name=row['name'],
                        types=types,
                        max_hp=int(row['hp']) * 3,
                        current_hp=int(row['hp']) * 3,
                        attacks=[
                            Attack(
                                name=row['attack1'],
                                type=row['attack1_type'].lower(),
                                power=int(row['attack1_power'])
                            ),
                            Attack(
                                name=row['attack2'],
                                type=row['attack2_type'].lower(),
                                power=int(row['attack2_power'])
                            )
                        ],
                        image=self._load_image(main_image_name),
                        card_image=self._load_image_from_subdir("cards", card_image_name),
                        sprite_pos=(int(row.get('sprite_x', 0)), int(row.get('sprite_y', 0)))
                    )
                    
        except Exception as e:
            print(f"[ERROR] No se pudo cargar la base de datos: {e}")
            return self._create_fallback_db()
            
        return pokemon_db

    def _create_fallback_db(self) -> Dict[str, Pokemon]:
        return {
            'pikachu': Pokemon(
                name='Pikachu',
                types=['electric'],
                max_hp=100,
                current_hp=100,
                attacks=[
                    Attack(name='Impactrueno', type='electric', power=40),
                    Attack(name='Rapidez', type='normal', power=30)
                ],
                image=self._load_image('pikachu.png'),
                card_image=self._load_image_from_subdir("cards", "pikachu_card.png")
            )
        }

    def get_pokemon(self, name: str) -> Pokemon:
        if name.lower() not in self.pokemon_db:
            available = ", ".join([p.name for p in self.pokemon_db.values()])
            raise ValueError(f"Pokémon {name} no encontrado. Disponibles: {available}")

        original = self.pokemon_db[name.lower()]
        return Pokemon(
            name=original.name,
            types=original.types.copy(),
            max_hp=original.max_hp,
            current_hp=original.max_hp,
            attacks=[Attack(**a.__dict__) for a in original.attacks],
            image=original.image,
            card_image=original.card_image,
            sprite_pos=original.sprite_pos
        )

    def get_all_pokemon_names(self) -> List[str]:
        return [p.name for p in self.pokemon_db.values()]

# --------------------------
# Inicialización Global
# --------------------------
pokemon_loader = PokemonLoader()

# --------------------------
# API Pública
# --------------------------
def get_pokemon(name: str) -> Pokemon:
    return pokemon_loader.get_pokemon(name)

def get_all_pokemon_names() -> List[str]:
    return pokemon_loader.get_all_pokemon_names()

def calculate_damage(attacker: Pokemon, defender: Pokemon, attack: Attack) -> int:
    effectiveness = 1.0
    for defender_type in defender.types:
        effectiveness *= EFFECTIVITY_TABLE.get(attack.type, {}).get(defender_type, 1.0)
    
    damage = int(attack.power * effectiveness)
    return damage if effectiveness != 0 else 0

def is_fainted(pokemon: Pokemon) -> bool:
    return pokemon.current_hp <= 0
