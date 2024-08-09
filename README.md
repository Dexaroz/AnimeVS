# AnimeVS
## Overview
The Anime Management System is a Python-based application designed to facilitate the management and tracking of anime series and episodes. Utilizing an SQLite database, the system allows users to add, view, and rate anime series, as well as manage episodes by marking them as watched. The project integrates with an external API to fetch and display additional anime details and links.

## Key Features
* **Database Management:**
  - **Setup and Configuration:** Create and configure the SQLite database with animes and episodes tables.
  - **Add Anime:** Insert new anime series into the database.
  - **Add Episodes:** Add episodes for a specific anime, including links fetched from an external API.
  - **Update and Rate Anime:** Update the rating for an anime and mark episodes as watched.

* **Anime Tracking:**

  - **Search Anime:** Search for anime by name and view existing entries.
  - **View Anime History:** Retrieve and display a list of animes along with their ratings and watched status.
  - **Episode Management:** Select and manage episodes, including marking them as watched.

* **Error Handling:**
Implement robust error handling to manage database connectivity issues and data integrity errors.

* **Database Schema**
* animes Table:
  - anime_id: TEXT PRIMARY KEY - Unique identifier for the anime.
  - stars: INTEGER DEFAULT 0 - Rating of the anime (0 to 5 stars).
  - name: TEXT NOT NULL - Name of the anime.

* episodes Table:
  - episode_id: TEXT PRIMARY KEY - Unique identifier for the episode.
  - anime_id: TEXT NOT NULL - Foreign key linking to the animes table.
  - watched: INTEGER DEFAULT 0 - Status indicating if the episode has been watched (0 for not watched, 1 for watched).
  - link: TEXT NOT NULL - URL link for the episode.

* **Functionality**
  
  - Connect to Database: Establishes connection to the SQLite database.
  - Setup and Drop Tables: Functions to create or drop database tables.
  - CRUD Operations: Functions for creating, reading, updating, and deleting records in the database.
  - User Interaction: Command-line interface for user input and interaction to manage anime and episodes.

* **Prerequisites**
  - Python 3.x
  - SQLite3
  - External API for fetching anime details (e.g., AnimeFLV)
