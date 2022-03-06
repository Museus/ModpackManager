from pathlib import Path
from hashlib import md5

test_modimporter_path = Path("./modimporters")
legal_modimporters = set()
for modimporter in test_modimporter_path.iterdir():
    with open(modimporter, "rb") as modimporter_file:
        legal_modimporters.add(md5(modimporter_file.read()).hexdigest())

with open("../legal_modimporters.txt", "w") as legal_output:
    for line in legal_modimporters:
        legal_output.write(f"{line}\n")
