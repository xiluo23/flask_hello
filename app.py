from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:926472@localhost:3306/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return f'<User {self.name}>'

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    year = db.Column(db.String(4))  # 改为 String 类型

    def __repr__(self):
        return f'<Movie {self.title} ({self.year})>'

# 初始化数据
def init_data():
    # 添加用户
    user = User(id=1, name='Grey Li')
    db.session.add(user)

    # 添加电影
    movies = [
        Movie(id=1, title='Leon', year='1994'),
        Movie(id=2, title='Mahjong', year='1996'),
    ]
    db.session.add_all(movies)

    db.session.commit()

# 示例数据
name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

# 根路由
@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)

# 添加电影的路由
@app.route('/add')
def add_movie():
    movie = Movie(title='New Movie', year='2023')
    db.session.add(movie)
    db.session.commit()
    return 'Movie added!'

# 404 错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)