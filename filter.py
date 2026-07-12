import json
import urllib.request


SOURCE_URL = "https://9280.kstore.vip/wex.json"


SOURCE_FILE = "fish.json"

CONFIG_FILE = "config.json"

OUTPUT_FILE = "fish_clean.json"



def download_source():

    try:

        urllib.request.urlretrieve(
            SOURCE_URL,
            SOURCE_FILE
        )

        print("配置更新成功")

    except Exception as e:

        print(
            "下载失败:",
            e
        )



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


    remove = set(
        config["remove_sites"]
    )


    sites=[]


    for item in data["sites"]:


        if item["key"] in remove:

            continue


        sites.append(item)



    data["sites"]=sites


    return data



def main():


    download_source()


    config=load_json(
        CONFIG_FILE
    )


    data=load_json(
        SOURCE_FILE
    )


    result=filter_sites(
        data,
        config
    )


    save_json(
        OUTPUT_FILE,
        result
    )


    print(
        "完成生成:",
        OUTPUT_FILE
    )



if __name__=="__main__":

    main()
