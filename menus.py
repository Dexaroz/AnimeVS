from commands import *

class Menu:
    def display(self):
        print("What would you like to do?")
        print("1.- Watch anime.")
        print("2.- Anime history.")
        print("3.- Exit.")

    def execute_command(self, command):
        try:
            if command == 1:
                watch_anime()
            elif command == 2:
                anime_history()
            elif command == 3:
                exit()
            else:
                print("Invalid choice. Try again!")
        except Exception as e:
            print(f"Error in menu: {e}")

    def run(self):
        while True:
            self.display()
            command = int(input())
            self.execute_command(command)