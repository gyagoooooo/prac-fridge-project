from flask import Flask, render_template, request, redirect
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
    
# 남은 유통기한 계산 함수
def get_dday(expire_date):
    today = date.today()
    expire = datetime.strptime(expire_date, "%Y-%m-%d").date()
    return (expire - today).days

@app.route("/")
def index():
    conn = get_db()
    ingredients = conn.execute("SELECT * FROM ingredients ORDER BY expire_date ASC").fetchall()
    conn.close()
    
    result = []
    for item in ingredients:
        item_dict = dict(item) # 1. Row 객체를 딕셔너리로 변환
        item_dict["dday"] = get_dday(item["expire_date"]) # 2. 남은 유통기한 계산 후 딕셔너리에 추가
        result.append(item_dict) # 3. 결과 리스트에 딕셔너리 추가
        
    return render_template("index.html", ingredients=result)


# 재료 추가 라우트
@app.route("/add", methods=["GET", "POST"])
def add_ingredient():
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        storage_type = request.form["storage_type"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]
        expire_date = request.form["expire_date"]
        memo = request.form["memo"]
        
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
                datetime.now()
        ))
        conn.commit()
        conn.close()
        
        return redirect("/")
    return render_template("add.html")


@app.route("/edit/<int:ingredient_id>", methods=["GET", "POST"])
def edit_ingredient(ingredient_id):
    conn = get_db()
    
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        storage_type = request.form["storage_type"]
        quantity = request.form["quantity"]
        unit = request.form["unit"]
        expire_date = request.form["expire_date"]
        memo = request.form["memo"]
        
        conn.execute("""
            UPDATE ingredients
            SET name = ?, category = ?, storage_type = ?, quantity = ?, unit = ?, expire_date = ?, memo = ?
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
        
        return redirect("/")

    ingredient = conn.execute(
        "SELECT * FROM ingredients WHERE id = ?",
        (ingredient_id,)
    ).fetchone()
    conn.close()
    
    return render_template("edit.html", ingredient=ingredient)

# 재료 삭제 라우트
@app.route("/delete/<int:ingredient_id>", methods=["POST"])
def delete_ingredient(ingredient_id):
    conn = get_db()
    conn.execute(
        "DELETE FROM ingredients WHERE id = ?", 
        (ingredient_id,)
    )
    conn.commit()
    conn.close()
    
    return redirect("/")    

# 재료 소비 => 수량 감소 라우트
@app.route("/consume/<int:ingredient_id>", methods=["POST"])
def consume_ingredient(ingredient_id):
    conn = get_db()
    
    ingredient = conn.execute(
        "SELECT quantity FROM ingredients WHERE id = ?", 
        (ingredient_id,)
    ).fetchone()
    
    if ingredient:
        new_quantity = ingredient["quantity"] - 1
        
        if new_quantity <= 0:
            conn.execute(
                "DELETE FROM ingredients WHERE id = ?", 
                (ingredient_id,)
            )
        else:
            conn.execute(
                "UPDATE ingredients SET quantity = ? WHERE id = ?", 
                (new_quantity, ingredient_id)
            )
        conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)        