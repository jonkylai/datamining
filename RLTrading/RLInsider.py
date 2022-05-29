import time
import requests
import re

import pandas as pd


def get_price_list(url: str):
    #time.sleep(2) # Needed when network slow
    response = requests.get(url) # Alternate method instead of webdriver
    html = response.text.replace('\n', '')
    price_list = re.findall("hoverSettingsLabel[^0-9]*([0-9]+)", html)
    return price_list


def main():
    start_time = time.time()

    # Extracted from BakkesMod
    df = pd.read_csv("inventory.csv", encoding = "ISO-8859-1")
    df.drop(df[df["tradeable"] == False].index, inplace=True)
    df.drop(df[df["slot"] == "Blueprint"].index, inplace=True)
    df.drop(df[df["slot"] == "Antenna"].index, inplace=True)
    df.drop(df[df["crate"] == "Season reward"].index, inplace=True)
    df = df.sort_values(by="instanceid", ascending=False) # Newest to oldest
    length = len(df)

    #df = df.iloc[100:, :] # Drop first N rows for debugging
    #pd.set_option('display.max_columns', None)
    #print(df)
    #exit()

    f = open("inventory_insider.csv", "w")
    header_list = list()
    for col in df.columns:
        header_list.append(col)
    header_string = ",".join(header_list) + ",Credits"
    f.write(header_string)

    i = 0
    for index, row in df.iterrows():
        i += 1
        progress = '{}/{}'.format(i, length)
        print(progress)
        row_string = '\n' + ','.join([x.strip() for x in row.to_string(header=False, index=False).split('\n')])

        # First try without slot type specifier
        name = re.sub('[^0-9a-zA-Z]+', '_', row["name"].lower()).strip('_')
        name = special_rename(name)
        url = 'http://rl.insider.gg/en/pc/{}'.format(name + paint2str(row["paint"]))
        price_list = get_price_list(url)
        if name in EXCEPTION_CASES:
            print(progress, url, 'skipped using manual exception')
            f.write(row_string + ",")
            continue

        if len(price_list) == 0:
            #print(progress, url, 'skipped')

            # Second try with slot type specifier
            slot_name = name + slot2str(row["slot"])
            url = 'http://rl.insider.gg/en/pc/{}'.format(slot_name + paint2str(row["paint"]))
            price_list = get_price_list(url)

            # Check if white version exists, if it does then BakkesMod thinks it's tradeable when it's not
            if len(price_list) == 0:
                url = 'http://rl.insider.gg/en/pc/{}'.format(name + "/white")
                price_list = get_price_list(url)
                if len(price_list) > 0:
                    print(progress, url[:-5], 'skipped non painted exception')
                    f.write(row_string + ",")
                    continue
                url = 'http://rl.insider.gg/en/pc/{}'.format(slot_name + "/white")
                price_list = get_price_list(url)
                if len(price_list) > 0:
                    print(progress, url[:-5], 'skipped non painted exception')
                    f.write(row_string + ",")
                    continue
                print(progress, url[:-5], 'fail')
                f.write(row_string + ",")
                exit()

        #print(progress, url, 'success')
        price = price_list[0] # 0 = All origins, 1 = Not from Series, 2 = From Series, 3 = Blueprint value, 4 = Crafting cost
        f.write(row_string + "," + price)

    print("Done writing to inventory_insider.csv")
    f.close()
    print("Elapsed time = {} minutes".format((time.time()-start_time)/float(60)))


def special_rename(name: str) -> str:
    if name == "blade_wave":
        return "blade_wave_2020"
    elif name == "backfire_cruster_buster":
        return "cruster_buster"
    elif name == "y_o_u":
        return "y_o_u_"
    elif name == "disc_bliss":
        return "disco_bliss"
    elif name == "nomad_blinkpad":
        return "blinkpad"
    elif name == "backfire_greatgrid":
        return "greatgrid"
    elif name == "breakout_type_s_s_mored":
        return "breakout_type_s_smored"
    elif name == "j_ger_619":
        return "jager_619"
    elif name == "j_ger_619_snakeskin":
        return "jager_619_snakeskin"
    else:
        return name


EXCEPTION_CASES = [
    "vortex", # Ignore the 3 rarities associated with wheel
    "stern",  # Ignore the 3 rarities associated with wheel
    "falco",  # Ignore the 3 rarities associated with wheel
    "paladin",  # Ignore the 3 rarities associated with body/avatar
    "hotshot",  # Ignore the 2 rarities associated with body
    "tunica",  # Ignore the 2 rarities associated with wheel
    "short_fuse",
    "shen_avatar",
    "top_llama_me",
    "shen",
    "ski_free",
    "invader",
]


def slot2str(slot: str) -> str:
    if slot == "Animated Decal":
        return "_decal"
    if slot == "Antenna":
        return "_antenna"
    elif slot == "Avatar Border":
        return "_avatar_border"
    elif slot == "Body":
        return "_body"
    elif slot == "Crate":
        return "_crate"
    elif slot == "Decal":
        return "_decal"
    elif slot == "Goal Explosion":
        return "_goal_explosion"
    elif slot == "Player Banner":
        return "_banner"
    elif slot == "Rocket Boost":
        return "_boost"
    elif slot == "Topper":
        return "_topper"
    elif slot == "Trail":
        return "_trail"
    elif slot == "Wheels":
        return "_wheels"
    else:
        raise Exception("Slot name {} not defined".format(slot))


def paint2str(paint: str) -> str:
    if paint == "none":
        return "/"
    elif paint == "Black":
        return "/black"
    elif paint == "Burnt Sienna":
        return "/sienna"
    elif paint == "Cobalt":
        return "/cobalt"
    elif paint == "Crimson":
        return "/crimson"
    elif paint == "Forest Green":
        return "/fgreen"
    elif paint == "Grey":
        return "/grey"
    elif paint == "Lime":
        return "/lime"
    elif paint == "Orange":
        return "/orange"
    elif paint == "Pink":
        return "/pink"
    elif paint == "Purple":
        return "/purple"
    elif paint == "Saffron":
        return "/saffron"
    elif paint == "Sky Blue":
        return "/sblue"
    elif paint == "Titanium White":
        return "/white"
    else:
        raise Exception("Paint color {} not defined".format(paint))


if __name__ == "__main__":
    main()

