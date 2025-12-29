async def test_update_item_quantity(client, sample_item):
    response = await client.patch(
        f"/api/v1/items/{sample_item.uuid}", json={"quantity": 123}
    )
    assert response.status_code == 200
    assert response.json()["quantity"] == 123
