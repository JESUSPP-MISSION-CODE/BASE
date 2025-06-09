from flask import Flask, render_template, abort, request, redirect, url_for
import os
import markdown
import re

app = Flask(__name__)
POSTS_DIR = 'posts'

def get_markdown_files():
    files = [
        f for f in os.listdir(POSTS_DIR)
        if re.match(r'\d{8}\.md$', f)
    ]
    return sorted(files, reverse=True)

@app.route('/')
def index():
    posts = []
    for filename in get_markdown_files():
        filepath = os.path.join(POSTS_DIR, filename)
        date = filename[:-3]
        title, tags, _ = parse_post(filepath)
        posts.append({'date': date, 'title': title, 'tags': tags})
    return render_template('index.html', posts=posts)

@app.route('/post/<date>')
def show_post(date):
    filename = f"{date}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    if not os.path.exists(filepath):
        abort(404)

    title, tags, content = parse_post(filepath)
    html_content = markdown.markdown(content)
    return render_template('post.html', content=html_content, date=date, title=title, tags=tags)

@app.route('/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        date = request.form['date']
        title = request.form['title']
        tags = request.form['tags']
        content = request.form['content']
        
        if not re.match(r'^\d{8}$', date):
            return render_template('new.html', error="날짜 형식이 올바르지 않습니다.")
        
        filename = f"{date}.md"
        filepath = os.path.join(POSTS_DIR, filename)

        # 🔽 디렉토리 없으면 생성
        os.makedirs(POSTS_DIR, exist_ok=True)

        if os.path.exists(filepath):
            return render_template('new.html', error="이미 해당 날짜의 게시물이 존재합니다.")

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"---\ntitle: {title}\ntags: {tags}\n---\n\n{content}")
        except Exception as e:
            return render_template('new.html', error=f"파일 저장 실패: {e}")

        return redirect(url_for('show_post', date=date))

    return render_template('new.html', error=None)

@app.route('/edit/<date>', methods=['GET', 'POST'])
def edit_post(date):
    filepath = os.path.join(POSTS_DIR, f"{date}.md")
    if not os.path.exists(filepath):
        abort(404)

    if request.method == 'POST':
        title = request.form['title']
        tags = request.form['tags']
        content = request.form['content']

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: {title}\ntags: {tags}\n---\n\n{content}")
        return redirect(url_for('show_post', date=date))

    title, tags, content = parse_post(filepath)
    return render_template('edit.html', date=date, title=title, tags=', '.join(tags), content=content)

@app.route('/delete/<date>')
def delete_post(date):
    filename = f"{date}.md"
    filepath = os.path.join(POSTS_DIR, filename)

    if not os.path.exists(filepath):
        abort(404)

    os.remove(filepath)
    return redirect(url_for('index'))

def parse_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    title = "제목 없음"
    tags = []
    content_start = 0

    if lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                content_start = i + 1
                break
            if lines[i].startswith('title:'):
                title = lines[i].split(':', 1)[1].strip()
            elif lines[i].startswith('tags:'):
                tags = [tag.strip() for tag in lines[i].split(':', 1)[1].split(',')]

    content = ''.join(lines[content_start:])
    return title, tags, content

if __name__ == '__main__':
    app.run(debug=True)