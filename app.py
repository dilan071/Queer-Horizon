from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'webm', 'mkv', 'avi'}
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    video_filename = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    video = request.files['video']
    
    if video and allowed_file(video.filename):
        video_filename = secure_filename(video.filename)
        video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))
        
        user = User(name=name, email=email, video_filename=video_filename)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('success'))
    else:
        return "Error: el archivo no es válido o no se proporcionó."

@app.route('/success')
def success():
    users = User.query.all()
    return render_template('success.html', users=users)

@app.route('/delete/<int:video_id>', methods=['POST'])
def delete_video(video_id):
    video_to_delete = User.userdb(video_id)
    
    # Eliminar el archivo de video del servidor
    os.remove(os.path.join('static/uploads', video_to_delete.video_filename))

    # Eliminar el registro de video de la base de datos
    db.session.delete(video_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
