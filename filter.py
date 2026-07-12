import json
import urllib.request
import os


# 原始配置地址
SOURCE_URL = "https://9280.kstore.vip/wex.json"


# 本地文件
SOURCE_FILE = "fish.json"

CONFIG_FILE = "config.json"

OUTPUT_FILE = "fish_clean.json"



def download_source():

    try:

        print("正在下载最新配置...")

        urllib.request.urlretrieve(
            SOURCE_URL,
            SOURCE_FILE
        )

        print("下载完成:", SOURCE_FILE)


    except Exception as e:

        print(
            "下载失败:",
            e
        )

        exit()



def load_json(file):

    with open(
        file,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)



def save_json(file,data):

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



def filter_sites(data,config):


    remove_sites = set(
        config.get(
            "remove_sites",
            []
        )
    )


    rename_sites = config.get(
        "rename_sites",
        {}
    )


    new_sites = []


    for site in data.get(
        "sites",
        []
    ):


        key = site.get(
            "key",
            ""
        )


        name = site.get(
            "name",
            ""
        )


        # 删除站点
        if (
            key in remove_sites
            or
            name in remove_sites
        ):

            print(
                "删除:",
                name
            )

            continue



        # 修改名称
        if key in rename_sites:

            site["name"] = rename_sites[key]


        new_sites.append(site)



    data["sites"] = new_sites


    return data



def main():


    # 1.下载最新配置

    download_source()



    # 2.读取规则

    config = load_json(
        CONFIG_FILE
    )



    # 3.读取源配置

    data = load_json(
        SOURCE_FILE
    )



    # 4.过滤

    result = filter_sites(
        data,
        config
    )



    # 5.输出

    save_json(
        OUTPUT_FILE,
        result
    )



    print("===================")

    print(
        "过滤完成"
    )

    print(
        "输出文件:",
        OUTPUT_FILE
    )

    print(
        "剩余站点:",
        len(
            result.get(
                "sites",
                []
            )
        )
    )



if __name__ == "__main__":

    main()
