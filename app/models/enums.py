import enum


class MaterialScrapType(enum.Enum):
    OK_MATERIAL = 'ok_material'
    NOT_GOOD = 'not_good'
    INTERNAL_REJECTION = 'internal_rejection'


class ProductScrapType(enum.Enum):
    OK_MATERIAL = 'ok_material'
    NOT_GOOD = 'not_good'
    INTERNAL_REJECTION = 'internal_rejection'
    EXTERNAL_REJECTION = 'external_rejection'


class ActionType(enum.Enum):
    INSERT = 'insert'
    UPDATE = 'update'
    DELETE = 'delete'
