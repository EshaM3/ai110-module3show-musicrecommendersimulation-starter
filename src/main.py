"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {"favorite_genre": "rock", "favorite_mood": "intense", "target_energy": 0.7,
                  "target_valence": 0.38, "target_tempo": 110, "target_dance": 0.20, 
                  "target_acoustic": 0.4}

    #     user_prefs = {
    #     "favorite_genre": "pop",
    #     "favorite_mood": "playful",   # ← "playful" is a VALUE in RELATED_MOODS but not a KEY
    #     "target_energy": 0.8, "target_valence": 0.8,
    #     "target_tempo": 120, "target_dance": 0.8, "target_acoustic": 0.2
    # }

    # user_prefs = {
    # "favorite_genre": "reggae",   # ← in songs.csv but NOT a key in RELATED_GENRES
    # "favorite_mood": "relaxed",
    # "target_energy": 0.6, "target_valence": 0.7,
    # "target_tempo": 96, "target_dance": 0.7, "target_acoustic": 0.5
    # }

    # user_prefs = {
    # "favorite_genre": "pop",
    # "favorite_mood": "happy",
    # "target_energy": 0.8, "target_valence": 0.8,
    # "target_tempo": 120, "target_dance": 0.9,   # ← the key used by main.py
    # "target_acoustic": 0.1
    # }



    recommendations = recommend_songs(user_prefs, songs, k=5)

    divider = "-" * 50
    print(f"\n{'=' * 50}")
    print(f"  Top {len(recommendations)} Recommendations")
    print(f"{'=' * 50}")

    for i, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        reasons = explanation.split("; ")

        print(f"\n  #{i}  {song['title']} - {song['artist']}")
        print(f"       Score: {score:.4f}")
        print(f"  {divider}")
        for reason in reasons:
            print(f"    * {reason}")

    print(f"\n{'=' * 50}\n")


if __name__ == "__main__":
    main()
