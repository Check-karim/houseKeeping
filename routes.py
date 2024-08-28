from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from models.models import User, Housekeeper, Admin, Task
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

main = Blueprint('main', __name__)  # routename= main

@main.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@main.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    user_type = request.form.get('user_type')

    if password != confirm_password:
        flash('Passwords do not match!')
        return redirect(url_for('main.home'))

    if user_type == 'user':
        new_user = User(email=email, password=password)
    else:
        new_housekeeper = Housekeeper(email=email, password=password)

    try:
        if user_type == 'user':
            new_user.save()
        else:
            new_housekeeper.save()
        flash('Registration successful! Please log in.')
    except:
        flash('Email already exists!')
        return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))

@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user_type = request.form.get('user_type')

    if user_type == 'user':
        user = User.query.filter_by(email=email).first()
    elif user_type == 'housekeeper':
        user = Housekeeper.query.filter_by(email=email).first()
    elif user_type == 'admin':
        user = Admin.query.filter_by(email=email).first()

    if user and user.password == password:
        session['user_id'] = user.id
        session['user_type'] = user_type
        if user_type == 'user':
            return redirect(url_for('main.user_dashboard'))
        elif user_type == 'housekeeper':
            return redirect(url_for('main.housekeeper_dashboard'))
        elif user_type == 'admin':
            return redirect(url_for('main.admin_dashboard'))
    else:
        flash('Login failed! Check your credentials and try again.')
        return redirect(url_for('main.home'))

@main.route('/user_dashboard', methods=['GET'])
def user_dashboard():
    if 'user_id' in session and session.get('user_type') == 'user':
        user = User.query.filter_by(id=session['user_id']).first()
        task = Task()
        tasks = task.get_by_user_id(user_id=session['user_id'])
        return render_template("user_dashboard.html", user=user, tasks = tasks)
    else:
        return redirect(url_for('main.home'))

@main.route('/housekeeper_dashboard', methods=['GET'])
def housekeeper_dashboard():
    if 'user_id' in session and session.get('user_type') == 'housekeeper':
        housekeeper_id = session['user_id']
        housekeeper = Housekeeper.query.filter_by(id=session['user_id']).first()
        available_tasks = db.session.query(Task, User).join(User, Task.user_id == User.id).filter(Task.is_taken == False).all()
        managed_tasks = Task.query.filter_by(housekeeper_id=housekeeper_id).all()

        print(housekeeper)

        return render_template("housekeeper_dashboard.html",housekeeper=housekeeper, available_tasks=available_tasks, managed_tasks=managed_tasks)
    else:
        return redirect(url_for('main.home'))

@main.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    if 'user_id' in session and session.get('user_type') == 'admin':
        admin = Admin.query.filter_by(id=session['user_id']).first()
        return render_template("admin_dashboard.html", admin=admin)
    else:
        return redirect(url_for('main.home'))

@main.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main.home'))

@main.route('/admin_update', methods=['POST'])
def admin_update():
    if 'user_id' in session and session.get('user_type') == 'admin':
        email = request.form.get('email')
        password = request.form.get('password')
        admin = Admin.query.filter_by(id=session['user_id']).first()

        if email:
            admin.email = email
        if password:
            admin.password = password
        
        try:
            admin.save()
            flash('Account updated successfully!')
        except:
            flash('Update failed. Please try again.')

        return redirect(url_for('main.admin_dashboard'))
    else:
        return redirect(url_for('main.home'))

@main.route('/admin_tasks', methods=['GET'])
def admin_tasks():
    if 'user_id' in session and session.get('user_type') == 'admin':
        tasks = Task.query.all()  # Ensure you have a Task model defined
        return render_template("admin_tasks.html", tasks=tasks)
    else:
        return redirect(url_for('main.home'))

@main.route('/create_task', methods=['POST'])
def create_task():
    if 'user_id' in session and session.get('user_type') == 'user':
        user_id = session['user_id']
        address = request.form.get('address')
        phone = request.form.get('phone')
        summary = request.form.get('summary')
        description = request.form.get('full_description')
        price = request.form.get('price')

        print(description)

        new_task = Task(
            user_id=user_id,
            housekeeper_id=0,  # or assign based on some logic
            address=address,
            phone=phone,
            summary=summary,
            description=description,
            price=price,
            is_done=False
        )

        try:
            new_task.save()
            flash('Task created successfully!', 'success')
        except SQLAlchemyError as e:
            # Flash the specific error message
            flash(f'Failed to create task due to a database error: {str(e)}', 'error')
        except Exception as e:
            # Flash any other errors
            flash(f'Failed to create task. Error: {str(e)}', 'error')

        return redirect(url_for('main.user_dashboard'))
    else:
        return redirect(url_for('main.home'))


