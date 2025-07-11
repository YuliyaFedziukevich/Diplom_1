from unittest.mock import Mock
import pytest

class TestBurger:
    # Тестирование успешного установления булочки
    def test_set_buns(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    # Тестирование успешного расчета цены бургера
    @pytest.mark.parametrize(
        'buns_price, ingredients_price, total_price',
        [
            (10, [7, 5], 10 * 2 + 7 + 5), # цена булочки - 10, цена ингредиентов 7 и 5
            (10, None, 10 * 2)            # цена булочки - 10, бургер без ингредиентов
        ])
    def test_successful_get_price(self, burger, buns_price, ingredients_price, total_price):
        mock_bun = Mock()
        mock_bun.get_price.return_value = buns_price
        burger.set_buns(mock_bun)

        if ingredients_price is not None:
            for price in ingredients_price:
                mock_ingredient = Mock()
                mock_ingredient.get_price.return_value = price
                burger.add_ingredient(mock_ingredient)

        assert burger.get_price() == total_price

    # Тестирование успешного получения чека
    @pytest.mark.parametrize(
    'bun, ingredients, receipt',
    [
        ({'name': 'Булочка1', 'price': 10},
         [{'type': 'SAUCE', 'name': 'Space sauce', 'price': 3}],
         f'(==== Булочка1 ====)\n= sauce Space sauce =\n(==== Булочка1 ====)\n\nPrice: {10 * 2 + 3}'),                  #Бургер с булочкой и 1 ингредиентом

        ({'name': 'Булочка2', 'price': 9},
         [{'type': 'FILLING', 'name': 'Meat', 'price': 12}, {'type': 'SAUCE', 'name': 'Spicy X', 'price': 3}],
         f'(==== Булочка2 ====)\n= filling Meat =\n= sauce Spicy X =\n(==== Булочка2 ====)\n\nPrice: {9 * 2 + 12 + 3}'),#Бургер с булочкой и 2 ингредиентами

        ({'name': 'Булочка3', 'price': 13},
         None,
         f'(==== Булочка3 ====)\n(==== Булочка3 ====)\n\nPrice: {13 * 2}'),                                             #Бургер с булочкой и без ингредиентов
    ])
    def test_successful_get_receipt(self, burger, bun, ingredients, receipt):
        mock_bun = Mock()
        mock_bun.get_price.return_value = bun['price']
        mock_bun.get_name.return_value = bun['name']
        burger.set_buns(mock_bun)

        if ingredients is not None:
            for ingredient in ingredients:
                mock_ingredient = Mock()
                mock_ingredient.get_type.return_value = ingredient['type']
                mock_ingredient.get_name.return_value = ingredient['name']
                mock_ingredient.get_price.return_value = ingredient['price']
                burger.add_ingredient(mock_ingredient)

        assert burger.get_receipt() == receipt

    # Тестирование успешного добавления ингредиентов в бургер
    def test_successful_add_ingredients(self, testing_burger):
        mock_ingredient = Mock()
        mock_ingredient.get_type.return_value = 'FILLING'
        mock_ingredient.get_name.return_value = 'Meat'
        mock_ingredient.get_price.return_value = 15
        testing_burger.add_ingredient(mock_ingredient)
        assert (testing_burger.get_receipt() ==
                f'(==== Булочка ====)\n= sauce Spicy X =\n= filling Cheese =\n= filling Meat =\n(==== Булочка ====)\n\nPrice: {10 * 2 + 3 + 12 + 15}')

    # Тестирование успешного удаления ингредиентов из бургера
    @pytest.mark.parametrize('command, receipt',
                             [('remove_first', f'(==== Булочка ====)\n= filling Cheese =\n(==== Булочка ====)\n\nPrice: {10 * 2 + 12}'), # Удаление одного ингредиента
                             ('remove_both', f'(==== Булочка ====)\n(==== Булочка ====)\n\nPrice: {10 * 2}')])                           # Удаление всех ингредиентов
    def test_successful_remove_ingredient(self, command, receipt, testing_burger):
        if command == 'remove_first':
            testing_burger.remove_ingredient(0)
        elif command == 'remove_both':
            testing_burger.remove_ingredient(1)
            testing_burger.remove_ingredient(0)
        assert testing_burger.get_receipt() == receipt

    # Тестирование возможности поменять ингредиенты в бургере местами
    def test_successful_move_ingredient(self, testing_burger):
        testing_burger.move_ingredient(1, 0)
        assert testing_burger.get_receipt() == f'(==== Булочка ====)\n= filling Cheese =\n= sauce Spicy X =\n(==== Булочка ====)\n\nPrice: {10 * 2 + 3 + 12}'
