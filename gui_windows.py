"""
GUI Windows - Fenêtres principales de l'application
Menu principal, fenêtre de jeu, tutoriel interactif et créateur de thèmes
"""

import tkinter as tk
from tkinter import ttk

import gamelife_core as core
import theme_manager as tm
import history_manager as hm

from gui_components import (
    show_custom_message,
    show_custom_input,
    show_color_picker,
    ModernButton,
    ThemePreview
)

class ThemeCreatorWindow(tk.Toplevel):
    """
    Fenêtre dédiée à la création et à la modification de thèmes personnalisés.
    Permet de sélectionner les couleurs et d'afficher un aperçu en temps réel.
    """

    def __init__(self, master, edit_theme=None):
        """
        Initialise la fenêtre du créateur de thème.
        Configure la fenêtre, les variables et charge les données du thème à éditer si nécessaire.

        Args:
            master: Fenêtre parente (tk.Tk ou tk.Toplevel)
            edit_theme (str, optional): Nom du thème à modifier. None si création d'un nouveau thème
        """
        # Appel du constructeur de la classe parente Toplevel
        super().__init__(master)

        # Configuration générale de la fenêtre
        self.title("🎨 Créateur de Thème")  # Titre affiché dans la barre
        self.geometry("850x750")  # Dimensions fixes de la fenêtre
        self.resizable(False, False)  # Empêche le redimensionnement
        self.config(bg=tm.current_theme["bg"])  # Applique le thème actuel

        # Conserve le contexte d'édition ou de création
        self.edit_theme = edit_theme  # Nom du thème édité ou None
        self.theme_colors = {}  # Dictionnaire des couleurs du thème

        # Si un thème existant est fourni, on en charge les couleurs
        if edit_theme and edit_theme in tm.THEMES:
            # Copie profonde pour éviter de modifier l'original
            self.theme_colors = tm.THEMES[edit_theme].copy()
            self.theme_name = edit_theme  # Nom du thème en cours d'édition
        else:
            # Valeurs par défaut pour un nouveau thème (basées sur le thème dark)
            self.theme_colors = {
                "bg": "#1a1a2e",  # Arrière-plan principal
                "panel": "#16213e",  # Couleur des panneaux
                "accent": "#0f3460",  # Couleur d'accent
                "alive": "#00ff88",  # Cellules vivantes
                "dead": "#2d3561",  # Cellules mortes
                "text": "#eeeeee",  # Texte principal
                "button_bg": "#0f3460",  # Fond des boutons
                "button_hover": "#1e5f8c",  # Couleur au survol
                "button_text": "#ffffff"  # Texte des boutons
            }
            self.theme_name = ""  # Aucun nom pour un nouveau thème

        # Construction de l'interface graphique
        self.create_ui()

    def create_ui(self):
        """
        Construit l'interface graphique du créateur de thème.
        Crée la mise en page avec sélecteurs de couleurs à gauche et aperçu à droite.
        """
        # Conteneur principal occupant toute la fenêtre
        main_container = tk.Frame(self, bg=tm.current_theme["bg"])
        main_container.pack(fill='both', expand=True)

        # Titre de la fenêtre en haut
        title = tk.Label(
            main_container,
            text="🎨 Créateur de Thème Personnalisé",
            font=("Arial", 18, "bold"),  # Police grande et en gras
            bg=tm.current_theme["bg"],
            fg=tm.current_theme["text"]
        )
        title.pack(pady=(0, 20))  # Marge inférieure de 20px

        # Conteneur principal du contenu (gauche + droite)
        content = tk.Frame(main_container, bg=tm.current_theme["bg"])
        content.pack(fill='both', expand=True)

        # Zone gauche : paramètres du thème (largeur fixe)
        left_frame = tk.Frame(content, bg=tm.current_theme["panel"], width=420)
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        left_frame.pack_propagate(False)  # Empêche le redimensionnement automatique

        # Conteneur interne avec padding pour les widgets
        left_inner = tk.Frame(left_frame, bg=tm.current_theme["panel"])
        left_inner.pack(padx=20, pady=20)

        # Champ de saisie du nom du thème
        tk.Label(
            left_inner,
            text="Nom du thème :",
            font=("Arial", 12, "bold"),
            bg=tm.current_theme["panel"],
            fg=tm.current_theme["text"]
        ).pack(pady=5)

        # Widget Entry pour saisir le nom
        self.name_entry = tk.Entry(
            left_inner,
            font=("Arial", 12),
            width=25,  # Largeur en caractères
            bg=tm.current_theme["accent"],
            fg=tm.current_theme["text"]
        )
        self.name_entry.pack(pady=5)

        # Mise à jour immédiate de l'aperçu lors de la saisie
        # Bind l'événement KeyRelease pour détecter chaque frappe
        self.name_entry.bind('<KeyRelease>', lambda e: self.update_preview())

        # En mode édition, le nom du thème est verrouillé
        if self.edit_theme:
            self.name_entry.insert(0, self.edit_theme)  # Pré-remplit le champ
            self.name_entry.config(state='readonly')  # Désactive la modification

        # Titre de la section de sélection des couleurs
        tk.Label(
            left_inner,
            text="Choisissez les couleurs :",
            font=("Arial", 12, "bold"),
            bg=tm.current_theme["panel"],
            fg=tm.current_theme["text"]
        ).pack(pady=(15, 10))

        # Dictionnaire pour stocker les références aux widgets de couleurs
        self.color_buttons = {}

        # Libellés des couleurs configurables (clé : label affiché)
        color_labels = {
            "bg": "Arrière-plan principal",
            "panel": "Panneaux",
            "accent": "Accent",
            "alive": "Cellule vivante",
            "dead": "Cellule morte",
            "text": "Texte",
            "button_bg": "Bouton",
            "button_hover": "Bouton (survol)",
            "button_text": "Texte bouton"
        }

        # Création dynamique des lignes de sélection de couleur
        for key, label in color_labels.items():
            # Frame pour une ligne de couleur
            row_frame = tk.Frame(left_inner, bg=tm.current_theme["panel"])
            row_frame.pack(fill='x', pady=3)

            # Nom de la couleur (aligné à gauche)
            tk.Label(
                row_frame,
                text=label + " :",
                font=("Arial", 9),
                bg=tm.current_theme["panel"],
                fg=tm.current_theme["text"],
                width=18,  # Largeur fixe pour alignement
                anchor='w'  # Ancrage à gauche (west)
            ).pack(side='left', padx=2)

            # Aperçu visuel de la couleur (petit carré coloré)
            color_display = tk.Canvas(
                row_frame,
                width=40,  # Carré de 40x25 pixels
                height=25,
                bg=self.theme_colors[key],  # Couleur actuelle
                highlightthickness=1,  # Bordure de 1px
                highlightbackground=tm.current_theme["text"]
            )
            color_display.pack(side='left', padx=3)

            # Code hexadécimal affiché à côté
            color_code = tk.Label(
                row_frame,
                text=self.theme_colors[key],
                font=("Arial", 7),
                bg=tm.current_theme["panel"],
                fg=tm.current_theme["text"],
                width=8
            )
            color_code.pack(side='left', padx=2)

            # Bouton d'ouverture du sélecteur de couleur
            # Lambda avec arguments par défaut pour capturer les valeurs actuelles
            btn = tk.Button(
                row_frame,
                text="🎨",
                command=lambda k=key, c=color_display, cc=color_code: self.choose_color(k, c, cc),
                bg=tm.current_theme["button_bg"],
                fg=tm.current_theme["button_text"],
                font=("Arial", 9),
                relief='flat',  # Sans relief 3D
                cursor="hand2",  # Curseur en forme de main
                width=3
            )
            btn.pack(side='left', padx=2)

            # Stockage des références pour mises à jour ultérieures
            self.color_buttons[key] = (color_display, color_code)

        # Zone droite : aperçu du thème (largeur fixe)
        right_frame = tk.Frame(content, bg=tm.current_theme["bg"], width=400)
        right_frame.pack(side='left', fill='both', expand=True)
        right_frame.pack_propagate(False)

        # Titre de la section aperçu
        tk.Label(
            right_frame,
            text="👁️ Aperçu en Temps Réel",
            font=("Arial", 12, "bold"),
            bg=tm.current_theme["bg"],
            fg=tm.current_theme["text"]
        ).pack(pady=10)

        # Conteneur pour le canvas d'aperçu
        preview_container = tk.Frame(right_frame, bg=tm.current_theme["panel"])
        preview_container.pack(pady=10)

        # Canvas d'aperçu du thème (widget personnalisé ThemePreview)
        self.preview_canvas = ThemePreview(
            preview_container,
            self.theme_colors,  # Thème à prévisualiser
            width=340,
            height=200
        )
        self.preview_canvas.pack(padx=10, pady=10)

        # Section aperçu du bouton de thème
        tk.Label(
            right_frame,
            text="Apparence du bouton de thème :",
            font=("Arial", 10),
            bg=tm.current_theme["bg"],
            fg=tm.current_theme["text"]
        ).pack(pady=(20, 5))

        # Bouton simulant l'apparence dans la liste des thèmes
        self.theme_button_preview = tk.Button(
            right_frame,
            text=self.theme_name.upper()[:6] if self.theme_name else "THEME",  # 6 premiers caractères
            bg=self.theme_colors["alive"],  # Fond = couleur des cellules vivantes
            fg=self.theme_colors["bg"],  # Texte = couleur de fond
            font=("Arial", 10, "bold"),
            relief='flat',
            width=12,
            height=2
        )
        self.theme_button_preview.pack(pady=10)

        # Boutons d'action en bas de la fenêtre
        action_frame = tk.Frame(main_container, bg=tm.current_theme["bg"])
        action_frame.pack(pady=20)

        # Bouton pour enregistrer le thème
        ModernButton(
            action_frame,
            "💾 Enregistrer",
            self.save_theme,
            width=180,
            height=45,
            bg=tm.current_theme["bg"]
        ).pack(side='left', padx=10)

        # Bouton pour annuler et fermer
        ModernButton(
            action_frame,
            "❌ Annuler",
            self.destroy,  # Ferme la fenêtre sans sauvegarder
            width=180,
            height=45,
            bg=tm.current_theme["bg"]
        ).pack(side='left', padx=10)

    def choose_color(self, key, canvas, color_code_label):
        """
        Ouvre le sélecteur de couleur et met à jour
        la couleur correspondante du thème.
        
        Args:
            key (str): Clé de la couleur dans le dictionnaire (ex: "bg", "alive")
            canvas (tk.Canvas): Canvas affichant l'aperçu de la couleur
            color_code_label (tk.Label): Label affichant le code hexadécimal
        """
        # Ouverture du sélecteur avec la couleur actuelle comme valeur initiale
        color = show_color_picker(self, f"Couleur : {key}", self.theme_colors[key])

        # Si une couleur a été sélectionnée (pas d'annulation)
        if color:
            # Met à jour la couleur dans le dictionnaire du thème
            self.theme_colors[key] = color
            # Met à jour le canvas d'aperçu
            canvas.config(bg=color)
            # Met à jour le texte du code hexadécimal
            color_code_label.config(text=color)

            # Rafraîchissement immédiat de l'aperçu complet
            self.update_preview()

    def update_preview(self):
        """
        Met à jour l'aperçu graphique et le bouton
        représentant le thème en temps réel.
        """
        # Mise à jour du canvas d'aperçu avec les nouvelles couleurs
        self.preview_canvas.update_theme(self.theme_colors)

        # Génération du texte du bouton à partir du nom du thème
        theme_name = (
            self.name_entry.get().strip().upper()[:6]  # Prend les 6 premiers caractères en majuscules
            if self.name_entry.get().strip()  # Si un nom est saisi
            else "THEME"  # Sinon texte par défaut
        )

        # Application des nouvelles couleurs au bouton d'aperçu
        self.theme_button_preview.config(
            text=theme_name,
            bg=self.theme_colors["alive"],  # Fond = couleur vivante
            fg=self.theme_colors["bg"]  # Texte = couleur de fond
        )

    def save_theme(self):
        """
        Valide, sauvegarde et applique le thème personnalisé.
        Effectue plusieurs vérifications avant la sauvegarde.
        """
        # Récupère le nom du thème en minuscules et sans espaces
        theme_name = self.name_entry.get().strip().lower()

        # Vérification du nom du thème (ne doit pas être vide)
        if not theme_name:
            show_custom_message(self, "Erreur", "Veuillez entrer un nom pour le thème !", "error")
            return

        # Vérification des conflits de noms (seulement en mode création)
        if not self.edit_theme and theme_name in tm.THEMES:
            show_custom_message(self, "Erreur", "Ce nom de thème existe déjà !", "error")
            return

        # Empêche d'utiliser un nom réservé aux thèmes par défaut
        if not self.edit_theme and theme_name in tm.DEFAULT_THEMES:
            show_custom_message(self, "Erreur", "Ce nom est réservé aux thèmes par défaut !", "error")
            return

        # Sauvegarde du thème personnalisé dans le dictionnaire global
        tm.THEMES[theme_name] = self.theme_colors.copy()
        # Sauvegarde dans le fichier JSON
        tm.save_custom_themes()

        # Application immédiate du thème créé/modifié
        tm.current_theme_name = theme_name
        tm.current_theme = tm.THEMES[theme_name]
        tm.save_config()  # Sauvegarde de la configuration

        # Sauvegarde la référence au parent AVANT de détruire la fenêtre
        parent = self.master

        # Rafraîchissement des interfaces parentes si présentes
        # Vérifie que la méthode existe avant de l'appeler
        if hasattr(parent, 'create_ui'):
            parent.create_ui()  # Reconstruit l'interface du menu
        if hasattr(parent, 'refresh_themes'):
            parent.refresh_themes()  # Rafraîchit la liste des thèmes
        if hasattr(parent, 'refresh_theme_buttons'):
            parent.refresh_theme_buttons()

        # Redessin du jeu si nécessaire (fenêtre de jeu active)
        if hasattr(parent, 'canvas'):
            core.redraw_event.set()  # Déclenche le rafraîchissement

        # Rafraîchissement du menu principal si existant
        if hasattr(parent, 'return_to_menu') and self.master.return_to_menu:
            if hasattr(self.master.return_to_menu, 'create_ui'):
                try:
                    self.master.return_to_menu.create_ui()
                except:
                    pass  # Ignore les erreurs de rafraîchissement

        # Fermeture de la fenêtre de création
        self.destroy()

        # Confirmation utilisateur avec message de succès
        parent.after(100, lambda: show_custom_message(
            parent,
            "Succès",
            f"Thème '{theme_name}' enregistré et appliqué avec succès !",
            "success"
        ))

