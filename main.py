"""
Game of Life - Version Moderne Complète Améliorée 
Réalisé pour le Mini-Projet Threads (Programmation concurrente)
Auteur: LAM Hoang Anh Harry

Point d'entrée principal de l'application

Améliorations dans cette version:
- Grille qui remplit complètement l'espace disponible
- Redimensionnement automatique et optimal
- Taille de cellule minimum réduite pour plus de flexibilité
- Meilleure gestion de l'espace écran
- Architecture modulaire avec séparation des responsabilités

Dépendances optionnelles:
- PIL/Pillow: Pour un rendu plus rapide du gradient de couleurs
  Installation: pip install Pillow

Structure du projet:
- gamelife_core.py : Logique du jeu (threads, barrière, règles de Conway)
- history_manager.py : Gestion de l'historique (undo/redo)
- theme_manager.py : Gestion des thèmes et personnalisation
- gui_components.py : Composants GUI réutilisables
- gui_windows.py : Fenêtres principales (Menu, Tutoriel, Créateur de thème)
- gui_game.py : Fenêtre de simulation du jeu
- main.py : Point d'entrée (ce fichier)
"""

from gui_windows import ModernMainMenu

# Point d'entrée du programme
if __name__ == "__main__":
    # Crée l'instance du menu principal
    menu = ModernMainMenu()
    # Lance la boucle d'événements Tkinter (boucle principale de l'application)
    menu.mainloop()