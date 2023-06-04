import requests
# import pandas as pd
from collections import defaultdict
from tabulate import tabulate
from time import sleep
import json
from tqdm import tqdm
from os import system

def get_info(app_id):
    main = []
    dlc = []
    
    country = ['us', 'id', 'ar', 'tr', 'ua']
    # country = ['us'] # test purpose

    # Download the JSON file
    for x in country:
        url = f'https://store.steampowered.com/api/appdetails?appids={app_id}&cc={x}'
        response = requests.get(url)
        data = response.json()
        # main_datas
        name = data[app_id]["data"]["name"]
        # extract the information
        package_groups = data[app_id]["data"]["package_groups"]
        main_data = []
        dlc_data = []

        for group in tqdm(package_groups, desc = f"Getting {name} Data in {x.upper()}"):
            subs = group["subs"]
            for sub in subs:
                main_data.append({
                    "percent_savings_text": sub["percent_savings_text"],
                    "option_text": sub["option_text"].rsplit("-", 1)[0].strip(),
                    "price_with_discount": sub["price_in_cents_with_discount"] / 100
                })

        # for i in tqdm(range(0, 100), desc ="Scrapping SteamAPI"):
        try:
            for dlc_id in tqdm(data[app_id]["data"]["dlc"], desc = f"Getting {name} DLC Data in {x.upper()}"):
                url = f'https://store.steampowered.com/api/appdetails?appids={dlc_id}&cc={x}'
                response = requests.get(url)
                data = response.json()
                try:
                    # Process the data for each DLC ID as needed
                    data = data[str(dlc_id)]['data']
                    dlc_data.append({
                        "percent_savings_text": '' if data['price_overview']['discount_percent'] is None else data['price_overview']['discount_percent'],
                        "option_text": data['name'],
                        "price_with_discount": data['price_overview']['final'] / 100
                    })
                except KeyError:
                    # Process the data for each DLC ID as needed
                    try:
                        dlc_data.append({
                            "percent_savings_text": data["package_groups"][0]["subs"][0]["percent_savings_text"],
                            "option_text": data['name'],
                            "price_with_discount": data["package_groups"][0]["subs"][0]["price_in_cents_with_discount"] / 100
                        })
                    except:
                        dlc_data.append({
                            "percent_savings_text": '',
                            "option_text": 'no dlc' if data['name'] is None else data['name'],
                            "price_with_discount": 0
                        })
                        sleep(.05)
        except KeyError:
            dlc_data.append({
                "percent_savings_text": '',
                "option_text": 'no dlc',
                "price_with_discount": 0
            })
            sleep(.05)

        main_data = dict({x: main_data})
        dlc_data = dict({x: dlc_data})
        # addon_data = dict({x: addon_data})
        # main_datas.clear()
        main.append(main_data)
        dlc.append(dlc_data)
    sleep(.05)
    system('clear')
    # print(main)
    # print(dlc)
    return main, dlc


def get_table(key, main_datas):
    table_data = []
    updated_data = []
    combined_data = {}
    discount_data = {}
    multipliers = [14844, 1, 64, 753, 402] #forex purpose

    for piece in main_datas:
        for country, items in piece.items():
            for item in items:
                row = [
                    item["option_text"],
                    item["percent_savings_text"],
                    int(item["price_with_discount"])
                ]
                table_data.append(row)

    for item in table_data:
        updated_text = item[0]
        updated_item = [updated_text] + item[1:]
        updated_data.append(updated_item)

    for item in updated_data:
        name = item[0]
        discount = item[1]
        # print(discount)
        if discount == 0 or '' or '  ' :
            discount = ''
        elif discount in range(1,100):
            discount = str(f'( -{item[1]}% )')
        elif isinstance(discount, str) or not ' ':
            discount = str(f'( {item[1]})')
        
        discount = discount if discount != 0 else ''
        # print(discount)

        if name in combined_data:
            combined_data[name].append(item[2])
        else:
            combined_data[name] = [item[2]]
            
        if name in discount_data:
            discount_data[name].append(discount)
        else:
            discount_data[name] = [discount]
    for values in combined_data.values():
        for i in range(len(values)):
            values[i] *= multipliers[i]

    table = []

    headers = ["Game" if key == "game" else "DLC", "USD", "IDR", "ARS", "TRY", "UAH"]

    # headers = ["Game" if key == "game" else "DLC", "USD"]
    # print(f'its discount_data >{discount_data}<')
    for name, prices in combined_data.items():
        discounts = discount_data[name]
        # print(discount)
        table.append([name] + ["Free" if prices[0] == 0 else "Rp. {:,} {}".format(price, discount) for price, discount in zip(prices, discounts)])

    table = [[sublist[0]] + [num for num in sublist[1:]] for sublist in table]

    result = tabulate(table, headers=headers, tablefmt="fancy_grid", intfmt=",")
    return result


def table_result(app_id):
    system('clear')
    game, dlc = get_info(app_id)
    data = {'game':game, 'dlc':dlc}
    x = []
    for key, value in data.items():
        # print(get_table(key, value))
        x.append(get_table(key, value))
    return x
for x in table_result('1501750'):
    print(x)