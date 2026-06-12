from fastapi import FastAPI
from sqlalchemy.orm import Session

from database import (
    engine,
    SessionLocal
)

from models import (
    Base,
    Ingredient
)

from schemas import (
    IngredientCreate
)

app = FastAPI()

Base.metadata.create_all(
    bind=engine
)

# router ===================================================================
@app.get("/ingredients")
def get_ingredients():
    db: Session = SessionLocal()

    items = db.query(
        Ingredient
    ).all()

    db.close()

    return items


@app.post("/ingredients")
def create_ingredient(
    ingredient: IngredientCreate
):
    db: Session = SessionLocal()

    item = Ingredient(
        **ingredient.model_dump()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    db.close()

    return item


@app.delete("/ingredients/{ingredient_id}")
def delete_ingredient(
    ingredient_id: int
):
    db: Session = SessionLocal()

    item = db.query(
        Ingredient
    ).filter(
        Ingredient.id == ingredient_id
    ).first()

    if item:
        db.delete(item)
        db.commit()

    db.close()

    return {
        "message": "삭제 완료"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=5000,
        reload=True
    )