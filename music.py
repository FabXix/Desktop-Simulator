import time
import os
from colorama import Fore, Style

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_progress(duration, elapsed):
    progress = int((elapsed / duration) * 100)
    bar = ('|' * (progress // 5)).ljust(20)
    print(f"▶︎ •{bar} {progress}%")

def music():
    print("Your Playlist")
    songs = [{"name": "Data", "artist": "Tainy", "duration": 5},
             {"name": "Vida Rockstar", "artist": "Jhayco", "duration": 7},
             {"name": "wave", "artist": "wave to earth", "duration": 12}]
    queue = []
    current_index = 0

    while True:

        for i, song in enumerate(songs):
            minutes, seconds = divmod(song['duration'], 60)
            if i == current_index:
                print(f"> {Fore.GREEN}{song['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
            else:
                print(f"{Fore.GREEN}{song['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
            print(f"{Fore.BLUE}{song['artist']}{Style.RESET_ALL}")
            print("     ")

        action = input("\n[Up, Down, Queue, List, Play, Skip, Exit]: ").strip().lower()

        if action == "down":
            clear_screen()
            current_index = (current_index + 1) % len(songs)
        elif action == "up":
            clear_screen()
            current_index = (current_index - 1) % len(songs)
        elif action == "queue":
            clear_screen()
            queue.append(songs[current_index])
            print(f"Added {songs[current_index]['name']} to the queue!")
        elif action == "list":
            clear_screen()
            if not queue:
                print("The queue is empty!")
            else:
                print("Songs in Queue:")
                for song in queue:
                    minutes, seconds = divmod(song['duration'], 60)
                    print(f"{Fore.GREEN}{song['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                    print(f"{Fore.BLUE}{song['artist']}{Style.RESET_ALL}")
                    print("   ")
                    print("   ")
        elif action == "play":
            clear_screen()
            if not queue:
                print("Queue is empty! Add some songs first.")
            else:
                song = queue[0]
                song_duration = song['duration']
                song_elapsed_time = 0

                while song_elapsed_time < song_duration:
                    clear_screen()
                    print(f"Now playing: {Fore.GREEN}{song['name']}{Style.RESET_ALL} by {Fore.BLUE}{song['artist']}{Style.RESET_ALL}")
                    display_progress(song_duration, song_elapsed_time)

                    time.sleep(0.5)
                    song_elapsed_time += 0.5
                    

                clear_screen()
                print(f"Finished: {Fore.GREEN}{song['name']}{Style.RESET_ALL}")
                time.sleep(1)
                queue.pop(0)  

                if queue:
                    next_song = queue[0]
                    minutes, seconds = divmod(next_song['duration'], 60)
                    print(f"Up Next: {Fore.GREEN}{next_song['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                    print("   ")
                    time.sleep(1)
                else:
                    print("Queue is empty!")
                    print("  ")
                    time.sleep(1)
                
        elif action == "skip":
            clear_screen()
            if queue:
                skipped_song = queue.pop(0)
                if queue:
                    next_song = queue[0]
                    print(f"Skipped: {Fore.RED}{skipped_song['name']}{Style.RESET_ALL} by {Fore.RED}{skipped_song['artist']}{Style.RESET_ALL}")
                    print(f"Up Next: {Fore.GREEN}{next_song['name']}{Style.RESET_ALL}")
                else:
                    print(f"Skipped: {Fore.RED}{skipped_song['name']}{Style.RESET_ALL}. Queue is empty.")
            else:
                print("Queue is empty.")
        elif action == "exit":
            break
        else:
            print("Invalid command. Use 'down', 'up', 'queue', 'list', 'play', 'skip' or 'exit'.")

music()
