import json


def backup(xlink):
    with open("backup.json", "r", encoding="utf-8", errors="ignore") as file:
        # Load the JSON data
        dataSave = json.load(file)

    with open(xlink + ".json", "r", encoding="utf-8", errors="ignore") as file:
        # Load the JSON data
        data = json.load(file)

    dataSave += data

    json_data = json.dumps(dataSave, indent=4, ensure_ascii=False)

    with open("backup.json", "w", encoding="utf-8", errors="ignore") as json_file:
        json_file.write(json_data)
