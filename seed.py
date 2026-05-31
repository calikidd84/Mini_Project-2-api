import random
from decimal import Decimal

from dotenv import load_dotenv
from sqlalchemy.orm import Session

import models
from database import Base, SessionLocal, engine

load_dotenv()

Base.metadata.create_all(bind=engine)

publishers_data = [
    {"name": "Nintendo", "country": "Japan", "founded_year": 1889},
    {"name": "Sony Interactive Entertainment", "country": "Japan", "founded_year": 1993},
    {"name": "Xbox Game Studios", "country": "United States", "founded_year": 2000},
    {"name": "Sega", "country": "Japan", "founded_year": 1960},
    {"name": "Electronic Arts", "country": "United States", "founded_year": 1982},
    {"name": "Ubisoft", "country": "France", "founded_year": 1986},
    {"name": "Capcom", "country": "Japan", "founded_year": 1979},
    {"name": "Bandai Namco Entertainment", "country": "Japan", "founded_year": 1955},
    {"name": "Square Enix", "country": "Japan", "founded_year": 2003},
    {"name": "Activision", "country": "United States", "founded_year": 1979},
]

consoles_data = [
    {"name": "Nintendo Switch", "manufacturer": "Nintendo", "release_year": 2017},
    {"name": "Nintendo Switch 2", "manufacturer": "Nintendo", "release_year": 2025},
    {"name": "PlayStation 5", "manufacturer": "Sony", "release_year": 2020},
    {"name": "PlayStation 4", "manufacturer": "Sony", "release_year": 2013},
    {"name": "Xbox Series X", "manufacturer": "Microsoft", "release_year": 2020},
    {"name": "Xbox One", "manufacturer": "Microsoft", "release_year": 2013},
    {"name": "Steam Deck", "manufacturer": "Valve", "release_year": 2022},
    {"name": "PC", "manufacturer": "Various", "release_year": 1970},
    {"name": "Nintendo 3DS", "manufacturer": "Nintendo", "release_year": 2011},
    {"name": "PlayStation Vita", "manufacturer": "Sony", "release_year": 2011},
]

