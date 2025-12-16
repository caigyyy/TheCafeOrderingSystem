from __future__ import annotations
from typing import Any
from menu_items import MenuItem, FoodItem, DrinkItem


class MenuItemFactory:
    """
    Mirrors the diagram idea: createMenuItem(type, id, name, price, ...)
    """
    @staticmethod
    def create_menu_item(type: str, **kwargs: Any) -> MenuItem:
        t = type.strip().lower()
        if t in ("food", "fooditem"):
            return FoodItem(**kwargs)
        if t in ("drink", "drinkitem"):
            return DrinkItem(**kwargs)
        raise ValueError(f"Unknown menu item type: {type}")
