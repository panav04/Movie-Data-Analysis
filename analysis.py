# =========================================
# MOVIE DATA ANALYSIS ASSIGNMENT
# =========================================

import pandas as pd
import ast
from collections import Counter

# =========================================
# LOAD SMALL DATASET
# =========================================

df = pd.read_csv("imdb_small.csv", encoding='utf-8', on_bad_lines='skip')

print("Dataset Loaded Successfully!\n")

# =========================================
# DATA CLEANING
# =========================================

df = df.drop_duplicates()

# Convert numeric columns
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')

# Remove null & invalid values
df = df.dropna(subset=['budget', 'revenue'])
df = df[df['budget'] > 0]

# =========================================
# CREATE NEW COLUMNS
# =========================================

df['profit'] = df['revenue'] - df['budget']
df['ROI'] = df['profit'] / df['budget']

# =========================================
# EXTRACT ACTORS & DIRECTOR
# =========================================

def get_actors(x):
    try:
        data = ast.literal_eval(x)
        return [i['name'] for i in data[:3]]
    except:
        return []

def get_director(x):
    try:
        data = ast.literal_eval(x)
        for i in data:
            if i['job'] == 'Director':
                return i['name']
    except:
        return None

df['actors'] = df['cast'].apply(get_actors)
df['director'] = df['crew'].apply(get_director)

# =========================================
# QUESTION 1: HIGHEST PROFIT MOVIE
# =========================================

max_profit_movie = df.loc[df['profit'].idxmax()]

print("\n===== QUESTION 1 =====")
print(max_profit_movie[['title', 'profit', 'director', 'actors']])

# =========================================
# QUESTION 2: LANGUAGE WITH HIGHEST ROI
# =========================================

language_roi = df.groupby('original_language')['ROI'].mean().sort_values(ascending=False)

print("\n===== QUESTION 2 =====")
print(language_roi.head())

# =========================================
# QUESTION 3: UNIQUE GENRES
# =========================================

def get_genres(x):
    try:
        data = ast.literal_eval(x)
        return [i['name'] for i in data]
    except:
        return []

df['genres_list'] = df['genres'].apply(get_genres)

all_genres = set()
for g in df['genres_list']:
    all_genres.update(g)

print("\n===== QUESTION 3 =====")
print(all_genres)

# =========================================
# QUESTION 4: TOP PRODUCERS BY ROI
# =========================================

def get_producers(x):
    try:
        data = ast.literal_eval(x)
        return [i['name'] for i in data]
    except:
        return []

df['producers'] = df['production_companies'].apply(get_producers)

# explode producers
df_exploded = df.explode('producers')

producer_roi = df_exploded.groupby('producers')['ROI'].mean().sort_values(ascending=False)

print("\n===== QUESTION 4 =====")
print("Top 3 Producers by Average ROI:")
print(producer_roi.head(3))

# =========================================
# QUESTION 5: ACTOR WITH MOST MOVIES
# =========================================

actor_list = []
for actors in df['actors']:
    actor_list.extend(actors)

actor_count = Counter(actor_list)
top_actor = actor_count.most_common(1)[0][0]

print("\n===== QUESTION 5 =====")
print("Actor with Most Movies:", top_actor)

actor_movies = df[df['actors'].apply(lambda x: top_actor in x)]

print("\nMovies of this actor:")
print(actor_movies[['title', 'genres_list', 'profit']])

# =========================================
# QUESTION 6: TOP DIRECTORS & FAVORITE ACTORS
# =========================================

top_directors = df['director'].value_counts().head(3).index

print("\n===== QUESTION 6 =====")

for director in top_directors:
    movies = df[df['director'] == director]
    
    actors = []
    for a in movies['actors']:
        actors.extend(a)
    
    fav_actor = Counter(actors).most_common(1)
    
    print(f"\nDirector: {director}")
    print(f"Favorite Actor: {fav_actor}")