games_by_publisher = {
    "Nintendo": [
        ("The Legend of Zelda: Breath of the Wild", "Action-adventure"),
        ("The Legend of Zelda: Tears of the Kingdom", "Action-adventure"),
        ("Super Mario Odyssey", "Platformer"),
        ("Mario Kart 8 Deluxe", "Racing"),
        ("Animal Crossing: New Horizons", "Simulation"),
        ("Super Smash Bros. Ultimate", "Fighting"),
        ("Splatoon 3", "Shooter"),
        ("Metroid Dread", "Action-adventure"),
        ("Luigi's Mansion 3", "Action-adventure"),
        ("Pokemon Scarlet", "RPG"),
        ("Pokemon Violet", "RPG"),
        ("Kirby and the Forgotten Land", "Platformer"),
        ("Fire Emblem Engage", "Strategy RPG"),
        ("Xenoblade Chronicles 3", "RPG"),
        ("Pikmin 4", "Strategy"),
        ("Mario Party Superstars", "Party"),
        ("Super Mario Bros. Wonder", "Platformer"),
        ("Nintendo Switch Sports", "Sports"),
        ("Paper Mario: The Thousand-Year Door", "RPG"),
        ("Princess Peach: Showtime!", "Action-adventure"),
    ],
    "Sony Interactive Entertainment": [
        ("Marvel's Spider-Man 2", "Action-adventure"),
        ("God of War Ragnarok", "Action-adventure"),
        ("Horizon Forbidden West", "Action RPG"),
        ("The Last of Us Part I", "Action-adventure"),
        ("The Last of Us Part II Remastered", "Action-adventure"),
        ("Gran Turismo 7", "Racing"),
        ("Ratchet & Clank: Rift Apart", "Action-platformer"),
        ("Returnal", "Roguelike shooter"),
        ("Demon's Souls", "Action RPG"),
        ("Astro Bot", "Platformer"),
        ("Ghost of Tsushima Director's Cut", "Action-adventure"),
        ("Helldivers 2", "Shooter"),
        ("Sackboy: A Big Adventure", "Platformer"),
        ("MLB The Show 24", "Sports"),
        ("Until Dawn", "Horror"),
        ("Concrete Genie", "Action-adventure"),
        ("Dreams", "Creative sandbox"),
        ("Death Stranding Director's Cut", "Action"),
        ("Uncharted: Legacy of Thieves Collection", "Action-adventure"),
        ("Shadow of the Colossus", "Action-adventure"),
    ],
    "Xbox Game Studios": [
        ("Halo Infinite", "Shooter"),
        ("Forza Horizon 5", "Racing"),
        ("Starfield", "RPG"),
        ("Sea of Thieves", "Action-adventure"),
        ("Grounded", "Survival"),
        ("Psychonauts 2", "Platformer"),
        ("Microsoft Flight Simulator", "Simulation"),
        ("Age of Empires IV", "RTS"),
        ("Avowed", "RPG"),
        ("Senua's Saga: Hellblade II", "Action-adventure"),
        ("Ori and the Will of the Wisps", "Metroidvania"),
        ("Pentiment", "Adventure"),
        ("Hi-Fi Rush", "Action rhythm"),
        ("Ara: History Untold", "Strategy"),
        ("State of Decay 2", "Survival"),
        ("Gears 5", "Shooter"),
        ("As Dusk Falls", "Interactive drama"),
        ("Minecraft Legends", "Action strategy"),
        ("Age of Mythology: Retold", "RTS"),
        ("Fable", "RPG"),
    ],
    "Sega": [
        ("Sonic Frontiers", "Action-platformer"),
        ("Like a Dragon: Infinite Wealth", "RPG"),
        ("Persona 3 Reload", "RPG"),
        ("Total War: Warhammer III", "Strategy"),
        ("Football Manager 2024", "Sports simulation"),
        ("Shin Megami Tensei V: Vengeance", "RPG"),
        ("Yakuza: Like a Dragon", "RPG"),
        ("Persona 5 Royal", "RPG"),
        ("Sonic Superstars", "Platformer"),
        ("Two Point Campus", "Simulation"),
        ("Company of Heroes 3", "RTS"),
        ("Phantasy Star Online 2: New Genesis", "MMORPG"),
        ("Super Monkey Ball Banana Rumble", "Party"),
        ("Like a Dragon Gaiden", "Action-adventure"),
        ("Demon Slayer: Kimetsu no Yaiba - The Hinokami Chronicles", "Fighting"),
        ("Persona 5 Tactica", "Strategy RPG"),
        ("Sonic Origins Plus", "Platformer"),
        ("Endless Dungeon", "Tactical roguelite"),
        ("Alien: Isolation", "Survival horror"),
        ("Virtua Fighter 5 R.E.V.O.", "Fighting"),
    ],
    "Electronic Arts": [
        ("EA Sports FC 25", "Sports"),
        ("Madden NFL 25", "Sports"),
        ("The Sims 4", "Simulation"),
        ("Apex Legends", "Battle royale"),
        ("Star Wars Jedi: Survivor", "Action-adventure"),
        ("Battlefield 2042", "Shooter"),
        ("Need for Speed Unbound", "Racing"),
        ("Dragon Age: The Veilguard", "RPG"),
        ("It Takes Two", "Co-op adventure"),
        ("Dead Space", "Survival horror"),
        ("F1 24", "Racing"),
        ("NHL 25", "Sports"),
        ("College Football 25", "Sports"),
        ("Skate.", "Sports"),
        ("Star Wars Squadrons", "Space combat"),
        ("Mass Effect Legendary Edition", "RPG"),
        ("Plants vs. Zombies: Battle for Neighborville", "Shooter"),
        ("Knockout City", "Sports action"),
        ("Wild Hearts", "Action RPG"),
        ("Immortals of Aveum", "FPS"),
    ],
    "Ubisoft": [
        ("Assassin's Creed Mirage", "Action-adventure"),
        ("Assassin's Creed Shadows", "Action RPG"),
        ("Far Cry 6", "Shooter"),
        ("Tom Clancy's Rainbow Six Siege", "Tactical shooter"),
        ("Prince of Persia: The Lost Crown", "Metroidvania"),
        ("The Crew Motorfest", "Racing"),
        ("Just Dance 2025 Edition", "Rhythm"),
        ("Avatar: Frontiers of Pandora", "Action-adventure"),
        ("Star Wars Outlaws", "Action-adventure"),
        ("Anno 1800", "City-building"),
        ("Mario + Rabbids Sparks of Hope", "Strategy"),
        ("Skull and Bones", "Action-adventure"),
        ("Watch Dogs: Legion", "Action-adventure"),
        ("Riders Republic", "Sports"),
        ("South Park: Snow Day!", "Action"),
        ("XDefiant", "Arena shooter"),
        ("Immortals Fenyx Rising", "Action-adventure"),
        ("Brawlhalla", "Fighting"),
        ("Tom Clancy's The Division 2", "Action RPG"),
        ("Child of Light", "Platform RPG"),
    ],
    "Capcom": [
        ("Monster Hunter Wilds", "Action RPG"),
        ("Monster Hunter Rise", "Action RPG"),
        ("Street Fighter 6", "Fighting"),
        ("Resident Evil 4", "Survival horror"),
        ("Resident Evil Village", "Survival horror"),
        ("Dragon's Dogma 2", "Action RPG"),
        ("Devil May Cry 5", "Action"),
        ("Mega Man 11", "Platformer"),
        ("Ace Attorney Investigations Collection", "Adventure"),
        ("Exoprimal", "Shooter"),
        ("Kunitsu-Gami: Path of the Goddess", "Action strategy"),
        ("Pragmata", "Sci-fi action"),
        ("Ghost Trick: Phantom Detective", "Puzzle-adventure"),
        ("Marvel vs. Capcom Fighting Collection", "Fighting"),
        ("Okami HD", "Action-adventure"),
        ("Dead Rising Deluxe Remaster", "Action"),
        ("Capcom Fighting Collection 2", "Fighting"),
        ("Onimusha: Warlords", "Action-adventure"),
        ("Monster Hunter Stories 2", "RPG"),
        ("Apollo Justice: Ace Attorney Trilogy", "Adventure"),
    ],
    "Bandai Namco Entertainment": [
        ("Elden Ring", "Action RPG"),
        ("Tekken 8", "Fighting"),
        ("Dragon Ball: Sparking! Zero", "Fighting"),
        ("Sand Land", "Action RPG"),
        ("Little Nightmares III", "Puzzle-platformer"),
        ("Tales of Arise", "RPG"),
        ("Pac-Man World Re-Pac", "Platformer"),
        ("Scarlet Nexus", "Action RPG"),
        ("Klonoa Phantasy Reverie Series", "Platformer"),
        ("Sword Art Online: Last Recollection", "Action RPG"),
        ("One Piece Odyssey", "RPG"),
        ("Naruto X Boruto Ultimate Ninja Storm Connections", "Fighting"),
        ("Armored Core VI: Fires of Rubicon", "Action"),
        ("Ace Combat 7: Skies Unknown", "Flight combat"),
        ("Taiko no Tatsujin: Rhythm Festival", "Rhythm"),
        ("Baten Kaitos I & II HD Remaster", "RPG"),
        ("Gundam Breaker 4", "Action"),
        ("Code Vein", "Action RPG"),
        ("Blue Protocol", "MMORPG"),
        ("The Dark Pictures Anthology: The Devil in Me", "Horror"),
    ],
    "Square Enix": [
        ("Final Fantasy VII Rebirth", "RPG"),
        ("Final Fantasy XVI", "Action RPG"),
        ("Dragon Quest XI S", "RPG"),
        ("Kingdom Hearts III", "Action RPG"),
        ("Octopath Traveler II", "RPG"),
        ("NieR: Automata", "Action RPG"),
        ("Foamstars", "Shooter"),
        ("SaGa Emerald Beyond", "RPG"),
        ("Life is Strange: Double Exposure", "Adventure"),
        ("Romancing SaGa 2: Revenge of the Seven", "RPG"),
        ("Triangle Strategy", "Strategy RPG"),
        ("Harvestella", "Life sim RPG"),
        ("Star Ocean: The Second Story R", "Action RPG"),
        ("Visions of Mana", "Action RPG"),
        ("Dragon Quest Monsters: The Dark Prince", "RPG"),
        ("Theatrhythm Final Bar Line", "Rhythm"),
        ("Chrono Cross: The Radical Dreamers Edition", "RPG"),
        ("Tactics Ogre: Reborn", "Strategy RPG"),
        ("Bravely Default II", "RPG"),
        ("PowerWash Simulator", "Simulation"),
    ],
    "Activision": [
        ("Call of Duty: Black Ops 6", "Shooter"),
        ("Call of Duty: Modern Warfare III", "Shooter"),
        ("Diablo IV", "Action RPG"),
        ("Overwatch 2", "Hero shooter"),
        ("Crash Bandicoot 4: It's About Time", "Platformer"),
        ("Spyro Reignited Trilogy", "Platformer"),
        ("Tony Hawk's Pro Skater 1 + 2", "Sports"),
        ("Sekiro: Shadows Die Twice", "Action-adventure"),
        ("Crash Team Rumble", "Party"),
        ("Warcraft Rumble", "Strategy"),
        ("World of Warcraft: The War Within", "MMORPG"),
        ("Candy Crush Saga", "Puzzle"),
        ("Call of Duty: Warzone", "Battle royale"),
        ("Guitar Hero Live", "Rhythm"),
        ("Prototype 2", "Action"),
        ("Singularity", "Shooter"),
        ("Geometry Dash", "Platformer"),
        ("Skylanders: Trap Team", "Action-adventure"),
        ("Crash Bandicoot N. Sane Trilogy", "Platformer"),
        ("Heroes of the Storm", "MOBA"),
    ],
}

