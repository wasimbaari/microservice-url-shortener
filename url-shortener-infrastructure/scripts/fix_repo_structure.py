import os
import shutil

# Project root (run script from infrastructure root)
ROOT_DIR = os.getcwd()

MODULES_DIR = os.path.join(ROOT_DIR, "modules")
ENV_DIR = os.path.join(ROOT_DIR, "environments", "dev")
SCRIPTS_DIR = os.path.join(ROOT_DIR, "scripts")

WRONG_MODULE_PATH = os.path.join(ROOT_DIR, "environments", "dev", "scripts", "modules", "eks")
WRONG_SCRIPTS_PATH = os.path.join(ROOT_DIR, "environments", "dev", "scripts")

CORRECT_EKS_MODULE_PATH = os.path.join(MODULES_DIR, "eks")

print("Starting Terraform repo structure fix...")

# Create required directories
os.makedirs(MODULES_DIR, exist_ok=True)
os.makedirs(SCRIPTS_DIR, exist_ok=True)

# Move EKS module if found
if os.path.exists(WRONG_MODULE_PATH):
    print("Moving EKS module to modules/eks")

    if not os.path.exists(CORRECT_EKS_MODULE_PATH):
        shutil.move(WRONG_MODULE_PATH, CORRECT_EKS_MODULE_PATH)
    else:
        print("modules/eks already exists, skipping move")

# Move python scripts
if os.path.exists(WRONG_SCRIPTS_PATH):
    for file in os.listdir(WRONG_SCRIPTS_PATH):

        src = os.path.join(WRONG_SCRIPTS_PATH, file)
        dst = os.path.join(SCRIPTS_DIR, file)

        if file.endswith(".py"):

            if not os.path.exists(dst):
                print(f"Moving script: {file}")
                shutil.move(src, dst)

print("Cleaning empty directories...")

# Remove empty wrong directories
try:
    shutil.rmtree(os.path.join(ROOT_DIR, "environments", "dev", "scripts", "modules"))
except:
    pass

print("Terraform repository structure fixed successfully!")