import pytest

@pytest.mark.asyncio
async def test_list_milestones_empty(auth_client):
    response = await auth_client.get("/api/milestones/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
