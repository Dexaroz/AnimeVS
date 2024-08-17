import sqlite3

# Connect to the database

DATABASE = 'anime_vs.db'
watched = {0: '❌', 1: '✔️'}

def connect_db():
    """
    Connects to the SQLite database.

    Returns:
        sqlite3.Connection: The connection object to the database.
    """
    try:
        return sqlite3.connect(DATABASE)
    except Exception as e:
        print(f"Database connection error: {e}")
        return

def drop_tables():
    """
    Drops the 'animes' and 'episodes' tables if they exist.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
    DROP TABLE IF EXISTS animes
    """)
    cursor.execute("""
    DROP TABLE IF EXISTS episodes
    """)
    db.commit()
    db.close()

def setup_db():
    """
    Sets up the database by creating 'animes' and 'episodes' tables if they do not exist.
    """
    db = connect_db()
    cursor = db.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS animes (
        anime_id TEXT PRIMARY KEY,
        stars INTEGER DEFAULT 0,
        name TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS episodes (
        episode_id TEXT PRIMARY KEY,
        anime_id TEXT NOT NULL,    
        watched INTEGER DEFAULT 0,
        link TEXT NOT NULL,
        FOREIGN KEY (anime_id) REFERENCES animes (anime_id)
    )
    """)

    db.commit()
    db.close()

def add_anime(anime_id, name):
    """
    Adds a new anime to the 'animes' table.

    Args:
        anime_id (str): The ID of the anime.
        name (str): The name of the anime.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO animes (anime_id, name) VALUES (?, ?)', (anime_id, name,))
    db.commit()
    db.close()

def add_episodes(api, anime_id, episodes):
    """
    Adds episodes to the 'episodes' table for a given anime.

    Args:
        api (AnimeFLV): An instance of the AnimeFLV class used to fetch episode links.
        anime_id (str): The ID of the anime.
        episodes (list): A list of episode objects to be added.
    """
    db = connect_db()
    cursor = db.cursor()

    try:
        for episode in episodes:
            unique_episode_id = f"{anime_id} {episode.id}"
            links = api.get_links(anime_id, int(episode.id))
            if links:
                cursor.execute('INSERT INTO episodes (episode_id, anime_id, watched, link) VALUES (?, ?, ?, ?)', (unique_episode_id, anime_id, 0, links[0].url))
    except sqlite3.IntegrityError as e:
        print(f"Integrity error: {e}")
    except Exception as e:
        print(f"Error in add episodes: {e}")
        db.rollback()
    finally:
        db.commit()
        db.close()

def anime_exists(anime_id):
    """
    Checks if an anime exists in the 'animes' table.

    Args:
        anime_id (str): The ID of the anime to check.

    Returns:
        bool: True if the anime exists, False otherwise.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT 1 FROM animes WHERE anime_id = ?', (anime_id,))
    exists = cursor.fetchone() is not None
    db.close()
    return exists

def search_anime_db(name):
    """
    Searches for an anime by name in the 'animes' table.

    Returns:
        tuple: A tuple containing the search query and the search results.
            - query (str): The name of the anime searched.
            - result (list): A list of tuples containing anime_id and name of matching animes.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
    SELECT anime_id, name
    FROM animes
    WHERE name = ?
    ''', (name,))

    result = cursor.fetchall()
    db.close()
    return name, result

def select_anime_db(animes):
    """
    Prompts the user to select an anime from a list of animes.

    Args:
        animes (list): A list of tuples containing anime_id and name.

    Returns:
        tuple: The selected anime (anime_id, name).
    """
    for i, anime in enumerate(animes):
        print(f"{i + 1} - {anime[1]}")

    while True:
        try:
            selection = int(input("Select an anime: "))
            if selection > 0 and selection <= len(animes):
                return animes[selection - 1]
            else:
                print("Invalid choice. Please try again!")
        except ValueError:
            print("Invalid input.")

def select_episode_db(episodes):
    """
    Prompts the user to select an episode from a list of episodes.

    Args:
        episodes (list): A list of tuples containing episode_id, watched status, and link.

    Returns:
        tuple: The selected episode (episode_id, watched status, link).
    """
    for i, episode in enumerate(episodes):
        episode_number = episode[0].split()[1]
        print(f"{i+1} - Episode {episode_number} {watched[episode[1]]}")

    while True:
        try:
            selection = int(input("Select an episode: "))
            if selection > 0 and selection <= len(episodes):
                return episodes[selection - 1]
            else:
                print("Invalid choice. Please try again!")
        except ValueError:
            print("Invalid input.")

def mark_episode(anime_id, episode_id):
    """
    Marks an episode as watched in the 'episodes' table.

    Args:
        anime_id (str): The ID of the anime.
        episode_id (str): The ID of the episode to mark as watched.
    """
    unique_episode_id = f"{anime_id} {episode_id}"
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('UPDATE episodes SET watched = 1 WHERE episode_id = ?', (unique_episode_id,))
    db.commit()
    db.close()

def mark_episode_db(episode_id):
    """
    Marks an episode as watched in the 'episodes' table using the episode_id.

    Args:
        episode_id (str): The ID of the episode to mark as watched.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('UPDATE episodes SET watched = 1 WHERE episode_id = ?', (episode_id,))
    db.commit()
    db.close()

def valorate_anime(anime_id, stars):
    """
    Updates the rating of an anime in the 'animes' table.

    Args:
        anime_id (str): The ID of the anime to rate.
        stars (int): The rating to assign (0-5).
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('UPDATE animes SET stars = ? WHERE anime_id = ?', (stars, anime_id))
    db.commit()
    db.close()

def get_animes():
    """
    Retrieves all animes from the 'animes' table.

    Returns:
        list: A list of tuples containing anime_id, name, and stars for each anime.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('SELECT anime_id, name, stars FROM animes')
    result = cursor.fetchall()
    db.close()
    return result

def get_episodes_for_anime(anime_id):
    """
    Retrieves all episodes for a specific anime from the 'episodes' table.

    Args:
        anime_id (str): The ID of the anime to fetch episodes for.

    Returns:
        list: A list of tuples containing episode_id, watched status, and link for each episode.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
    SELECT episode_id, watched, link
    FROM episodes
    WHERE anime_id = ?
    ''', (anime_id,))

    result = cursor.fetchall()
    db.close()
    return result

def get_episodes_viewed_for_anime(anime_id):
    """
        Retrieves all viewed episodes for a specific anime from the 'episodes' table.

        Args:
            anime_id (str): The ID of the anime to fetch viewed episodes for.

        Returns:
            list: A list of tuples containing episode_id for each viewed episode.
        """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
    SELECT episode_id
    FROM episodes
    WHERE anime_id = ? and watched = 1    
    ''', (anime_id,))

    result = cursor.fetchall()
    db.close()
    return result

def remove_anime(anime_id):
    """
    Removes an anime from the 'animes' table.

    Args:
        anime_id (str): The ID of the anime to remove.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
    DELETE
    FROM animes
    WHERE anime_id = ?
    ''', (anime_id,))
    db.commit()
    db.close()

def remove_episodes(anime_id):
    """
    Removes all episodes for a specific anime from the 'episodes' table.

    Args:
        anime_id (str): The ID of the anime whose episodes are to be removed.
    """
    db = connect_db()
    cursor = db.cursor()
    cursor.execute('''
    DELETE
    FROM episodes
    WHERE anime_id = ?
    ''', (anime_id,))
    db.commit()
    db.close()
