# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Dict, List, Type


class InvalidItemError(Exception):
    """Custom exception for invalid item attributes."""
    pass


class Item:
    """Represents an item in the inventory."""

    def __init__(self, name: str, sell_in: int, quality: int) -> None:
        if not isinstance(name, str):
            raise InvalidItemError("Item name must be a string.")

        if not isinstance(sell_in, int) or not isinstance(quality, int):
            raise InvalidItemError("sell_in and quality must be integers.")

        if quality < 0:
            raise InvalidItemError("Quality cannot be negative.")

        if quality > 50 and name != "Sulfuras, Hand of Ragnaros":
            raise InvalidItemError("Quality cannot exceed 50 (except for Sulfuras).")

        self.name: str = name
        self.sell_in: int = sell_in
        self.quality: int = quality

    def __repr__(self) -> str:
        return f"{self.name}, {self.sell_in}, {self.quality}"


class ItemCategory(ABC):
    """Abstract base class for different item categories."""

    def __init__(self, item: Item) -> None:
        self.item: Item = item

    def update(self) -> None:
        """Updates item quality and sell_in values."""
        self.update_quality()
        self.update_sell_in()
        if self.item.sell_in < 0:
            self.handle_expired()

    def update_quality(self) -> None:
        """Default behavior: decrease quality by 1."""
        self.change_quality(-1)

    def update_sell_in(self) -> None:
        """Decreases sell_in value."""
        self.item.sell_in -= 1

    def handle_expired(self) -> None:
        """Default behavior when item is expired: further decrease quality."""
        self.change_quality(-1)

    def change_quality(self, amount: int) -> None:
        """Adjusts item quality within valid bounds (0 to 50)."""
        self.item.quality = max(0, min(50, self.item.quality + amount))


class AgedBrie(ItemCategory):
    """Aged Brie increases in quality over time."""

    def update_quality(self) -> None:
        self.change_quality(1)

    def handle_expired(self) -> None:
        self.change_quality(1)


class BackstagePasses(ItemCategory):
    """Backstage passes increase in quality, but drop to 0 after the event."""

    def update_quality(self) -> None:
        if self.item.sell_in > 10:
            self.change_quality(1)
        elif self.item.sell_in > 5:
            self.change_quality(2)
        elif self.item.sell_in > 0:
            self.change_quality(3)

    def handle_expired(self) -> None:
        self.item.quality = 0  # Drops to 0 after the concert


class Sulfuras(ItemCategory):
    """Sulfuras is a legendary item that never changes."""

    def update_quality(self) -> None:
        pass  # No change in quality

    def update_sell_in(self) -> None:
        pass  # No change in sell_in

    def handle_expired(self) -> None:
        pass  # No change when expired


class Conjured(ItemCategory):
    """Conjured items degrade in quality twice as fast."""

    def update_quality(self) -> None:
        self.change_quality(-2)

    def handle_expired(self) -> None:
        self.change_quality(-2)


class GildedRose:
    """Main class managing all items in the inventory."""

    ITEM_CATEGORIES: Dict[str, Type[ItemCategory]] = {
        "Aged Brie": AgedBrie,
        "Backstage passes to a TAFKAL80ETC concert": BackstagePasses,
        "Sulfuras, Hand of Ragnaros": Sulfuras,
        "Conjured": Conjured,
    }

    def __init__(self, items: List[Item]) -> None:
        self.items: List[Item] = items

    def update_quality(self) -> None:
        """Updates all items in the inventory."""
        for item in self.items:
            item_class = self.ITEM_CATEGORIES.get(item.name, ItemCategory)

            if item_class is ItemCategory:
                print(f"Warning: '{item.name}' is an unrecognized item type.")

            try:
                item_category = item_class(item)
                item_category.update()
            except Exception as e:
                print(f"Error updating item '{item.name}': {e}")
