import os, sys
import settings

base_dir = settings.BASE_DIR

for i in range(1, len(sys.argv)):
    migration_file_path = f"{base_dir}/{sys.argv[i]}/migrations"
    pycache_file_path = f"{base_dir}/{sys.argv[i]}/migrations/__pycache__"
    for file in os.listdir(migration_file_path):
        if os.path.isfile(f"{migration_file_path}/{file}") and file != '__init__.py':
            os.remove(f"{migration_file_path}/{file}")
    print("-----------------")
    for file in os.listdir(pycache_file_path):
        if os.path.isfile(f"{pycache_file_path}/{file}") and file != '__init__.cpython-38.pyc':
            os.remove(f"{pycache_file_path}/{file}")

print("Migrations deleted successfully")