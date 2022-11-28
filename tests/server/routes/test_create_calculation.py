from faker import Faker
from starlette.testclient import TestClient

fake = Faker()


def test_create_calculation(client: TestClient, session):
    response = client.post(
        '/calculations/create',
        json={
            'date_start': fake.date(),
            'date_fin': fake.date(),
            'lag':fake.random_int(max=9_999)
        }
    )
    assert response.status_code == 200

    count_calculation_db: int = session.execute("""SELECT COUNT(id) FROM calculation""").one()[0]
    assert count_calculation_db == 1

    response = client.post(
        '/calculations/create',
        json={
            'date_start': fake.date(),
            'date_fin': fake.date(),
            'lag':fake.random_int(max=9_999)
        }
    )
    assert response.status_code == 200

    count_calculation_db: int = session.execute("""SELECT COUNT(id) FROM calculation""").one()[0]
    assert count_calculation_db == 2
