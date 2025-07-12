from unittest.mock import Mock
import pytest

class TestBurger:
    # Тестирование успешного установления булочки
    def test_set_buns(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    # Тестирование успешного расчета цены бургера с ингредиентами
    def test_successful_get_price_with_ingredients(self,burger, mock_bun, mock_ingredient):
        burger.set_buns(mock_bun)
        burger.add_ingredient(mock_ingredient)
        assert burger.get_price() == 10 * 2 + 15

    # Тестирование успешного расчета цены бургера без ингредиентов
    def test_successful_get_price_without_ingredients(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.get_price() == 10 * 2

    # Тестирование успешного получения чека на бургер с ингредиентами
    @pytest.mark.parametrize(
    'bun, ingredients, receipt',
    [
        ({'name': 'Булочка1', 'price': 10},
         [{'type': 'SAUCE', 'name': 'Space sauce', 'price': 3}],
         f'(==== Булочка1 ====)\n= sauce Space sauce =\n(==== Булочка1 ====)\n\nPrice: {10 * 2 + 3}'),                  # Бургер с булочкой и 1 ингредиентом

        ({'name': 'Булочка2', 'price': 9},
         [{'type': 'FILLING', 'name': 'Meat', 'price': 12}, {'type': 'SAUCE', 'name': 'Spicy X', 'price': 3}],
         f'(==== Булочка2 ====)\n= filling Meat =\n= sauce Spicy X =\n(==== Булочка2 ====)\n\nPrice: {9 * 2 + 12 + 3}')]) # Бургер с булочкой и 2 ингредиентами
    def test_successful_get_burger_receipt_with_ingredients(self, burger, bun, ingredients, receipt):
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun['price']
        mock_bun.get_name.return_value = bun['name']
        burger.set_buns(mock_bun)
        for ingredient in ingredients:
            mock_ingredient = Mock()
            mock_ingredient.get_type.return_value = ingredient['type']
            mock_ingredient.get_name.return_value = ingredient['name']
            mock_ingredient.get_price.return_value = ingredient['price']
            burger.add_ingredient(mock_ingredient)
        assert burger.get_receipt() == receipt


    # Тестирование успешного получения чека на бургер без ингредиентов
    def test_successful_get_burger_receipt_without_ingredients(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.get_receipt() == f'(==== Булочка ====)\n(==== Булочка ====)\n\nPrice: {10 * 2}'


    # Тестирование успешного добавления ингредиентов в бургер
    def test_successful_add_ingredients(self, testing_burger):
        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = 'FILLING'
        mock_ingredient.get_name.return_value = 'Meat'
        mock_ingredient.get_price.return_value = 15
        testing_burger.add_ingredient(mock_ingredient)
        assert (testing_burger.get_receipt() ==
                f'(==== Булочка ====)\n= sauce Spicy X =\n= filling Cheese =\n= filling Meat =\n(==== Булочка ====)\n\nPrice: {10 * 2 + 3 + 12 + 15}')

    # Тестирование успешного удаления одного ингредиента из бургера
    def test_successful_remove_one_ingredient(self,testing_burger):
        testing_burger.remove_ingredient(0)
        assert testing_burger.get_receipt() == f'(==== Булочка ====)\n= filling Cheese =\n(==== Булочка ====)\n\nPrice: {10 * 2 + 12}'

    # Тестирование успешного удаления всех ингредиентов из бургера
    def test_successful_remove_ingredient(self, testing_burger):
        testing_burger.remove_ingredient(1)
        testing_burger.remove_ingredient(0)
        assert testing_burger.get_receipt() == f'(==== Булочка ====)\n(==== Булочка ====)\n\nPrice: {10 * 2}'

    # Тестирование возможности поменять ингредиенты в бургере местами
    def test_successful_move_ingredient(self, testing_burger):
        testing_burger.move_ingredient(1, 0)
        assert testing_burger.get_receipt() == f'(==== Булочка ====)\n= filling Cheese =\n= sauce Spicy X =\n(==== Булочка ====)\n\nPrice: {10 * 2 + 3 + 12}'
