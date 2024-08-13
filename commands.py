from api_functions import *
from db_functions import *
from animeflv import AnimeFLV

def watch_anime():
    """
        Function to handle watching an anime.
        It retrieves an anime from the database and fetches the corresponding information from an API.

        If an anime is found in the database, it attempts to fetch its episodes from the API and allows the user to
         select and watch an episode.
    """
    try:
        name = anime_from_db()
        if name:
            anime_from_api(name)
    except Exception as e:
        print(f"Error in watch anime: {e}")

def anime_history():
    """
        Function to manage the user's anime history.
        Displays a list of watched animes, allows the user to vote, remove animes, or exit the menu.
    """
    try:
        show_animes()

        print("What would you like to do? \n 1.- Vote an anime \n 2.- Remove an anime \n 3.- Exit")
        option_history = int(input())

        if option_history == 1:
            vote_anime()
        elif option_history == 2:
            delete_animes()
        elif option_history == 3:
            return
        else:
            print("Invalid choice. Try again!")
    except Exception as e:
        print(f"Error in anime history: {e}")

def show_animes():
    for i in get_animes():
        print(i[1] + " - " + ('⭐' * i[2] if i[2] > 0 else "Not valorated."))

def delete_animes():
    try:
        anime = select_anime_db(get_animes())
        remove_anime(anime[0])
        remove_episodes(anime[0])
    except Exception as e:
        print(f"Error in delete animes: {e}")


def vote_anime():
    """
        Allows the user to vote for an anime in the database.

        The user can assign a rating between 0 and 5 stars to a selected anime.
    """
    while True:
        try:
            animes = get_animes()

            if not animes:
                print("Not animes in database.")
                return

            anime = select_anime_db(animes)
            stars = int(input("What rating does this anime deserve? "))

            if stars >= 0 and stars <= 5:
                valorate_anime(anime[0], stars)
                return
            else:
                print("Invalid valoration. Try again")
        except Exception as e:
            print(e)

def anime_from_api(name):
    """
        Fetches anime information and episodes from an external API and manages user interaction.

        Args:
            name (str): The name of the anime to search for.

        It searches for the anime using the API, retrieves its episodes, and allows the user to select and watch an
         episode.
    """
    api = AnimeFLV()
    try:
        elements = search_anime(api, name)
        if not elements:
            print("No animes found.")
            return

        anime = select_anime(elements)
        info = api.get_anime_info(anime.id)
        info.episodes.reverse()

        if not anime_exists(anime.id):
            add_anime(anime.id, str(anime.title))
            add_episodes(api, anime.id, info.episodes)

        episode = select_episode(info.episodes)
        results = api.get_links(anime.id, episode.id)

        if results:
            select_links(results)
            mark_episode(anime.id, episode.id)
        else:
            print("No links found.")
    except AttributeError as e:
        print("AttributeError in anime from api, please check your API data.")
    except Exception as e:
        print(f"Error in anime from api: {e}")

def anime_from_db():
    """
        Retrieves anime information from the local database.

        Returns the name of the anime if not found in the database, or None if found.

        It allows the user to select an episode from the database and marks it as watched.
    """
    setup_db()
    name, elements = search_anime_db()
    if elements:
        anime = select_anime_db(elements)
        episodes = get_episodes_for_anime(anime[0])
        episode = select_episode_db(episodes)

        if episode:
            print(episode[-1])
            mark_episode_db(episode[0])
        else:
            print("No links found.")

        return None
    return name

