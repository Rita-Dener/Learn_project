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

def api_delete(endpoint: str):
    return requests.delete(f"{API_URL}{endpoint}", timeout=5)

@app.route('/')
def index():
    try:
        response = api_get('/materials')
        materials = response.json() if response.ok else []
        return render_template('index.html', materials=materials)
    except Exception as error:
        flash(f"Данные от API не получены: {error}", "danger")
    return render_template('index.html', materials=[])

@app.route('/materials/<material_id>')
def material_by_id(material_id: int):
    response = api_get(f'/materials/{material_id}')
    if not response.ok:
        flash("Материал не найден", "danger")
        return redirect(url_for('index'))
    return render_template("material_by_id.html", material=response.json())

@app.route('/materials/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        material = {
            'title': request.form['title'],
            'description': request.form.get("description", ""),
            'link': request.form['link']
        }
        response = api_post('/materials', material)
        if response.ok:
            flash("Материал добавлен!", "success")
            return redirect(url_for("index"))
        flash(f"Ошибка API: {response.text}", "danger")
    return render_template("form.html", materials=None, action_url=url_for('create'))

@app.route('/materials/<int:material_id>/edit', methods=['GET','POST'])
def edit(material_id: int):
    if request.method == 'POST':
        material = {
            'title': request.form['title'],
            'description': request.form.get("description", ""),
            'link': request.form['link']
        }
        response = api_put(f'/materials/{material_id}', material)
        if response.ok:
            flash("Материал обновлен)))", "success")
            return redirect(url_for("index"))
        flash("Ошибка API", "danger")

    response = api_get(f'/materials/{material_id}')
    if not response.ok:
        flash("Материал не найден", "danger")
        return redirect(url_for('index'))
    return render_template("form.html",
                         material=response.json(),
                         action_url=url_for('edit', material_id=material_id))

@app.route('/materials/<int:material_id>/delete', methods=['POST'])
def delete(material_id: int):
    response = api_delete(f'/materials/{material_id}')
    if response.ok:
        flash("Материла удалён!!!!", "success")
    else:
        flash("Материла не удален(((", "danger")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)