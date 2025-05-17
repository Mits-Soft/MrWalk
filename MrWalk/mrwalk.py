import os
from pathlib import Path

class MrWalk:
    def __init__(self, root_path = '.'):
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
        self.mrwalk = {}

    def walk(self, extensions: list = [], exclude: list = []):
        mrwalk = {}
        for root, dirs, files in os.walk(self.root_path):
            root_parts = Path(root).parts
            current_level = mrwalk
            for d in dirs:
                if d in exclude:
                    dirs.remove(d)
            for part in root_parts:
                if part not in exclude:
                    current_level = current_level.setdefault(part, {})
            print(f"Root: {root}")
            for dir in dirs:
                if dir not in exclude:
                    current_level[dir] = {}
                    print(f"Folder: {dir}")
            for file in files:
                f = Path(file)
                if file not in exclude:
                    if extensions == None:
                        current_level[file] = f.suffix if os.path.isfile(os.path.join(root, file)) else "unknown"
                    if not extensions == None and f.suffix in extensions:
                        current_level[file] = f.suffix if os.path.isfile(os.path.join(root, file)) else "unknown"
                    print(f"File: {file}")
        self.mrwalk = mrwalk
        return mrwalk
    
    def prune(self, selection: list = None):
        mw = self.mrwalk
        mwk = list(mw.keys())[0]
        mwv = list(mw.values())[0]
        result = self.prune_dictionary(mwv, selection)   
        self.mrwalk[mwk] = result
        return self.mrwalk
    
    def prune_dictionary(self, dictionary, keys_to_remove):
        """
        Removes specified keys from a nested dictionary.

        :param dictionary: The original dictionary to prune.
        :param keys_to_remove: List of keys to be removed.
        :return: The pruned dictionary.
        """
        if isinstance(dictionary, dict):
            # Create a new dictionary excluding the keys to remove
            return {k: self.prune_dictionary(v, keys_to_remove)
                    for k, v in dictionary.items()
                    if k not in keys_to_remove}
        elif isinstance(dictionary, list):
            # Recursively apply pruning to elements of lists
            return [self.prune_dictionary(element, keys_to_remove) for element in dictionary]
        else:
            # If it is a non-compound value, return it directly
            return dictionary

    def tree(self, current=None, prefix=""):
        if current is None:
            current = self.mrwalk

        tree_output = ""
        for key, value in current.items():
            tree_output += f"{prefix}├── {key}\n"
            if isinstance(value, dict):
                tree_output += self.tree(value, prefix + "│   ")
        return tree_output

# Example usage:
# root_path = "." / "source" / "jsondot"
# walker = MrWalk('"."')
# structure = walker.walk()
# print(structure)
