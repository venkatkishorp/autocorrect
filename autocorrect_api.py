from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import textdistance
import pandas as pd

app = Flask(__name__)
# CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/health_check", methods=['GET'])
def health_check():
    return jsonify({
        'result': 'API up and running!'
    })

@app.route("/autocorrect", methods=['GET'])
def autocorrect():
    word = request.args.get('word')

    [word_prob, unique_word_list, word_freq] = pickle.load(open('autocorrect-pickle.pkl', 'rb'))
    result = ''

    if word in unique_word_list:
        result = 'The entered word is correct'
    else:
        correct_words = []
        
        unique_wrds = list(word_freq.keys())
        
        # This loop creates a multidimensional list with the word, its probability and its distance from the 
        # original word typed by the user calculated by the textdistance library
        for i in range(len(unique_wrds)):
            correct_words.append([unique_wrds[i], word_prob[unique_wrds[i]], 1 - (textdistance.Jaccard(qval=2).distance(unique_wrds[i], word))])
            
        correct_words_df = pd.DataFrame(correct_words, columns = ['Words', 'Word Probability', 'Word Distance'])
        
        # Formed a dataframe to sort it so as to find the most matched word
        correct_words_df = correct_words_df.sort_values(by = ['Word Distance', 'Word Probability'], ascending=False)
        
        result = ','.join(correct_words_df.head(3)['Words'].tolist())

    return jsonify({
            'result': result
        })