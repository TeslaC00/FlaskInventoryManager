def test_new_buyer(new_buyer):
    assert new_buyer.id is not None
    assert new_buyer.name == 'test'
    assert new_buyer.GST_No == '123456789012345'
    assert new_buyer.state_code == 1
    assert new_buyer.address == 'test address'

# def test_new_material(new_material):
#     assert new_material.part_no == 1
#     assert new_material.name == 'material'
#     assert new_material.unit_id == 1
#     assert new_material.quantity == 10
