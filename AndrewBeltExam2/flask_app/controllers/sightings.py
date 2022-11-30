from flask import redirect, render_template, request, session

from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.sighting import Sighting
from flask_app.models.user import User

# Dashboard and controlling all things past user login and reg should be controlled here.
#Most app routes will be put here if they are involving object user is interacting with.

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one(user_data)
    all = Sighting.get_all()
    return render_template('dashboard.html', user = user, all = all)

@app.route('/createsighting')
def create_sighting():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('createSighting.html')

@app.route('/sighting/post', methods=['POST'])
def post_sighting():
    isValid = Sighting.validate(request.form)
    if not isValid:
        return redirect('/createsighting')
    data = {
        'location': request.form['location'],
        'description': request.form['description'],
        'num_sasquatch': request.form['num_sasquatch'],
        'date_made': request.form['date_made'],
        'user_id': session['user_id']
    }
    Sighting.create_sighting(data)
    return redirect('/dashboard')

#  Display a single sighting
@app.route('/showSighting/<int:sighting_id>')
def show_sighting(sighting_id):
    data = {
        'id': sighting_id
    }
    user_data = {
        'id': session['user_id']
    }
    user = User.get_one(user_data)
    sighting = Sighting.get_one(data)
    return render_template('showSighting.html', sighting = sighting, user = user)

#  Edit a single sighting
@app.route('/editSighting/<int:sighting_id>')
def edit_sighting(sighting_id):
    data = {
        'id': sighting_id
    }
    sighting = Sighting.get_one(data)
    return render_template('editSighting.html', sighting = sighting)

#  Update a single sighting
@app.route('/updateSighting/<int:sighting_id>', methods=['POST'])
def update_sighting(sighting_id):
    Sighting.update_sighting(request.form, sighting_id)
    return redirect('/dashboard')

#  Delete a single sighting 
@app.route('/delete/<int:sighting_id>')
def delete(sighting_id):
    data = {
        'id': sighting_id
    }
    Sighting.delete_sighting(data)
    return redirect('/dashboard')

