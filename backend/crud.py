from .database import connect

def get_all():
    conn = connect()
    rows = conn.execute('SELECT * FROM materials ORDER BY id').fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_by_id(material_id: int):
    conn = connect()
    row = conn.execute('SELECT * FROM materials WHERE id = ?', (material_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def create_material(materials: dict):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO materials(title, description, link) 
        VALUES (?, ?, ?)
        ''',
        (
            materials['title'],
            materials.get('description', ''),
            materials['link']
        )
    )
    conn.commit()
    material_id = cursor.lastrowid
    conn.close()
    return get_by_id(material_id)

def update_material(material_id: int, materials: dict):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        '''
        UPDATE materials 
        SET title = ?, description = ?, link = ? WHERE id = ?
        ''',
        (
            materials['title'],
            materials.get('description', ''),
            materials['link'],
            material_id
        )
    )
    conn.commit()
    update_rows = cursor.rowcount
    conn.close()
    if update_rows == 0:
        return None
    return get_by_id(material_id)

def delete_material(material_id: int):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM materials WHERE id = ?", (material_id,))
    conn.commit()
    delete_rows = cursor.rowcount
    conn.close()
    return delete_rows > 0