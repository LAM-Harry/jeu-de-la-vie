"""
History Manager - Gestion de l'historique des générations
Permet de naviguer dans l'historique (undo/redo)
"""

import json
import os
import gamelife_core as core

# Dictionnaire contenant l'état de la grille pour chaque génération
# Format : {numero_generation: grille}
generation_history = {}

# Constantes de configuration
MAX_HISTORY_GENERATIONS = 100  # Nombre maximum de générations conservées en mémoire
HISTORY_FILE = "gamelife_history.json"  # Fichier de sauvegarde de l'historique

def save_state_to_history():
    """
    Sauvegarde l'état actuel de la grille dans l'historique.
    Limite la taille de l'historique à MAX_HISTORY_GENERATIONS.
    """
    global generation_history

    # Vérifie que la grille existe
    if not core.T:
        return

    # Copie profonde de la grille actuelle pour éviter les références
    # Chaque ligne est copiée indépendamment pour préserver l'état
    state = [row[:] for row in core.T]

    # Sauvegarde l'état avec le numéro de génération comme clé
    generation_history[core.gen_counter] = state

    # Limite la taille de l'historique si nécessaire
    if len(generation_history) > MAX_HISTORY_GENERATIONS:
        # Trouve la génération la plus ancienne dans l'historique
        min_gen = min(generation_history.keys())
        # Supprime cette génération pour libérer de la mémoire
        del generation_history[min_gen]

def load_state_from_history(direction):
    """
    Charge un état depuis l'historique.
    
    Args:
        direction (str): Direction de navigation ("undo" ou "redo")
    
    Returns:
        bool: True si l'opération a réussi, False sinon
    """
    # Vérifie que l'historique existe et n'est pas vide
    if not generation_history:
        return False

    # Liste triée des générations disponibles (ordre chronologique)
    available_gens = sorted(generation_history.keys())

    if direction == "undo":
        # Cherche les générations antérieures à la génération actuelle
        previous_gens = [g for g in available_gens if g < core.gen_counter]
        if previous_gens:
            # Prend la génération précédente la plus proche (dernière de la liste)
            target_gen = previous_gens[-1]
        else:
            # Aucune génération antérieure disponible
            return False

    elif direction == "redo":
        # Cherche les générations ultérieures à la génération actuelle
        next_gens = [g for g in available_gens if g > core.gen_counter]
        if next_gens:
            # Prend la génération suivante la plus proche (première de la liste)
            target_gen = next_gens[0]
        else:
            # Aucune génération ultérieure disponible
            return False

    else:
        # Direction inconnue, opération impossible
        return False

    # Récupère l'état de la grille à restaurer depuis l'historique
    state = generation_history[target_gen]

    # Copie les cellules dans la grille actuelle
    # Parcourt toutes les lignes de l'état sauvegardé
    for i in range(len(state)):
        # Parcourt toutes les colonnes de chaque ligne
        for j in range(len(state[i])):
            # Restaure l'état de chaque cellule (vivante ou morte)
            core.T[i][j] = state[i][j]

    # Met à jour le compteur de génération pour refléter le nouvel état
    core.gen_counter = target_gen

    # Force le rafraîchissement de l'affichage pour montrer le nouvel état
    core.redraw_event.set()

    # Opération réussie
    return True

def can_undo():
    """
    Vérifie s'il est possible de revenir à une génération précédente.
    
    Returns:
        bool: True si un undo est possible, False sinon
    """
    # Aucun undo possible si l'historique est vide
    if not generation_history:
        return False

    # Récupère les générations disponibles triées
    available_gens = sorted(generation_history.keys())

    # Undo possible si on n'est pas à la plus ancienne génération
    # Compare la génération actuelle avec la plus ancienne disponible
    return core.gen_counter > min(available_gens)

def can_redo():
    """
    Vérifie s'il est possible d'aller à une génération suivante.
    
    Returns:
        bool: True si un redo est possible, False sinon
    """
    # Aucun redo possible si l'historique est vide
    if not generation_history:
        return False

    # Récupère les générations disponibles triées
    available_gens = sorted(generation_history.keys())

    # Redo possible si on n'est pas à la plus récente génération
    # Compare la génération actuelle avec la plus récente disponible
    return core.gen_counter < max(available_gens)

def clear_history():
    """
    Supprime complètement l'historique des générations.
    Libère la mémoire utilisée par tous les snapshots sauvegardés.
    """
    global generation_history
    # Vide le dictionnaire d'historique (supprime toutes les entrées)
    generation_history.clear()

def save_history_to_file():
    """
    Sauvegarde l'historique complet dans un fichier JSON.
    Enregistre l'historique, la génération courante et l'état de la grille.
    """
    try:
        # Ouvre le fichier en écriture (écrase le fichier existant)
        with open(HISTORY_FILE, "w") as f:
            # Convertit les clés entières en chaînes pour la compatibilité JSON
            # JSON ne supporte pas les clés entières directement
            history_data = {
                str(gen): state for gen, state in generation_history.items()
            }

            # Sauvegarde l'historique, la génération courante et la grille
            # Crée un objet JSON avec trois champs principaux
            json.dump({
                "history": history_data,  # Historique complet des générations
                "current_gen": core.gen_counter,  # Numéro de la génération actuelle
                "grid_state": core.T  # État actuel de la grille
            }, f)
    except Exception:
        # Ignore les erreurs d'écriture (permissions, espace disque, etc.)
        pass

def load_history_from_file():
    """
    Charge l'historique depuis un fichier JSON.
    Restaure l'historique, la génération courante et l'état de la grille.
    """
    global generation_history

    # Vérifie que le fichier existe avant de tenter de le lire
    if os.path.exists(HISTORY_FILE):
        try:
            # Ouvre le fichier en lecture
            with open(HISTORY_FILE, "r") as f:
                # Charge les données depuis JSON
                data = json.load(f)

                # Récupère l'historique sauvegardé (dictionnaire vide si absent)
                history_data = data.get("history", {})

                # Reconvertit les clés de chaînes en entiers
                # Les clés JSON sont toujours des chaînes, on doit les reconvertir
                generation_history = {
                    int(gen): state for gen, state in history_data.items()
                }

                # Restaure la génération courante (0 par défaut si absente)
                core.gen_counter = data.get("current_gen", 0)

                # Récupère la grille sauvegardée (None si absente)
                saved_grid = data.get("grid_state", None)

                # Restaure la grille si possible (vérifie que les deux grilles existent)
                if saved_grid and core.T:
                    # Parcourt toutes les lignes de la grille sauvegardée
                    for i in range(len(saved_grid)):
                        # Parcourt toutes les colonnes de chaque ligne
                        for j in range(len(saved_grid[i])):
                            # Vérifie que la position existe dans la grille actuelle
                            # Évite les erreurs si les dimensions ont changé
                            if i < len(core.T) and j < len(core.T[i]):
                                # Restaure l'état de la cellule
                                core.T[i][j] = saved_grid[i][j]
        except Exception:
            # Ignore les erreurs de lecture (fichier corrompu, format invalide, etc.)
            pass