import os
import shutil
import zipfile
import json

# def copy_and_rename_file(src, dst):
#     shutil.copy(src, dst)
#     print(f"Copied and renamed file from {src} to {dst}")

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
    output_path = "./output" 
    #read json.
    with open(extracted_path + "/project.json", 'r',encoding="UTF-8") as file:
        data = json.load(file)
    print(f"Read JSON data")

    #Create output directory.
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(output_path+"/Stage", exist_ok=True)
    os.makedirs(output_path+"/Sprites", exist_ok=True)

    #Start extract.
    print("------------------------------")
    print("Start extract.")

    for Obj in data["targets"]:
        print("----------"+Obj["name"]+"----------")
        print(f"Current costume: {Obj["costumes"][Obj["currentCostume"]]["name"]}")

        if Obj["isStage"]:#Stage
            os.makedirs(output_path+"/"+sanitize_name(Obj["name"]), exist_ok=True)
            for cos in Obj["costumes"]:
                src = os.path.join(extracted_path, cos["md5ext"])#./<sb3name>/md5ext
                dst = os.path.join(output_path, sanitize_name(Obj["name"]), sanitize_name(cos["name"]).replace("?","_") + os.path.splitext(cos["md5ext"])[1])#./output/<stage name>/<costume name>.<ext>
                shutil.copy(src, dst)
                print(f"Processed: {src} to {dst}")

        else:#Sprite
            os.makedirs(output_path+"/Sprites/"+sanitize_name(Obj["name"]), exist_ok=True)
            for cos in Obj["costumes"]:
                src = os.path.join(extracted_path, cos["md5ext"])#./<sb3name>/md5ext
                dst = os.path.join(output_path,"Sprites",sanitize_name(Obj["name"]), sanitize_name(cos["name"]).replace("?","_") + os.path.splitext(cos["md5ext"])[1])#./output/Sprite/<sprite name>/<costume name>.<ext>
                shutil.copy(src, dst)
                print(f"Processed: {src} to {dst}")