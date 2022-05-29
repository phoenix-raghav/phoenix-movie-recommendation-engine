import helper
from flask import Flask, redirect, render_template, request,redirect
import requests
import json
from datetime import datetime

app = Flask(__name__)
# Getting data of helper file in df
df=helper.new_df

# Creating Object to store movie watched by user and time played
class User_action:
    def __init__(self, user_title, timing):
        self.user_title =user_title
        self.timing=timing

class merge_name_add_time:
    def __init__(self, name, add,time):
        self.name =name
        self.add=add
        self.time=time

class merge_comedy_action_recommend:
    def __init__(self,C,A,recom):
        self.comedy=C
        self.action=A
        self.recom=recom

class merge_n_a_gen_cast_crew:
    def __init__(self, name, add, genres, cast, crew):
        self.name =name
        self.add=add
        self.genres=genres
        self.cast=cast
        self.crew=crew

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=75206f90526fab7c1e8e39044b7098d6&language=en-US'
                 .format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Gives list of movies acc. to category
def titles(category):
    tit_names = []
    tit_img=[]
    counter=0
    for text in df['tags']:
        if category in text:
            if counter != 10:
                tit_names.append(df['title'][df[df['tags']==text].index[0]])
                tit_img.append(df['movie_id'][df[df['tags']==text].index[0]])
                counter = counter +1
            else:
                break    
    return tit_names,tit_img       

# Function which give recommended movies based on latest viewed movies
def get_recommended_movies(c):
    gr_list = []
    while(c<3):
        gr_titles,gr_mov_idx=helper.recommend(latest_viewed_movies[c].user_title,recommended_movies)
        for i,j in zip(gr_titles,gr_mov_idx):
            gr_list.append(merge_name_add_time(i, fetch_poster(j),latest_viewed_movies[c].timing))
        c = c + 1    
    return gr_list


def category_list(category):
    cl_names,cl_img = titles(category)
    List=[]
    for i,j in zip(cl_names,cl_img):
        List.append(merge_name_add_time(i, fetch_poster(j),0))
    return List   


def get_idx(m):
    return df[df['title']==m].index[0]
def get_id(idx):
    return df['movie_id'][idx] 
def get_genres(idx):
    return df['genres'][idx]
def get_cast(idx):
    return df['cast'][idx]
def get_director(idx):
    p=df['crew'][idx]
    return p

# latest_viewed_movies--> stores recent 3 movies watch by user
latest_viewed_movies = []
recommended_movies = []

# By default values
latest_viewed_movies.append(User_action("AVATAR",0))
latest_viewed_movies.append(User_action("TANGLED",0))
latest_viewed_movies.append(User_action("BATMAN",0))

comedy_list=category_list('comedi')
action_list=category_list('action')

list=get_recommended_movies(0)
for i in list:
    recommended_movies.append(i)

@app.route("/", methods=['GET','POST'])
def home():
    if request.method=='POST':
        output=request.get_json()
        result=json.loads(output)
        x=result["name"]
        y=round(result["totalTime"])

        # Replacing smallest played movie
        if len(latest_viewed_movies)==3:
            latest_viewed_movies.pop(2)
        obj=User_action(x,y)
        latest_viewed_movies.append(obj)

        # Replacing last 3 recommendations
        list=get_recommended_movies(2)
        for i in list:
            recommended_movies.append(i)
        recommended_movies.pop(8)
        recommended_movies.pop(7)
        recommended_movies.pop(6)

        # Sort the recommended movies according to time played (Screen time recording)
        recommended_movies.sort(key=lambda x: x.time, reverse=True)
        obj_recom = merge_comedy_action_recommend(comedy_list,action_list,recommended_movies)
        return render_template('index.html', obj_recom=obj_recom)
        
    else:
        obj_recom = merge_comedy_action_recommend(comedy_list,action_list,recommended_movies)
        return render_template('index.html', obj_recom=obj_recom)
 
@app.route("/movie/<string:movie>", methods=['GET','POST'])
def movie(movie):
    movie=movie.upper()

    # If movie not found in database
    if helper.recommend(movie,recommended_movies)==-1:
        movie="NotFound"
        obj= merge_n_a_gen_cast_crew(movie,"","","","") 
        return render_template('movie.html',obj=obj)

    else:
        idx=get_idx(movie)
        print(get_director(idx))
        obj= merge_n_a_gen_cast_crew(movie,fetch_poster(get_id(idx)),get_genres(idx),get_cast(idx),get_director(idx))  
        return render_template('movie.html',obj=obj)  
    
if __name__=='__main__':
    app.run(debug=True, port=8000)       