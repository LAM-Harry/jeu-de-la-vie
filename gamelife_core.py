"""
Game of Life - Core Logic (Threads & Barriers)
Contient la logique principale du jeu demandée par le TP :
- Gestion des threads (un thread par cellule)
- Barrière de synchronisation
- Règles d'évolution de Conway
- Grilles et calculs
"""

import threading
import random
import time

# Variables globales du jeu
T = []  # Grille actuelle du jeu (matrice 2D)
Tnext = []  # Grille suivante (calculée avant l'échange)
n = 30  # Taille de la grille (n x n cellules)
cell_size = 20  # Taille d'une cellule en pixels (utilisée par l'affichage)
threads = []  # Liste contenant tous les threads des cellules
barrier = None  # Barrière de synchronisation pour les threads
stop_event = threading.Event()  # Événement pour arrêter complètement les threads
running = threading.Event()  # Événement indiquant si la simulation tourne
step_event = threading.Event()  # Événement pour exécuter une seule génération (mode pas à pas)
redraw_event = threading.Event()  # Événement pour demander un redessin de la grille
gen_counter = 0  # Compteur de générations (commence à 0)
speed_lock = threading.Lock()  # Verrou pour protéger l'accès à la vitesse (thread-safe)
_speed = 5.0  # Vitesse de simulation (générations par seconde)
swap_lock = threading.Lock()  # Verrou utilisé lors de l'échange des grilles

# Paramètres par défaut et limites
DEFAULT_N = 30  # Taille par défaut de la grille
CELL_SIZE = 20  # Taille par défaut d'une cellule en pixels
MIN_N = 5  # Taille minimale de la grille
MAX_N = 80  # Taille maximale de la grille

def make_grid(size):
    """
    Crée une grille de taille (size + 2) x (size + 2).
    Les bordures (+2) servent de tampon pour simplifier les calculs des voisins.
    
    Args:
        size (int): Taille réelle de la grille (sans bordures)
        
    Returns:
        list: Grille 2D initialisée à 0 (toutes les cellules mortes)
    """
    # Crée une matrice (size+2) x (size+2) remplie de zéros
    # La bordure extérieure reste à 0 et ne sera jamais utilisée
    return [[0] * (size + 2) for _ in range(size + 2)]

def has_living_cells():
    """
    Vérifie s'il reste au moins une cellule vivante dans la grille.
    
    Returns:
        bool: True si au moins une cellule est vivante, False sinon
    """
    # Parcourt toutes les cellules (hors bordures)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # Vérifie si la cellule est vivante
            if T[i][j] == 1:
                return True
    # Aucune cellule vivante trouvée
    return False

def randomize_grid(grid):
    """
    Remplit la grille aléatoirement avec environ 25% de cellules vivantes.
    
    Args:
        grid (list): Grille à remplir
    """
    # Parcourt toutes les cellules (hors bordures)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # Génère une cellule vivante avec une probabilité de 25%
            # random.random() retourne un nombre entre 0 et 1
            grid[i][j] = 1 if random.random() < 0.25 else 0

def clear_grid(grid):
    """
    Vide complètement la grille (toutes les cellules mortes).
    
    Args:
        grid (list): Grille à vider
    """
    # Parcourt toutes les cellules (hors bordures)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # Met chaque cellule à 0 (morte)
            grid[i][j] = 0

def barrier_action():
    """
    Action exécutée automatiquement par la barrière après que tous les threads ont terminé.
    Cette fonction est appelée par UN SEUL thread (le dernier arrivé).
    """
    global T, Tnext, gen_counter

    # Échange les grilles actuelle et suivante de manière atomique
    with swap_lock:
        # La grille calculée devient la grille actuelle
        T, Tnext = Tnext, T
        # Incrémente le compteur de générations
        gen_counter += 1

    # Import local pour éviter les dépendances circulaires
    from history_manager import save_state_to_history

    # Sauvegarde l'état actuel dans l'historique
    save_state_to_history()

    # Demande un redessin de la grille à l'interface graphique
    redraw_event.set()

    # Si on était en mode "une seule étape" (pas à pas)
    if step_event.is_set():
        # Arrête immédiatement la simulation après cette génération
        running.clear()
        # Réinitialise le flag d'étape unique
        step_event.clear()

    # Applique une pause selon la vitesse choisie
    with speed_lock:
        # Copie locale de la vitesse pour éviter de garder le verrou
        local_speed = _speed

    # Si la vitesse est positive, applique un délai
    if local_speed > 0:
        # Délai = 1 / vitesse (en secondes)
        # Ex: vitesse=5 → délai=0.2s → 5 générations/seconde
        time.sleep(max(0.0, 1.0 / local_speed))

