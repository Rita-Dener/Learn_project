from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'super secret key'
API_URL = 'http://127.0.0.1:8000'

def api_get(endpoint: str):
    return requests.get(f"{API_URL}{endpoint}", timeout=5)

def api_post(endpoint: str, data: dict):
    return requests.post(f"{API_URL}{endpoint}", json=data, timeout=5)

def api_put(endpoint: str, data: dict):
    return requests.put(f"{API_URL}{endpoint}", json=data, timeout=5)

def api_patch(endpoint: str, data: dict):
    return requests.patch(f"{API_URL}{endpoint}", json=data, timeout=5)

def api_delete(endpoint: str):
    return requests.delete(f"{API_URL}{endpoint}", timeout=5)

@app.route('/')
def index():
    try:
        response = api_get('/materials')
        materials = response.json() if response.status_code == 200 else []
        return render_template('index.html', materials=materials)
    except:
        flash("Данные от API не получены", "danger")
    return render_template('index.html', materials=[])

@app.route('/materials/<material_id>')
def material_by_id(material_id: int):
    response = api_get(f'/materials/{material_id}')
    if not response.status_code == 200:
        flash("Материал не найден", "danger")
        return redirect(url_for('index'))
    return render_template("material_by_id.html", materials=response.json())

@app.route('/materials/create', methods=['POST'])
def create():
    if request.method == 'POST':
        material = {
            'title': request.form['title'],
            'description': request.form.get("description", ""),
            'link': request.form['link']
        }
        response = api_post('/materials', material)
        if response.status_code == 200:
            flash("Материал добавлен!", "success")
            return redirect(url_for("index"))
        flash("Ошибка API", "danger")
    return render_template("form.html", material=None)

@app.route('/materials/<int:material_id>/edit', methods=['POST'])
def edit(material_id: int):
    material = {
        'title': request.form['title'],
        'description': request.form.get("description", ""),
        'link': request.form['link']
    }
    response = api_put(f'/materials/{material_id}', material)
    if response.status_code == 200:
        flash("Материал обновлен полностью)))", "success")
    else:
        flash("Ошибка API", "danger")
    return render_template("index.html")

@app.route('/materials/<int:material_id>/patch', methods=['POST'])
def patch(material_id: int):
    patch_material = {}
    if request.form.get('title'):
        patch_material['title'] = request.form['title']
    if request.form.get('description'):
        patch_material['description'] = request.form['description']
    if request.form.get('link'):
        patch_material['link'] = request.form['link']

    response = api_patch(f'/materials/{material_id}', patch_material)
    if response.status_code == 200:
        flash("Материал не найден", "danger")
        return redirect(url_for("index"))
    return render_template("edit.html", material=patch_material)

@app.route('/materials/<int:material_id>/delete', methods=['POST'])
def delete(material_id: int):
    response = api_delete(f'/materials/{material_id}')
    if response.status_code == 200:
        flash("Материла удалён!!!!", "success")
    else:
        flash("Материла не удален(((", "danger")
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)