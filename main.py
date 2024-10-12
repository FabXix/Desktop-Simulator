import os
import subprocess
from colorama import Fore, Style

class Node:
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath

def clear_screen():
    print("\033[H\033[J", end="")

def open_app():
    nodes = [
        Node('MusicApp', './MusicApp/music.py'),
        Node('FilesApp', './FilesApp/files.py')
    ]

    current_index = 0  

    while True:
        clear_screen()
        print("Desktop:")
        for i, node in enumerate(nodes):
            if i == current_index:
                print(f"> {Fore.RED}{node.name}{Style.RESET_ALL}")
            else:
                print(f"  {node.name}")
        command = input("Command: ").strip().lower()

        if command == "up":
            if current_index > 0:
                current_index -= 1
            else:
                current_index = len(nodes) - 1  
        elif command == "down":
            if current_index < len(nodes) - 1:
                current_index += 1
            else:
                current_index = 0  
        elif command == "open":
            selected_node = nodes[current_index]
            print(f"Opening {selected_node.name}...")
            try:
                subprocess.run(['python', selected_node.filepath], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Error running {selected_node.name}: {e}")
        elif command == "exit":
            print("Closing Desktop ...")
            break 
        else:
            print("Invalid command. Type 'help' for a list of commands.")

if __name__ == "__main__":
    open_app()
