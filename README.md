# Steam Inventory Query

## Deps
```shell
pip 
pip install platformdirs
```

## Fetch Steam profile ID
[Profile ID finder](https://www.steamidfinder.com/)

## Fetch  Steam API Key
[Steam API Key](https://steamcommunity.com/dev/apikey)

## How to run
```shell
set env variable $steam_api_key
python steam_inventory_manager/cli.py --profile-id 123123123 --api-key AT328ATTE2888
```
<!-- python steam_inventory_manager/cli.py --profile-id $steam_profile_id --api-key $steam_api_key -->

## TODO

- [ ] Add option to display the whole inventory, HERO and MISC as well.
- [ ] Refactor display_inventory function
- [ ] Add Github actions to perform system level test
- [ ] Generate page with the inventory periodically