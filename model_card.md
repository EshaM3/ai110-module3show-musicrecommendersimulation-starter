# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MyAlgoRhythm**  

---

## 2. Intended Use  

Input your favorite genre, song mood, and average song bpm/tempo. And try to determine percentage scores for your preferred energy, valence, acousticness, and danceability in a song. This program will attempt to give you the most curated song recommendations list. This can be for any purpose, whether you are recommending a friend or creating a playlist for a party.

---

## 3. How the Model Works  

There is a CSV of songs with all of their determined scores and data. Given the user's inputted data, the model will go through the song list, assign each a match score based on the user-given data (some categories are more important than others in determining this score), prune through any duplicate songs, and rank them all based on score. Ties are broken based on higher novelty, so that the list will have as much variety as possible. This ranked list will then be displayed to you as a truncated list of top 5 songs.

---

## 4. Data  

There are 17 songs in the catalog with about 14 genres. Each has a title, artist, genre, mood, tempo (bpm), energy score, valence score, danceability score, and acousticness score.

---

## 5. Strengths  

When the genre and mood are a common match (like rock/intense or pop/happy) at least the top result will be pretty relevant given the current weightages. The output is good at showing scores and breaking down how the scores was calculated. Duplicates are not included, and novelty tie-breakers help provide more diverse results.

---

## 6. Limitations and Bias   

In an experiment, I set the genre weightage to be half of what it used to be, so it is now 0.15. And I doubled the weightage of energy, so it is now 0.40. This creates an obvious bias since a more general metric (energy) is taking precedence over a more specific metric (genre). This issue is also compounded with the fact that the dataset is quite small and skewed with more lofi and lofi-adjacent tracks than rock and rock-adjacent tracks. If a user wants low-energy rock music, they may find more lofi tracks being recommended to them than any rock tracks since all the lofi tracks have low energy scores, which are prioritized.

---

## 7. Evaluation   

Initially, my weightage for genre was 0.30 and my weightage for energy was 0.20...

I tested users with preferences for the following genres/moods: rock/intense, pop/playful/, reggae/relaxed, and pop/happy. Initially, the results showed decently relevant tracks (even if less relevant tracks showed later in the list, they were still scored low. And this came more from a lack of dataset coverage). 

After adjusting the weightages to make energy 0.40 and genre 0.15, the track recommendations became slightly off kilter (only slightly because the mood weightage was still 0.25 and the user test examples had more common genre/mood combinations. So, the mood score was able to offset the bias a bit). But when I tested a user who liked the rock genre, liked a chill mood, and preferred low energy (0.1), which could be valid for more lowkey rock music, all of the results were lofi or lofi-adjacent tracks with decently high match scores (in the 0.70s).

---

## 8. Future Work   

In the future I would want to:
- Make the data set much larger and filled with a balance list of various genres.
- Switch back the weightages to give most importance to genre, less to energy. 
- Find a way to gather user data without them just manually inputting. Manual input can be optional instead
- Find a way to gather song data from wider databases
- Add followed artists to user profile data
- Make curated playlists that combine a user data score and content score for the playlist
- Add frontend so that this can run as an app on streamlit

---

## 9. Personal Reflection  

It was very interesting to see and write out how the scoring and ranking process works. It helps me see better how all that spotify data is processed to make things like their annual "Spotify Wrapped." I also now finally understand what exactly 'valence' and 'acousticness' both mean (I would see those terms in a Spotify-related app called Stats.fm and would always wonder what they meant).
