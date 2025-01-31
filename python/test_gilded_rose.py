# -*- coding: utf-8 -*-
import pytest
from gilded_rose import GildedRose, Item


@pytest.fixture
def normal_item():
    """Fixture for a normal item."""
    return Item("Normal Item", 10, 20)


@pytest.fixture
def aged_brie():
    """Fixture for Aged Brie."""
    return Item("Aged Brie", 2, 0)


@pytest.fixture
def backstage_pass():
    """Fixture for Backstage Passes."""
    return Item("Backstage passes to a TAFKAL80ETC concert", 10, 20)


@pytest.fixture
def conjured_item():
    """Fixture for Conjured items."""
    return Item("Conjured", 5, 10)


@pytest.fixture
def sulfuras():
    """Fixture for Sulfuras."""
    return Item("Sulfuras, Hand of Ragnaros", 5, 80)


def test_standard_item(normal_item):
    """Normal items decrease in quality and sell_in over time."""
    gilded_rose = GildedRose([normal_item])
    gilded_rose.update_quality()
    assert normal_item.sell_in == 9
    assert normal_item.quality == 19


def test_aged_brie_increases_in_quality(aged_brie):
    """Aged Brie increases in quality as it ages."""
    gilded_rose = GildedRose([aged_brie])
    gilded_rose.update_quality()
    assert aged_brie.quality == 1


def test_backstage_passes(backstage_pass):
    """Backstage passes increase in quality but drop to 0 after the event."""
    gilded_rose = GildedRose([backstage_pass])
    gilded_rose.update_quality()
    assert backstage_pass.quality == 22  # +2 because sell_in ≤ 10


def test_conjured_items_degrade_twice_as_fast(conjured_item):
    """Conjured items lose quality twice as fast."""
    gilded_rose = GildedRose([conjured_item])
    gilded_rose.update_quality()
    assert conjured_item.quality == 8  # -2 quality


def test_sulfuras_does_not_change(sulfuras):
    """Sulfuras does not change in quality or sell_in."""
    gilded_rose = GildedRose([sulfuras])
    gilded_rose.update_quality()
    assert sulfuras.quality == 80
    assert sulfuras.sell_in == 5


@pytest.mark.parametrize(
    "item_name, sell_in, quality, expected_sell_in, expected_quality",
    [
        ("Normal Item", 10, 20, 9, 19),
        ("Aged Brie", 2, 0, 1, 1),
        ("Backstage passes to a TAFKAL80ETC concert", 10, 20, 9, 22),
        ("Conjured", 5, 10, 4, 8),
        ("Sulfuras, Hand of Ragnaros", 5, 80, 5, 80),  # Should not change
    ],
)
def test_items(item_name, sell_in, quality, expected_sell_in, expected_quality):
    """Test multiple item types using parameterization."""
    item = Item(item_name, sell_in, quality)
    gilded_rose = GildedRose([item])
    gilded_rose.update_quality()
    assert item.sell_in == expected_sell_in
    assert item.quality == expected_quality
