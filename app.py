from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/', methods=['POST'])
def add_config():
    data = request.form
    word_type = data.get('word-type', '')
    content = data.get('content', '')
    reply_type = data.get('reply-type', '')
    reply_content = data.get('reply-content', '')
    print(reply_content)
    with open('content.txt', 'a', encoding='utf-8') as f:
        content_to_write = '\n' + ','.join([content,word_type, reply_type, reply_content, '', '', '0'])
        # print(content_to_write)
        f.write(content_to_write)
    
    return 'OK'