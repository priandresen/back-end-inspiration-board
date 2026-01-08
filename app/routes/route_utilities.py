from flask import abort, make_response
from app.models.card import Card
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except (TypeError, ValueError):
        return abort(make_response({"message": f"{cls.__name__} id {model_id} invalid"}, 400))
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    if not model:
        return abort(make_response({"message": f"{cls.__name__} id {model_id} not found"}, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)              
    except KeyError as e:
        return abort(make_response({"details": f"Missing field: {e.args[0]}"}, 400))
    except ValueError as e:
        return abort(make_response({"details": str(e)}, 400))
    db.session.add(new_model)
    db.session.commit()
    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
    if filters and filters.get("sort") == "asc":
        query = query.order_by(cls.title.asc())
    if filters and filters.get("sort") == "desc":
        query = query.order_by(cls.title.desc())
    else:
        query = query.order_by(cls.id)
    
    models = db.session.scalars(query).all()
    models_response = [model.to_dict() for model in models]
    return models_response

def apply_card_sort(query, sort):
    if sort == "alpha":
        return query.order_by(Card.message.asc())
    if sort == "likes":
        return query.order_by(Card.likes_count.desc(), Card.id.asc())
    return query.order_by(Card.id.asc())
