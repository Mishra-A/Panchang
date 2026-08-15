from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_daily_panchang_api():

    response = client.get(
        "/api/v1/panchang/daily",
        params={
            "date": "2026-08-14",
            "city": "Lucknow",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["date"] == "2026-08-14"

    assert data["location"]["city"] == "Lucknow"

    assert "panchang" in data
    assert "kaal" in data


def test_daily_panchang_with_muhurat():

    response = client.get(
        "/api/v1/panchang/daily",
        params={
            "date": "2026-08-14",
            "city": "Lucknow",
            "activity": "vehicle_purchase",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "muhurat" in data

    assert (
        data["muhurat"]["activity"]
        == "vehicle_purchase"
    )

    assert "best_windows" in data["muhurat"]

    assert isinstance(
        data["muhurat"]["best_windows"],
        list,
    )


def test_unsupported_location():

    response = client.get(
        "/api/v1/panchang/daily",
        params={
            "date": "2026-08-14",
            "city": "xyz",
        },
    )

    assert response.status_code == 404