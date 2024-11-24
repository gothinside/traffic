import pytest
from datetime import datetime

@pytest.mark.asyncio
async def test_get_traffic_no_params(test_client):

        expect_response = {
            'Traffics': [
                {
                    'CustomerName': 'Alice Johnson',
                    'TrafficsSum': 1530,
                },
                {
                    'CustomerName': 'Bob Brown',
                    'TrafficsSum': 1930,
                },
                {
                    'CustomerName': 'Jane Smith',
                    'TrafficsSum': 890,
                },
                {
                    'CustomerName': 'John Doe',
                    'TrafficsSum': 1085,
                },
            ],
        }

        response = await test_client.get("/traffic/")
        assert response.status_code == 200
        assert response.json() == expect_response

@pytest.mark.asyncio
async def test_get_traffic_customer_id(test_client):

        expect_response = {
            'Traffics': [
                {
                    'CustomerName': 'John Doe',
                    'TrafficsSum': 1085,
                },
            ],
        }
        params = {
                "customer_id": 1,
        }
        response = await test_client.get(url = "/traffic/", params = params)
        assert response.status_code == 200
        assert response.json() == expect_response

@pytest.mark.asyncio
async def test_get_traffic_before(test_client):

        expect_response = {'Traffics': [
                {
                    'CustomerName': 'Alice Johnson',
                    'TrafficsSum': 470,
                },
                {
                    'CustomerName': 'Jane Smith',
                    'TrafficsSum': 200,
                },
                {
                    'CustomerName': 'John Doe',
                    'TrafficsSum': 330,
                },
            ],
        }

        params = {
                "before": datetime.strptime("2023-03-01 12:00:00", "%Y-%m-%d %H:%M:%S"),
        }
        response = await test_client.get(url = "/traffic/", params = params)

        assert response.status_code == 200
        assert response.json() == expect_response

@pytest.mark.asyncio
async def test_get_traffic_after(test_client):

        expect_response = {'Traffics': [
                {
                    'CustomerName': 'Alice Johnson',
                    'TrafficsSum': 1060,
                },
                {
                    'CustomerName': 'Bob Brown',
                    'TrafficsSum': 1930,
                },
                {
                    'CustomerName': 'Jane Smith',
                    'TrafficsSum': 515,
                },
                {
                    'CustomerName': 'John Doe',
                    'TrafficsSum': 755,
                },
            ],
        }

        params = {
                "after": datetime.strptime("2023-03-01 16:30:00", "%Y-%m-%d %H:%M:%S"),
        }
        response = await test_client.get(url = "/traffic/", params = params)

        assert response.status_code == 200
        assert response.json() == expect_response

@pytest.mark.asyncio
async def test_get_traffic_after_and_before(test_client):

        expect_response = {'Traffics': [
                {
                    'CustomerName': 'Alice Johnson',
                    'TrafficsSum': 220,
                },
            ],
        }

        params = {
                "after": datetime.strptime("2023-02-01 12:00:00", "%Y-%m-%d %H:%M:%S"),
                "before": datetime.strptime("2023-03-01 12:00:00", "%Y-%m-%d %H:%M:%S")
        }
        response = await test_client.get(url = "/traffic/", params = params)

        assert response.status_code == 200
        assert response.json() == expect_response

@pytest.mark.asyncio
async def test_get_traffic_by_ip(test_client):

        expect_response = {'Traffics': [
                {
                    'CustomerName': 'Alice Johnson',
                    'TrafficsSum': 240,
                },
                {
                    'CustomerName': 'Jane Smith',
                    'TrafficsSum': 405,
                },
                {
                    'CustomerName': 'John Doe',
                    'TrafficsSum': 445,
                },
            ],
        }

        params = {
                "ip": "192.168.218.159",
        }
        response = await test_client.get(url = "/traffic/", params = params)

        assert response.status_code == 200
        assert response.json() == expect_response

@pytest.mark.asyncio
async def test_get_traffic_empty_response(test_client):

        expect_response = {'Traffics': []}

        params = {
                "customer_id": 1,
                "ip": "192.168.218.152",
        }
        response = await test_client.get(url = "/traffic/", params = params)

        assert response.status_code == 200
        assert response.json() == expect_response



@pytest.mark.asyncio
async def test_get_traffic_all_param(test_client):

        expect_response = {'Traffics': [
                {
                    'CustomerName': 'John Doe',
                    'TrafficsSum': 180,
                },
            ],
        }

        params = {
                "id": 1,
                "after": datetime.strptime("2022-05-01 15:00:00", "%Y-%m-%d %H:%M:%S"),
                "before": datetime.strptime("2023-03-01 12:00:00", "%Y-%m-%d %H:%M:%S"),
                "ip": "192.168.214.201"
        }
        response = await test_client.get(url = "/traffic/", params = params)

        assert response.status_code == 200
        assert response.json() == expect_response