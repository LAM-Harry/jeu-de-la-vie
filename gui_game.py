"""
GUI Game - Fenêtre principale du jeu
Interface de simulation du Jeu de la Vie
"""

import tkinter as tk
from tkinter import ttk
import gamelife_core as core
import theme_manager as tm
import history_manager as hm
from gui_components import show_custom_message, ModernButton
from gui_windows import ModernTutorialWindow, ThemeCreatorWindow

class ModernApp(tk.Tk):
    """
    Fenêtre principale de simulation du Jeu de la Vie.
    Gère l'interface graphique complète avec la grille, les contrôles et la configuration.
    """
    
    def __init__(self, return_to_menu=None):
        """
        Initialise la fenêtre principale du jeu.
        Configure la fenêtre, charge la configuration et démarre les workers.
        
        Args:
            return_to_menu: Référence à la fenêtre du menu principal pour y retourner
        """
        # Appel du constructeur de la classe parente Tk
        super().__init__()
        
        # Configuration de la fenêtre
        self.title("🎮 Jeu de la Vie - Simulation")
        self.return_to_menu = return_to_menu  # Stocke la référence au menu

        # ID du after pour la boucle UI
        self.ui_loop_id = None
        
        # Active le plein écran par défaut
        self.attributes("-fullscreen", True)

        # Force la mise à jour pour récupérer les dimensions réelles de l'écran
        self.update_idletasks()

        # Dimensions de l'écran physique
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        # Ratio largeur / hauteur de l'écran
        # Utilisé pour conserver des proportions correctes en mode fenêtré
        self.window_ratio = screen_w / screen_h

        def exit_fullscreen(event=None):
            """
            Quitte le mode plein écran et bascule en mode fenêtré
            en conservant le ratio de l'écran.
            
            Args:
                event (tk.Event, optional): Événement clavier (Échap)
            """
            # Désactive le plein écran
            self.attributes("-fullscreen", False)

            # Restaure la barre de titre et les contrôles système
            self.overrideredirect(False)

            # Définit une taille fenêtrée proportionnelle à l'écran (85%)
            w = int(screen_w * 0.85)
            h = int(w / self.window_ratio)

            # Applique la nouvelle géométrie
            self.geometry(f"{w}x{h}")

            # Empêche la fenêtre de devenir trop petite
            self.minsize(w, h)

        def toggle_fullscreen(event=None):
            """
            Bascule entre plein écran et mode fenêtré (touche F11).
            """
            # Vérifie l'état actuel
            is_fullscreen = self.attributes("-fullscreen")

            # Si l'on est en plein écran
            if is_fullscreen:
                # Quitte le plein écran
                exit_fullscreen()
            else:
                # Active le plein écran
                self.attributes("-fullscreen", True)
                # Cache la barre de titre et les contrôles système
                self.overrideredirect(False)

        # Touche Échap = sortie propre du plein écran
        self.bind("<Escape>", exit_fullscreen)

        # Flag interne pour éviter les boucles infinies de redimensionnement
        self._resizing = False

        # Échap = quitter le plein écran
        self.bind("<Escape>", exit_fullscreen)

        # F11 = bascule plein écran / fenêtré
        self.bind("<F11>", toggle_fullscreen)

        def on_resize(event):
            """
            Gère le redimensionnement de la fenêtre en mode fenêtré.
            Verrouille le ratio largeur / hauteur pour éviter
            l'étirement vertical de l'interface et de la grille.
            
            Args:
                event (tk.Event): Événement de redimensionnement
            """
            # Ne rien faire en plein écran
            if self.attributes("-fullscreen"):
                return

            # Empêche les appels récursifs (geometry -> Configure -> geometry)
            if self._resizing:
                return

            # Active le verrou de redimensionnement
            self._resizing = True

            # Largeur actuelle de la fenêtre
            w = event.width
            # Hauteur calculée à partir du ratio écran
            h = int(w / self.window_ratio)

            # Applique uniquement si nécessaire pour éviter les tremblements
            if event.height != h:
                self.geometry(f"{w}x{h}")

            # Libère le verrou de redimensionnement
            self._resizing = False

        # Applique le verrouillage du ratio uniquement en mode fenêtré
        self.bind("<Configure>", on_resize)

        # Charge la configuration et récupère l'état précédent (en cours ou en pause)
        was_running = tm.load_config()
        
        # Applique la couleur de fond du thème actuel
        self.config(bg=tm.current_theme["bg"])
        
        # Construction de l'interface utilisateur
        self.create_ui()
        
        # Démarre les threads workers pour les calculs parallèles
        core.start_workers(core.n)
        
        # Charger l'historique AVANT de randomiser
        hm.load_history_from_file()
        
        # Si l'historique est vide, générer une grille aléatoire de départ
        if not hm.generation_history:
            core.randomize_grid(core.T)
            hm.save_state_to_history()
        
        # Force le premier dessin de la grille
        core.redraw_event.set()
        
        # Restaurer l'état running si la simulation était en cours
        if was_running:
            core.running.set()  # Réactive la simulation
            self.start_btn.text = "⏸ Pause"
            self.start_btn.draw()
            self.status_label.config(text="▶️ En cours")
        else:
            core.running.clear()  # Garde la simulation en pause
            self.start_btn.text = "▶ Démarrer"
            self.start_btn.draw()
            self.status_label.config(text="⏸️ En pause")
        
        # Met à jour l'état des boutons de contrôle
        self.update_control_buttons()

        # Vérifier s'il y a une session précédente
        has_previous_session = bool(hm.generation_history) and core.gen_counter > 0
        
        # Gestion de la fermeture de la fenêtre
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Afficher message de reprise après 500ms si session précédente détectée
        # Le délai permet à l'interface de se charger complètement avant d'afficher le message
        if has_previous_session:
            self.after(500, lambda: self.show_resume_info_with_choice(was_running))
        
        # Démarre la boucle de mise à jour de l'interface (30ms)
        self.after(30, self.ui_loop)
    
    def create_ui(self):
        """
        Construit l'interface graphique complète.
        Crée les statistiques, les contrôles, la grille et la configuration.
        """
        # Supprime tous les widgets existants (pour reconstruction lors changement de thème)
        for widget in self.winfo_children():
            widget.destroy()

        # Conteneur principal avec marges
        main_container = tk.Frame(self, bg=tm.current_theme["bg"])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Barre de statistiques en haut (hauteur fixe)
        stats_frame = tk.Frame(main_container, bg=tm.current_theme["panel"], height=60)
        stats_frame.pack(fill='x', pady=(0, 10))
        stats_frame.pack_propagate(False)  # Conserve la hauteur fixe

        # Conteneur interne pour les statistiques
        stats_inner = tk.Frame(stats_frame, bg=tm.current_theme["panel"])
        stats_inner.pack(expand=True, fill='both')

        # Label du compteur de génération (à gauche)
        self.gen_label = tk.Label(
            stats_inner, text=f"🧬 Génération: {core.gen_counter}",
            font=("Arial", 14, "bold"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["alive"]
        )
        self.gen_label.pack(side='left', padx=20)

        # Label du statut de la simulation (à droite)
        self.status_label = tk.Label(
            stats_inner, text="▶️ En cours" if core.running.is_set() else "⏸️ En pause",
            font=("Arial", 12),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        )
        self.status_label.pack(side='right', padx=20)

        # Zone centrale contenant les contrôles et la grille
        center = tk.Frame(main_container, bg=tm.current_theme["bg"])
        center.pack(fill='both', expand=True)

        # Création du panneau de contrôle à gauche
        self.create_control_panel(center)
        # Création de la grille et du panneau de configuration
        self.create_game_panel(center)
        
        # Force un redimensionnement initial après construction
        self.after(100, self.force_initial_resize)
    
    def create_control_panel(self, parent):
        """
        Crée le panneau de contrôle avec tous les boutons d'action.
        
        Args:
            parent: Frame parent où insérer le panneau
        """
        # Panneau principal des contrôles (à gauche)
        panel = tk.Frame(parent, bg=tm.current_theme["panel"], relief='flat', bd=0)
        panel.pack(side='left', fill='y', padx=(0, 20))

        # Conteneur interne avec padding
        inner = tk.Frame(panel, bg=tm.current_theme["panel"])
        inner.pack(padx=15, pady=15)

        # Titre du panneau
        title = tk.Label(
            inner, text="⚡ CONTRÔLES",
            font=("Arial", 14, "bold"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        )
        title.pack(pady=(0, 15))

        # Bouton Démarrer/Pause (principal)
        self.start_btn = ModernButton(
            inner, "⏸ Pause" if core.running.is_set() else "▶ Démarrer", 
            self.toggle_start,
            width=160, height=40, bg=tm.current_theme["panel"]
        )
        self.start_btn.pack(pady=5)

        # Liste pour gérer l'état des boutons
        self.buttons = [self.start_btn]

        # Bouton avancer d'une génération (+1 Gen)
        self.step_btn = ModernButton(inner, "⏩ +1 Gen", self.one_step,
                        width=160, height=35, bg=tm.current_theme["panel"])
        self.step_btn.pack(pady=5)
        self.buttons.append(self.step_btn)

        # Bouton générer une grille aléatoire
        btn = ModernButton(inner, "🎲 Aléatoire", self.randomize,
                        width=160, height=35, bg=tm.current_theme["panel"])
        btn.pack(pady=5)
        self.buttons.append(btn)

        # Bouton effacer la grille
        btn = ModernButton(inner, "🗑️ Effacer", self.clear,
                        width=160, height=35, bg=tm.current_theme["panel"])
        btn.pack(pady=5)
        self.buttons.append(btn)

        # Frame pour les boutons d'historique (côte à côte)
        history_frame = tk.Frame(inner, bg=tm.current_theme["panel"])
        history_frame.pack(pady=10)

        # Bouton Undo (génération précédente)
        self.prev_btn = ModernButton(history_frame, "◀ Précédent", self.undo,
                        width=78, height=35, bg=tm.current_theme["panel"])
        self.prev_btn.pack(side='left', padx=2)
        self.buttons.append(self.prev_btn)

        # Bouton Redo (génération suivante)
        self.next_btn = ModernButton(history_frame, "Suivant ▶", self.redo,
                        width=78, height=35, bg=tm.current_theme["panel"])
        self.next_btn.pack(side='left', padx=2)
        self.buttons.append(self.next_btn)

        # Bouton ouvrir le tutoriel
        btn = ModernButton(inner, "📚 Tutoriel", self.open_tutorial,
                        width=160, height=35, bg=tm.current_theme["panel"])
        btn.pack(pady=5)
        self.buttons.append(btn)

        # Séparateur visuel
        sep = tk.Frame(inner, height=2, bg=tm.current_theme["accent"])
        sep.pack(fill='x', pady=10)

        # Bouton retour au menu principal
        btn = ModernButton(inner, "🏠 Menu principal", self.back_to_menu,
                        width=160, height=35, bg=tm.current_theme["panel"])
        btn.pack(pady=4)

        # Bouton quitter l'application
        btn = ModernButton(inner, "❌ Quitter", self.on_close,
                        width=160, height=35, bg=tm.current_theme["panel"])
        btn.pack(pady=4)
    
    def update_control_buttons(self):
        """
        Met à jour l'état des boutons selon l'état de la simulation.
        Désactive le bouton +1 Gen si la simulation est en cours.
        """
        # Si la simulation est en cours
        if core.running.is_set():
            # Désactive le bouton +1 Gen (pas de pas à pas en mode auto)
            self.step_btn.config(state='disabled')
            self.step_btn.bg_color = tm.current_theme["dead"]  # Couleur grisée
            self.step_btn.hover_color = tm.current_theme["dead"]
        else:
            # Active le bouton +1 Gen en mode pause
            self.step_btn.config(state='normal')
            self.step_btn.bg_color = tm.current_theme["button_bg"]
            self.step_btn.hover_color = tm.current_theme["button_hover"]
        # Redessine le bouton avec le nouvel état
        self.step_btn.draw()
    
    def refresh_theme_buttons(self):
        """
        Rafraîchit les boutons de sélection de thèmes.
        Supprime et recrée tous les boutons de thèmes disponibles.
        """
        # Supprime tous les boutons existants
        for widget in self.theme_frame.winfo_children():
            widget.destroy()

        # Crée un bouton pour chaque thème disponible
        for i, (theme_name, theme_data) in enumerate(tm.THEMES.items()):
            # Nom affiché (5 premiers caractères en majuscules)
            display_name = theme_name.upper()[:5]

            # Création du bouton de thème
            btn = tk.Button(
                self.theme_frame,
                text=display_name,
                command=lambda t=theme_name: self.change_theme(t),
                bg=theme_data["alive"],  # Fond = couleur vivante
                fg=theme_data["bg"],  # Texte = couleur de fond
                font=("Arial", 8, "bold"),
                relief="flat",
                width=7,
                height=2,
                cursor="hand2"
            )

            # Placement en grille (une ligne, plusieurs colonnes)
            btn.grid(row=0, column=i, padx=4, pady=4)

    def create_game_panel(self, parent):
        """
        Crée le panneau de jeu avec la grille et le panneau de configuration.
        
        Args:
            parent: Frame parent où insérer le panneau
        """
        # Conteneur central-droit pour la grille et la config
        center_right = tk.Frame(parent, bg=tm.current_theme["bg"])
        center_right.pack(side='left', fill='both', expand=True)

        # Frame du milieu contenant grille + config
        middle = tk.Frame(center_right, bg=tm.current_theme["bg"])
        middle.pack(fill='both', expand=True)

        # Cadre de la grille avec bordure colorée
        grid_frame = tk.Frame(middle, bg=tm.current_theme["accent"])
        grid_frame.pack(side='left', padx=(0, 15), fill='both', expand=True)

        # Canvas principal pour dessiner la grille
        self.canvas = tk.Canvas(
            grid_frame,
            bg=tm.current_theme["bg"],
            highlightthickness=0  # Pas de bordure par défaut
        )
        self.canvas.pack(fill='both', expand=True, padx=3, pady=3)

        # Liste 2D pour stocker les références des rectangles
        self.rects = []
        # Construction initiale du canvas
        self.build_canvas()

        # Variables pour gérer le dessin au drag (clic + glissement)
        self.is_dragging = False  # Indique si l'utilisateur est en train de dessiner
        self.drag_mode = None  # Mode 'draw' (dessiner) ou 'erase' (effacer)
        self.last_cell = None  # Dernière cellule touchée pour éviter les répétitions

        # Bindings des événements souris sur le canvas
        self.canvas.bind("<Configure>", self.on_canvas_resize)  # Redimensionnement
        self.canvas.bind("<Button-1>", self.on_canvas_press)  # Clic initial
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)  # Glissement avec bouton enfoncé
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)  # Relâchement

        # Panneau de configuration à droite
        config_panel = tk.Frame(middle, bg=tm.current_theme["panel"], relief='flat', bd=0)
        config_panel.pack(side='left', fill='y')

        # Conteneur interne avec padding
        config_inner = tk.Frame(config_panel, bg=tm.current_theme["panel"])
        config_inner.pack(padx=15, pady=15)

        # Titre du panneau de configuration
        title_cfg = tk.Label(
            config_inner, text="⚙️ CONFIGURATION",
            font=("Arial", 14, "bold"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        )
        title_cfg.pack(pady=(0, 15))

        # Section vitesse de simulation
        tk.Label(
            config_inner, text="⚡ Vitesse (gen/s)",
            font=("Arial", 9, "bold"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        ).pack(pady=(5, 2))

        # Curseur de vitesse (1 à 30 générations par seconde)
        self.speed_scale = tk.Scale(
            config_inner, from_=1, to=30, orient='horizontal',
            command=self.on_speed,  # Callback lors du changement
            bg=tm.current_theme["accent"],
            fg=tm.current_theme["text"],
            highlightthickness=0,
            troughcolor=tm.current_theme["bg"],
            length=140
        )
        self.speed_scale.set(core._speed)  # Valeur initiale
        self.speed_scale.pack(pady=2)

        # Section sélection de thèmes
        tk.Label(
            config_inner, text="🎨 Thèmes",
            font=("Arial", 9, "bold"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        ).pack(pady=(10, 4))

        # Zone scrollable pour les boutons de thèmes
        themes_center = tk.Frame(config_inner, bg=tm.current_theme["panel"])
        themes_center.pack(anchor="center", pady=5)

        # Canvas pour le scrolling
        theme_canvas = tk.Canvas(
            themes_center, bg=tm.current_theme["panel"],
            height=55, width=160, highlightthickness=0
        )
        theme_canvas.pack()

        # Scrollbar horizontale
        theme_scrollbar = tk.Scrollbar(
            themes_center, orient="horizontal", command=theme_canvas.xview
        )
        theme_scrollbar.pack(fill="x", pady=(2, 0))

        # Configuration bidirectionnelle
        theme_canvas.configure(xscrollcommand=theme_scrollbar.set)

        # Frame contenant les boutons de thèmes
        self.theme_frame = tk.Frame(theme_canvas, bg=tm.current_theme["panel"])
        theme_canvas.create_window((0, 0), window=self.theme_frame, anchor="nw")

        # Callback pour ajuster la région scrollable
        def on_theme_configure(event):
            """
            Met à jour la zone scrollable du canvas lors d'un changement de taille.

            Args:
                event (tk.Event): Événement déclenché par le redimensionnement du canvas.
            """
            theme_canvas.configure(scrollregion=theme_canvas.bbox("all"))

        self.theme_frame.bind("<Configure>", on_theme_configure)
        # Création des boutons de thèmes
        self.refresh_theme_buttons()

        # Texte d'aide
        tk.Label(
            config_inner, text="Gérer vos thèmes",
            font=("Arial", 8, "italic"),
            bg=tm.current_theme["panel"], fg=tm.current_theme["text"]
        ).pack(pady=(8, 5))

        # Boutons de gestion des thèmes personnalisés
        ModernButton(config_inner, "➕ Créer", self.create_custom_theme,
                    width=160, height=35, bg=tm.current_theme["panel"]).pack(pady=3)
        ModernButton(config_inner, "✏️ Modifier", self.edit_custom_theme,
                    width=160, height=35, bg=tm.current_theme["panel"]).pack(pady=3)
        ModernButton(config_inner, "🗑️ Supprimer", self.delete_custom_theme_ui,
                    width=160, height=35, bg=tm.current_theme["panel"]).pack(pady=3)

        # Séparateur
        sep_cfg = tk.Frame(config_inner, height=2, bg=tm.current_theme["accent"])
        sep_cfg.pack(fill='x', pady=10)

        # Bouton de réinitialisation des paramètres
        reset_btn = ModernButton(
            config_inner, "🔄 Réinitialiser", self.reset_params,
            width=160, height=35, bg=tm.current_theme["panel"]
        )
        reset_btn.pack(pady=(4, 0))
    
    def get_cell_from_coords(self, event):
        """
        Convertit les coordonnées pixel de la souris en coordonnées de cellule.
        
        Args:
            event: Événement tkinter contenant les coordonnées x, y
            
        Returns:
            tuple: (i, j) coordonnées de la cellule, ou (None, None) si hors grille
        """
        # Récupère les dimensions actuelles du canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Calcule la taille d'une cellule
        cell_width = canvas_width / core.n
        cell_height = canvas_height / core.n
        
        # Conversion des coordonnées pixel en indices de cellule (1-indexed)
        j = int(event.x / cell_width) + 1
        i = int(event.y / cell_height) + 1
        
        # Vérifie que les coordonnées sont dans la grille valide
        if 1 <= i <= core.n and 1 <= j <= core.n:
            return i, j
        # Retourne None si hors limites
        return None, None

    def on_canvas_press(self, event):
        """
        Gère le clic initial sur le canvas.
        Détermine le mode (dessiner/effacer) et gère les états spéciaux.
        
        Args:
            event: Événement de clic souris
        """
        # Récupère les coordonnées de la cellule cliquée
        i, j = self.get_cell_from_coords(event)
        
        # Si le clic est valide (dans la grille)
        if i is not None and j is not None:
            # Si la simulation est en cours
            if core.running.is_set():
                # Demande confirmation pour arrêter et réinitialiser
                result = show_custom_message(
                    self, 
                    "⚠️ Simulation en cours", 
                    "La simulation est en cours.\n\nVoulez-vous prendre cette grille actuelle comme base\net remettre le compteur à 0 ?\n(La simulation sera mise en pause, vous pourrez ensuite dessiner)",
                    "question"
                )
                
                # Si l'utilisateur annule
                if not result:
                    return
                
                # Arrête la simulation
                core.running.clear()
                self.start_btn.text = "▶ Démarrer"
                self.start_btn.draw()
                self.status_label.config(text="⏸️ En pause")
                self.update_control_buttons()
                
                # Réinitialise l'historique et le compteur
                hm.generation_history.clear()
                core.gen_counter = 0
                hm.save_state_to_history()
                self.gen_label.config(text=f"🧬 Génération: {core.gen_counter}")
                self.update_history_buttons()
                
                return
            
            # Si on peut faire redo ou si on n'est pas à la génération 0
            elif hm.can_redo() or core.gen_counter > 0:
                # Demande confirmation pour réinitialiser
                result = show_custom_message(
                    self,
                    "⚠️ Réinitialiser ?",
                    f"Vous êtes à la génération {core.gen_counter}.\n\nVoulez-vous prendre cette grille actuelle comme base\net remettre le compteur à 0 ?\n(Vous pourrez ensuite dessiner)",
                    "question"
                )
                
                # Si l'utilisateur annule
                if not result:
                    return
                
                # Réinitialise l'historique
                hm.generation_history.clear()
                core.gen_counter = 0
                hm.save_state_to_history()
                self.update_history_buttons()
                self.gen_label.config(text=f"🧬 Génération: {core.gen_counter}")
                
                return
            
            # Mode dessin normal : active le drag
            self.is_dragging = True
            self.last_cell = (i, j)
            # Détermine le mode selon l'état actuel de la cellule
            self.drag_mode = 'erase' if core.T[i][j] == 1 else 'draw'
            # Inverse l'état de la cellule cliquée
            core.T[i][j] = 0 if core.T[i][j] == 1 else 1
            # Force le rafraîchissement
            core.redraw_event.set()

    def on_canvas_drag(self, event):
        """
        Gère le glissement de la souris avec bouton enfoncé.
        Dessine ou efface les cellules selon le mode.
        
        Args:
            event: Événement de mouvement souris
        """
        # Si on n'est pas en mode drag, ignore
        if not self.is_dragging:
            return
        
        # Récupère la cellule sous le curseur
        i, j = self.get_cell_from_coords(event)
        
        # Si valide et différente de la dernière cellule touchée
        if i is not None and j is not None:
            if (i, j) != self.last_cell:
                self.last_cell = (i, j)
                
                # Applique le mode approprié
                if self.drag_mode == 'draw':
                    core.T[i][j] = 1  # Dessine (cellule vivante)
                else:
                    core.T[i][j] = 0  # Efface (cellule morte)
                
                # Force le rafraîchissement
                core.redraw_event.set()

    def on_canvas_release(self, event):
        """
        Gère le relâchement du bouton de la souris.
        Sauvegarde l'état dans l'historique.
        
        Args:
            event: Événement de relâchement souris
        """
        # Si on était en mode drag
        if self.is_dragging:
            # Désactive le mode drag
            self.is_dragging = False
            self.drag_mode = None
            self.last_cell = None
            # Sauvegarde l'état modifié dans l'historique
            hm.save_state_to_history()
            # Met à jour les boutons undo/redo
            self.update_history_buttons()
            # Force le rafraîchissement
            core.redraw_event.set()

    def on_canvas_resize(self, event):
        """
        Gère le redimensionnement du canvas.
        Recalcule la taille des cellules et reconstruit la grille.
        
        Args:
            event: Événement de redimensionnement
        """
        # Vérifie que le canvas existe et que la grille est initialisée
        if not hasattr(self, 'canvas') or core.n == 0:
            return
        
        # Récupère les nouvelles dimensions
        new_width = event.width
        new_height = event.height
        
        # Ignore les dimensions trop petites
        if new_width < 50 or new_height < 50:
            return
        
        # Calcule la nouvelle taille de cellule (carré)
        new_cell_size = min(new_width // core.n, new_height // core.n)
        
        # Si la taille a changé significativement
        if new_cell_size != core.cell_size and new_cell_size >= 3:
            core.cell_size = max(3, new_cell_size)  # Minimum 3 pixels
            # Reconstruit le canvas avec la nouvelle taille
            self.build_canvas()
            
    def build_canvas(self):
        """
        Construit ou reconstruit le canvas de la grille.
        Crée tous les rectangles représentant les cellules.
        """
        # Supprime tous les éléments existants du canvas
        self.canvas.delete('all')
        # Réinitialise la liste des rectangles
        self.rects = [[None]*(core.n+1) for _ in range(core.n+1)]
        
        # Force la mise à jour des dimensions
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        # Si les dimensions ne sont pas encore disponibles, réessaye plus tard
        if canvas_width <= 1 or canvas_height <= 1:
            self.after(50, self.build_canvas)
            return
        
        # Calcule la taille d'une cellule en pixels
        cell_width = canvas_width / core.n
        cell_height = canvas_height / core.n
        
        # Crée tous les rectangles de la grille
        for i in range(1, core.n+1):
            for j in range(1, core.n+1):
                # Calcule les coordonnées du rectangle
                x0 = (j-1) * cell_width
                y0 = (i-1) * cell_height
                x1 = j * cell_width
                y1 = i * cell_height
                
                # Détermine la couleur selon l'état de la cellule
                color = tm.current_theme["alive"] if core.T and core.T[i][j] else tm.current_theme["dead"]
                # Crée le rectangle
                r = self.canvas.create_rectangle(x0, y0, x1, y1,
                                                fill=color, 
                                                outline=tm.current_theme["bg"], 
                                                width=1)
                # Stocke la référence du rectangle
                self.rects[i][j] = r
        
        # Met à jour la taille de cellule globale
        core.cell_size = int((cell_width + cell_height) / 2)
    
    def force_initial_resize(self):
        """
        Force un redimensionnement initial du canvas.
        Nécessaire car les dimensions ne sont pas immédiatement disponibles.
        """
        if hasattr(self, 'canvas'):
            # Force la mise à jour
            self.canvas.update_idletasks()
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            
            # Si les dimensions sont valides
            if width > 10 and height > 10:
                # Calcule et applique la taille de cellule
                cell_size_float = min(width / core.n, height / core.n)
                core.cell_size = max(3, int(cell_size_float))
                # Reconstruit le canvas
                self.build_canvas()
                # Force le dessin
                core.redraw_event.set()
            else:
                # Réessaye dans 100ms
                self.after(100, self.force_initial_resize)
    
    def toggle_start(self):
        """
        Bascule entre démarrer et mettre en pause la simulation.
        Vérifie qu'il y a des cellules vivantes avant de démarrer.
        """
        # Si la simulation est en cours
        if core.running.is_set():
            # Met en pause
            core.running.clear()
            self.start_btn.text = "▶ Démarrer"
            self.start_btn.draw()
            self.status_label.config(text="⏸️ En pause")
        else:
            # Vérifie qu'il y a au moins une cellule vivante
            if not core.has_living_cells():
                show_custom_message(
                    self,
                    "⚠️ Grille vide",
                    "La grille est vide !\n\nVeuillez dessiner des cellules ou générer une grille aléatoire avant de démarrer.",
                    "warning"
                )
                return
            
            # Sauvegarde l'état avant de démarrer
            hm.save_state_to_history()
            # Démarre la simulation
            core.running.set()
            self.start_btn.text = "⏸ Pause"
            self.start_btn.draw()
            self.status_label.config(text="▶️ En cours")
        # Met à jour les boutons historique et contrôles
        self.update_history_buttons()
        self.update_control_buttons()

    def one_step(self):
        """
        Avance d'une seule génération (mode pas à pas).
        Désactivé si la simulation est en cours.
        """
        # Si la simulation est en cours ou un pas est déjà en attente
        if core.running.is_set() or core.step_event.is_set():
            return
        
        # Vérifie qu'il y a des cellules vivantes
        if not core.has_living_cells():
            show_custom_message(
                self,
                "⚠️ Grille vide",
                "La grille est vide !\n\nVeuillez dessiner des cellules ou générer une grille aléatoire.",
                "warning"
            )
            return
        
        # Sauvegarde l'état actuel
        hm.save_state_to_history()
        # Active le mode "un seul pas"
        core.step_event.set()
        core.running.set()
        self.status_label.config(text="⏩ +1 Génération")
        # Attend 150ms puis réinitialise l'état
        self.after(150, self.after_one_step)

    def after_one_step(self):
        """
        Callback appelé après l'exécution d'un pas unique.
        Remet le statut à "en pause" et met à jour les boutons.
        """
        self.status_label.config(text="⏸️ En pause")
        self.update_history_buttons()
        self.update_control_buttons()
    
    def clear(self):
        """
        Efface toute la grille et réinitialise le compteur.
        Demande confirmation si pas à la génération 0.
        """
        # Arrête la simulation si en cours
        if core.running.is_set():
            core.running.clear()
            self.start_btn.text = "▶ Démarrer"
            self.start_btn.draw()
            self.status_label.config(text="⏸️ En pause")
            self.update_control_buttons()
        
        # Si on n'est pas à la génération 0, demande confirmation
        if core.gen_counter > 0:
            result = show_custom_message(
                self, 
                "⚠️ Réinitialiser ?", 
                f"Vous êtes à la génération {core.gen_counter}.\n\nVoulez-vous effacer la grille et remettre le compteur à 0 ?",
                "question"
            )
            
            # Si l'utilisateur annule
            if not result:
                return
        
        # Efface toutes les cellules
        core.clear_grid(core.T)
        # Réinitialise le compteur
        core.gen_counter = 0
        # Vide l'historique
        hm.generation_history.clear()
        # Sauvegarde l'état vide
        hm.save_state_to_history()
        # Force le rafraîchissement
        core.redraw_event.set()
        # Met à jour les boutons
        self.update_history_buttons()

    def randomize(self):
        """
        Génère une grille aléatoire (~25% de cellules vivantes).
        Demande confirmation si pas à la génération 0.
        """
        # Arrête la simulation si en cours
        if core.running.is_set():
            core.running.clear()
            self.start_btn.text = "▶ Démarrer"
            self.start_btn.draw()
            self.status_label.config(text="⏸️ En pause")
            self.update_control_buttons()
        
        # Si on n'est pas à la génération 0, demande confirmation
        if core.gen_counter > 0:
            result = show_custom_message(
                self, 
                "⚠️ Réinitialiser ?", 
                f"Vous êtes à la génération {core.gen_counter}.\n\nVoulez-vous générer une nouvelle grille aléatoire et remettre le compteur à 0 ?",
                "question"
            )
            
            # Si l'utilisateur annule
            if not result:
                return
        
        # Génère une grille aléatoire
        core.randomize_grid(core.T)
        # Réinitialise le compteur
        core.gen_counter = 0
        # Vide l'historique
        hm.generation_history.clear()
        # Sauvegarde le nouvel état
        hm.save_state_to_history()
        # Force le rafraîchissement
        core.redraw_event.set()
        # Met à jour les boutons
        self.update_history_buttons()

    def undo(self):
        """
        Revient à la génération précédente dans l'historique.
        Arrête la simulation si en cours.
        """
        # Arrête la simulation si en cours
        if core.running.is_set():
            core.running.clear()
            self.start_btn.text = "▶ Démarrer"
            self.start_btn.draw()
            self.status_label.config(text="⏸️ En pause")
            self.update_control_buttons()
        
        # Tente de charger l'état précédent
        if hm.load_state_from_history("undo"):
            # Met à jour le statut avec le nouveau numéro de génération
            self.status_label.config(text=f"◀ Génération {core.gen_counter}")
            self.update_history_buttons()
        else:
            # Aucune génération précédente disponible
            show_custom_message(self, "Info", 
                            "Aucune génération précédente disponible", "info")

    def redo(self):
        """
        Avance à la génération suivante dans l'historique.
        Arrête la simulation si en cours.
        """
        # Arrête la simulation si en cours
        if core.running.is_set():
            core.running.clear()
            self.start_btn.text = "▶ Démarrer"
            self.start_btn.draw()
            self.status_label.config(text="⏸️ En pause")
            self.update_control_buttons()
        
        # Tente de charger l'état suivant
        if hm.load_state_from_history("redo"):
            # Met à jour le statut avec le nouveau numéro de génération
            self.status_label.config(text=f"▶ Génération {core.gen_counter}")
            self.update_history_buttons()
        else:
            # Aucune génération suivante disponible
            show_custom_message(self, "Info", 
                            "Aucune génération suivante disponible", "info")

    def update_history_buttons(self):
        """
        Met à jour l'état des boutons d'historique (undo/redo).
        Active ou désactive selon la disponibilité dans l'historique.
        """
        # Parcourt tous les boutons
        for btn in self.buttons:
            if hasattr(btn, 'text'):
                # Bouton Précédent (undo)
                if "Précédent" in btn.text or "◀" in btn.text:
                    if hm.can_undo():
                        # Active le bouton
                        btn.config(state='normal')
                        btn.bg_color = tm.current_theme["button_bg"]
                        btn.hover_color = tm.current_theme["button_hover"]
                    else:
                        # Désactive le bouton
                        btn.config(state='disabled')
                        btn.bg_color = tm.current_theme["dead"]
                        btn.hover_color = tm.current_theme["dead"]
                    btn.draw()
                
                # Bouton Suivant (redo) - exclut "Démarrer"
                elif "Suivant" in btn.text or "▶" in btn.text and "Démarrer" not in btn.text:
                    if hm.can_redo():
                        # Active le bouton
                        btn.config(state='normal')
                        btn.bg_color = tm.current_theme["button_bg"]
                        btn.hover_color = tm.current_theme["button_hover"]
                    else:
                        # Désactive le bouton
                        btn.config(state='disabled')
                        btn.bg_color = tm.current_theme["dead"]
                        btn.hover_color = tm.current_theme["dead"]
                    btn.draw()
    def show_resume_info_with_choice(self, was_running):
        """
        Affiche un message de reprise avec choix de continuer ou recommencer.
        Demande à l'utilisateur s'il veut reprendre la session sauvegardée ou repartir à zéro.
        
        Args:
            was_running (bool): True si la simulation était en cours avant la fermeture
        """
        # Prépare le message selon l'état précédent de la simulation
        if was_running:
            # Message si la simulation était en cours
            message = (
                f"Une session en cours a été détectée !\n\n"
                f"📊 Génération actuelle : {core.gen_counter}\n"
                f"▶️ État : La simulation était en cours\n"
                f"⚡ Vitesse : {core.get_speed():.0f} gen/s\n\n"
                f"Voulez-vous reprendre cette session ?\n\n"
                f"• OUI : Continue la simulation\n"
                f"• NON : Repart à zéro avec une nouvelle grille"
            )
        else:
            # Message si la simulation était en pause
            message = (
                f"Une session sauvegardée a été trouvée !\n\n"
                f"📊 Génération actuelle : {core.gen_counter}\n"
                f"⏸️ État : La simulation était en pause\n\n"
                f"Voulez-vous reprendre cette session ?\n\n"
                f"• OUI : Continue où vous vous êtes arrêté\n"
                f"• NON : Repart à zéro avec une nouvelle grille"
            )
        
        # Affiche la boîte de dialogue et récupère le choix
        result = show_custom_message(
            self,
            "💾 Session précédente détectée",
            message,
            "question"
        )
        
        # Si l'utilisateur clique sur NON (refuse de reprendre)
        if not result:
            # Arrête la simulation si elle était en cours
            core.running.clear()
            
            # Réinitialise complètement la grille et l'historique
            core.clear_grid(core.T)  # Vide la grille
            core.gen_counter = 0  # Remet le compteur à 0
            hm.generation_history.clear()  # Vide l'historique
            
            # Génère une nouvelle grille aléatoire de départ
            core.randomize_grid(core.T)
            hm.save_state_to_history()  # Sauvegarde le nouvel état initial
            
            # Met à jour tous les éléments de l'interface
            self.start_btn.text = "▶ Démarrer"  # Change le texte du bouton
            self.start_btn.draw()  # Redessine le bouton
            self.status_label.config(text="⏸️ En pause")  # Met à jour le statut
            self.gen_label.config(text=f"🧬 Génération: {core.gen_counter}")  # Met à jour le compteur
            self.update_control_buttons()  # Réactive les boutons de contrôle
            self.update_history_buttons()  # Met à jour les boutons undo/redo
            
            # Force le rafraîchissement visuel de la grille
            core.redraw_event.set()
    
    def on_speed(self, val):
        """
        Callback appelé lors du changement de vitesse.
        Met à jour la vitesse de simulation et sauvegarde.
        
        Args:
            val: Nouvelle valeur de vitesse (générations/seconde)
        """
        # Met à jour la vitesse globale
        core.set_speed(float(val))
        # Sauvegarde la configuration
        tm.save_config()
    
    def reset_params(self):
        """
        Réinitialise les paramètres (vitesse et thème) aux valeurs par défaut.
        Demande confirmation avant de procéder.
        """
        # Demande confirmation
        result = show_custom_message(self, "Confirmation", 
                                    "Voulez-vous réinitialiser la vitesse et le thème aux valeurs par défaut ?",
                                    "question")
        
        if result:
            # Mémorise si la simulation était en cours
            was_running = core.running.is_set()
            
            # Réinitialise au thème dark
            tm.current_theme_name = "dark"
            tm.current_theme = tm.THEMES["dark"]
            # Réinitialise la vitesse à 5 gen/s
            core._speed = 5.0
            
            # Reconstruit l'interface avec les nouvelles valeurs
            self.create_ui()
            
            # Restaure l'état de la simulation
            if was_running:
                core.running.set()
                self.start_btn.text = "⏸ Pause"
                self.status_label.config(text="▶️ En cours")
            else:
                core.running.clear()
                self.start_btn.text = "▶ Démarrer"
                self.status_label.config(text="⏸️ En pause")
            
            # Met à jour l'interface
            self.start_btn.draw()
            self.speed_scale.set(core._speed)
            self.update_control_buttons()
            
            # Sauvegarde la configuration
            tm.save_config()
            # Force le rafraîchissement
            core.redraw_event.set()
            
            # Met à jour le menu principal si existant
            if self.return_to_menu and hasattr(self.return_to_menu, 'create_ui'):
                try:
                    self.return_to_menu.create_ui()
                except:
                    pass
    
    def change_theme(self, theme_name):
        """
        Applique un nouveau thème et reconstruit l'interface.
        Préserve l'état de la simulation (en cours / pause).

        Args:
            theme_name (str): Nom du thème à appliquer.

        Returns:
            None: La fonction met à jour l'interface et l'état des composants,
            mais ne renvoie aucune valeur.
        """
        # Sauvegarde l'état actuel de la simulation
        was_running = core.running.is_set()
        
        # Change le thème dans le gestionnaire de thèmes
        tm.change_theme(theme_name)
        
        # Met à jour la couleur de fond de la fenêtre principale
        self.config(bg=tm.current_theme["bg"])
        
        # Reconstruit toute l'interface avec les nouvelles couleurs
        self.create_ui()
        
        # Restaure l'état du bouton Démarrer/Pause
        if was_running:
            # La simulation était en cours
            self.start_btn.text = "⏸ Pause"
            self.status_label.config(text="▶️ En cours")
        else:
            # La simulation était en pause
            self.start_btn.text = "▶ Démarrer"
            self.status_label.config(text="⏸️ En pause")
        
        # Redessine le bouton avec le bon texte
        self.start_btn.draw()
        
        # Met à jour l'état des boutons de contrôle
        self.update_control_buttons()
        
        # Force le rafraîchissement visuel immédiat
        self.update_idletasks()
        
        # Demande le redessin du canvas de la grille
        core.redraw_event.set()
        
        # Synchronise le menu principal si il existe
        if self.return_to_menu and hasattr(self.return_to_menu, 'create_ui'):
            try:
                self.return_to_menu.create_ui()
            except:
                # Ignore les erreurs si le menu n'est pas accessible
                pass
        
    def create_custom_theme(self):
        """
        Ouvre la fenêtre de création de thème personnalisé.
        """
        ThemeCreatorWindow(self)
    
    def edit_custom_theme(self):
        """
        Ouvre la fenêtre d'édition d'un thème personnalisé existant.
        Demande le nom du thème à modifier.
        """
        # Liste des thèmes personnalisés (exclut les thèmes par défaut)
        custom_themes = [name for name in tm.THEMES.keys() if name not in tm.DEFAULT_THEMES]
        
        # Si aucun thème personnalisé
        if not custom_themes:
            show_custom_message(self, "Info", 
                              "Aucun thème personnalisé à modifier.", "info")
            return
        
        # Import local pour éviter les imports circulaires
        from gui_components import show_custom_input
        # Demande le nom du thème
        theme_name = show_custom_input(self, "✏️ Modifier un thème",
                                      "Entrez le nom du thème à modifier :",
                                      f"Thèmes disponibles : {', '.join(custom_themes)}")
        
        # Si le nom est valide et existe
        if theme_name and theme_name.lower() in tm.THEMES:
            # Ouvre l'éditeur en mode modification
            ThemeCreatorWindow(self, edit_theme=theme_name.lower())
        elif theme_name:
            # Nom saisi mais thème inexistant
            show_custom_message(self, "Erreur", "Thème non trouvé !", "error")
    
    def delete_custom_theme_ui(self):
        """
        Interface de suppression d'un thème personnalisé.
        Demande le nom et confirmation avant suppression.
        """
        # Liste des thèmes personnalisés
        custom_themes = [name for name in tm.THEMES.keys() if name not in tm.DEFAULT_THEMES]
        
        # Si aucun thème personnalisé
        if not custom_themes:
            show_custom_message(self, "Info", 
                              "Aucun thème personnalisé à supprimer.", "info")
            return
        
        # Import local
        from gui_components import show_custom_input
        # Demande le nom du thème à supprimer
        theme_name = show_custom_input(self, "🗑️ Supprimer un thème",
                                      "Entrez le nom du thème à supprimer :",
                                      f"Thèmes disponibles : {', '.join(custom_themes)}")
        
        # Si le thème existe
        if theme_name and theme_name.lower() in tm.THEMES:
            # Demande confirmation
            result = show_custom_message(self, "❓ Confirmation",
                                        f"Voulez-vous vraiment supprimer le thème '{theme_name}' ?",
                                        "question")
            if result:
                # Supprime le thème
                if tm.delete_custom_theme(theme_name.lower()):
                    show_custom_message(self, "Succès", 
                                      f"Thème '{theme_name}' supprimé !", "success")
                    # Rafraîchit les boutons
                    self.refresh_theme_buttons()
                    
                    # Met à jour le menu principal si existant
                    if self.return_to_menu and hasattr(self.return_to_menu, 'refresh_themes'):
                        try:
                            self.return_to_menu.refresh_themes()
                        except:
                            pass
        elif theme_name:
            # Thème inexistant
            show_custom_message(self, "Erreur", "Thème non trouvé !", "error")
    
    def open_tutorial(self):
        """
        Ouvre la fenêtre de tutoriel interactif.
        """
        ModernTutorialWindow(self)
    
    def back_to_menu(self):
        """
        Retourne au menu principal.
        Arrête la simulation et sauvegarde l'état.
        """
        # Si la simulation est en cours, demande confirmation
        if core.running.is_set():
            result = show_custom_message(
                self, 
                "⚠️ Simulation en cours", 
                "La simulation est en cours.\n\nVoulez-vous vraiment retourner au menu principal ?\n(La simulation sera arrêtée)",
                "question"
            )
            
            if not result:
                return
        else:
            # Demande confirmation simple si en pause
            result = show_custom_message(self, "Retour au menu", 
                                        "Voulez-vous vraiment retourner au menu principal ?",
                                        "question")
            
            if not result:
                return
        
        # Arrête la simulation
        core.running.clear()
        # Arrête les threads workers
        core.stop_workers()
        # Sauvegarde la configuration
        tm.save_config()
        # Sauvegarde l'historique
        hm.save_history_to_file()   

        # Annule la boucle UI si active
        if hasattr(self, "ui_loop_id") and self.ui_loop_id:
            try:
                self.after_cancel(self.ui_loop_id)
            except:
                pass

        # Ferme la fenêtre de jeu
        self.destroy()
        
        # Réaffiche le menu principal si existant
        if self.return_to_menu:
            # Met à jour le thème du menu
            self.return_to_menu.config(bg=tm.current_theme["bg"])
            # Reconstruit l'interface du menu
            self.return_to_menu.create_ui()
            # # Réaffiche la fenêtre du menu qui avait été cachée 
            self.return_to_menu.deiconify()
        
    def ui_loop(self):
        """
        Boucle principale de mise à jour de l'interface.
        Appelée toutes les 30ms pour rafraîchir l'affichage.
        """
        # Si la fenêtre n'existe plus, on arrête définitivement
        if not self.winfo_exists():
            return

        # Si un rafraîchissement est demandé
        if core.redraw_event.is_set():
            # Redessine la grille
            self.redraw()
            # Réinitialise le flag
            core.redraw_event.clear()
            
        # Met à jour le compteur de génération
        self.gen_label.config(text=f"🧬 Génération: {core.gen_counter}")
        # Met à jour les boutons historique
        self.update_history_buttons()
        # Planifie le prochain appel de la boucle UI
        self.ui_loop_id = self.after(30, self.ui_loop)
    
    def redraw(self):
        """
        Redessine toutes les cellules de la grille.
        Met à jour les couleurs selon l'état actuel.
        """
        # Parcourt toutes les cellules
        for i in range(1, core.n+1):
            for j in range(1, core.n+1):
                # Détermine la couleur selon l'état (vivante ou morte)
                color = tm.current_theme["alive"] if core.T[i][j] else tm.current_theme["dead"]
                try:
                    # Met à jour la couleur du rectangle
                    self.canvas.itemconfig(self.rects[i][j], fill=color)
                except:
                    # Ignore les erreurs (rectangle inexistant)
                    pass
    
    def on_close(self):
        """
        Gère la fermeture de l'application.
        Demande confirmation, arrête la simulation et sauvegarde.
        """
        # Si la simulation est en cours, demande confirmation spéciale
        if core.running.is_set():
            result = show_custom_message(
                self, 
                "⚠️ Simulation en cours", 
                "La simulation est en cours.\n\nVoulez-vous vraiment quitter l'application ?\n(La simulation sera arrêtée)",
                "question"
            )
            
            if not result:
                return
        else:
            # Demande confirmation simple
            result = show_custom_message(self, "Quitter", 
                                        "Voulez-vous vraiment quitter l'application ?",
                                        "question")
            
            if not result:
                return
        
        # Arrête la simulation
        core.running.clear()
        # Arrête tous les threads workers
        core.stop_workers()
        # Sauvegarde la configuration
        tm.save_config()
        # Sauvegarde l'historique
        hm.save_history_to_file()
        
        # Ferme la fenêtre de jeu
        self.destroy()
        
        # Ferme aussi le menu principal si existant
        if self.return_to_menu:
            self.return_to_menu.destroy()