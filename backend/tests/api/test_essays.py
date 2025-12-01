import pytest

@pytest.mark.asyncio
async def test_create_essay(auth_client):
    response = await auth_client.post(
        "/api/essays/",
        json={
            "prompt": "Explain a challenge you overcame.",
            "content": "This is the content of my essay.",
            "applicant_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["prompt"] == "Explain a challenge you overcame."
    assert data["content"] == "This is the content of my essay."
    assert data["applicant_id"] == 1

@pytest.mark.asyncio
async def test_list_essays(auth_client):
    # Create an essay first
    await auth_client.post(
        "/api/essays/",
        json={
            "prompt": "Explain a challenge you overcame.",
            "content": "This is the content of my essay.",
            "applicant_id": 1
        }
    )

    response = await auth_client.get("/api/essays/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["prompt"] == "Explain a challenge you overcame."

@pytest.mark.asyncio
async def test_create_essay_wrong_applicant(auth_client):
    response = await auth_client.post(
        "/api/essays/",
        json={
            "prompt": "Explain a challenge you overcame.",
            "content": "This is the content of my essay.",
            "applicant_id": 999
        }
    )
    # The endpoint check is: if essay_in.applicant_id != current_user.id: raise 403
    assert response.status_code == 403
