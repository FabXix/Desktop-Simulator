import time
from colorama import Fore, Style

def help():
    print("[help]/[h] Gives a list of commands.")
    print("[down]/[d] Moves your actual index down.")
    print("[up]/[u] Moves your actual index up.")
    print("[queue]/[q] Adds the selected song to the queue.")
    print("[queue_all]/[qa] Adds all the songs from a playlist to the queue.")
    print("[skip]/[s] Skips to the next song.")
    print("[play]/[p] Plays the next song in the queue.")
    print("[autoplay]/[ap] Plays all the songs from the queue nonstop.")
    print("[list]/[l] Displays all the songs in the queue.")
    print("[playlist_create]/[pc] Creates a playlist.")
    print("[playlist_manager]/[pm] Opens the playlist menu.")
    print("[add] Adds a song to the playlist selected while in the playlist menu.")
    print("[remove]/[r] Removes a song to the playlist selected while in the playlist menu.")
    print("[exit] Exits Music.py. ")
    time.sleep(2.1)


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Queue:
    def __init__(self):
        self.first = None
        self.last = None
        self.length = 0

    def is_empty(self):
        return self.first is None

    def enqueue(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.first = new_node
            self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node
        self.length += 1

    def dequeue(self):
        if self.is_empty():
            return None
        value = self.first.value
        self.first = self.first.next
        if self.is_empty():
            self.last = None
        self.length -= 1
        return value

    def peek(self):
        return None if self.is_empty() else self.first.value

    def pretty_print(self):
        current = self.first
        while current is not None:
            minutes, seconds = divmod(current.value['duration'], 60)
            print(f"{Fore.GREEN}{current.value['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
            print(f"{Fore.BLUE}{current.value['artist']}{Style.RESET_ALL}")
            print("   ")
            current = current.next

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = Queue()

    def is_song_in_playlist(self, song):
        current = self.songs.first
        while current is not None:
            if current.value == song:
                return True
            current = current.next
        return False

    def add_song(self, song):
        if not self.is_song_in_playlist(song):
            self.songs.enqueue(song)
            print(f"Added {song['name']} to playlist '{self.name}'")
        else:
            print(f"{song['name']} is already in the playlist '{self.name}'")

    def remove_song(self, index):
        current = self.songs.first
        prev = None
        current_index = 0

        while current is not None and current_index < index:
            prev = current
            current = current.next
            current_index += 1

        if current is None:
            print("Index out of range!")
            return None

        if prev is None:
            self.songs.first = current.next
        else:
            prev.next = current.next

        if current.next is None:
            self.songs.last = prev

        self.songs.length -= 1
        return current.value

    def list_songs(self):
        if self.songs.is_empty():
            print("The playlist is empty!")
        else:
            print(f"Songs in '{self.name}':")
            current = self.songs.first
            while current:
                minutes, seconds = divmod(current.value['duration'], 60)
                print(f"{Fore.GREEN}{current.value['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                print(f"{Fore.BLUE}{current.value['artist']}{Style.RESET_ALL}")
                print("   ")
                current = current.next



class PlaylistManager:
    def __init__(self):
        self.playlists = {}

    def create_playlist(self, name):
        if name not in self.playlists:
            self.playlists[name] = Playlist(name)
        else:
            print(f"Playlist '{name}' already exists!")

    def get_playlist(self, name):
        return self.playlists.get(name, None)

    def list_playlists(self):
        if not self.playlists:
            print("No playlists available!")
        else:
            print("Playlists:")
            for name in self.playlists:
                print(f"  {name}")

def clear_screen():
    print("\033[H\033[J", end="")

def display_progress(duration, elapsed):
    progress = int((elapsed / duration) * 100)
    bar = ('|' * (progress // 5)).ljust(20)
    print(f"▶︎ •{bar} {progress}%")

def music():
    print("Your Library:")
    #All songs durations are reduced to showcase the code.
    songs = [{"name": "MOJABI GHOST", "artist": "Tainy & Bad Bunny", "duration": 5},
             {"name": "Vida Rockstar", "artist": "Jhayco", "duration": 7},
             {"name": "Next Semester", "artist": "Twenty One Pilots", "duration": 12}]
    cola = Queue()
    playlist_manager = PlaylistManager()
    current_index = 0

    while True:
        print("Library Songs:")
        for i, song in enumerate(songs):
            minutes, seconds = divmod(song['duration'], 60)
            if i == current_index:
                print(f"> {Fore.GREEN}{song['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
            else:
                print(f"{Fore.GREEN}{song['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
            print(f"{Fore.BLUE}{song['artist']}{Style.RESET_ALL}")
            print("     ")

        action = input("\nMusic: ").strip().lower()

        if action == "down":
            clear_screen()
            current_index = (current_index + 1) % len(songs)
        elif action == "up":
            clear_screen()
            current_index = (current_index - 1) % len(songs)
        elif action == "queue" or action == "q":
            clear_screen()
            cola.enqueue(songs[current_index])
            print(f"Added {songs[current_index]['name']} to the queue!")
        elif action == "skip" or action == "s":
            clear_screen()
            if cola.is_empty():
                print("The queue is empty!")
            else:
                skipped_song = cola.dequeue()
                print(f"Skipped {skipped_song['name']}!")
                time.sleep(1)
                print(f"Next song: {cola.peek()}")
                time.sleep(1)
        elif action == "help" or action == "h":
            clear_screen()
            help()
        elif action == "play" or action == "p":
            clear_screen()
            if cola.is_empty():
                print("Queue is empty! Add some songs first.")
            else:
                song = cola.peek()
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
                cola.dequeue()
        elif action == "autoplay" or action == "ap":
            for i in range(cola.length):
                clear_screen()
                if cola.is_empty():
                    print("Queue is empty! Add some songs first.")
                else:
                    song = cola.peek()
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
                    cola.dequeue()
        elif action == "list" or action == "l":
            clear_screen()
            if cola.is_empty():
                print("The queue is empty!")
            else:
                print("Songs in Queue:")
                cola.pretty_print()
                print("------")
                print("      ")
        elif action == "playlist_create" or action == "pc":
            clear_screen()
            playlist_name = input("Enter playlist name: ").strip()
            playlist_manager.create_playlist(playlist_name)
            print(f"Playlist '{playlist_name}' created!")
        elif action == "playlist_manager" or action == "pm":
            clear_screen()
            playlist_manager.list_playlists()
            playlist_name = input("Enter playlist name to manage: ").strip()
            playlist = playlist_manager.get_playlist(playlist_name)
            if playlist:
                while True:
                    print(f"\nManaging Playlist: {playlist.name}")
                    playlist.list_songs()
                    playlist_action = input("\n[Add, Remove, Queue, Queue All, Exit]: ").strip().lower()

                    if playlist_action == "add" or playlist_action == "a":
                        clear_screen()
                        while True:
                            print("Select a song to add to the playlist:")
                            for i, song in enumerate(songs):
                                minutes, seconds = divmod(song['duration'], 60)
                                if i == current_index:
                                    print(f"> {Fore.GREEN}{song['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                                else:
                                    print(f"{Fore.GREEN}{song['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                                print(f"{Fore.BLUE}{song['artist']}{Style.RESET_ALL}")
                                print("     ")

                            action = input("\nUse 'up'/'down' to navigate and 'add' to select: ").strip().lower()

                            if action == "down":
                                clear_screen()
                                current_index = (current_index + 1) % len(songs)
                            elif action == "up":
                                clear_screen()
                                current_index = (current_index - 1) % len(songs)
                            elif action == "add" or action == "a":
                                clear_screen()
                                playlist.add_song(songs[current_index])
                                break
                            elif action == "exit":
                                clear_screen()
                                break
                            else:
                                clear_screen()
                                print("Invalid action.")
                    elif playlist_action == "remove" or playlist_action == "r":
                        clear_screen()
                        if playlist.songs.is_empty():
                            print("The playlist is empty!")
                        else:
                            playlist_current_index = 0
                            while True:
                                print("Select a song to remove from the playlist:")
                                current_song = playlist.songs.first
                                for i in range(playlist.songs.length):
                                    minutes, seconds = divmod(current_song.value['duration'], 60)
                                    if i == playlist_current_index:
                                        print(f"> {Fore.GREEN}{current_song.value['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                                    else:
                                        print(f"{Fore.GREEN}{current_song.value['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                                    print(f"{Fore.BLUE}{current_song.value['artist']}{Style.RESET_ALL}")
                                    print("     ")
                                    current_song = current_song.next

                                action = input("\nUse 'up'/'down' to navigate and 'remove' to select: ").strip().lower()

                                if action == "down":
                                    clear_screen()
                                    playlist_current_index = (playlist_current_index + 1) % playlist.songs.length
                                elif action == "up":
                                    clear_screen()
                                    playlist_current_index = (playlist_current_index - 1) % playlist.songs.length
                                elif action == "remove" or action == "r":
                                    clear_screen()
                                    removed_song = playlist.remove_song(playlist_current_index)
                                    if removed_song:
                                        print(f"Removed {Fore.RED}{removed_song['name']}{Style.RESET_ALL} from the playlist!")
                                    break
                                elif action == "exit":
                                    clear_screen()
                                    break
                                else:
                                    clear_screen()
                                    print("Invalid action.")
                    elif playlist_action == "queue" or playlist_action == "q":
                        clear_screen()
                        if playlist.songs.is_empty():
                            print("The playlist is empty!")
                        else:
                            playlist_current_index = 0
                            while True:
                                print("Select a song to queue from the playlist:")
                                current_song = playlist.songs.first
                                for i in range(playlist.songs.length):
                                    minutes, seconds = divmod(current_song.value['duration'], 60)
                                    if i == playlist_current_index:
                                        print(f"> {Fore.GREEN}{current_song.value['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                                    else:
                                        print(f"{Fore.GREEN}{current_song.value['name']}{Style.RESET_ALL} {minutes}:{seconds:02d}")
                                    print(f"{Fore.BLUE}{current_song.value['artist']}{Style.RESET_ALL}")
                                    print("     ")
                                    current_song = current_song.next

                                action = input("\nUse 'up'/'down' to navigate and 'queue' to select: ").strip().lower()

                                if action == "down":
                                    clear_screen()
                                    playlist_current_index = (playlist_current_index + 1) % playlist.songs.length
                                elif action == "up":
                                    clear_screen()
                                    playlist_current_index = (playlist_current_index - 1) % playlist.songs.length
                                elif action == "queue" or action == "q":
                                    current_song = playlist.songs.first
                                    for _ in range(playlist_current_index):
                                        current_song = current_song.next
                                    cola.enqueue(current_song.value)
                                    print(f"Added {Fore.GREEN}{current_song.value['name']}{Style.RESET_ALL} to the queue!")
                                    break
                                elif action == "exit":
                                    clear_screen()
                                    break
                                else:
                                    clear_screen()
                                    print("Invalid action.")

                    elif playlist_action == "queue all" or playlist_action == "qa":
                        clear_screen()
                        current = playlist.songs.first
                        while current:
                            cola.enqueue(current.value)
                            current = current.next
                        print(f"Added all songs from {Fore.BLUE}'{playlist.name}'{Style.RESET_ALL} to the queue!")
                    elif playlist_action == "exit":
                        clear_screen()
                        break
                    else:
                        clear_screen()
                        print("Invalid action.")
            else:
                print(f"No playlist found with the name {Fore.BLUE}'{playlist_name}{Style.RESET_ALL}'")
        elif action == "exit":
            break
        else:
            clear_screen()
            print("Invalid action.")
            
music()