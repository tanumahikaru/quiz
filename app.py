from flask import Flask, render_template, request, redirect , url_for, session
import db, string, random

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))

@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')
    
    if msg == None:
        return render_template('index.html')
    else:
        return render_template('index.html', msg = msg)
    
@app.route('/', methods=['POST'])
def login():
    user_name = request.form.get('username')
    password = request.form.get('password')
    
    if db.login(user_name, password):
        session['user'] = True #sessionにuserバリューにTrueを保存
        return redirect(url_for('mypage'))
    else:
        error = 'ログインに失敗しました。'
        input_data  = {
            'user_name': user_name,
            'password': password
        }
        return render_template('index.html', error = error, data = input_data)
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/mypage', methods=['GET'])
def mypage():
    if 'user' in session:
        return render_template('mypage.html')
    else:
        return redirect(url_for('index'))

@app.route('/register')
def register_form():
    return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
    user_name = request.form.get('username')
    mail = request.form.get('mail')
    password = request.form.get('password')
    
    if user_name == '':
        error = 'ユーザー名が未入力です。'
        return render_template('register.html', error = error)
    if password == '':
        error = 'パスワードが未入力です。'
        return render_template('register.html', error = error)
    if mail == '':
        error = 'メールが未入力です。'
        return render_template('register.html', error = error)
    
    count = db.insert_user(user_name, mail, password)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('index.html', msg=msg)
    else:
        error = '登録に失敗しました。'
    return render_template('register.html', error=error)

@app.route('/register_quiz_form')
def register_quiz_form():
    return render_template('register_quiz.html')


@app.route('/register_quiz', methods=['POST'])
def register_quiz():
    title = request.form.get('title')
    answer1 = request.form.get('answer1')
    answer2 = request.form.get('answer2')
    answer3 = request.form.get('answer3')
    answer4 = request.form.get('answer4')
    correctanswer = request.form.get('correctanswer')
    
    if title == '':
        error = '問題文が未入力です。'
        return render_template('register_quiz.html', error = error)
    if answer1 == '':
        error = '回答１が未入力です。'
        return render_template('register_quiz.html', error = error)
    if answer2 == '':
        error = '回答２が未入力です。'
        return render_template('register_quiz.html', error = error)
    if answer3 == '':
        error = '回答３が未入力です。'
        return render_template('register_quiz.html', error = error)
    if answer4 == '':
        error = '回答４が未入力です。'
        return render_template('register_quiz.html', error = error)
    if correctanswer == '':
        error = '正解が未入力です。'
        return render_template('register_quiz.html', error = error)
    
    count = db.insert_quiz(title, answer1, answer2, answer3, answer4, correctanswer)
    
    if count == 1:
        msg = '登録が完了しました。'
        return render_template('register_quiz.html', msg=msg)
    else:
        error = '登録に失敗しました。'
    return render_template('register_quiz.html', error=error)

@app.route('/delete_quiz_form')
def delete_quiz_form():
    return render_template('delete_quiz.html')

@app.route('/delete_quiz', methods=['POST'])
def delete_quiz():
    quizid = request.form.get('quizid')
   
    if quizid == '':
        error = 'IDが未入力です。'
        return render_template('delete_quiz.html', error = error)
    
    count = db.de_quiz(quizid)
    
    if count == 1:
        msg = '削除が完了しました。'
        return render_template('delete_quiz.html', msg=msg)
    else:
        error = '削除に失敗しました。'
        return render_template('delete_quiz.html', error=error)






@app.route('/edit_quiz_form')
def edit_quiz_form():
    return render_template('edit_quiz.html')


@app.route('/edit_quiz', methods=['POST'])
def edit_quiz():
    title = request.form.get('title')
    answer1 = request.form.get('answer1')
    answer2 = request.form.get('answer2')
    answer3 = request.form.get('answer3')
    answer4 = request.form.get('answer4')
    correctanswer = request.form.get('correctanswer')
    quizid = request.form.get('quizid')
    
    if title == '':
        error = '問題文が未入力です。'
        return render_template('edit_quiz.html', error = error)
    if answer1 == '':
        error = '回答１が未入力です。'
        return render_template('edit_quiz.html', error = error)
    if answer2 == '':
        error = '回答２が未入力です。'
        return render_template('edit_quiz.html', error = error)
    if answer3 == '':
        error = '回答３が未入力です。'
        return render_template('edit_quiz.html', error = error)
    if answer4 == '':
        error = '回答４が未入力です。'
        return render_template('edit_quiz.html', error = error)
    if correctanswer == '':
        error = '正解が未入力です。'
        return render_template('edit_quiz.html', error = error)
    if quizid == '':
        error = 'IDが未入力です。'
        return render_template('edit_quiz.html', error = error)
    
    count = db.edit_quiz(quizid, title, answer1, answer2, answer3, answer4, correctanswer)
    
    if count == 1:
        msg = '編集が完了しました。'
        return render_template('register_quiz.html', msg=msg)
    else:
        error = '編集に失敗しました。'
    return render_template('register_quiz.html', error=error)











# リスト
@app.route('/list')
def sample_list():
    quiz_list = db.select_all_quiz()
    return render_template('list.html', quizs=quiz_list)


if __name__ == '__main__':
    app.run(debug=True)