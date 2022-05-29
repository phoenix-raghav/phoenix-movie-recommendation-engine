# phoenix-movie-recommendation-engine

## Made by Raghav Agarwal

This is a movie recommendation engine which acts like Netflix and Spotify

Github Link : https://github.com/phoenix-raghav/phoenix-movie-recommendation-engine

The Recommender System recommends the movies based on the latest 3 movies watched by user and sort the recommended movies on the basis of time spent by user on watching the movie.
Let's take an example: 
If user watched Toy Story : 30 minutes
                Spider-man : 2 hrs and
                Titanic: 1hr
then recommended movies will be according to: Spider-Man, Titanic, Toy Story
If user searches for any movie he lands on a page displaying information related to that movie
Also if movie not found then "Not found" message will occur

## How to run the project?

OPTION 1:
1. Clone or download this repository to your local machine.
2. Open your terminal/command prompt from your project directory and install all the libraries mentioned in the [requirements.txt] executing the command
   `pip install -r requirements.txt` (if OS ERROR occurs try using `pip install --user -r requirements.txt`)
    (May be intalling collected packages takes time at last)
3. In the same terminal/command prompt from your project directory run the file `app.py` by executing the command `python .\app.py`.
4. Wait for sometime you will get the link. 
5. Click on the link `http://127.0.0.1:8000/`.
6. Page is loading.
7. Hurray! That's it.

OPTION 2:
1. Clone or download this repository to your local machine.
2. Open the folder in VSCode, you get some dialog box relating to Pylance just close it or click output till it disappears (it will disappear definitely) 
3. Open the terminal, install all the libraries mentioned in the [requirements.txt] file with the command `pip install -r requirements.txt` .
4. Intalling collected packages takes time at last.
5. In the terminal of VSCode run the file `app.py` by executing the command `(python .\app.py)`.
6. Wait for sometime you will get the link.
7. Click on the link `http://127.0.0.1:8000/`.
8. Page is loading.
9. Hurray! That's it.
                                     
## How the application searches the most similar movies to the item watched by user?
   Firstly, a vectorization process starts where every movie gets plotted on a coordinate system based on text details.
   Now when an item(movie watched by user) is passed to the function it calculates the similarity using cosine similarity technique (discussed below) which gives value    0 to 1 for every movie with that item.
   Now sorting technique is used to get the most similar movie (value closed to 1) hence these top similar movies are recommended.
   
## How Cosine similarity works?
  Cosine similarity is a technique used to measure the similarity between 2 documents. It is the cosine of the angle between 2 vectors (like in mathematics) hence it     gives more accurate results than measuring Euclidean distances between movies. As angle decreases similarity increases.

