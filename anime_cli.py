import sys
from terminal import Terminal

def main():
    """
        Main function to start the application.
        Handles the initial menu and exceptions during execution.
    """
    try:
        if len(sys.argv) > 1:
            menu = sys.argv[1].lower() == True
        else:
            menu = True

        terminal = Terminal(menu=False)
        terminal.run()
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    main()