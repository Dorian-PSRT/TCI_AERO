import os

# Dossier racine de ton workspace
root_dir = "."

TARGET = "turtlesim_msgs."
REPLACEMENT = "turtlesim_msgs."

for path, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".py"):
            full_path = os.path.join(path, file)

            with open(full_path, "r") as f:
                content = f.read()

            new_content = content.replace(TARGET, REPLACEMENT)

            if new_content != content:
                print(f"✔ Modifié : {full_path}")
                with open(full_path, "w") as f:
                    f.write(new_content)

print("\n🎉 Terminé ! Tous les turtlesim_msgs.srv → turtlesim_msgs.srv ont été remplacés.")
