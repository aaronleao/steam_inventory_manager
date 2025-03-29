"""This module contains the class definition."""

# import json
import logging
import os
import sys
from datetime import datetime
from steam_inventory_manager import constants
from steam_inventory_manager import filesystem_handler
from steam_inventory_manager import steam_api_handler
from steam_inventory_manager import item

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__package__)


class Player:
    """
    This class represents an inventory from a player item.
    """

    def __init__(
        self,
        api_key: str,
        steam_id: str,
        overwrite: bool = False,
        app_id: str = constants.APP_NAME,
        steam_user: str = None,
    ):
        """
        Initialize the player data.
        """

        self.app_id = app_id
        self.steam_id = (
            steam_id
            if steam_id is not None and steam_user is None
            else steam_api_handler.resolve_vanity(api_key, steam_user)
        )
        self.steam_user = ""
        self.player_json_path = self.get_player_summaries_path(self.steam_id)
        self.inventory_json_path = self.get_inventory_json_path(
            self.steam_id, self.app_id
        )
        self.persona_name = ""
        self.profile_url = ""
        self.avatar = ""
        self.avatar_medium = ""
        self.avatar_full = ""
        self.avatar_hash = ""
        self.persona_state = ""
        self.persona_state_flags = ""
        self.community_visibility_state = ""
        self.profile_state = ""
        self.last_logoff = ""
        self.comment_permission = ""
        self.real_name = ""
        self.primary_clan_id = ""
        self.time_created = ""
        self.game_id = ""
        self.game_extrainfo = ""
        self.city_id = ""
        self.state_code = ""
        self.country_code = ""
        self.loc_country_code = ""
        self.loc_state_code = ""

        # Load summaries
        self.player_summaries = self.fetch_summaries(api_key, overwrite)
        self.load_info()
        # Load inventory
        self.inventory = []
        self.inventory_json = self.fetch_inventory(api_key, overwrite)
        self.inventory_json_assets = self.inventory_json.get("assets")
        self.inventory_json_descriptions = self.inventory_json.get("descriptions")
        self.load_inventory()

    def print(self):
        """
        Print the player summaries.
        """
        print(f"Steam ID: {self.steam_id}")
        print(f"Steam user: {self.steam_user}")
        print(f"player_json_path: {self.player_json_path}")
        print(f"inventory_json_path: {self.inventory_json_path}")
        print(f"Persona name: {self.persona_name}")
        print(f"Profile URL: {self.profile_url}")
        print(f"Avatar: {self.avatar}")
        print(f"Avatar medium: {self.avatar_medium}")
        print(f"Avatar full: {self.avatar_full}")
        print(f"Avatar hash: {self.avatar_hash}")
        print(f"Persona state: {self.persona_state}")
        print(f"Persona state flags: {self.persona_state_flags}")
        print(f"Community visibility state: {self.community_visibility_state}")
        print(f"Profile state: {self.profile_state}")
        print(f"Last logoff: { datetime.fromtimestamp(self.last_logoff)}")
        print(f"Comment permission: {self.comment_permission}")
        print(f"Real name: {self.real_name}")
        print(f"Primary clan ID: {self.primary_clan_id}")
        print(f"Time created: {datetime.fromtimestamp(self.time_created)}")
        print(f"Game ID: {self.game_id}")
        print(f"Game extra info: {self.game_extrainfo}")
        print(f"City ID: {self.city_id}")
        print(f"State code: {self.state_code}")
        print(f"Country code: {self.country_code}")
        print(f"Location country code: {self.loc_country_code}")
        print(f"Location state code: {self.loc_state_code}")
        print("_" * 142, "\n")

    def get_player_summaries_path(self, steam_id: str):
        """
        Returns the file path for the player file.
        """
        player_file = f"{steam_id}_summaries.json"
        player_path = f"{constants.CACHE_DIR}/{player_file}"
        return player_path

    def get_inventory_json_path(self, steam_id: str, app_id: str):
        """
        Returns the file path for the inventory file.
        """
        inventory_file_name = f"{steam_id}_full_inventory_{app_id}.json"
        inventory_file_path = f"{constants.CACHE_DIR}/{inventory_file_name}"
        return inventory_file_path

    def fetch_summaries(self, api_key, overwrite):
        """
        Either fetch player summaries from disk or online
        Returns the player summaries.
        """
        if os.path.exists(self.player_json_path) and not overwrite:
            player_summaries = filesystem_handler.read_json(self.player_json_path)
            return player_summaries
        else:
            logger.info("Fetching player summaries online")
            player_summaries = steam_api_handler.fetch_player_summaries(
                api_key, self.steam_id
            )[0]
            filesystem_handler.write_json(self.player_json_path, player_summaries)
            return player_summaries

    def load_info(self):
        """
        Load info from summaries dict
        """
        self.persona_name = self.player_summaries.get("personaname")
        self.profile_url = self.player_summaries.get("profileurl")
        self.steam_user = self.get_user_name_from_url()
        self.avatar = self.player_summaries.get("avatar")
        self.avatar_medium = self.player_summaries.get("avatarmedium")
        self.avatar_full = self.player_summaries.get("avatarfull")
        self.avatar_hash = self.player_summaries.get("avatarhash")
        self.persona_state = self.player_summaries.get("personastate")
        self.persona_state_flags = self.player_summaries.get("personastateflags")
        self.community_visibility_state = self.player_summaries.get(
            "communityvisibilitystate"
        )
        self.profile_state = self.player_summaries.get("profilestate")
        self.last_logoff = self.player_summaries.get("lastlogoff")
        self.comment_permission = self.player_summaries.get("commentpermission")
        self.real_name = self.player_summaries.get("realname")
        self.primary_clan_id = self.player_summaries.get("primaryclanid")
        self.time_created = self.player_summaries.get("timecreated")
        self.game_id = self.player_summaries.get("gameid")
        self.game_extrainfo = self.player_summaries.get("gameextrainfo")
        self.city_id = self.player_summaries.get("cityid")
        self.state_code = self.player_summaries.get("statecode")
        self.country_code = self.player_summaries.get("countrycode")
        self.loc_country_code = self.player_summaries.get("loccountrycode")
        self.loc_state_code = self.player_summaries.get("locstatecode")

    def fetch_inventory(self, api_key, overwrite):
        """
        Either fetch player inventory from disk or online
        """
        if os.path.exists(self.inventory_json_path) and not overwrite:
            inventory = filesystem_handler.read_json(self.inventory_json_path)
            return inventory
        else:
            logger.info("Fetching player inventory online")
            inventory = steam_api_handler.fetch_inventory(
                self.steam_id, self.app_id, api_key, constants.CONTEXT_ID
            )
            filesystem_handler.write_json(self.inventory_json_path, inventory)
            return inventory

    def load_inventory(self):
        """
        Load inventory from inventory dict
        """
        self.inventory = [
            item.Item(item_description)
            for item_description in self.inventory_json_descriptions
        ]

    def print_inventory(self, args):
        """
        Print inventory items
        """
        inventory_to_print = self.get_filtered_inventory(args)
        for i in inventory_to_print:
            i.print(args)

    def update_inventory_json_descriptions(self):
        """
        Update Inventory JSON
        """
        for i in self.inventory:
            for d in self.inventory_json_descriptions:
                # print("update ", i.classid, d.get("classid"))
                if (i.classid == d.get("classid")) and (
                    i.instanceid == d.get("instanceid")
                ):
                    # print("update", i.classid, d.get("classid"), i.classid == d.get("classid"), i.instanceid, d.get("instanceid"), i.instanceid == d.get("instanceid"))
                    d["lowest_price"] = i.lowest_price
                    d["median_price"] = i.median_price
                    d["volume"] = i.volume

    def get_user_name_from_url(self):
        """
        Split Custom URL to get the username
        """
        return self.profile_url.split("/")[4]

    def get_filtered_inventory(self, args):
        """
        Return filtered inventory.
        1) Get the base inventory
        2) From the first selection aplly the secondary filters
        """

        inventory = self.get_inventory_full_or_filtered(args.display_inventory_full)

        if args.filter_by_hero:
            inventory = [item for item in inventory if item.match_hero(args.filter_by_hero)]
        if args.filter_by_type:
            inventory = [item for item in inventory if item.match_type(args.filter_by_type)]
        if args.filter_by_marketable:
            inventory = [item for item in inventory if item.marketable]
        if args.filter_by_tradable:
            inventory = [item for item in inventory if item.tradable]
        if args.filter_by_giftable:
            inventory = [item for item in inventory if item.may_be_gifted_once]

        return inventory
        

    # elif args.pattern_2:
    #     inventory = [item for item in base_inventory if pattern_2.match(item)]
    # else:
    #     inventory = base_inventory


    def get_inventory_full_or_filtered(self, display_inventory_full:bool = False):
        """
        Get all items or only default items
        1) Filter for full inventory: Get either all items of any type, or items NOT (MISC or HERO)
        """

        inventory = []
        if (display_inventory_full):
            inventory = self.inventory
        else:            
            for item in self.inventory:
                if (item.type_desc == constants.ItemType.HERO.name
                    or item.type_desc == constants.ItemType.MISC.name):
                    continue
                inventory.append(item)

        return inventory
