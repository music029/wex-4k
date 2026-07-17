import json
import urllib.request


CONFIG_FILE = "config.json"
OUTPUT_FILE = "fish.json"



def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_json(file, data):

    with open(
        file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )



def download_json(url):

    print("下载接口:")
    print(url)


    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )


    with urllib.request.urlopen(
        req,
        timeout=30
    ) as r:

        text = r.read().decode(
            "utf-8"
        )


    return json.loads(text)



def get_order(key, order_list):

    for i, item in enumerate(order_list):

        if key == item:

            return i

    return 999



def sort_site(site, config):

    key = site.get(
        "key",
        ""
    )


    # 功能

    index = get_order(
        key,
        config.get(
            "function_order",
            []
        )
    )

    if index != 999:

        return (
            0,
            index
        )



    # 4K

    index = get_order(
        key,
        config.get(
            "fourk_order",
            []
        )
    )

    if index != 999:

        return (
            1,
            index
        )



    # 影视

    index = get_order(
        key,
        config.get(
            "movie_order",
            []
        )
    )

    if index != 999:

        return (
            2,
            index
        )



    # 其它

    index = get_order(
        key,
        config.get(
            "other_order",
            []
        )
    )

    if index != 999:

        return (
            3,
            index
        )


    return (
        9,
        999
    )



def main():

    config = load_json(
        CONFIG_FILE
    )


    data = download_json(
        config["source_url"]
    )


    old_sites = data.get(
        "sites",
        []
    )


    print(
        "原始站点:",
        len(old_sites)
    )


    keep = set(
        config.get(
            "keep_sites",
            []
        )
    )


    rename = config.get(
        "rename_by_key",
        {}
    )


    new_sites = []

    seen = set()



    for site in old_sites:


        key = site.get(
            "key",
            ""
        )


        if not key:

            continue


        if key in seen:

            continue


        seen.add(key)



        if key not in keep:

            continue



        if key in rename:

            site["name"] = rename[key]



        new_sites.append(site)



    new_sites.sort(
        key=lambda x:
        sort_site(
            x,
            config
        )
    )



    if len(new_sites) < config.get(
        "min_sites",
        0
    ):

        raise Exception(
            f"站点数量异常: {len(new_sites)}"
        )



    data["sites"] = new_sites



    save_json(
        OUTPUT_FILE,
        data
    )



    print("================")

    print(
        "最终保留:",
        len(new_sites)
    )


    for s in new_sites:

        print(
            s["key"],
            s["name"]
        )


    print("================")



if __name__ == "__main__":

    main()
