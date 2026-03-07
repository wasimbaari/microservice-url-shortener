import os
import shutil

root = os.getcwd()

modules_dir = os.path.join(root, "modules")
scripts_dir = os.path.join(root, "scripts")
env_scripts = os.path.join(root, "environments", "dev", "scripts")
env_modules = os.path.join(root, "environments", "dev", "modules")

print("Starting infrastructure repo cleanup...")

# Create modules folder if missing
os.makedirs(modules_dir, exist_ok=True)

# Move EKS module if inside wrong location
wrong_eks = os.path.join(env_scripts, "modules", "eks")
correct_eks = os.path.join(modules_dir, "eks")

if os.path.exists(wrong_eks):
    print("Moving EKS module to modules/eks")
    shutil.move(wrong_eks, correct_eks)

# Move Python scripts
if os.path.exists(env_scripts):

    os.makedirs(scripts_dir, exist_ok=True)

    for file in os.listdir(env_scripts):

        src = os.path.join(env_scripts, file)
        dst = os.path.join(scripts_dir, file)

        if file.endswith(".py") and not os.path.exists(dst):

            print(f"Moving script: {file}")
            shutil.move(src, dst)

# Remove wrong modules folder
if os.path.exists(env_modules):
    print("Removing environments/dev/modules")
    shutil.rmtree(env_modules)

# Remove empty scripts folder
try:
    shutil.rmtree(env_scripts)
except:
    pass

print("Infrastructure repository structure fixed successfully.")