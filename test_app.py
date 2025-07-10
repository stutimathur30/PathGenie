from flask import Flask, session

app = Flask(__name__)
app.secret_key = "your_random_secret_key_here"  # Required for sessions

@app.route('/')
def home():
    session['test'] = 'working'  # Force a session cookie
    return "Check your cookies now!"

if __name__ == '__main__':
    app.run(debug=True)