from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime, date

app = Flask(__name__)
DB_NAME = "refrigerator.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            storage_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit TEXT NOT NULL,
            expire_date TEXT NOT NULL,
            memo TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
  
 
# 필요한 함수 정의 ======================================================================= 
# D-Day 계산 함수  
def get_dday(expire_date):
    today = date.today()
    expire = datetime.strptime(expire_date, "%Y-%m-%d").date()
    return (expire - today).days

# DB에서 가져온 row를 dict로 변환하는 함수 (D-Day 계산 포함)
def row_to_dict(row):
    item = dict(row)
    item["dday"] = get_dday(item["expire_date"])
    return item

# 라우터 ================================================================================
@app.route("/")
def index():
    return render_template("index.html")    

# API 엔드포인트: 재료 목록 가져오기
@app.route("/api/ingredients", methods=["GET"])
def get_ingredients():
    conn = get_db()
    cursor = conn.execute("""
        SELECT * FROM ingredients 
        ORDER BY created_at DESC
    """).fetchall()
    conn.close()
    
    ingredients = [row_to_dict(row) for row in cursor]
    
    return jsonify({
        "success": True,
        "data": ingredients
    })
    
    
# API 엔드포인트: 재료 등록하기
@app.route("/api/ingredients", methods=["POST"])
def create_ingredient():
    data = request.get_json()
    
    name = data.get("name")
    category = data.get("category")
    storage_type = data.get("storage_type")
    quantity = data.get("quantity")
    unit = data.get("unit")
    expire_date = data.get("expire_date")
    memo = data.get("memo", "")
    
    if not name or not category or not storage_type or not quantity or not unit or not expire_date:
        '''
        HTTP 응답의 Content-Type 을 application/json 으로 자동 설정 
        -> 클라이언트가 JSON 형식의 응답임을 인식할 수 있도록 함
        '''
        return jsonify({
            "success": False, 
            "message": "모든 필수 항목을 입력해주세요."
        }), 400
        
    conn = get_db()
    conn.execute("""
        INSERT INTO ingredients 
        (name, category, storage_type, quantity, unit, expire_date, memo, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, 
        category, 
        storage_type, 
        quantity, 
        unit, 
        expire_date, 
        memo, 
        # datetime.now().isoformat()
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "재료가 등록되었습니다."
    })
    
    
# API 엔드포인트: 재료 수정하기
@app.route("/api/ingredients/<int:ingredient_id>", methods=["PUT"])
def update_ingredient(ingredient_id):
    data = request.get_json()
    
    name = data.get("name")
    category = data.get("category")
    storage_type = data.get("storage_type")
    quantity = data.get("quantity")
    unit = data.get("unit")
    expire_date = data.get("expire_date")
    memo = data.get("memo", "")
    
    conn = get_db()
    conn.execute("""
        UPDATE ingredients 
        SET name = ?, 
            category = ?, 
            storage_type = ?, 
            quantity = ?, 
            unit = ?, 
            expire_date = ?, 
            memo = ?
        WHERE id = ?
    """, (
        name, 
        category, 
        storage_type, 
        quantity, 
        unit, 
        expire_date, 
        memo, 
        ingredient_id
    ))
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,       
        "message": "재료가 수정되었습니다."
    })
    
    
# API 엔드포인트: 재료 삭제하기
@app.route("/api/ingredients/<int:ingredient_id>", methods=["DELETE"])
def delete_ingredient(ingredient_id):
    conn = get_db()
    conn.execute("DELETE FROM ingredients WHERE id = ?", 
        (ingredient_id,)
    )
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "재료가 삭제되었습니다."
    })
    
    
# API 엔드포인트: 재료 소비하기 (수량 -1)
@app.route("/api/ingredients/<int:ingredient_id>/consume", methods=["PATCH"])
def consume_ingredient(ingredient_id):
    conn = get_db()
    
    item = conn.execute(
        "SELECT * FROM ingredients WHERE id = ?",
        (ingredient_id,)
    ).fetchone()
    
    if item is None:
        conn.close()
        return jsonify({
            "success": False,
            "message": "재료를 찾을 수 없습니다."
        }), 404
        
    new_quantity = item["quantity"] - 1
    
    if new_quantity < 0:
        conn.execute(
            "DELETE FROM ingredients WHERE id = ?",
            (ingredient_id,)
        )
    else:
        conn.execute(
            "UPDATE ingredients SET quantity = ? WHERE id = ?",
            (new_quantity, ingredient_id) # new_quantity 값을 ingredient_id 에 업데이트
        )
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "재료가 소비되었습니다."
    })
    
if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)