import os
import shutil

ROOT = os.getcwd()

infra_dir = os.path.join(ROOT, "url-shortener-infrastructure")
infra_k8s = os.path.join(infra_dir, "k8s-app")

root_k8s = os.path.join(ROOT, "k8s-app")

print("\nFixing repository structure...\n")

# Move k8s-app to root if inside infrastructure
if os.path.exists(infra_k8s):

    if not os.path.exists(root_k8s):

        shutil.move(infra_k8s, root_k8s)

        print("Moved k8s-app from infrastructure → root")

    else:
        print("k8s-app already exists at root")

else:
    print("No k8s-app found inside infrastructure")

print("\nRepository structure fixed successfully.\n")