@main.route('/update_user_account', methods=['POST'])
def update_user_account():
    if 'user_id' in session and session.get('user_type') == 'user':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(id=session['user_id']).first()

        if email:
            user.email = email
        if password:
            user.password = password
        
        try:
            user.save()
            flash('Account updated successfully!')
        except:
            flash('Update failed. Please try again.')

        return redirect(url_for('main.user_dashboard'))
    else:
        return redirect(url_for('main.home'))

@main.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    if 'user_id' in session and session.get('user_type') == 'user':
        task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()

        if request.method == 'POST':
            task.summary = request.form.get('description')
            task.description = request.form.get('full_description')
            task.address = request.form.get('address')
            task.phone = request.form.get('phone')
            task.price = request.form.get('price')
            task.save()

            flash('Task updated successfully!')
            return redirect(url_for('main.user_dashboard'))

        return render_template('update_task.html', task=task)
    else:
        return redirect(url_for('main.home'))

@main.route('/delete_task/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    if 'user_id' in session and session.get('user_type') == 'user':
        task = Task.query.filter_by(id=task_id, user_id=session['user_id']).first()
        if task:
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully!')
        return redirect(url_for('main.user_dashboard'))
    else:
        return redirect(url_for('main.home'))
    

@main.route('/accept_task/<int:task_id>', methods=['GET'])
def accept_task(task_id):
    if 'user_id' in session and session.get('user_type') == 'housekeeper':
        task = Task.query.get_or_404(task_id)
        if task.is_taken:
            flash('This task has already been accepted by another housekeeper.')
            return redirect(url_for('main.housekeeper_dashboard'))
        
        task.is_taken = True
        task.housekeeper_id = session['user_id']
        try:
            db.session.commit()
            flash('Task successfully accepted!')
        except SQLAlchemyError as e:
            flash(f'Failed to accept task due to a database error: {str(e)}', 'error')
        except Exception as e:
            flash(f'Failed to accept task. Error: {str(e)}', 'error')

        return redirect(url_for('main.housekeeper_dashboard'))
    else:
        return redirect(url_for('main.home'))

@main.route('/deny_task/<int:task_id>', methods=['GET'])
def deny_task(task_id):
    if 'user_id' in session and session.get('user_type') == 'housekeeper':
        task = Task.query.get_or_404(task_id)
        if task.housekeeper_id != session['user_id']:
            flash('You are not authorized to deny this task.')
            return redirect(url_for('main.housekeeper_dashboard'))

        task.is_taken = False
        task.housekeeper_id = None
        try:
            db.session.commit()
            flash('Task successfully denied.')
        except SQLAlchemyError as e:
            flash(f'Failed to deny task due to a database error: {str(e)}', 'error')
        except Exception as e:
            flash(f'Failed to deny task. Error: {str(e)}', 'error')

        return redirect(url_for('main.housekeeper_dashboard'))
    else:
        return redirect(url_for('main.home'))

@main.route('/update_task_status/<int:task_id>', methods=['GET', 'POST'])
def update_task_status(task_id):
    if 'user_id' in session and session.get('user_type') == 'housekeeper':
        task = Task.query.get_or_404(task_id)
        if task.housekeeper_id != session['user_id']:
            flash('You are not authorized to update the status of this task.')
            return redirect(url_for('main.housekeeper_dashboard'))

        if request.method == 'POST':
            task.is_done = not task.is_done
            try:
                db.session.commit()
                flash('Task status updated successfully.')
            except SQLAlchemyError as e:
                flash(f'Failed to update task status due to a database error: {str(e)}', 'error')
            except Exception as e:
                flash(f'Failed to update task status. Error: {str(e)}', 'error')

            return redirect(url_for('main.housekeeper_dashboard'))

        return render_template('update_task_status.html', task=task)
    else:
        return redirect(url_for('main.home'))

@main.route('/update_housekeeper_account', methods=['POST'])
def update_housekeeper_account():
    if 'user_id' in session and session.get('user_type') == 'housekeeper':
        housekeeper = Housekeeper.query.get_or_404(session['user_id'])
        
        email = request.form.get('email')
        password = request.form.get('password')

        if email:
            housekeeper.email = email
        if password:
            housekeeper.password = password
        
        try:
            db.session.commit()
            flash('Account updated successfully!')
        except SQLAlchemyError as e:
            flash(f'Failed to update account due to a database error: {str(e)}', 'error')
        except Exception as e:
            flash(f'Failed to update account. Error: {str(e)}', 'error')

        return redirect(url_for('main.housekeeper_dashboard'))
    else:
        return redirect(url_for('main.home'))