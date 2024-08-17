from menus import Menu
from commands import *

class Terminal:
    def __init__(self, menu):
        self.mode = menu
        if menu:
            self.main_menu = Menu()
        else:
            self.commands = {'search_anime' : watch_anime,
                             'anime_history' : show_animes,
                             'vote_anime' : vote_anime,
                             'delete_anime' : delete_animes,
                             'help' : help,
                             'exit' : exit}

    def execute_command(self, command_input):
        try:
            command, *args = command_input.split()
            if command in self.commands:
                if args:
                    args = [" ".join(args)]
                self.commands[command](*args)
            else:
                print(f"Comando '{command}' no reconocido. Escribe 'help' para ver la lista de comandos.")
        except Exception as e:
            print(f"Error in execute commands: {e}")

    def run(self):
        if self.mode:
            while True:
                try:
                    self.main_menu.display()
                    command = int(input())
                    self.main_menu.execute_command(command)
                except Exception as e:
                    print(f"Error in terminal: {e}")
        else:
            while True:
                try:
                    command_input = input("anime-vs> ").strip().lower()
                    self.execute_command(command_input)
                except Exception as e:
                    print(f"Error in run: {e}")