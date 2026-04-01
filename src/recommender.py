import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_tempo: float
    target_danceability: float
    target_acoustic: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs: List[Dict] = []

    with open(csv_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            if not row:
                continue

            songs.append({
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            })

    return songs


MIN_TEMPO = 60.0
MAX_TEMPO = 152.0
TEMPO_RANGE = MAX_TEMPO - MIN_TEMPO

RELATED_GENRES = {
    "pop": {"indie pop", "synthwave", "electronic", "latin", "dance"},
    "rock": {"indie", "alternative", "metal", "punk"},
    "lofi": {"ambient", "chill", "jazz"},
    "ambient": {"electronic", "chill"},
    "country": {"folk", "acoustic"},
    "jazz": {"blues", "soul"},
    "electronic": {"synthwave", "pop", "dance"},
    # genres present in songs.csv but previously missing as keys
    "metal": {"rock", "punk", "alternative"},
    "synthwave": {"electronic", "pop", "ambient"},
    "folk": {"country", "acoustic", "indie"},
    "classical": {"ambient", "orchestral"},
    "world": {"latin", "folk", "reggae"},
    "indie pop": {"pop", "indie", "alternative"},
    "latin": {"pop", "reggae", "world"},
    "reggae": {"ska", "latin", "folk"},
}

RELATED_MOODS = {
    "happy": {"playful", "upbeat", "energetic"},
    "chill": {"relaxed", "calm", "laid-back", "focused"},
    "intense": {"energetic", "angry", "moody"},
    "relaxed": {"chill", "calm", "serene"},
    "moody": {"thoughtful", "intense"},
    "focused": {"thoughtful", "calm"},
    "serene": {"calm", "relaxed"},
    "angry": {"intense"},
    "thoughtful": {"moody", "focused"},
    # moods present in songs.csv as values but previously missing as keys
    "energetic": {"intense", "happy", "upbeat"},
    "laid-back": {"chill", "relaxed", "calm"},
    "calm": {"relaxed", "serene", "chill"},
    "playful": {"happy", "upbeat", "energetic"},
    "upbeat": {"happy", "energetic", "playful"},
}

WEIGHTS = {
    "genre": 0.15,
    "mood": 0.25,
    "energy": 0.40,
    "valence": 0.10,
    "tempo": 0.05,
    "dance": 0.05,
    "acoustic": 0.05,
}


def _get_first_value(source, *keys):
    """Return the first matching value from a dict or object by trying each key in order."""
    for key in keys:
        if isinstance(source, dict) and key in source:
            return source[key]
        if not isinstance(source, dict) and hasattr(source, key):
            return getattr(source, key)
    return None


def _to_float(value, default: float = 0.0) -> float:
    """Safely convert a value to float, returning default if conversion fails."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _match_score(value, target, related_map):
    """Return a (score, reason) tuple for exact, related, or no match against a target value."""
    if value == target:
        return 1.0, "exact match"
    if target in related_map and value in related_map[target]:
        return 0.5, "related match"
    return 0.0, "no match"


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against a user preference profile and return reasons."""
    user_genre = _get_first_value(user_prefs, "genre", "favorite_genre")
    user_mood = _get_first_value(user_prefs, "mood", "favorite_mood")
    user_energy = _to_float(_get_first_value(user_prefs, "energy", "target_energy"))
    user_valence = _to_float(_get_first_value(user_prefs, "valence", "target_valence"))
    user_tempo = max(MIN_TEMPO, min(MAX_TEMPO, _to_float(_get_first_value(user_prefs, "tempo", "target_tempo"))))
    user_dance = _to_float(_get_first_value(user_prefs, "dance", "target_dance", "target_danceability"))
    user_acoustic = _to_float(_get_first_value(user_prefs, "acoustic", "target_acoustic"))

    song_genre = _get_first_value(song, "genre")
    song_mood = _get_first_value(song, "mood")
    song_energy = _to_float(_get_first_value(song, "energy"))
    song_valence = _to_float(_get_first_value(song, "valence"))
    song_tempo = _to_float(_get_first_value(song, "tempo_bpm"))
    song_dance = _to_float(_get_first_value(song, "danceability"))
    song_acoustic = _to_float(_get_first_value(song, "acousticness"))

    reasons: List[str] = []
    total_score = 0.0

    genre_score, genre_reason = _match_score(song_genre, user_genre, RELATED_GENRES)
    genre_contribution = genre_score * WEIGHTS["genre"]
    total_score += genre_contribution
    reasons.append(f"genre {genre_reason} (+{genre_contribution:.2f})")

    mood_score, mood_reason = _match_score(song_mood, user_mood, RELATED_MOODS)
    mood_contribution = mood_score * WEIGHTS["mood"]
    total_score += mood_contribution
    reasons.append(f"mood {mood_reason} (+{mood_contribution:.2f})")

    energy_score = max(0.0, 1.0 - abs(song_energy - user_energy))
    energy_contribution = energy_score * WEIGHTS["energy"]
    total_score += energy_contribution
    reasons.append(f"energy closeness (+{energy_contribution:.2f})")

    valence_score = max(0.0, 1.0 - abs(song_valence - user_valence))
    valence_contribution = valence_score * WEIGHTS["valence"]
    total_score += valence_contribution
    reasons.append(f"valence closeness (+{valence_contribution:.2f})")

    tempo_score = max(0.0, 1.0 - abs(song_tempo - user_tempo) / TEMPO_RANGE)
    tempo_contribution = tempo_score * WEIGHTS["tempo"]
    total_score += tempo_contribution
    reasons.append(f"tempo closeness (+{tempo_contribution:.2f})")

    dance_score = max(0.0, 1.0 - abs(song_dance - user_dance))
    dance_contribution = dance_score * WEIGHTS["dance"]
    total_score += dance_contribution
    reasons.append(f"danceability closeness (+{dance_contribution:.2f})")

    acoustic_score = max(0.0, 1.0 - abs(song_acoustic - user_acoustic))
    acoustic_contribution = acoustic_score * WEIGHTS["acoustic"]
    total_score += acoustic_contribution
    reasons.append(f"acousticness closeness (+{acoustic_contribution:.2f})")

    return round(total_score, 4), reasons


def _novelty_distance(user_prefs: Dict, song: Dict) -> float:
    """Compute a novelty distance score measuring how different a song is from the user's preferences."""
    song_genre = _get_first_value(song, "genre")
    song_mood = _get_first_value(song, "mood")
    song_energy = _to_float(_get_first_value(song, "energy"))
    song_valence = _to_float(_get_first_value(song, "valence"))
    song_tempo = _to_float(_get_first_value(song, "tempo_bpm"))
    song_dance = _to_float(_get_first_value(song, "danceability"))
    song_acoustic = _to_float(_get_first_value(song, "acousticness"))

    user_genre = _get_first_value(user_prefs, "genre", "favorite_genre")
    user_mood = _get_first_value(user_prefs, "mood", "favorite_mood")
    target_energy = _to_float(_get_first_value(user_prefs, "energy", "target_energy"))
    target_valence = _to_float(_get_first_value(user_prefs, "valence", "target_valence"))
    target_tempo = max(MIN_TEMPO, min(MAX_TEMPO, _to_float(_get_first_value(user_prefs, "tempo", "target_tempo"))))
    target_dance = _to_float(_get_first_value(user_prefs, "dance", "target_dance", "target_danceability"))
    target_acoustic = _to_float(_get_first_value(user_prefs, "acoustic", "target_acoustic"))

    genre_distance = 0.0 if song_genre == user_genre else 1.0
    mood_distance = 0.0 if song_mood == user_mood else 1.0
    tempo_distance = abs(song_tempo - target_tempo) / TEMPO_RANGE

    return (
        genre_distance
        + mood_distance
        + abs(song_energy - target_energy)
        + abs(song_valence - target_valence)
        + tempo_distance
        + abs(song_dance - target_dance)
        + abs(song_acoustic - target_acoustic)
    )


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    unique_songs: List[Dict] = []
    seen_ids = set()
    seen_keys = set()

    for song in songs:
        song_id = song.get("id")
        if song_id is not None:
            if song_id in seen_ids:
                continue
            seen_ids.add(song_id)
        else:
            unique_key = (song.get("title"), song.get("artist"))
            if unique_key in seen_keys:
                continue
            seen_keys.add(unique_key)

        unique_songs.append(song)

    scored_songs = []
    for song in unique_songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        novelty = _novelty_distance(user_prefs, song)
        scored_songs.append((song, score, novelty, explanation))

    scored_songs.sort(key=lambda item: (-item[1], item[2]))

    return [(song, score, explanation) for song, score, _, explanation in scored_songs[:k]]
