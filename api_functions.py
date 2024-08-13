def search_anime(api, query):
    """
    Searches for an anime using the provided API and query.

    Args:
        api (AnimeFLV): An instance of the AnimeFLV class used for searching.
        query (str): The search query to find the anime.

    Returns:
        list: A list of anime objects returned by the API search.
    """
    return api.search(query)

def select_anime(animes):
    """
    Prompts the user to select an anime from a list of animes.

    Args:
        animes (list): A list of anime objects to choose from.

    Returns:
        Anime: The selected anime object.
    """
    for i, anime in enumerate(animes):
        print(f"{i + 1} - {anime.title}")

    while True:
        try:
            selection = int(input("Select an anime: "))
            if selection > 0 and selection <= len(animes):
                return animes[selection - 1]
            else:
                print("Invalid choice. Please try again!")
        except ValueError:
            print("Invalid input.")

def select_episode(episodes):
    """
    Prompts the user to select an episode from a list of episodes.

    Args:
        episodes (list): A list of episode objects to choose from.

    Returns:
        Episode: The selected episode object.
    """
    for i, episode in enumerate(episodes):
        print(f"{i+1} - Episode {episode.id} ❌")

    while True:
        try:
            selection = int(input("Select an episode: "))
            if selection > 0 and selection <= len(episodes):
                return episodes[selection - 1]
            else:
                print("Invalid choice. Please try again!")
        except ValueError:
            print("Invalid input.")

def select_links(links):
    """
    Displays a list of links for the user to choose from.

    Args:
        links (list): A list of link objects, each containing server information and URL.
    """
    for i in range(0, len(links) - 1):
        print(f"{links[i].server} - {links[i].url}")
    print(f"{links[-1].server} - {links[-1].url} \n")
