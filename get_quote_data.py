from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Welcome'

@app.route('/quote_data')
def api_articles():
    return 'List of ' + url_for('api_articles')

@app.route('/quote_data/<symbol>')
def api_article(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    app.run()