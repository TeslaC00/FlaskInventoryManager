from typing import Type

from flask_sqlalchemy.query import Query
from sqlalchemy import text, or_

from app.models import Buyer, Supplier


def apply_sorting(query, query_args, pagination_parameters):
    if 'sort_order' in query_args:
        order = 'DESC' if query_args['sort_order'] == 'desc' else 'ASC'
        query = query.order_by(text(f"{query_args['sort_by']} {order}"))
    pagination_parameters.item_count = query.count()
    page = pagination_parameters.page
    per_page = pagination_parameters.page_size
    records = query.offset((page - 1) * per_page).limit(per_page).all()
    return records


def apply_generic_sorting(query: Query, model, filters: dict) -> Query:
    # Apply sorting
    if 'sort_by' in filters:
        sort_column = getattr(model, filters.get('sort_by'), None)
        if sort_column:
            if filters.get('sort_order', 'asc') == 'desc':
                query = query.order_by(sort_column.desc())
            else:
                query = query.order_by(sort_column.asc())
    return query


def apply_person_filters(query: Query, model: Type[Supplier | Buyer], filters: dict) -> Query:
    # Apply filters
    if 'name' in filters:
        query = query.filter(model.name.like(f"%{filters['name']}%"))
    if 'GST_No' in filters:
        query = query.filter(model.GST_No.like(f"%{filters['GST_No']}%"))
    if 'state_code' in filters:
        query = query.filter(model.state_code.like(f"%{filters['state_code']}%"))
    if 'state_name' in filters:
        query = query.filter(model.state_name.like(f"%{filters['state_name']}%"))
    if 'search' in filters:
        search = f"%{filters['search']}%"
        query = query.filter(or_(
            model.name.like(search),
            model.GST_No.like(search),
            model.state_name.like(search),
            model.address.like(search)
        ))
    return query
