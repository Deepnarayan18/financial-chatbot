import wikipedia
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
chatbot = None

class FinancialChatbot:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def fetch_wikipedia_summary(self, query):
        try:
            summary = wikipedia.summary(query, sentences=3)
            return summary
        except wikipedia.DisambiguationError as e:
            return f"Your query is ambiguous. Possible options include: {e.options}"
        except wikipedia.PageError:
            return "I'm sorry, I couldn't find information on that topic."
        except Exception as e:
            return f"An error occurred: {e}"

    def process_query(self, query):
        words = word_tokenize(query.lower())
        filtered_words = [word for word in words if word.isalnum() and word not in self.stop_words]
        return ' '.join(filtered_words)

    def respond(self, user_input):
        processed_query = self.process_query(user_input)
        response = self.fetch_wikipedia_summary(processed_query)
        return response

# Initialize the chatbot instance
chatbot = FinancialChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.form['user_input']
    response = chatbot.respond(user_message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
