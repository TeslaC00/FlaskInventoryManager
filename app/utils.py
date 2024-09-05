from typing import Type

from flask_sqlalchemy.query import Query
from sqlalchemy import or_, desc, asc

from app.models import Buyer, Supplier, IndianState


def apply_generic_sorting(query: Query, model, filters: dict) -> Query:
    # Apply sorting
    if 'sort_by' in filters:
        sort_column = getattr(model, filters.get('sort_by'), None)
        if sort_column:
            sort_order = filters.get('sort_order', 'desc')
            sort_func = desc if sort_order == 'desc' else asc
            query = query.order_by(sort_func(sort_column))
    return query


def apply_person_sorting(query: Query, model: Type[Buyer | Supplier], filters: dict) -> Query:
    # Apply sorting
    sort_by = filters.get('sort_by', 'name')
    sort_order = filters.get('sort_order', 'desc')
    sort_func = desc if sort_order == 'desc' else asc

    if sort_by == 'name':
        query = query.order_by(sort_func(model.name))
    elif sort_by in ['state_name', 'state_code']:
        query = query.join(model.state)
        sort_column = IndianState.name if sort_by == 'state_name' else IndianState.id
        query = query.order_by(sort_func(sort_column))
    return query


def apply_person_filters(query: Query, model: Type[Supplier | Buyer], filters: dict) -> Query:
    # Apply filters
    if 'name' in filters:
        query = query.filter(model.name.like(f"%{filters['name']}%"))
    if 'GST_No' in filters:
        query = query.filter(model.GST_No.like(f"%{filters['GST_No']}%"))

    if any(key in filters for key in ['state_name', 'state_code', 'search']):
        query = query.join(model.state)

    if 'state_code' in filters:
        query = query.filter(IndianState.id.like(f"%{filters['state_code']}%"))
    if 'state_name' in filters:
        query = query.filter(IndianState.name.like(f"%{filters['state_name']}%"))

    if 'search' in filters:
        search = f"%{filters['search']}%"
        query = query.filter(or_(
            model.name.like(search),
            model.GST_No.like(search),
            model.address.like(search),
            IndianState.name.like(search)
        ))
    return query
