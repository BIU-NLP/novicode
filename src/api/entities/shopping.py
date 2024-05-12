from entities.resolvable import Resolvable
from entities.entity import Entity


class OrderEntity(Entity):
    """
    The OrderEntity class is used to represent an order. An order is made when a user purchases products.
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class ProductName(Entity, Resolvable):
    """
    The ProductName entity class is used to represent a product name. A product name can be a generic description
    of a product (like "shoes") or a specific product name (like "Nike Air Force 1").
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class ProductAttribute(Entity, Resolvable):
    """
    The ProductAttribute entity class is used to represent an attribute of a product. An attribute of a product
    allows the user to specify an attribute on a product. For example, "red (shoes)", "discounted (flat screen tv)"
    or "(peanut butter) in stock") (the product name appears in parentheses).
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class ProductEntity(Entity):
    """
    The ProductEntity class is used to represent a product. The find_products in the Shopping action class returns
    a list of this entity class.
    This class inherits from the Entity class.
    """

    pass


class ShoppingListName(Entity, Resolvable):
    """
    The ShoppingListName entity class is used to represent a shopping list name. For exmaple,
    "my shopping list" or "groceries".
    This class inherits from the Entity class and the Resolvable class.
    """

    pass


class ShoppingListEntity(Entity, Resolvable):
    """
    The ShoppingListEntity class is used to represent a shopping list. The find_shopping_list in the Shopping action class returns
    a list of this entity class.
    This class inherits from the Entity class.
    """

    pass