def cell_thread(i, j):
    """
    Thread associé à une cellule (i, j).
    Ce thread tourne en boucle infinie jusqu'à ce que stop_event soit activé.
    
    Args:
        i (int): Ligne de la cellule (1 à n)
        j (int): Colonne de la cellule (1 à n)
    """
    try:
        # Boucle principale du thread
        while not stop_event.is_set():
            # Attend que la simulation soit lancée ou que l'arrêt soit demandé
            while not (running.is_set() or stop_event.is_set()):
                # Petite pause pour ne pas consommer de CPU inutilement
                time.sleep(0.01)

            # Vérifie si l'arrêt a été demandé
            if stop_event.is_set():
                break  # Sort de la boucle principale

            # Calcule le nombre de voisins vivants (8 cellules autour)
            neighbors = (
                T[i-1][j-1] + T[i-1][j] + T[i-1][j+1] +  # Ligne du dessus
                T[i][j-1] + T[i][j+1] +  # Ligne du milieu (gauche et droite)
                T[i+1][j-1] + T[i+1][j] + T[i+1][j+1]  # Ligne du dessous
            )

            # Applique les règles de Conway
            if T[i][j] == 1:
                # Cellule vivante : survit avec 2 ou 3 voisins, sinon meurt
                Tnext[i][j] = 1 if neighbors in (2, 3) else 0
            else:
                # Cellule morte : naît avec exactement 3 voisins
                Tnext[i][j] = 1 if neighbors == 3 else 0

            # Attend que toutes les cellules aient fini leur calcul
            # Le dernier thread arrivé exécutera barrier_action()
            barrier.wait()

    except Exception as e:
        # Affiche une erreur si un thread plante (pour le débogage)
        print(f"Erreur thread {i},{j}: {e}")

def start_workers(grid_size):
    """
    Crée et démarre un thread pour chaque cellule de la grille.
    
    Args:
        grid_size (int): Taille de la grille (nombre de cellules par côté)
    """
    global threads, barrier, T, Tnext, n, stop_event, running, gen_counter

    # Arrête les anciens threads s'ils existent
    stop_workers()

    # Met à jour la taille de la grille
    n = grid_size

    # Initialise les grilles (actuelle et suivante)
    T = make_grid(n)
    Tnext = make_grid(n)

    # Réinitialise le compteur de générations à 0
    gen_counter = 0

    # Nombre total de threads (un par cellule)
    parties = n * n

    # Crée la barrière avec l'action associée
    # parties threads doivent appeler wait() avant que barrier_action() soit exécutée
    barrier = threading.Barrier(parties, action=barrier_action)

    # Initialise la liste des threads
    threads = []
    # Réinitialise les événements
    stop_event.clear()
    running.clear()

    # Crée et démarre les threads des cellules
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # Crée un thread pour la cellule (i, j)
            t = threading.Thread(
                target=cell_thread,  # Fonction à exécuter
                args=(i, j),  # Arguments de la fonction
                daemon=True  # Thread daemon (se ferme avec le programme)
            )
            # Ajoute le thread à la liste
            threads.append(t)
            # Démarre le thread
            t.start()

def stop_workers():
    """
    Arrête proprement tous les threads en cours.
    """
    global threads, stop_event

    # Vérifie s'il y a des threads à arrêter
    if threads:
        # Signale l'arrêt à tous les threads
        stop_event.set()
        # Laisse un peu de temps aux threads pour terminer proprement
        time.sleep(0.1)
        # Vide la liste des threads
        threads = []
        # Réinitialise l'événement d'arrêt pour une prochaine utilisation
        stop_event.clear()

def set_speed(new_speed):
    """
    Modifie la vitesse de simulation de manière thread-safe.
    
    Args:
        new_speed (float): Nouvelle vitesse (générations par seconde)
    """
    global _speed
    # Utilise le verrou pour garantir la cohérence
    with speed_lock:
        # Convertit en float pour s'assurer du type
        _speed = float(new_speed)

def get_speed():
    """
    Retourne la vitesse actuelle de la simulation.
    
    Returns:
        float: Vitesse actuelle (générations par seconde)
    """
    # Utilise le verrou pour garantir une lecture cohérente
    with speed_lock:
        return _speed