console_pool = list(consoles_data)

new_item_titles = {
    "Nintendo Switch 2",
    "PlayStation Vita",
    "Princess Peach: Showtime!",
    "Monster Hunter Wilds",
    "Fable",
    "Little Nightmares III",
}

def random_score_and_votes(name: str):
    if name in new_item_titles or random.random() < 0.08:
        return None, 0
    score = Decimal(str(round(random.uniform(6.5, 9.8), 1)))
    votes = random.randint(120, 5000)
    return score, votes

def seed_publishers(db: Session):
    publisher_map = {}
    for item in publishers_data:
        existing = db.query(models.Publisher).filter_by(name=item["name"]).first()
        if existing:
            publisher_map[item["name"]] = existing
            continue

        obj = models.Publisher(**item)
        db.add(obj)
        db.flush()
        publisher_map[item["name"]] = obj

    return publisher_map

def seed_consoles(db: Session):
    console_map = {}

    for item in consoles_data:
        existing = db.query(models.Console).filter_by(name=item["name"]).first()
        score, votes = random_score_and_votes(item["name"])

        payload = {
            **item,
            "fan_rating": score,
            "vote_count": votes,
        }

        if existing:
            existing.manufacturer = item["manufacturer"]
            existing.release_year = item["release_year"]
            existing.fan_rating = score
            existing.vote_count = votes
            console_map[item["name"]] = existing
            continue

        obj = models.Console(**payload)
        db.add(obj)
        db.flush()
        console_map[item["name"]] = obj

    return console_map

