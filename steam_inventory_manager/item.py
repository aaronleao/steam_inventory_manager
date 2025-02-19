"""This module contains the class to represent an inventory item."""

# import sys
from steam_inventory_manager import constants
# from steam_inventory_manager import steam_api_handler


class Item:
    """
    This class represents an inventory item.
    It provides methods to extract and display relevant information
    from the item description.
    """

    def __init__(self, item_description: dict):
        if not item_description:
            raise SystemExit("Inventory: Invalid item_description")

        # Steam Inventory Item keys
        self.appid = item_description.get('appid')
        self.classid = item_description.get('classid')
        self.instanceid = item_description.get('instanceid')
        self.currency = item_description.get('currency')
        self.background_color = item_description.get('background_color')
        self.icon_url = item_description.get('icon_url')
        self.icon_url_large = item_description.get('icon_url_large')
        self.descriptions = item_description.get('descriptions')
        self.tradable = item_description.get('tradable')
        self.name = item_description.get('name')
        self.name_color = item_description.get('name_color')
        self.type = item_description.get('type')
        self.market_name = item_description.get('market_name')
        self.market_hash_name = item_description.get('market_hash_name')
        self.commodity = item_description.get('commodity')
        self.market_tradable_restriction = item_description.get('market_tradable_restriction')
        self.market_marketable_restriction = item_description.get('market_marketable_restriction')
        self.marketable = item_description.get('marketable')
        self.tags = item_description.get('tags')

        # Custom Inventory Item keys
        self.lowest_price = item_description.get('lowest_price')
        self.median_price = item_description.get('median_price')
        self.volume = item_description.get('volume')
        self.descriptions = item_description.get("descriptions")
        self.description_values = self.get_descriptions_values()
        [self.type_desc, self.type_desc_name] = self.set_item_type()
        self.may_be_gifted_once = self.set_is_gifted_once()


        # if self.marketable and api_key:
        #     self.fetch_steam_maket_price(api_key)

    def print(self, display_full_inventory: bool=False):
        """
        Prints the item description.
        """
        may_be_gifted_once = "1" if self.may_be_gifted_once else "0"
        line = f"{self.type_desc: <12}|{self.marketable: <2}|{self.tradable: <2}|{may_be_gifted_once: <2}|{self.market_name: <40}|{self.market_hash_name: <40}|{self.type_desc_name: <30}|{self.type: <30}|{self.name: <60}|"
        if (
            not display_full_inventory
            and (self.type_desc == constants.ItemType.HERO.name
            or self.type_desc == constants.ItemType.MISC.name)
        ):
            return
        print(line)


    def set_is_gifted_once(self) -> bool:
        """
        Return if the item may be gifted once
        """
        if self.description_values is not None:
            for value in self.description_values:
                if  "This item may be gifted once" in value:
                    return True
            return False

    def get_descriptions_values(self):
        """Returns the values of the descriptions."""

        if self.descriptions is not None:
            values = [d["value"] for d in self.descriptions if "value" in d]
            return values
        return None

    def is_hero(self, description_values: list) -> str:
        """Returns if it is a HERO item"""
        if not description_values:
            return None

        return [
            value.split(":")[1].strip()
            for value in description_values
            if value.startswith("Used By:")
        ]

    def is_weather(self, item_type: str) -> bool:
        """Returns if it is a WEATHER item"""
        if item_type and "Weather" in item_type:
            return True
        return False

    def is_bundle(self, item_type: str) -> bool:
        """Returns if it is a BUNDLE item"""
        if item_type and "Bundle" in item_type:
            return True
        return False

    def is_ward(self, item_type: str) -> bool:
        """Returns if it is a WARD item"""
        if item_type and "Ward" in item_type:
            return True
        return False

    def is_courier(self, item_type: str) -> bool:
        """Returns if it is a COURIER item"""
        if item_type and "Courier" in item_type:
            return True
        return False

    def set_item_type(self):
        """
        Returns the item type based on the description type.
        The sequence of checks is important.
        1. Check if it is a courier
        2. Check if it is a weather effect
        3. Check if it is a ward
        4. Check if it is a hero
        5. Check if it is a hero bundle
        6. Check if it is a bundle
        7. If none of the above, it is a misc item
        """

        if self.is_courier(self.type):
            return [constants.ItemType.COURIER.name, constants.ItemType.COURIER.value]

        if self.is_weather(self.type):
            return [constants.ItemType.WEATHER.name, constants.ItemType.WEATHER.value]

        if self.is_ward(self.type):
            return [constants.ItemType.WARD.name, constants.ItemType.WARD.value]

        hero = self.is_hero(self.description_values)
        if hero:
            if self.is_bundle(self.type):
                return [constants.ItemType.HERO_BUNDLE.name, hero[0]]
            return [constants.ItemType.HERO.name, hero[0]]

        if self.is_bundle(self.type):
            return [constants.ItemType.BUNDLE.name, constants.ItemType.BUNDLE.value]

        return [constants.ItemType.MISC.name, constants.ItemType.MISC.value]

    # def fetch_steam_maket_price(self, api_key: str):
    #     """
    #     Fetch Item Market price
    #     """
    #     return
        # if self.marketable:
        #     [self.lowest_price,
        #      self.median_price,
        #      self.volume] = steam_api_handler.fetch_steam_market_item_price(api_key,
        #                                                                      self.appid,
        #                                                                      self.market_hash_name)
