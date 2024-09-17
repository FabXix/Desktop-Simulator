from colorama import Fore, Style
import time

class TreeNode:
    def __init__(self, name, is_folder=False):
        self.name = name
        self.is_folder = is_folder
        self.content = "" if not is_folder else None
        self.children = [] if is_folder else None
        self.parent = None

    def add_child(self, child_node):
        if self.is_folder:
            child_node.parent = self
            self.children.append(child_node)
        else:
            print(f"Error: {self.name} is a file.")
            
    def delete_child(self, index):
        if self.is_folder and index < len(self.children):
            del self.children[index]
        else:
            print("Error: This is not a folder")
            
    def delete(self):
        if self.parent:
            self.parent.children.remove(self)
            print(f"{self.name} has been deleted.")
        else:
            print("Unable to delete Root")
    
    def show(self):
        node_type = "Folder" if self.is_folder else "File"
        print(f"Current {node_type}: {self.name}")
        if not self.is_folder and self.content is not None:
            print(f"Content: {self.content}")
    
    def move_to_parent(self):
        if self.parent:
            return self.parent
        else:
            print(f"{self.name} has no parent")
            return None
    
    def move_to_child(self, index):
        if self.is_folder and index < len(self.children):
            return self.children[index]
        else:
            print("This is not a folder or invalid index")
            return None
    
    def modify_content(self, new_content=None):
        if not self.is_folder:
            print("Enter new content line by line. Press Enter on an empty line to finish:")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            self.content = "\n".join(lines)
        else:
            print(f"{self.name} is a folder")

    def append_content(self):
        if not self.is_folder:
            print("Current content:\n" + self.content)
            print("Enter new content to append. Press Enter on an empty line to finish:")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            new_content = "\n".join(lines)
            
            self.content += "\n" + new_content if self.content else new_content
            
            print("Content updated.")
        else:
            print(f"{self.name} is a folder")


def clear_screen():
    print("\033[H\033[J", end="")

def file_explorer(root):
    current_node = root
    current_index = 0

    while True:
        print(f"Current Directory: {current_node.name}")
        
        if current_node.is_folder:
            for i, child in enumerate(current_node.children):
                if i == current_index:
                    if child.is_folder:
                        print(f"> {Fore.RED}{child.name}{Style.RESET_ALL} 📁")
                    else:
                        print(f"> {Fore.RED}{child.name}{Style.RESET_ALL} 🗒️")
                else:
                    if child.is_folder:
                        print(f"{Fore.GREEN}{child.name}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.BLUE}{child.name}{Style.RESET_ALL}")
        else:
            print(current_node.content)
            
        command = input("Enter command: ").strip().lower()
        
        if command == "up":
            clear_screen()
            if current_node.is_folder:
                if current_index > 0:
                    current_index -= 1
                else:
                    current_index = len(current_node.children) - 1  
            else:
                print("Cannot move up. This is not a folder.")
        elif command == "down":
            clear_screen()
            if current_node.is_folder:
                if current_index < len(current_node.children) - 1:
                    current_index += 1
                else:
                    current_index = 0  
            else:
                print("Cannot move down. This is not a folder.")
        elif command == "close":
            clear_screen()
            if current_node.parent is not None:
                current_node = current_node.parent
            else:
                print("Closing Files.py")
                time.sleep(2)
                break
        elif command == "delete":
            current_node.delete_child(current_index)
        elif command == "write":
            clear_screen()
            current_node.modify_content()
        elif command == "append":
            clear_screen()
            current_node.append_content()
        elif command == "open":
            clear_screen()
            new_node = current_node.move_to_child(current_index)
            if new_node:
                current_node = new_node
                current_index = 0  
        elif command == "create file":
            clear_screen()
            if current_node.is_folder:
                name = input("Enter the name of the new file: ").strip()
                new_file = TreeNode(name, is_folder=False)
                current_node.add_child(new_file)
            else:
                print("Cannot create files within a file.")
        elif command == "create folder":
            clear_screen()
            if current_node.is_folder:
                name = input("Enter the name of the new folder: ").strip()
                new_folder = TreeNode(name, is_folder=True)
                current_node.add_child(new_folder)
            else:
                clear_screen()
                print("Cannot create folders within a file.")
        elif command == "quit":
            break
        else:
            clear_screen()
            print("Invalid command.")

root = TreeNode("Root", is_folder=True)
file_explorer(root)
