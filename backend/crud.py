from .database import connect

def get_all():
    conn = connect()
    rows = conn.execute('SELECT * FROM material ORDER BY id').fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_by_id(material_id: int):
    conn = connect()
    row = conn.execute('SELECT * FROM material WHERE id = ?', (material_id,)).fetchall()
    conn.close()
    return dict(row) if row else None

def create_material(material: dict):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO material(title, description, link) 
        VALUES (?, ?, ?)
        ''',
        (
            material['title'],
            material.get('description', ''),
            material['link']
        )
    )
    conn.commit()
    material_id = cursor.lastrowid
    conn.close()
    return get_by_id(material_id)

def update_material(material_id: int, material: dict):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE material 
        SET title = ?, description = ?, link = ? WHERE id = ?
        ''',
        (
            material['title'],
            material.get('description', ''),
            material['link'],
            material_id
        )
    )
    conn.commit()
    update_rows = cursor.rowcount
    conn.close()
    if update_rows == 0:
        return None
    return get_by_id(material_id)

def patch_material(material_id: int, material: dict):
    existing = get_by_id(material_id)
    if not existing:
        return None

    updated = {
        'title': material.get('title', existing['title']),
        'description': material.get('description', existing['description']),
        'link': material.get('link', existing['link']),
    }
    return update_material(material_id, updated)

def delete_material(material_id: int):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM material WHERE id = ?", (material_id,))
    conn.commit()
    delete_rows = cursor.rowcount
    conn.close()
    return delete_rows > 0