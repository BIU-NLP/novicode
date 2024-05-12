from typing import List, Optional, List, Union
from actions.action import Action
from entities.generic import *
from entities.shopping import *
from providers.data_model import DataModel


class Shopping(Action):
    """
    The Shopping class contains all the methods of a virtual assistant agent in the shopping domain.
    This class define a specific API for the shopping domain and inherits from the markup Action class.
    This class defines an API to:

        * Find products
        * Find shopping lists
        * Add products to shopping lists
        * Order products
    """

    @classmethod
    def find_products(
        cls,
        product_name: Optional[ProductName] = None,
        product_attribute: Optional[ProductAttribute] = None,
        shopping_list_name: Optional[ShoppingListName] = None,
        date_time: Optional[DateTime] = None,
        location: Optional[Location] = None,
    ) -> List[ProductEntity]:
        """
        This class method find products based on the given parameters.

        Parameters
        ----------
        product_name : ProductName, optional
            The name of the product to find
        product_attribute : ProductAttribute, optional
            The attribute of the product to find (e.g., available, on sale, etc.)
        date_time : DateTime, optional
            The date and time to find the product at
        shopping_list_name : ShoppingListName, optional
            The name of the shopping list to find the product at
        location : Location, optional
            The location (usually the store) to find the product at

        Returns
        -------
        List[ProductEntity]
            The list of weather forecasts that were found
        """
        data_model = DataModel()
        data = data_model.get_data(ProductEntity)
        if product_name:
            data = [x for x in data if x.product_name == product_name]

        if product_attribute:
            data = [x for x in data if x.product_attribute == product_attribute]

        if shopping_list_name:
            data = [x for x in data if x.shopping_list_name == shopping_list_name]

        if date_time:
            data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        return data

    @classmethod
    def find_shopping_lists(
        cls,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
    ) -> List[ShoppingListEntity]:
        """
        This class method finds saved shopping list based on the given parameters.

        Parameters
        ----------
        date_time : DateTime, optional
            The date and time to find that is associated with the shopping list
        location : Location, optional
            The location (usually the store) to that is associated with the shopping list

        Returns
        -------
        List[ShoppingListEntity]
            A list of shopping list entities that were found
        """
        data_model = DataModel()
        data = data_model.get_data(ShoppingListEntity)
        if date_time:
            if type(date_time) == list:
                data = [x for x in data if x.date_time in date_time]
            else:
                data = [x for x in data if x.date_time == date_time]

        if location:
            data = [x for x in data if x.location == location]

        return data

    @classmethod
    def add_to_shopping_list(
        cls,
        shopping_list_name: ShoppingListName,
        product_name: Optional[ProductName] = None,
        amount: Optional[Amount] = None,
    ) -> ShoppingListEntity:
        """
        This class method adds a product to a shopping list.

        Parameters
        ----------
        shopping_list_name : ShoppingListName, optional
            The name of the shopping list to add the product to
        product_name : ProductName, optional
            The name of the product to add to the shopping list
        amount : Amount, optional
            The amount of products to add to the shopping list

        Returns
        -------
        ShoppingListEntity
            The shopping list entity that the product was added to
        """
        shopping_list = ShoppingListEntity(
            shopping_list_name=shopping_list_name,
            product_name=product_name,
            amount=amount,
        )
        data_model = DataModel()
        data_model.append(shopping_list)
        return shopping_list

    @classmethod
    def order(
        cls,
        product_name: Optional[ProductName] = None,
        product_attribute: Optional[ProductAttribute] = None,
        date_time: Optional[Union[DateTime, List[DateTime]]] = None,
        location: Optional[Location] = None,
        amount: Optional[Amount] = None,
        shopping_list_name: Optional[ShoppingListName] = None,
    ) -> OrderEntity:
        """
        This class method places an order for a product.

        Parameters
        ----------
        product_name : ProductName, optional
            The name of the product to find
        product_attribute : ProductAttribute, optional
            The attribute of the product to find (e.g., available, on sale, etc.)
        date_time : DateTime, optional
            The date and time to find the product at
        location : Location, optional
            The location (usually the store) to find the product at
        amount : Amount, optional
            The amount of products to order
        shopping_list_name : ShoppingListName, optional
            The name of the shopping list that contains the products to order
            This parameter is mutually exclusive with the product and amount parameters

        Returns
        -------
        OrderEntity
            The order entity that was placed
        """
        order = OrderEntity(
            product_name=product_name,
            product_attribute=product_attribute,
            date_time=date_time,
            location=location,
            amount=amount,
            shopping_list_name=shopping_list_name,
        )
        data_model = DataModel()
        data_model.append(order)
        return order
