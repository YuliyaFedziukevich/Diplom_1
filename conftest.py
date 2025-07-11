import pytest
from unittest.mock import Mock
from praktikum.burger import Burger

@pytest.fixture(scope='function')
def burger():
    return Burger()

@pytest.fixture(scope='function')
def mock_bun():
    mock_bun = Mock()
    mock_bun.get_name.return_value = 'Булочка'
    mock_bun.get_price.return_value = 10
    return mock_bun

@pytest.fixture(scope='function')
def testing_burger():
    burger = Burger()

    mock_bun = Mock()
    mock_bun.get_price.return_value = 10
    mock_bun.get_name.return_value = 'Булочка'
    burger.set_buns(mock_bun)

    ingredients = [{'type': 'SAUCE', 'name': 'Spicy X', 'price': 3},
                       {'type': 'FILLING', 'name': 'Cheese', 'price': 12}]

    for ingredient in ingredients:
        mock_ingredient_1 = Mock()
        mock_ingredient_1.get_type.return_value = ingredient['type']
        mock_ingredient_1.get_name.return_value = ingredient['name']
        mock_ingredient_1.get_price.return_value = ingredient['price']
        burger.add_ingredient(mock_ingredient_1)

    return burger



