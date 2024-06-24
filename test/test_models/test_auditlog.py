import pytest
from datetime import datetime, timedelta
from app.models import AuditLog, ActionType


def test_audit_log_creation(session):
    audit_log = AuditLog(
        table_name='test_table',
        table_primary_key='1',
        column_name='test_column',
        old_value='old_value',
        new_value='new_value',
        username='test_user',
        change_timestamp=datetime.utcnow(),
        action_type=ActionType.UPDATE
    )
    session.add(audit_log)
    session.commit()

    assert audit_log.id is not None
    assert audit_log.table_name == 'test_table'
    assert audit_log.table_primary_key == '1'
    assert audit_log.column_name == 'test_column'
    assert audit_log.old_value == 'old_value'
    assert audit_log.new_value == 'new_value'
    assert audit_log.username == 'test_user'
    assert audit_log.action_type == ActionType.UPDATE


def test_to_dict_method(session):
    audit_log = AuditLog(
        table_name='test_table',
        table_primary_key='1',
        column_name='test_column',
        old_value='old_value',
        new_value='new_value',
        username='test_user',
        change_timestamp=datetime.utcnow(),
        action_type=ActionType.UPDATE
    )
    session.add(audit_log)
    session.commit()

    audit_dict = audit_log.to_dict()
    assert audit_dict['audit_id'] == audit_log.id
    assert audit_dict['table_name'] == 'test_table'
    assert audit_dict['table_primary_key'] == '1'
    assert audit_dict['column_name'] == 'test_column'
    assert audit_dict['old_value'] == 'old_value'
    assert audit_dict['new_value'] == 'new_value'
    assert audit_dict['username'] == 'test_user'
    assert audit_dict['action_type'] == ActionType.UPDATE.value


def test_get_audit_logs_no_params(session):
    audit_log1 = AuditLog(
        table_name='test_table',
        table_primary_key='1',
        column_name='test_column',
        old_value='old_value1',
        new_value='new_value1',
        username='test_user',
        change_timestamp=datetime.utcnow(),
        action_type=ActionType.UPDATE
    )
    audit_log2 = AuditLog(
        table_name='test_table',
        table_primary_key='2',
        column_name='test_column',
        old_value='old_value2',
        new_value='new_value2',
        username='test_user',
        change_timestamp=datetime.utcnow() + timedelta(seconds=1),
        action_type=ActionType.UPDATE
    )
    session.add(audit_log1)
    session.add(audit_log2)
    session.commit()

    logs = AuditLog.get_audit_logs()
    assert len(logs) == 2
    assert logs[0].table_primary_key == '2'
    assert logs[1].table_primary_key == '1'


def test_get_audit_logs_with_params(session):
    now = datetime.utcnow()
    audit_log1 = AuditLog(
        table_name='test_table',
        table_primary_key='1',
        column_name='test_column',
        old_value='old_value1',
        new_value='new_value1',
        username='test_user',
        change_timestamp=now - timedelta(days=1),
        action_type=ActionType.UPDATE
    )
    audit_log2 = AuditLog(
        table_name='test_table',
        table_primary_key='2',
        column_name='test_column',
        old_value='old_value2',
        new_value='new_value2',
        username='test_user',
        change_timestamp=now,
        action_type=ActionType.UPDATE
    )
    session.add(audit_log1)
    session.add(audit_log2)
    session.commit()

    start_date = now - timedelta(hours=12)
    end_date = now + timedelta(hours=12)
    logs = AuditLog.get_audit_logs(start_date, end_date)
    assert len(logs) == 1
    assert logs[0].table_primary_key == '2'


def test_get_audit_logs_with_invalid_dates(session):
    with pytest.raises(AssertionError):
        AuditLog.get_audit_logs('not_a_date', datetime.utcnow())

    with pytest.raises(AssertionError):
        AuditLog.get_audit_logs(datetime.utcnow(), 'not_a_date')


@pytest.mark.parametrize("field, value", [
    ("table_name", None),
    ("table_primary_key", None),
    ("column_name", None),
    ("old_value", None),
    ("new_value", None),
    ("username", None),
    ("change_timestamp", None),
    ("action_type", None)
])
def test_audit_log_missing_required_fields(session, field, value):
    audit_log_data = {'table_name': 'test_table', 'table_primary_key': '1', 'column_name': 'test_column',
                      'old_value': 'old_value', 'new_value': 'new_value', 'username': 'test_user',
                      'change_timestamp': datetime.now(), 'action_type': ActionType.UPDATE, field: value}

    with pytest.raises(ValueError):
        audit_log = AuditLog(**audit_log_data)
        session.add(audit_log)
        session.commit()
