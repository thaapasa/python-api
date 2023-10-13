from data.items import Item


def test_create_item():
    item = Item(name="athing", price=233.23, is_offer=True)
    assert item.name == "athing"


def test_create_image_dict():
    item = Item(**{"name": "another", "price": 432})
    assert item.name == "another"
