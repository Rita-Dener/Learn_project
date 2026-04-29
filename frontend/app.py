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
    view_mode = request.args.get('view_mode', 'two_columns')
    select_mode = request.args.get('select_mode', '0')
    try:
        response = api_get('/materials')
        materials = response.json() if response.ok else []
        return render_template('index.html', materials=materials, view_mode=view_mode, select_mode=select_mode)
    except Exception as error:
        flash(f"Данные от API не получены: {error}", "danger")

    return render_template('index.html', materials=[], view_mode=view_mode, select_mode=select_mode)

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
        flash("Материал удалён!!!!", "success")
    else:
        flash("Материал не удален(((", "danger")
    return redirect(url_for('index'))


@app.route('/materials/delete-selected', methods=['POST'])
def delete_selected():
    material_ids = request.form.getlist('selected_materials')
    for material_id in material_ids:
        response = api_delete(f'/materials/{material_id}')
        if response.ok:
            flash("Материалы удалены!!!!", "success")
        else:
            flash("Материалы не удалены(((", "danger")
    return redirect(url_for('index', select_mode='0'))

if __name__ == "__main__":
    app.run(debug=True)