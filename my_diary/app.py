import time
from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)

#نام فایل برای ذخیره داده ها
DATA_File = 'notes.json'

#تابع برای خواندن یادداشت ها از فایل
def load_notes():
    if os.path.exists(DATA_File):
        with open(DATA_File,'r', encoding='utf-8') as f:
            return json.load(f)
    return []
    
#تابع برای ذخیره یادداشت ها در فایل    
def save_notes():
    with open(DATA_File, 'w', encoding='utf-8') as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


#یادداشت ها را از فایل بخوان        
notes=load_notes()

@app.route('/')
def home():
    with open('notes.json', 'r') as f:
        notes = json.load(f)

    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    note_text = request.form['note']

    with open('notes.json', 'r') as f:
        notes = json.load(f)

    new_note = {
        "id": int(time.time() * 1000),
        "text": note_text
    }

    notes.append(new_note)

    with open('notes.json', 'w') as f:
        json.dump(notes, f)

    return redirect('/')

@app.route('/delete/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    with open('notes.json', 'r') as f:
        notes = json.load(f)

        notes = [note for note in notes if note["id"] != note_id]

    with open('notes.json', 'w') as f:
        json.dump(notes, f)

    return redirect('/')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
    app.run()

        