from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import os
import markdown
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Flask-Login 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 사용자 클래스 (단일 관리자 계정용)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    def get_id(self):
        return self.id

# 관리자 계정 정보 (ID: admin / PW: admin123)
ADMIN_ID = 'admin'
ADMIN_PASSWORD = 'admin123'

@login_manager.user_loader
def load_user(user_id):
    if user_id == ADMIN_ID:
        return User(user_id)
    return None

POSTS_DIR = 'posts'

def parse_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    meta_match = re.match(r'^---\n(.*?)\n---\n\n(.*)', content, re.DOTALL)
    title, tags, body = '제목 없음', '', content

    if meta_match:
        meta_block, body = meta_match.groups()
        for line in meta_block.split('\n'):
            if line.startswith('title:'):
                title = line[6:].strip()
            elif line.startswith('tags:'):
                tags = line[5:].strip()
    
    return title, tags, body

@app.route('/')
def index():
    posts = []
    for filename in os.listdir(POSTS_DIR):
        if filename.endswith('.md'):
            filepath = os.path.join(POSTS_DIR, filename)
            title, tags, _ = parse_post(filepath)
            posts.append({'filename': filename, 'title': title, 'tags': tags})
    posts.sort(key=lambda x: x['filename'], reverse=True)
    return render_template('index.html', posts=posts)

@app.route('/post/<filename>')
def view_post(filename):
    filepath = os.path.join(POSTS_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)
    _, _, body = parse_post(filepath)
    html_content = markdown.markdown(body)
    return render_template('view_post.html', content=html_content)

@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        filename = request.form['filename'].strip()
        title = request.form['title'].strip()
        tags = request.form['tags'].strip()
        content = request.form['content'].strip()

        if not filename.endswith('.md'):
            filename += '.md'

        filepath = os.path.join(POSTS_DIR, filename)
        if os.path.exists(filepath):
            flash('이미 같은 이름의 파일이 존재합니다.')
            return redirect(url_for('new_post'))

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"title: {title}\n")
            f.write(f"tags: {tags}\n")
            f.write(f"---\n\n")
            f.write(content)

        return redirect(url_for('index'))

    return render_template('edit_post.html', filename=None)

@app.route('/edit/<filename>', methods=['GET', 'POST'])
@login_required
def edit_post(filename):
    filepath = os.path.join(POSTS_DIR, filename)
    if not os.path.exists(filepath):
        abort(404)

    if request.method == 'POST':
        title = request.form['title'].strip()
        tags = request.form['tags'].strip()
        content = request.form['content'].strip()

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"title: {title}\n")
            f.write(f"tags: {tags}\n")
            f.write(f"---\n\n")
            f.write(content)

        return redirect(url_for('index'))

    title, tags, content = parse_post(filepath)
    return render_template('edit_post.html', filename=filename, title=title, tags=tags, content=content)

@app.route('/delete/<filename>', methods=['POST'])
@login_required
def delete_post(filename):
    filepath = os.path.join(POSTS_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['username']
        password = request.form['password']
        if userid == ADMIN_ID and password == ADMIN_PASSWORD:
            login_user(User(userid))
            return redirect(url_for('index'))
        else:
            flash('잘못된 사용자 이름 또는 비밀번호입니다.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(POSTS_DIR, exist_ok=True)
    app.run(debug=True)