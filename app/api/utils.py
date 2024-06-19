from sqlalchemy import text


def apply_sorting(query, query_args):
    if 'sort_order' in query_args == 'desc':
        query = query.order_by(text(f"{query_args['sort_by']} DESC"))
    else:
        query = query.order_by(text(f"{query_args['sort_by']} ASC"))
    records_count = query.count()
    records = query.offset(query_args['page']*query_args['limit']).limit(query_args['limit']).all()
    return records, records_count


def generate_meta(records_count, query_args):
    return {
        'records_count': records_count,
        'page': query_args['page'],
        'per_page': query_args['limit'],
    }
