import enum


class BooleanEnum(str, enum.Enum):
    yes = 'yes'
    no = 'no'


class CriteriaAssessmentEnum(str, enum.Enum):
    known = 'known'
    unknown = 'unknown'
    na = 'na'


class HigherOperationEnum(str, enum.Enum):
    create = 'create'
    delete = 'delete'
    split = 'split'
    merge = 'merge'
    update = 'update'


class OperationEnum(str, enum.Enum):
    create = 'create'
    delete = 'delete'
    update = 'update'


class StatusEnum(str, enum.Enum):
    in_progress = 'in_progress'
    complete = 'complete'
