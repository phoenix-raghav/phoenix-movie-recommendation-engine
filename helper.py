import ast
from importlib import find_loader
import sklearn
import pandas as pd
import numpy as np
import random
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
pd.options.mode.chained_assignment = None

# Reading data from csv file
movies=pd.read_csv('data.csv')
movies.dropna(inplace=True)
new_df=movies[['movie_id', 'title', 'genres', 'cast', 'crew', 'tags']]

# Code: Preprocessing the data for the model
# I had already preprocessed it and make a new file data.csv to avoid preprocessing time

    # movies = pd.read_csv('tmdb_5000_movies.csv')
    # credits = pd.read_csv('tmdb_5000_credits.csv')
    # movies=pd.merge(movies, credits, on='title', how='inner')
    # movies=movies[['movie_id', 'title', 'overview', 'genres', 'keywords', 'cast', 'crew']]
    # movies.dropna(inplace=True)

    # To get name from lists
    # def convert(obj):
    #     L = []
    #     for i in ast.literal_eval((obj)):
    #         L.append(i['name'])
    #     return L;

    # Top 3 casts
    # def top_three(obj):
    #     L = []
    #     counter=0;
    #     for i in ast.literal_eval((obj)):
    #         if counter!=3:
    #             L.append(i['name'])
    #             counter = counter + 1
    #         else:
    #             break
    #     return L;

    # To get the director:
    # def director(obj):
    #     L = []
    #     for i in ast.literal_eval((obj)):
    #         if i['job'] == 'Director':
    #             L.append(i['name'])
    #             break
    #     return L;

    # movies['genres']=movies['genres'].apply(convert)
    # movies['keywords']=movies['keywords'].apply(convert)
    # movies['cast']=movies['cast'].apply(top_three)
    # movies['crew']=movies['crew'].apply(director)

    # Replacing spaces in between words so to get a single word
    # movies['genres']=movies['genres'].apply(lambda x: [i.replace(" ","") for i in x])
    # movies['keywords']=movies['keywords'].apply(lambda x: [i.replace(" ","") for i in x])
    # movies['cast']=movies['cast'].apply(lambda x: [i.replace(" ","") for i in x])
    # movies['crew']=movies['crew'].apply(lambda x: [i.replace(" ","") for i in x])

    # movies['overview']=movies['overview'].apply(lambda x: x.split())

    # Adding overview,keywords,cast and crew in tags
    # movies['tags']=movies['overview']+movies['keywords']+movies['cast']+movies['crew']
    # movies['tags']=movies['tags'].apply(lambda x: " ".join(x))

    # movies['tags']=movies['tags'].apply(lambda x: x.lower())
    # movies['title']=movies['title'].apply(lambda x: x.upper())

    # new_df=movies[['movie_id', 'title', 'tags']]
    # Here also addded 3 more fields

# Function to get root of a word ("comedy-->comedi")
ps=PorterStemmer()
def stem(text):
    y = []
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

# Vectorization using Bag of words technique
cv=CountVectorizer(max_features=5000, stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()

#Getting distances(in this case getting angles of each movie with others to get accurate results) 
similarity = cosine_similarity(vectors)

# Give nearest neighbours(movies)
# movie --> whose nearest neighbours are to be find_loader
# recommended_movies --> previous recommended movies (see use below)
def recommend(movie,recommended_movies):
    if movie not in new_df['title'].unique():
        return -1

    movie_index = new_df[new_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True, key=lambda x: x[1])
    
    # If movie which we are gonna pass is already present in recommended movies list then ignore it
    counter=0
    x=1
    new_movie_list=[]
    names_list=[]
    for i in recommended_movies:
        names_list.append(i.name)
    while counter<3:
        if new_df['title'][movies_list[x][0]] in names_list:
            x = x + 1
        else:    
            new_movie_list.append(movies_list[x])
            counter = counter + 1
            x = x + 1

    recommended_titles = []
    recommended_movie_id = []
    for i in new_movie_list:
        recommended_titles.append(new_df['title'][i[0]])
        recommended_movie_id.append((new_df['movie_id'][i[0]]))
    return recommended_titles,recommended_movie_id