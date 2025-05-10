import os
from pathlib import Path

class MrWalk:
    def __init__(self, root_path):
        if not isinstance(root_path, str):
            raise TypeError("root_path must be a string")
        
        ps = root_path.split("/")
        np, i = [], 0
        for s in ps:           
            np.append(str(s).strip().replace('"', ''))
            i += 1
        root_path = Path(*np)        
        
        if not root_path.exists():
            raise FileNotFoundError(f"The path {root_path} does not exist")
        if not root_path.is_dir():
            raise NotADirectoryError(f"The path {root_path} is not a directory")
        
        self.root_path = root_path

    def walk(self):
        mrwalk = {}
        for root, dirs, files in os.walk(self.root_path):
            root_parts = Path(root).parts
            current_level = mrwalk
            for part in root_parts:
                current_level = current_level.setdefault(part, {})
            print(f"Root: {root}")
            for dir in dirs:
                current_level[dir] = {}
                print(f"Folder: {dir}")
            for file in files:
                current_level[file] = Path(file).suffix if os.path.isfile(os.path.join(root, file)) else "unknown"
                print(f"File: {file}")
        return mrwalk

# Example usage:
# root_path = "." / "source" / "jsondot"
# walker = MrWalk('"."')
# structure = walker.walk()
# print(structure)
