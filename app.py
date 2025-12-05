from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_db():
   conn = sqlite3.connect('applications.db')
   c = conn.cursor()
   c.execute('''
      CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surname TEXT NOT NULL,
            name TEXT NOT NULL,
            patronymic TEXT,
            age INTEGER NOT NULL,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
   conn.commit()
   conn.close()

@app.route('/')
def show_form():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_application():
   surname = request.form.get('surname')
   name = request.form.get('name')
   patronymic = request.form.get('patronymic', '')
   age = request.form.get('age')
   email = request.form.get('email')
   
   if not surname or not name or not age or not email:
      return "Заполните обязательные поля!"
   
   conn = sqlite3.connect('applications.db')
   c = conn.cursor()
   c.execute('''
      INSERT INTO applications (surname, name, patronymic, age, email)
      VALUES (?, ?, ?, ?, ?)
   ''', (surname, name, patronymic, int(age), email))
   conn.commit()
   conn.close()
    
   return redirect('/')

@app.route('/admin')
def admin():
   conn = sqlite3.connect('applications.db')
   c = conn.cursor()
   
   c.execute('SELECT * FROM applications ORDER BY created_at DESC')
   applications = c.fetchall()
   
   c.execute('SELECT COUNT(*) FROM applications')
   total = c.fetchone()[0]
   
   conn.close()
    
   return render_template('admin.html', 
                        applications=applications, 
                        total=total)

@app.route('/delete/<int:app_id>')
def delete_application(app_id):
   conn = sqlite3.connect('applications.db')
   c = conn.cursor()
   c.execute('DELETE FROM applications WHERE id = ?', (app_id,))
   conn.commit()
   conn.close()
   
   return redirect('/admin')

if __name__ == '__main__':
    create_db()
    app.run(debug=True)