"""
Theme Manager - Gestion des thèmes visuels
Gère les thèmes par défaut et personnalisés
"""

import json
import os

# Fichiers de configuration
CONFIG_FILE = "gamelife_config.json"
CUSTOM_THEMES_FILE = "custom_themes.json"
FAVORITE_COLORS_FILE = "favorite_colors.json"

# Définition des thèmes par défaut
DEFAULT_THEMES = {
    "dark": {
        "bg": "#1a1a2e",
        "panel": "#16213e",
        "accent": "#0f3460",
        "alive": "#00ff88",
        "dead": "#2d3561",
        "text": "#eeeeee",
        "button_bg": "#0f3460",
        "button_hover": "#1e5f8c",
        "button_text": "#ffffff"
    },
    "neon": {
        "bg": "#0d0221",
        "panel": "#1b0638",
        "accent": "#2e1a47",
        "alive": "#ff006e",
        "dead": "#1b1034",
        "text": "#fbf8f3",
        "button_bg": "#8338ec",
        "button_hover": "#a855f7",
        "button_text": "#ffffff"
    },
    "ocean": {
        "bg": "#0a2463",
        "panel": "#1e3a8a",
        "accent": "#3c56a8",
        "alive": "#00d9ff",
        "dead": "#1e3a8a",
        "text": "#e0f2fe",
        "button_bg": "#3b82f6",
        "button_hover": "#60a5fa",
        "button_text": "#ffffff"
    },
    "sunset": {
        "bg": "#2d1b4e",
        "panel": "#3d2963",
        "accent": "#4d3777",
        "alive": "#ff6b9d",
        "dead": "#3d2963",
        "text": "#fff0f5",
        "button_bg": "#c026d3",
        "button_hover": "#d946ef",
        "button_text": "#ffffff"
    }
}

# Variables globales
THEMES = DEFAULT_THEMES.copy()  # Collection de tous les thèmes (défaut + personnalisés)
current_theme = THEMES["dark"]  # Thème actuellement actif
current_theme_name = "dark"  # Nom du thème actuel

def load_favorite_colors():
    """
    Charge les couleurs favorites depuis le fichier.
    
    Returns:
        list: Liste des couleurs favorites au format hex
    """
    # Vérifie que le fichier existe
    if os.path.exists(FAVORITE_COLORS_FILE):
        try:
            # Ouvre le fichier en lecture
            with open(FAVORITE_COLORS_FILE, "r") as f:
                # Retourne la liste des couleurs désérialisée depuis JSON
                return json.load(f)
        except Exception:
            # Ignore les erreurs de lecture
            pass
    # Retourne une liste vide si le fichier n'existe pas ou en cas d'erreur
    return []

def save_favorite_colors(colors):
    """
    Sauvegarde les couleurs favorites dans un fichier.
    
    Args:
        colors (list): Liste des couleurs favorites à sauvegarder
    """
    try:
        # Ouvre le fichier en écriture (créé le fichier s'il n'existe pas)
        with open(FAVORITE_COLORS_FILE, "w") as f:
            # Écrit les couleurs au format JSON dans le fichier
            json.dump(colors, f)
    except Exception:
        # Ignore les erreurs d'écriture
        pass

def load_custom_themes():
    """
    Charge les thèmes personnalisés depuis le fichier.
    Fusionne avec les thèmes par défaut.
    """
    global THEMES

    # Réinitialise avec les thèmes par défaut pour partir d'une base propre
    THEMES = DEFAULT_THEMES.copy()

    # Vérifie que le fichier des thèmes personnalisés existe
    if os.path.exists(CUSTOM_THEMES_FILE):
        try:
            # Ouvre le fichier en lecture
            with open(CUSTOM_THEMES_FILE, "r") as f:
                # Charge les thèmes personnalisés depuis JSON
                custom = json.load(f)
                # Ajoute les thèmes personnalisés aux thèmes existants (fusion)
                THEMES.update(custom)
        except Exception:
            # Ignore les erreurs de lecture
            pass

def save_custom_themes():
    """
    Sauvegarde uniquement les thèmes personnalisés.
    Les thèmes par défaut ne sont jamais sauvegardés.
    """
    # Filtre pour garder uniquement les thèmes qui ne sont pas par défaut
    # Utilise une compréhension de dictionnaire pour créer un nouveau dict
    custom = {k: v for k, v in THEMES.items() if k not in DEFAULT_THEMES}

    try:
        # Ouvre le fichier en écriture
        with open(CUSTOM_THEMES_FILE, "w") as f:
            # Sauvegarde les thèmes avec indentation pour une meilleure lisibilité
            json.dump(custom, f, indent=2)
    except Exception:
        # Ignore les erreurs d'écriture
        pass

