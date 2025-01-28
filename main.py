import os
import shutil
import zipfile
import json

def extract_zip(zip_path)->str:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(zip_path.replace(".sb3", ""))
    print(f"Extracted {zip_path}.")
    return zip_path.replace(".sb3", "")

dangerous_chars = ["?", ":", "*", "<", ">", "|", "\\", "/"]
def sanitize_name(name: str) -> str:
    for char in dangerous_chars:
        name = name.replace(char, "_")
    return name

if __name__ == "__main__":
    #initialize.
    extracted_path = extract_zip(input("sb3Path: "))
    cos_output_path = "./output/costumes" 
    waw_output_path = "./output/sounds"
    #read json.
    with open(extracted_path + "/project.json", 'r',encoding="UTF-8") as file:
        data = json.load(file)
    print(f"Read JSON data")

    #Create output directory.
    os.makedirs(cos_output_path, exist_ok=True)
    os.makedirs(cos_output_path+"/Stage", exist_ok=True)
    os.makedirs(cos_output_path+"/Sprites", exist_ok=True)

    #Start extract.
    print("")
    print("------------------------------")
    print("Start extract costumes.")

    for Obj in data["targets"]:
        print("----------"+Obj["name"]+"----------")
        print(f"Current costume: {Obj["costumes"][Obj["currentCostume"]]["name"]}")

        if Obj["isStage"]:#Stage
            if len(Obj["costumes"]) == 0:
                print(f"Stage {Obj["name"]} has no costume.")
                continue
            os.makedirs(cos_output_path+"/"+sanitize_name(Obj["name"]), exist_ok=True)
            for cos in Obj["costumes"]:
                src = os.path.join(extracted_path, cos["md5ext"])#./<sb3name>/<md5ext>
                dst = os.path.join(cos_output_path, sanitize_name(Obj["name"]), sanitize_name(cos["name"]) + os.path.splitext(cos["md5ext"])[1])#./output/costumes/<stage name>/<costume name>.<ext>
                shutil.copy(src, dst)
                print(f"Processed: {src} to {dst}")

        else:#Sprite
            if len(Obj["costumes"]) == 0:    
                print(f"Sprite {Obj["name"]} has no costume.")
                continue
            os.makedirs(cos_output_path+"/Sprites/"+sanitize_name(Obj["name"]), exist_ok=True)
            for cos in Obj["costumes"]:
                src = os.path.join(extracted_path, cos["md5ext"])#./<sb3name>/<md5ext>
                dst = os.path.join(cos_output_path,"Sprites",sanitize_name(Obj["name"]), sanitize_name(cos["name"]) + os.path.splitext(cos["md5ext"])[1])#./output/costumes/Sprite/<sprite name>/<costume name>.<ext>
                shutil.copy(src, dst)
                print(f"Processed: {src} to {dst}")
    
    os.makedirs(waw_output_path, exist_ok=True)
    
    print("")
    print("------------------------------")
    print("Start extract sounds.")

    for Obj in data["targets"]:
        print("----------"+Obj["name"]+"----------")
        if len(Obj["sounds"]) == 0:
            print(f"{Obj["name"]} has no sound.")
            continue
        os.makedirs(waw_output_path+"/"+sanitize_name(Obj["name"]), exist_ok=True)
        for sound in Obj["sounds"]:
            src = os.path.join(extracted_path, sound["md5ext"])#./<sb3name>/<md5ext>
            dst = os.path.join(waw_output_path,sanitize_name(Obj["name"]), sanitize_name(sound["name"]) + os.path.splitext(sound["md5ext"])[1])#./output/sounds/<sound name>.<ext>
            shutil.copy(src, dst)
            print(f"Processed: {src} to {dst}")