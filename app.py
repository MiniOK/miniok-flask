from flask import Flask, render_template, request, redirect, url_for, session
import config
from models import User,Question
from exts import db
from decorator import login_required

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)




# 首页
@app.route('/')
def index():
    context = {
        "questions": Question.query.all()
    }

    return render_template('index.html', **context)

# 登录
@app.route('/login/', methods=['GET', "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get("password")
        user = User.query.filter(
            User.telephone == telephone,
            User.password == password).first()
        if user:
            session['user_id'] = user.id
            # 如果你要在31天内登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"手机号码或密码错误！"

# 注册
@app.route('/register/', methods=['GET', "POST"])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证， 如果过被注册了， 就不能在注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u"该手机号码已经被注册过，请更换手机号码！"
        else:
            # password1 与 password2 相同才可以
            if password1 != password2:
                return u"两次密码不相同，请核对后再填写！"
            else:
                print("hello")
                user = User(
                    telephone=telephone,
                    username=username,
                    password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果用户注册成功，就让页面跳转到登录页面
                return redirect(url_for('login'))

# 注销
@app.route("/logout/")
def logout():
    # 清除session的三种方式
    # session.pop("user_id")
    # del session["user_id"]
    session.clear()
    return redirect(url_for('login'))

# 发布问答
@app.route("/question/", methods=["GET", "POST"])
@login_required  # 对发布问答进行访问限制
def question():
    if request.method == 'GET':
        return render_template("question.html")
    else:
        title = request.form.get('title')
        context = request.form.get('content')
        question = Question(title = title, context = context)
        user_id = session.get("user_id")
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))



# 上下文处理器（钩子函数）
@app.context_processor
def my_context_processor():
    user_id = session.get("user_id")
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()
