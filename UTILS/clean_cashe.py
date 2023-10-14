import os
import shutil

def cleanup_cache():
    project_root = os.getcwd()  # Получаем корневую папку проекта
    folders_to_clear = [project_root, "API", "ENGIN", "MONEY", "UTILS"]

    for folder in folders_to_clear:
        folder_path = os.path.join(project_root, folder)
        pycache_path = os.path.join(folder_path, "__pycache__")

        if os.path.exists(pycache_path):
            shutil.rmtree(pycache_path)
            # print(f"Удален кеш из {pycache_path}")

# cleanup_cache()
# python -m UTILS.clean_cashe
