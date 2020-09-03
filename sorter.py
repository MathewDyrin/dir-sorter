import os
import hashlib
import json
import time

target_path = os.getcwd()
target_path_dirs_list = os.listdir(target_path)

video = {'avi', 'mp4', 'riff', 'vob', 'mpg', 'mov', '3gp', 'mkw'}
audio = {'mp3', 'm4a', 'wav'}
images = {'jpg', 'png', 'webp'}
package = {'zip', 'pkg', 'rar'}
executable = {'dmg', 'exe'}
torrents = {'torrent'}

paths = {
    "video_path": os.path.join(target_path, "Videos"),
    "audio_path": os.path.join(target_path, "Audios"),
    "images_path": os.path.join(target_path, "Images"),
    "package_path": os.path.join(target_path, "Packages"),
    "undetected_path": os.path.join(target_path, "Undetected"),
    "executable_path": os.path.join(target_path, "Executable"),
    "torrents_path": os.path.join(target_path, "Torrents")
}


def generate_dirs_hash_sum(dirs_list: list) -> str:
    hash_string_sum = ""
    for file_elem in dirs_list:
        hash_string_sum += str(file_elem)
    hash_sum = hashlib.sha256(str(hash_string_sum).encode('utf-8')).hexdigest()
    return hash_sum


def check_path(path: str):
    if not os.path.exists(paths[path]):
        os.mkdir(paths[path])


def sort_files():
    
    for file in target_path_dirs_list:
        if file == "sorter.py" or file == "runner.exe":
            continue
        if file == "Audios" or file == "Packages" or file == "Undetected" or file == "Videos" or file == "Executable" \
               or file == "Images" or file == "Torrents" or file.split('.')[-1].lower() == 'app':
            continue
        if file.split('.')[-1].lower() in video:
            check_path('video_path')
            os.replace(os.path.join(target_path, file), os.path.join(paths['video_path'], file))
            continue
        if file.split('.')[-1].lower() in audio:
            check_path('audio_path')
            os.replace(os.path.join(target_path, file), os.path.join(paths['audio_path'], file))
            continue
        if file.split('.')[-1].lower() in package:
            check_path('package_path')
            os.replace(os.path.join(target_path, file), os.path.join(paths['package_path'], file))
            continue
        if file.split('.')[-1].lower() in executable:
            check_path('executable_path')
            os.replace(os.path.join(target_path, file), os.path.join(paths['executable_path'], file))
            continue
        if file.split('.')[-1].lower() in images:
            check_path('images_path')
            os.replace(os.path.join(target_path, file), os.path.join(paths['images_path'], file))
            continue
        if file.split('.')[-1].lower() in torrents:
            check_path('torrents_path')
            os.replace(os.path.join(target_path, file), os.path.join(paths['torrents_path'], file))
            continue
        else:
            check_path('undetected_path')
            os.replace(os.path.join(target_path, file), os.path.join(paths['undetected_path'], file))

    tmp = os.getcwd().split("\\")[-1].lower()
    with open(f'/Users/{os.getlogin()}/dirstates/{tmp}.json', 'w') as f:
        json.dump(
            {"hash_sum": generate_dirs_hash_sum(target_path_dirs_list)}, f
        )

    print("Done.")


def check_hash():
    try:
        tmp = os.getcwd().split("\\")[-1].lower()
        with open(f'/Users/{os.getlogin()}/dirstates/{tmp}.json', 'r') as f:
            loaded_hash_sum = json.load(f)['hash_sum']
            if loaded_hash_sum == generate_dirs_hash_sum(target_path_dirs_list):
                print("No changes detected.")
            return loaded_hash_sum
    except:
        pass


saved_hash_sum = check_hash()


while True:
    target_path_dirs_list = os.listdir(target_path)
    if saved_hash_sum != generate_dirs_hash_sum(target_path_dirs_list):
        print("*************")
        print("Detected files struct changing. Sorting...")
        sort_files()
        saved_hash_sum = check_hash()

    time.sleep(1)
