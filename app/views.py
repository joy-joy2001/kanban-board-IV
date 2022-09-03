from flask import render_template, redirect, url_for, request
from flask_login import login_required, logout_user, login_user, current_user, LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
import datetime as dt

from app import my_app, User, Task, LoginForm, RegisterForm, db


login_manager = LoginManager()
date = dt.date
priorityLvls = {
    'high': "red",
    'medium': 'orange',
    'low': 'green',
}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


##########################################  TASK HANDLERS  #############################################################
def current_date():
    today = date.today()
    current_month = today.strftime("%m")
    current_day = today.strftime("%d")
    return f"{current_day}/{current_month}"


def create_board():
    all_lists = {
        'todo_list': Task.query.filter_by(type='todo', user_id=current_user.id).all(),
        'progress_list': Task.query.filter_by(type='in_progress', user_id=current_user.id).all(),
        'completed_list': Task.query.filter_by(type='completed', user_id=current_user.id).all(),
    }
    print(all_lists)
    return all_lists


def kanban_stats():
    all_lists = create_board()
    today = date.today()
    month = today.strftime("%B")[slice(3)].upper()
    year = today.strftime("%Y")
    stats = {
        'todo_no': len(all_lists['todo_list']),
        'inprogress_no': len(all_lists['progress_list']),
        'completed_no': len(all_lists['completed_list']),
        'total': (len(all_lists['todo_list']) + len(all_lists['progress_list']) + len(all_lists['completed_list'])),
        'date': f'{month} {year}'
    }
    return stats


def create_task():
    new_task = Task(
        type='todo',
        desc=request.form.get('task-details'),
        priority=priorityLvls[request.form.get('task-priority')],
        due_date=f"{request.form.get('task-duedate').split('-')[2]}/{request.form.get('task-duedate').split('-')[1]}",
        created_date=current_date(),
        user_id=current_user.id,
    )
    db.session.add(new_task)
    db.session.commit()


def delete_task():
    task_id = request.args.get('task_id')
    task_to_delete = Task.query.filter_by(id=task_id).first()
    db.session.delete(task_to_delete)
    db.session.commit()


def demote_task():
    task_id = request.args.get('task_id')
    current_task = Task.query.filter_by(id=task_id).first()
    if current_task.type == 'completed':
        current_task.type = 'in_progress'
        db.session.commit()
    elif current_task.type == 'in_progress':
        current_task.type = 'todo'
        db.session.commit()


def promote_task():
    task_id = request.args.get('task_id')
    current_task = Task.query.get(task_id)
    if current_task.type == 'todo':
        current_task.type = 'in_progress'
        print(current_task.type)
        db.session.commit()
    elif current_task.type == 'in_progress':
        current_task.type = 'completed'
        db.session.commit()


##################################################### VIEWS HANDLER ####################################################
@my_app.route("/")
def home():
        return render_template("index.html")


@my_app.route("/kanban-board/<username>", methods=['GET', 'POST'])
@login_required
def kanban(username):
    my_board = create_board()
    my_stats = kanban_stats()
    if request.method == 'POST':
        create_task()
        return redirect(url_for('kanban', username=current_user.username))
    return render_template("kanban-board.html", my_board=my_board, my_stats=my_stats, username=current_user.username)


@my_app.route("/login", methods=['GET', 'POST'])
def login():
    username_error = None
    password_error = None
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_exists = User.query.filter_by(username=request.form.get('username')).first()
        if user_exists and check_password_hash(user_exists.password, request.form.get('password')):
            login_user(user_exists)
            return redirect(url_for('home'))
        elif user_exists is None:
            username_error = 'This user does not exist'
        # elif len(request.form['password']) < 8:
        #     password_error = 'Incorrect password. Please try again'
        else:
            password_error = 'Incorrect password. Please try again'
    return render_template("login.html",
                           login_form=login_form,
                           username_error=username_error,
                           password_error=password_error,)


@my_app.route("/register", methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        hashed_password = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=8)

        new_user = User(
            username=request.form.get('username'),
            password=hashed_password,
            date_created=current_date(),
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('home'))
    return render_template("signup.html", register_form=register_form)


@my_app.route("/promote", methods=["GET", "POST"])
def promote():
    promote_task()
    return redirect(url_for('kanban', username=current_user.username))


@my_app.route("/demote", methods=["GET", "POST"])
def demote():
    demote_task()
    return redirect(url_for('kanban', username=current_user.username))


@my_app.route("/delete", methods=["GET", "POST"])
def delete():
    delete_task()
    return redirect(url_for('kanban', username=current_user.username))


@my_app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@my_app.errorhandler(401)
def unauthorised(e):
    return render_template('error_page.html', error=401), 401


@my_app.errorhandler(404)
def unauthorised(e):
    return render_template('error_page.html', error=404), 404