from flask import Flask, render_template, request
from newspaper import Article
from urllib.parse import urlparse
from googletrans import Translator

app = Flask(__name__, template_folder='.')
translator = Translator()

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def extract_content(url, target_language='hi'):
    article = Article(url)
    article.download()
    article.parse()
    title = translator.translate(article.title, dest=target_language).text
    content = translator.translate(article.text, dest=target_language).text
    return title, content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        is_url = is_valid_url(text)
        extracted_title = None
        extracted_content = None
        if is_url:
            extracted_title, extracted_content = extract_content(text)
        return render_template('index.html', text=text, is_url=is_url, extracted_title=extracted_title, extracted_content=extracted_content)
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