class ModernTutorialWindow(tk.Toplevel):
    """
    Fenêtre de tutoriel interactif expliquant le Jeu de la Vie et son interface.
    Navigation par pages avec texte explicatif et exemples visuels.
    """

    def __init__(self, master):
        """
        Initialise la fenêtre du tutoriel.
        Configure la fenêtre, charge les pages du tutoriel
        et affiche la première page.
        
        Args:
            master: Fenêtre parente (menu principal)
        """
        # Appel du constructeur de Toplevel
        super().__init__(master)

        # Configuration générale de la fenêtre
        self.title("📚 Tutoriel - Jeu de la Vie")
        self.geometry("950x700")  # Dimensions fixes
        self.resizable(False, False)  # Pas de redimensionnement
        self.config(bg=tm.current_theme["bg"])

        # Définition des pages du tutoriel (titre, texte, pattern optionnel)
        # Chaque page est un dictionnaire avec 3 clés
        self.pages = [
            {"title": "🎮 Bienvenue", "text": (
                "Bienvenue dans le Jeu de la Vie !\n\n"
                "Ce tutoriel va vous guider pas à pas dans\n"
                "l'utilisation de cette simulation fascinante.\n\n"
                "Le Jeu de la Vie est un automate cellulaire\n"
                "imaginé par John Conway en 1970.\n\n"
                "Version moderne avec threads concurrents\n"
                "et interface intuitive !"
            ), "pattern": None},
            
            {"title": "📋 Règles de base", "text": (
                "Le Jeu de la Vie suit des règles simples :\n\n"
                "• Une cellule vivante avec 2 ou 3 voisins SURVIT\n"
                "• Une cellule vivante avec <2 ou >3 voisins MEURT\n"
                "• Une cellule morte avec exactement 3 voisins NAÎT\n\n"
                "Les voisins incluent les 8 cases adjacentes\n"
                "(horizontales, verticales et diagonales).\n\n"
                "Ces règles simples créent des comportements\n"
                "complexes et fascinants !"
            ), "pattern": None},
            
            {"title": "🎮 Contrôles - Boutons principaux", "text": (
                "Contrôlez la simulation avec ces boutons :\n\n"
                "• ▶ Démarrer / ⏸ Pause\n"
                "  Lance ou met en pause la simulation automatique\n\n"
                "• ⏩ +1 Gen\n"
                "  Avance d'une seule génération (mode pas à pas)\n"
                "  Parfait pour analyser l'évolution !\n\n"
                "• 🎲 Aléatoire\n"
                "  Génère une grille aléatoire (~25% de cellules)\n\n"
                "• 🗑️ Effacer\n"
                "  Vide complètement la grille"
            ), "pattern": "block"},
            
            {"title": "↩️ Historique - Voyage dans le temps", "text": (
                "Naviguez dans l'historique des générations :\n\n"
                "• ◀ Précédent\n"
                "  Retourne à la génération précédente\n\n"
                "• ▶ Suivant\n"
                "  Avance à la génération suivante\n\n"
                "ℹ️ L'historique conserve les 100 dernières\n"
                "générations pour vous permettre d'analyser\n"
                "et de revenir en arrière.\n\n"
                "Les boutons sont grisés quand non disponibles."
            ), "pattern": "blinker"},
            
            {"title": "⚙️ Paramètres - Vitesse", "text": (
                "Ajustez la vitesse de simulation :\n\n"
                "• ⚡ Curseur Vitesse (1-30 gen/s)\n"
                "  Contrôle la rapidité de la simulation\n\n"
                "Conseils :\n"
                "• Vitesse 1-5 : Pour observer en détail\n"
                "• Vitesse 10-15 : Équilibre idéal\n"
                "• Vitesse 20-30 : Pour voir rapidement l'évolution\n\n"
                "La vitesse est sauvegardée automatiquement !"
            ), "pattern": None},
            
            {"title": "🎨 Thèmes - Personnalisation", "text": (
                "4 thèmes prédéfinis disponibles :\n\n"
                "• DARK : Sombre et élégant (défaut)\n"
                "• NEON : Couleurs vives et énergiques\n"
                "• OCEAN : Tons bleus apaisants\n"
                "• SUNSET : Ambiance chaude et rosée\n\n"
                "Cliquez simplement sur un bouton de thème\n"
                "pour l'appliquer instantanément !\n\n"
                "Vous pouvez aussi créer vos propres thèmes..."
            ), "pattern": "block"},
            
            {"title": "🎨 Créer vos thèmes", "text": (
                "Créez vos thèmes personnalisés !\n\n"
                "• ➕ Créer\n"
                "  Ouvre l'éditeur de thème avec :\n"
                "  - Sélecteur de couleurs 2D interactif\n"
                "  - Barre de teinte (hue)\n"
                "  - Couleurs favorites\n"
                "  - Aperçu en temps réel\n\n"
                "• ✏️ Modifier\n"
                "  Modifiez vos thèmes existants\n\n"
                "• 🗑️ Supprimer\n"
                "  Supprimez vos thèmes personnalisés"
            ), "pattern": None},
            
            {"title": "🖱️ Dessiner sur la grille", "text": (
                "Interagissez directement avec la grille !\n\n"
                "• Clic simple\n"
                "  Inverse l'état d'une cellule\n"
                "  (morte → vivante, vivante → morte)\n\n"
                "• Clic + Glisser\n"
                "  Dessinez ou effacez plusieurs cellules\n"
                "  Le mode (dessiner/effacer) dépend de\n"
                "  la première cellule cliquée\n\n"
                "Conseil : Mettez en pause pour dessiner\n"
                "tranquillement vos patterns !"
            ), "pattern": "blinker"},
            
            {"title": "🔲 Pattern : Block (Nature Morte)", "text": (
                "Le Block est un motif stable :\n\n"
                "• Formation carrée 2x2 de cellules\n"
                "• Ne change JAMAIS\n"
                "• C'est une \"nature morte\" (still life)\n\n"
                "Chaque cellule a exactement 3 voisins,\n"
                "donc elles survivent indéfiniment.\n\n"
                "Astuce : Parfait pour comprendre\n"
                "la stabilité dans le Jeu de la Vie.\n"
                "Essayez d'en créer plusieurs !"
            ), "pattern": "block"},
            
            {"title": "〰️ Pattern : Blinker (Oscillateur)", "text": (
                "Le Blinker est un oscillateur simple :\n\n"
                "• 3 cellules alignées verticalement\n"
                "• Alterne : vertical ↔ horizontal\n"
                "• Période de 2 générations\n\n"
                "C'est le plus petit oscillateur possible !\n\n"
                "Observez :\n"
                "1. Vertical : les cellules du haut/bas meurent,\n"
                "   les côtés naissent\n"
                "2. Horizontal : le processus inverse"
            ), "pattern": "blinker"},
            
            {"title": "✈️ Pattern : Glider (Vaisseau)", "text": (
                "Le Glider est un vaisseau spatial :\n\n"
                "• Se déplace en diagonale\n"
                "• Période de 4 générations\n"
                "• Parcourt toute la grille !\n\n"
                "C'est LE pattern le plus célèbre du\n"
                "Jeu de la Vie, découvert en 1970.\n\n"
                "Astuce : Placez-en plusieurs avec des\n"
                "décalages pour créer des collisions\n"
                "spectaculaires !"
            ), "pattern": "glider"},
            
            {"title": "💡 Conseils & Astuces", "text": (
                "Pour une meilleure expérience :\n\n"
                "✅ Démarrage :\n"
                "  - Utilisez 🎲 Aléatoire pour commencer\n"
                "  - Ou dessinez vos propres patterns\n\n"
                "✅ Analyse :\n"
                "  - Utilisez ⏩ +1 Gen pour étudier\n"
                "  - Naviguez avec ◀ / ▶ dans l'historique\n\n"
                "✅ Exploration :\n"
                "  - Cherchez \"Game of Life patterns\" en ligne\n"
                "  - Essayez Glider Gun, Pentadecathlon...\n\n"
                "Amusez-vous bien ! 🎉"
            ), "pattern": None},
        ]
        
        # Index de la page actuellement affichée
        self.current_page = 0

        # Construction de l'interface et affichage initial
        self.create_ui()
        self.update_page()

    def create_ui(self):
        """
        Construit l'interface graphique du tutoriel :
        - zone titre en haut
        - zone texte à gauche + exemple visuel à droite
        - navigation entre les pages en bas
        """

        # Conteneur principal avec marges
        main_container = tk.Frame(self, bg=tm.current_theme["bg"])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # En-tête avec le titre de la page (hauteur fixe)
        header = tk.Frame(main_container, bg=tm.current_theme["panel"], height=80)
        header.pack(fill='x', pady=(0, 15))
        header.pack_propagate(False)  # Empêche le redimensionnement

        # Label du titre (sera mis à jour à chaque page)
        self.title_label = tk.Label(
            header, text="", font=("Arial", 20, "bold"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["alive"]
        )
        self.title_label.pack(pady=20)

        # Zone centrale (texte + aperçu côte à côte)
        content = tk.Frame(main_container, bg=tm.current_theme["bg"])
        content.pack(fill='both', expand=True)

        # Partie gauche : texte explicatif (largeur fixe)
        left = tk.Frame(content, bg=tm.current_theme["panel"], width=500)
        left.pack(side='left', fill='both', expand=True, padx=(0, 15))
        left.pack_propagate(False)

        # Conteneur interne avec padding pour le texte
        text_inner = tk.Frame(left, bg=tm.current_theme["panel"])
        text_inner.pack(padx=30, pady=30)

        # Label du texte explicatif (sera mis à jour à chaque page)
        self.text_label = tk.Label(
            text_inner, text="", font=("Arial", 12),
            justify="left",  # Alignement du texte à gauche
            bg=tm.current_theme["panel"],
            fg=tm.current_theme["text"],
            wraplength=420  # Retour à la ligne automatique
        )
        self.text_label.pack()

        # Partie droite : canvas d'exemple de pattern
        right = tk.Frame(content, bg=tm.current_theme["bg"])
        right.pack(side='left', fill='both', expand=True)

        # Cadre décoratif pour le canvas
        canvas_frame = tk.Frame(right, bg=tm.current_theme["accent"])
        canvas_frame.pack(padx=10, pady=10)

        # Cadre intérieur (bordure visuelle)
        canvas_inner = tk.Frame(canvas_frame, bg=tm.current_theme["accent"])
        canvas_inner.pack(padx=3, pady=3)

        # Canvas pour dessiner les exemples de patterns
        self.example_canvas = tk.Canvas(
            canvas_inner, width=300, height=300,
            bg=tm.current_theme["bg"], highlightthickness=0
        )
        self.example_canvas.pack()

        # Barre de navigation (précédent / page / suivant / fermer)
        nav = tk.Frame(main_container, bg=tm.current_theme["bg"])
        nav.pack(pady=15)

        # Bouton pour revenir à la page précédente du tutoriel
        self.prev_btn = ModernButton(
            nav, "◀ Précédent", self.prev_page,
            width=140, height=40, bg=tm.current_theme["bg"]
        )
        self.prev_btn.pack(side='left', padx=10)

        # Indicateur de progression (page courante / total)
        self.page_label = tk.Label(
            nav, text="", font=("Arial", 11, "bold"),
            bg=tm.current_theme["bg"], fg=tm.current_theme["text"]
        )
        self.page_label.pack(side='left', padx=20)

        # Bouton pour passer à la page suivante du tutoriel
        self.next_btn = ModernButton(
            nav, "Suivant ▶", self.next_page,
            width=140, height=40, bg=tm.current_theme["bg"]
        )
        self.next_btn.pack(side='left', padx=10)

        # Bouton de fermeture immédiate du tutoriel
        ModernButton(
            nav, "❌ Fermer", self.destroy,
            width=120, height=40, bg=tm.current_theme["bg"]
        ).pack(side='left', padx=20)

    def draw_pattern(self, pattern):
        """
        Dessine un pattern d'exemple sur le canvas
        (block, blinker, glider ou vide si None).
        
        Args:
            pattern (str): Nom du pattern à dessiner ("block", "blinker", "glider" ou None)
        """

        # Nettoyage du canvas (supprime tous les éléments dessinés)
        self.example_canvas.delete('all')

        # Dessin de la grille de fond (6x6 cellules)
        cell_size = 60  # Taille d'une cellule en pixels
        for i in range(6):  # 6 lignes
            for j in range(6):  # 6 colonnes
                # Calcul des coordonnées de la cellule
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                # Dessin du rectangle (cellule morte)
                self.example_canvas.create_rectangle(
                    x0, y0, x1, y1,
                    fill=tm.current_theme["dead"],  # Couleur de fond
                    outline=tm.current_theme["bg"], width=2  # Bordure
                )

        # Aucun pattern à afficher (grille vide)
        if not pattern:
            return

        # Coordonnées prédéfinies des patterns célèbres
        # Format : liste de tuples (ligne, colonne) pour les cellules vivantes
        patterns = {
            "block": [(1,1),(1,2),(2,1),(2,2)],  # Carré 2x2
            "blinker": [(2,1),(2,2),(2,3)],  # 3 cellules alignées verticalement
            "glider": [(1,3),(2,1),(2,3),(3,2),(3,3)]  # Forme en L avec queue
        }

        # Récupère les coordonnées du pattern demandé
        coords = patterns.get(pattern, [])
        
        # Dessin des cellules vivantes du pattern
        for (r, c) in coords:
            # Calcul des coordonnées (ajustées de -1 car indexation commence à 1)
            x0 = (c - 1) * cell_size
            y0 = (r - 1) * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size
            # Dessin de la cellule vivante (légèrement réduite pour l'esthétique)
            self.example_canvas.create_rectangle(
                x0 + 2, y0 + 2, x1 - 2, y1 - 2,
                fill=tm.current_theme["alive"],  # Couleur des cellules vivantes
                outline=""  # Pas de bordure
            )

    def update_page(self):
        """
        Met à jour le contenu affiché selon la page courante :
        texte, titre, pattern et état des boutons de navigation.
        """

        # Récupère les données de la page actuelle
        page = self.pages[self.current_page]

        # Mise à jour du contenu textuel
        self.title_label.config(text=page["title"])  # Titre de la page
        self.text_label.config(text=page["text"])  # Texte explicatif
        # Affichage de la progression (ex: "3 / 13")
        self.page_label.config(
            text=f"{self.current_page + 1} / {len(self.pages)}"
        )

        # Mise à jour du pattern visuel sur le canvas
        self.draw_pattern(page.get("pattern"))

        # Gestion de l'état du bouton précédent
        # Désactivé sur la première page, activé sinon
        self.prev_btn.config(
            state='disabled' if self.current_page == 0 else 'normal'
        )

        # Adaptation du bouton suivant sur la dernière page
        if self.current_page == len(self.pages) - 1:
            self.next_btn.text = "✓ Terminer"  # Dernière page
        else:
            self.next_btn.text = "Suivant ▶"  # Pages intermédiaires
        self.next_btn.draw()  # Redessine le bouton avec le nouveau texte

    def next_page(self):
        """
        Passe à la page suivante ou ferme le tutoriel
        si la dernière page est atteinte.
        """
        # Si on n'est pas sur la dernière page, on avance
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1  # Incrément de l'index de page
            self.update_page()  # Rafraîchissement de l'affichage
        else:
            # Dernière page atteinte → fermeture du tutoriel
            self.destroy()

    def prev_page(self):
        """
        Revient à la page précédente du tutoriel.
        """
        # Vérifie qu'on ne dépasse pas la première page
        if self.current_page > 0:
            self.current_page -= 1  # Décrément de l'index de page
            self.update_page()  # Mise à jour de l'affichage


class ModernMainMenu(tk.Tk):
    """
    Fenêtre principale du menu du Jeu de la Vie (interface moderne).
    Point d'entrée de l'application avec navigation vers le jeu et le tutoriel.
    """

    def __init__(self):
        """
        Initialise la fenêtre principale et construit l'interface.
        Configure la fenêtre, charge le thème et centre l'affichage.
        """
        # Appel du constructeur de la classe parente Tk
        super().__init__()

        # Chargement de la configuration et du thème courant
        tm.load_config()

        # Titre de la fenêtre (barre de titre)
        self.title("🎮 Jeu de la Vie")

        # Dimensions fixes de la fenêtre
        self.geometry("620x880")
        self.resizable(False, False)  # Empêche le redimensionnement

        # Couleur de fond selon le thème actif
        self.config(bg=tm.current_theme["bg"])

        # Centrage de la fenêtre à l'écran
        self.update_idletasks()  # Force la mise à jour des dimensions
        # Calcul de la position centrale
        x = (self.winfo_screenwidth() // 2) - 310  # 620/2 = 310
        y = (self.winfo_screenheight() // 2) - 440  # 880/2 = 440
        # Application de la position
        self.geometry(f'620x880+{x}+{y}')

        # Gestion personnalisée de la fermeture de la fenêtre
        # Remplace le comportement par défaut du bouton X
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Construction de l'interface graphique
        self.create_ui()

    def on_close(self):
        """
        Demande confirmation avant de quitter l'application.
        Appelée lors du clic sur le bouton de fermeture.
        """
        # Affiche une boîte de dialogue de confirmation
        result = show_custom_message(
            self,
            "Quitter",
            "Voulez-vous vraiment quitter l'application ?",
            "question"
        )

        # Fermeture propre de l'application si confirmé
        if result:
            self.quit()  # Arrête la boucle principale
            self.destroy()  # Détruit la fenêtre

    def create_ui(self):
        """
        Construit entièrement l'interface du menu principal.
        Appelée au démarrage et lors des changements de thème.
        """

        # Suppression des widgets existants (utile lors du changement de thème)
        for widget in self.winfo_children():
            widget.destroy()

        # Conteneur principal avec marges
        container = tk.Frame(self, bg=tm.current_theme["bg"])
        container.pack(fill='both', expand=True, padx=40, pady=25)

        # Zone du titre (hauteur fixe)
        title_frame = tk.Frame(container, bg=tm.current_theme["panel"], height=100)
        title_frame.pack(fill='x', pady=(0, 15))
        title_frame.pack_propagate(False)  # Garde la hauteur fixe

        # Contenu centré du titre (utilise place pour centrage précis)
        title_content = tk.Frame(title_frame, bg=tm.current_theme["panel"])
        title_content.place(relx=0.5, rely=0.45, anchor='center')

        # Icône du jeu (emoji ADN)
        tk.Label(
            title_content, text="🧬", font=("Arial", 36),
            bg=tm.current_theme["panel"], fg=tm.current_theme["alive"]
        ).pack()

        # Titre principal en gros caractères
        tk.Label(
            title_content, text="JEU DE LA VIE", font=("Arial", 26, "bold"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        ).pack()

        # Description du jeu
        desc_frame = tk.Frame(container, bg=tm.current_theme["panel"])
        desc_frame.pack(fill='x', pady=10)

        # Première ligne de description
        tk.Label(
            desc_frame, text="Simulation du Game of Life de Conway",
            font=("Arial", 11),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        ).pack(pady=4)

        # Deuxième ligne de description (plus petite)
        tk.Label(
            desc_frame, text="Version moderne avec threads concurrents",
            font=("Arial", 9),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        ).pack(pady=4)

        # Zone des boutons principaux
        buttons_frame = tk.Frame(container, bg=tm.current_theme["bg"])
        buttons_frame.pack(pady=15)

        # Bouton lancer le jeu (grand et mis en valeur)
        ModernButton(
            buttons_frame, "▶ JOUER", self.launch_game,
            width=300, height=55, bg=tm.current_theme["bg"]
        ).pack(pady=8)

        # Bouton tutoriel (légèrement plus petit)
        ModernButton(
            buttons_frame, "📚 TUTORIEL", self.open_tutorial,
            width=300, height=45, bg=tm.current_theme["bg"]
        ).pack(pady=8)

        # Section informations / fonctionnalités
        info_frame = tk.Frame(container, bg=tm.current_theme["panel"])
        info_frame.pack(fill='x', pady=8)

        # Titre de la section
        tk.Label(
            info_frame, text="✨ Caractéristiques",
            font=("Arial", 12, "bold"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["alive"]
        ).pack(pady=8)

        # Liste des fonctionnalités principales
        features = [
            "🎨 4 thèmes + thèmes personnalisés",
            "⚡ Multi-threads haute performance",
            "🎮 Interface interactive",
            "↩️ Annulation/rétablissement",
            "💾 Sauvegarde automatique"
        ]

        # Affichage de chaque fonctionnalité
        for feat in features:
            tk.Label(
                info_frame, text=feat, font=("Arial", 9),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"],
                anchor='w'  # Aligné à gauche
            ).pack(pady=2, padx=20, fill='x')

        # Section de gestion des thèmes (appel à une méthode dédiée)
        self.create_theme_section(container)

    def create_theme_section(self, parent):
        """
        Crée la section de sélection et gestion des thèmes.
        Inclut les boutons de thèmes et les outils de gestion.
        
        Args:
            parent (tk.Frame): Frame parent où insérer la section
        """

        # Conteneur principal de la section thèmes
        theme_frame = tk.Frame(parent, bg=tm.current_theme["bg"])
        theme_frame.pack(pady=(6, 4))

        # Titre de la section thèmes
        tk.Label(
            theme_frame, text="🎨 Thèmes", font=("Arial", 11, "bold"),
            bg=tm.current_theme["bg"], fg=tm.current_theme["text"]
        ).pack(pady=5)

        # Zone centrale avec défilement horizontal pour les boutons
        themes_center = tk.Frame(theme_frame, bg=tm.current_theme["bg"])
        themes_center.pack(anchor="center")

        # Canvas pour permettre le scrolling horizontal
        canvas = tk.Canvas(
            themes_center,
            bg=tm.current_theme["bg"],
            height=55,  # Hauteur fixe pour une ligne de boutons
            width=420,  # Largeur visible
            highlightthickness=0  # Pas de bordure
        )
        canvas.pack()

        # Scrollbar horizontale liée au canvas
        scrollbar = tk.Scrollbar(
            theme_frame,
            orient="horizontal",  # Défilement horizontal
            command=canvas.xview  # Contrôle le canvas
        )
        scrollbar.pack(fill="x", pady=(2, 0))

        # Configuration bidirectionnelle canvas ↔ scrollbar
        canvas.configure(xscrollcommand=scrollbar.set)

        # Frame contenant les boutons de thèmes (sera dans le canvas)
        self.theme_buttons_frame = tk.Frame(canvas, bg=tm.current_theme["bg"])
        # Crée une fenêtre dans le canvas pour y placer le frame
        canvas.create_window((210, 0), window=self.theme_buttons_frame, anchor="n")

        # Ajustement automatique de la zone scrollable
        def on_frame_configure(event):
            """Callback pour mettre à jour la région scrollable"""
            canvas.configure(scrollregion=canvas.bbox("all"))

        # Bind l'événement de reconfiguration
        self.theme_buttons_frame.bind("<Configure>", on_frame_configure)

        # Création des boutons de thèmes disponibles
        self.refresh_theme_buttons()

        # Texte d'aide au-dessus des boutons de gestion
        tk.Label(
            theme_frame, text="Gérer vos thèmes",
            font=("Arial", 9, "italic"),
            bg=tm.current_theme["bg"], fg=tm.current_theme["text"]
        ).pack(pady=(8, 5))

        # Boutons de gestion des thèmes personnalisés
        management_frame = tk.Frame(theme_frame, bg=tm.current_theme["bg"])
        management_frame.pack(pady=8)

        # Bouton pour créer un nouveau thème
        ModernButton(
            management_frame, "➕ Créer", self.create_custom_theme,
            width=130, height=38, bg=tm.current_theme["bg"]
        ).pack(side='left', padx=5)

        # Bouton pour modifier un thème existant
        ModernButton(
            management_frame, "✏️ Modifier", self.edit_custom_theme,
            width=130, height=38, bg=tm.current_theme["bg"]
        ).pack(side='left', padx=5)

        # Bouton pour supprimer un thème personnalisé
        ModernButton(
            management_frame, "🗑️ Supprimer", self.delete_custom_theme_ui,
            width=130, height=38, bg=tm.current_theme["bg"]
        ).pack(side='left', padx=5)

        # Signature de l'auteur en bas
        tk.Label(
            theme_frame, text="Créé par : LAM Hoang Anh Harry",
            font=("Arial", 8),
            bg=tm.current_theme["bg"], fg=tm.current_theme["text"]
        ).pack(pady=(3, 0))

    def refresh_theme_buttons(self):
        """
        Rafraîchit la liste des boutons de thèmes disponibles.
        Supprime les anciens boutons et recrée tous les boutons de thèmes.
        """

        # Suppression des anciens boutons
        for widget in self.theme_buttons_frame.winfo_children():
            widget.destroy()

        # Récupère tous les thèmes disponibles (défaut + personnalisés)
        themes_list = list(tm.THEMES.items())

        # Création dynamique des boutons de thème
        for i, (theme_name, theme_data) in enumerate(themes_list):
            # Génération du nom affiché (6 premiers caractères en majuscules)
            display_name = (
                theme_name.upper()
                if len(theme_name) <= 6  # Si le nom est court, on garde tout
                else theme_name.upper()[:6]  # Sinon on tronque
            )

            # Création du bouton de thème
            # Utilise lambda avec argument par défaut pour capturer la valeur
            btn = tk.Button(
                self.theme_buttons_frame,
                text=display_name,
                command=lambda t=theme_name: self.change_theme(t),
                bg=theme_data["alive"],  # Fond = couleur des cellules vivantes
                fg=theme_data["bg"],  # Texte = couleur de fond du thème
                font=("Arial", 9, "bold"),
                relief='flat',  # Style plat sans relief
                width=10,  # Largeur en caractères
                height=2,  # Hauteur en lignes
                cursor="hand2"  # Curseur en forme de main
            )

            # Placement en grille (une seule ligne, colonnes variables)
            btn.grid(row=0, column=i, padx=5, pady=5)

    def refresh_themes(self):
        """
        Alias pour rafraîchir l'affichage des thèmes.
        Méthode alternative appelée depuis d'autres fenêtres.
        """
        self.refresh_theme_buttons()

    def create_custom_theme(self):
        """
        Ouvre la fenêtre de création de thème personnalisé.
        """
        ThemeCreatorWindow(self)

    def edit_custom_theme(self):
        """
        Permet de modifier un thème personnalisé existant.
        Demande le nom du thème et ouvre l'éditeur.
        """

        # Liste des thèmes personnalisés (exclut les thèmes par défaut)
        custom_themes = [
            name for name in tm.THEMES.keys()
            if name not in tm.DEFAULT_THEMES
        ]

        # Aucun thème personnalisé disponible
        if not custom_themes:
            show_custom_message(
                self, "Info",
                "Aucun thème personnalisé à modifier.", "info"
            )
            return

        # Demande du nom du thème à modifier
        theme_name = show_custom_input(
            self, "✏️ Modifier un thème",
            "Entrez le nom du thème à modifier :",
            f"Thèmes disponibles : {', '.join(custom_themes)}"
        )

        # Si un nom est saisi et existe dans les thèmes
        if theme_name and theme_name.lower() in tm.THEMES:
            # Ouvre l'éditeur en mode édition
            ThemeCreatorWindow(self, edit_theme=theme_name.lower())
        elif theme_name:
            # Nom saisi mais thème inexistant
            show_custom_message(self, "Erreur", "Thème non trouvé !", "error")

    def delete_custom_theme_ui(self):
        """
        Interface de suppression d'un thème personnalisé.
        Demande le nom et confirmation avant suppression.
        """

        # Liste des thèmes personnalisés disponibles
        custom_themes = [
            name for name in tm.THEMES.keys()
            if name not in tm.DEFAULT_THEMES
        ]

        # Aucun thème à supprimer
        if not custom_themes:
            show_custom_message(
                self, "Info",
                "Aucun thème personnalisé à supprimer.", "info"
            )
            return

        # Demande du thème à supprimer
        theme_name = show_custom_input(
            self, "🗑️ Supprimer un thème",
            "Entrez le nom du thème à supprimer :",
            f"Thèmes disponibles : {', '.join(custom_themes)}"
        )

        # Demande de confirmation si le thème existe
        if theme_name and theme_name.lower() in tm.THEMES:
            result = show_custom_message(
                self, "❓ Confirmation",
                f"Voulez-vous vraiment supprimer le thème '{theme_name}' ?",
                "question"
            )
            # Si confirmé, suppression du thème
            if result:
                if tm.delete_custom_theme(theme_name.lower()):
                    show_custom_message(
                        self, "Succès",
                        f"Thème '{theme_name}' supprimé !", "success"
                    )
                    # Rafraîchissement de la liste des boutons
                    self.refresh_theme_buttons()
        elif theme_name:
            # Nom saisi mais thème inexistant
            show_custom_message(self, "Erreur", "Thème non trouvé !", "error")

    def change_theme(self, theme_name):
        """
        Applique un nouveau thème et reconstruit l'interface.
        
        Args:
            theme_name (str): Nom du thème à appliquer
        """
        # Change le thème actif dans le gestionnaire
        tm.change_theme(theme_name)
        # Met à jour la couleur de fond de la fenêtre du menu
        self.config(bg=tm.current_theme["bg"])
        # Reconstruit l'interface avec les nouvelles couleurs
        self.create_ui()

    def open_tutorial(self):
        """
        Ouvre la fenêtre de tutoriel interactif.
        """
        ModernTutorialWindow(self)

    def launch_game(self):
        """
        Lance l'application principale du jeu.
        Cache le menu et affiche la fenêtre de jeu.
        """

        # Import local pour éviter les dépendances circulaires
        # (gui_game importe aussi des modules qui importent ce fichier)
        from gui_game import ModernApp

        # Cache le menu principal (ne le détruit pas)
        self.withdraw()
        # Crée et lance la fenêtre de jeu avec référence au menu
        app = ModernApp(return_to_menu=self)
        # Lance la boucle principale de la fenêtre de jeu
        app.mainloop()