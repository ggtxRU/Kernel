from faker import Faker
from starlette.testclient import TestClient

fake = Faker()


def test_get_calculation_by_id(client: TestClient, session, truncate_tables):
    response = client.post(
        '/calculations/create',
        json={
            'date_start': fake.date(),
            'date_fin': fake.date(),
            'lag':fake.random_int(max=9_999)
        }
    )
    assert response.status_code == 200
    created_calculation_id: int = session.execute("""SELECT id FROM calculation""").one()[0]
    session.execute(
        f"""
        INSERT INTO 
        calculation_result(
            calculation_result_date,
            liquid,
            oil,
            water,
            wct,
            time_spent,
            calculation_id)
        VALUES(
            '{fake.date_time()}',
            {fake.random_int(max=2_000)},
            {fake.random_int(max=2_000)},
            {fake.random_int(max=2_000)},
            {fake.random_int(max=2_000)},
            {fake.pyfloat()}, 
            {created_calculation_id}
        )
        """
    )
    response = client.get(
        f'/calculations/{created_calculation_id}',
    )
    assert response.status_code == 200

    response = client.get(
        f'/calculations/{fake.random_int(max=2_000_000)}',
    )
    assert response.status_code == 400
