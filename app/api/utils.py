from sqlalchemy import text


def apply_sorting(query, query_args, pagination_parameters):
    if 'sort_order' in query_args:
        order = 'DESC' if query_args['sort_order'] == 'desc' else 'ASC'
        query = query.order_by(text(f"{query_args['sort_by']} {order}"))
    pagination_parameters.item_count = query.count()
    page = pagination_parameters.page
    per_page = pagination_parameters.page_size
    records = query.offset((page - 1) * per_page).limit(per_page).all()
    return records
