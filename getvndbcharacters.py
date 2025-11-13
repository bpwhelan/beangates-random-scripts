import requests
import json

# Comment out fields you want/don't want to include
FIELDS_TO_GET = ['id',
                 'original',
                 'name',
                 'sex',
                 'birthday',
                 'height',
                 'bust', 'waist', 'hips', 'cup',
                #  'weight',
                #  'blood_type',
                #  'age',
                #  'example of field we want to not include',
                 ]


def get_vndb_data(vn_id):
    url = "https://api.vndb.org/kana/vn"
    headers = {"Content-Type": "application/json"}
    data = {
        "filters": ["id", "=", vn_id],
        "fields": "title,alttitle",
        "results": 1
    }

    response = requests.post(url, headers=headers, json=data)

    with open("vn_response.json", "w") as f:
        f.write(response.text)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Unable to fetch VN data from VNDB")
        return None


def get_vn_characters(vn_id):
    url = "https://api.vndb.org/kana/character"
    headers = {"Content-Type": "application/json"}
    data = {
        "filters": ["vn", "=", ["id", "=", vn_id]],
        "fields": ",".join(FIELDS_TO_GET),
        "results": 100
    }

    response = requests.post(url, headers=headers, json=data)

    with open("character_response.json", "w") as f:
        f.write(response.text)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Unable to fetch characters from VNDB")
        return None


def build_json(vn_id):
    vn_data = get_vndb_data(vn_id)
    characters = get_vn_characters(vn_id)

    print(vn_data)
    print(characters)

    if vn_data and characters:
        vn_name = vn_data['results'][0]['alttitle'] if vn_data['results'][0]['alttitle'] else vn_data['results'][0]['title']
        json_output = [vn_name]

        for char in characters['results']:
            surname_char = {}
            main_name_char = {}
            char_data = {
                "r": char['name'],
                # You can modify this to get more names or kanji if needed
                "s": [char['original']],
                "l": []
            }

            # Add additional info to the "l" field
            if char.get('original'):
                char_data["l"].append(f"Original: {char['original']}")
                if len(char.get('original').split(' ')) == 2 and len(char.get('name').split(' ')) == 2:
                    surname_char["r"] = char.get('name').split(' ')[0]
                    surname_char["s"] = [char.get('original').split(' ')[0]]
                    surname_char["l"] = [
                        f"(Surname), {char.get('name').split(' ')[0]}"]
                    main_name_char["r"] = char.get('name').split(' ')[1]
                    main_name_char["s"] = [char.get('original').split(' ')[1]]
                    if char.get('sex'):
                        sex = "Male" if 'm' in char['sex'] else "Female"
                        main_name_char["l"] = [
                            f"({sex}), {char.get('name').split(' ')[1]}"]
                    else:
                        main_name_char["l"] = [char.get('name').split(' ')[1]]
            if char.get('sex'):
                sex = "Male" if 'm' in char['sex'] else "Female"
                char_data["l"].append(f"Sex: {sex}")
            if char.get('birthday'):
                char_data["l"].append(
                    f"Birthday: {char['birthday'][0]}月{char['birthday'][1]}日")
            if char.get('height'):
                char_data["l"].append(f"Height: {char['height']}")
            if char.get('bust') and char.get('waist') and char.get('hips'):
                measurements = f"B/W/H: {char['bust']}/{char['waist']}/{char['hips']}"
                if char.get('cup'):
                    measurements += f", Cup Size: {char['cup']}"
                char_data["l"].append(measurements)
            if char.get('blood_type'):
                char_data["l"].append(f"Blood type: {char['blood_type']}")
            if char.get('age'):
                char_data["l"].append(f"Age: {char['age']}")
            # Add VN name to each character info
            char_data["l"].append(f"VN: {vn_name}")

            json_output.append(char_data)
            if surname_char:
                json_output.append(surname_char)
            if main_name_char:
                json_output.append(main_name_char)

        return json_output
    else:
        return None


def main():
    vn_id = input("Enter VNDB ID: ")
    json_result = build_json(vn_id)

    if json_result:
        print(json.dumps(json_result, indent=4, ensure_ascii=False))
        with open(f"{vn_id}.json", "w", encoding="utf-8") as f:
            json.dump(json_result, f, indent=4, ensure_ascii=False)
    else:
        print("Failed to generate JSON.")


if __name__ == "__main__":
    main()
