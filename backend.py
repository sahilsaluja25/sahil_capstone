import mysql.connector
from flask import Flask, request, render_template

app = Flask(__name__)

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="note_manager"
    )


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            add_note(note)
    
    notes = list_notes()
    return render_template('index.html', notes=notes)


def add_note(note):
    conn = connect_to_database()
    cursor = conn.cursor()
    
    query = "INSERT INTO notes (note) VALUES (%s)"
    values = (note,)
    
    cursor.execute(query, values)
    conn.commit()
    
    cursor.close()
    conn.close()

def list_notes():
    conn = connect_to_database()
    cursor = conn.cursor()

    query = "SELECT * FROM notes"
    
    cursor.execute(query)
    notes = cursor.fetchall()

    cursor.close()
    conn.close()

    return notes

if __name__ == '__main__':
    app.run(debug=True)
