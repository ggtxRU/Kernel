import datetime

from db.models.base import BaseModel


def test_base_model():
    date_time = datetime.datetime.now()
    base_model = BaseModel(
        created_at=date_time,
        updated_at=date_time
    )

    assert base_model.created_at == date_time
    assert base_model.updated_at == date_time