def assign_consoles_for_game(game_title: str, publisher_name: str, console_map: dict):
    name_set = set()

    switch_only_keywords = [
        "Pokemon", "Mario", "Zelda", "Pikmin", "Kirby",
        "Luigi", "Fire Emblem", "Princess Peach", "Xenoblade"
    ]
    sony_keywords = [
        "Spider-Man", "God of War", "Gran Turismo", "The Last of Us",
        "Ghost of Tsushima", "Ratchet", "Demon's Souls", "Astro Bot",
        "Sackboy", "Until Dawn", "Dreams", "Shadow of the Colossus"
    ]
    xbox_keywords = [
        "Halo", "Forza", "Sea of Thieves", "Grounded", "Pentiment",
        "Avowed", "Fable", "Gears", "Senua", "Age of Empires",
        "Age of Mythology", "Flight Simulator"
    ]

    if publisher_name == "Nintendo" or any(k in game_title for k in switch_only_keywords):
        name_set.update(["Nintendo Switch", "Nintendo Switch 2"])
        if "Pokemon" in game_title or "Mario Kart 8 Deluxe" in game_title:
            name_set.add("Nintendo 3DS")

    elif publisher_name == "Sony Interactive Entertainment" or any(k in game_title for k in sony_keywords):
        name_set.update(["PlayStation 5", "PlayStation 4"])
        if random.random() < 0.3:
            name_set.add("PC")

    elif publisher_name == "Xbox Game Studios" or any(k in game_title for k in xbox_keywords):
        name_set.update(["Xbox Series X", "Xbox One", "PC"])
        if random.random() < 0.25:
            name_set.add("Steam Deck")

    else:
        samples = random.sample(console_pool, k=random.randint(2, 4))
        name_set.update([item["name"] for item in samples])

        if "PC" not in name_set and random.random() < 0.5:
            name_set.add("PC")

    return [console_map[name] for name in name_set if name in console_map]

def seed_games(db: Session, publisher_map: dict, console_map: dict):
    for publisher_name, games in games_by_publisher.items():
        publisher = publisher_map[publisher_name]

        for title, genre in games:
            existing = db.query(models.Game).filter_by(title=title).first()
            score, votes = random_score_and_votes(title)
            release_year = random.randint(2017, 2026)
            assigned_consoles = assign_consoles_for_game(title, publisher_name, console_map)

            if existing:
                existing.genre = genre
                existing.release_year = release_year
                existing.publisher_id = publisher.id
                existing.fan_rating = score
                existing.vote_count = votes
                existing.consoles = assigned_consoles
                continue

            obj = models.Game(
                title=title,
                genre=genre,
                release_year=release_year,
                publisher_id=publisher.id,
                fan_rating=score,
                vote_count=votes,
            )
            obj.consoles = assigned_consoles
            db.add(obj)

def main():
    db = SessionLocal()
    try:
        publisher_map = seed_publishers(db)
        console_map = seed_consoles(db)
        seed_games(db, publisher_map, console_map)
        db.commit()
        print("Seed data inserted successfully.")
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()