def delete_custom_theme(theme_name):
    """
    Supprime un thème personnalisé.
    Les thèmes par défaut ne peuvent pas être supprimés.
    
    Args:
        theme_name (str): Nom du thème à supprimer
        
    Returns:
        bool: True si le thème a été supprimé, False sinon
    """
    global THEMES, current_theme, current_theme_name

    # Empêche la suppression d'un thème par défaut (protection)
    if theme_name in DEFAULT_THEMES:
        return False

    # Vérifie que le thème existe dans la collection
    if theme_name in THEMES:
        # Supprime le thème du dictionnaire
        del THEMES[theme_name]
        # Sauvegarde les changements dans le fichier
        save_custom_themes()

        # Si le thème supprimé était actuellement actif
        if current_theme_name == theme_name:
            # Revenir au thème dark par défaut pour éviter un état invalide
            current_theme_name = "dark"
            current_theme = THEMES["dark"]
            # Sauvegarde la nouvelle configuration
            save_config()

        # Retourne True pour indiquer que la suppression a réussi
        return True

    # Retourne False si le thème n'existe pas
    return False

def load_config():
    """
    Charge la configuration globale de l'application.
    Restaure le thème, la vitesse du jeu et l'état de pause.
    
    Returns:
        bool: True si le jeu était en cours, False sinon
    """
    global current_theme, current_theme_name

    # Charge les thèmes personnalisés d'abord
    load_custom_themes()

    # Import local pour éviter les imports circulaires
    import gamelife_core as core

    # Par défaut, on considère que le jeu est en pause
    was_running = False

    # Vérifie que le fichier de configuration existe
    if os.path.exists(CONFIG_FILE):
        try:
            # Ouvre le fichier en lecture
            with open(CONFIG_FILE, "r") as f:
                # Charge la configuration depuis JSON
                cfg = json.load(f)

                # Récupère le thème sauvegardé (par défaut "dark" si absent)
                theme_name = cfg.get("theme", "dark")
                current_theme_name = theme_name
                # Utilise le thème sauvegardé ou dark si le thème n'existe plus
                current_theme = THEMES.get(theme_name, THEMES["dark"])

                # Restaure la vitesse du jeu sauvegardée
                core._speed = cfg.get("speed", core._speed)

                # Récupère l'état du jeu (en cours ou en pause)
                was_running = cfg.get("was_running", False)
        except Exception:
            # Ignore les erreurs de lecture et utilise les valeurs par défaut
            pass

    # Retourne l'état du jeu pour que l'appelant puisse décider de le relancer
    return was_running

def save_config():
    """
    Sauvegarde la configuration actuelle.
    Enregistre le thème actif, la vitesse du jeu et l'état de pause.
    """
    # Import local pour éviter les imports circulaires
    import gamelife_core as core

    # Crée le dictionnaire de configuration avec toutes les données à sauvegarder
    cfg = {
        "theme": current_theme_name,  # Nom du thème actuel
        "speed": core._speed,  # Vitesse actuelle du jeu
        "was_running": core.running.is_set()  # État du jeu (True = en cours, False = en pause)
    }

    try:
        # Ouvre le fichier en écriture
        with open(CONFIG_FILE, "w") as f:
            # Sauvegarde la configuration au format JSON
            json.dump(cfg, f)
    except Exception:
        # Ignore les erreurs d'écriture
        pass

def change_theme(theme_name):
    """
    Change le thème actif.
    
    Args:
        theme_name (str): Nom du thème à activer
        
    Returns:
        bool: True si le thème a été changé, False sinon
    """
    global current_theme, current_theme_name

    # Vérifie que le thème demandé existe dans la collection
    if theme_name in THEMES:
        # Met à jour le nom du thème actuel
        current_theme_name = theme_name
        # Met à jour le dictionnaire de couleurs du thème actuel
        current_theme = THEMES[theme_name]
        # Sauvegarde le changement dans la configuration
        save_config()
        # Retourne True pour indiquer que le changement a réussi
        return True

    # Retourne False si le thème demandé n'existe pas
    return False