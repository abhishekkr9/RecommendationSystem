from flask import Flask, render_template, request
import pickle
import spacy
nlp = spacy.load('en_core_web_md')

app = Flask(__name__)

new_df = pickle.load(open('movie.pkl', 'rb'))

def recommend_movies(movie):
    movie_doc = nlp(movie.lower())
    new_df['similarity'] = new_df['tags'].apply(lambda x: movie_doc.similarity(nlp(x)))
    top_movies = new_df.sort_values('similarity', ascending=False)['title'][:5].tolist()
    return top_movies

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_movie', methods=['GET','POST'])
def recommend():
    userInput = request.form.get('user_input')
    return render_template('recommend.html', data=recommend_movies(userInput))

if __name__ == '__main__':
    app.run(debug=True)