from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import click
from faker import Faker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:926472@localhost:3306/movie'
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
    # 检查是否已经存在数据
    if User.query.first() or Movie.query.first():
        return

    # 添加用户
    user = User(name='Grey Li')
    db.session.add(user)

    # 添加电影
    movies = [
        Movie(title='Leon', year='1994'),
        Movie(title='Mahjong', year='1996'),
    ]
    db.session.add_all(movies)

    db.session.commit()

# 示例数据
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 初始化数据
    init_data()

    # 使用 Faker 生成假数据
    fake = Faker()
    name = fake.name()
    movies = [{'title': fake.sentence(nb_words=3), 'year': fake.year()} for _ in range(10)]

    # 插入用户
    user = User(name=name)
    db.session.add(user)

    # 插入电影
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    # 提交事务
    try:
        db.session.commit()
        click.echo('Done.')
    except Exception as e:
        db.session.rollback()
        click.echo(f'Error: {e}')

# 根路由
@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)

# 404 错误处理
@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html', user=user), 404

# 添加电影的路由
@app.route('/add')
def add_movie():
    movie = Movie(title='New Movie', year='2023')
    db.session.add(movie)
    db.session.commit()
    return 'Movie added!'

if __name__ == '__main__':
    app.run()