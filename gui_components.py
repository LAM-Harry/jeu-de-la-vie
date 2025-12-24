"""
GUI Components - Composants d'interface réutilisables
Boutons modernes, dialogues personnalisés, sélecteur de couleur, etc.
"""

import tkinter as tk
from tkinter import ttk
import theme_manager as tm

class CustomDialog(tk.Toplevel):
    """
    Boîte de dialogue personnalisée avec le thème actuel.
    Affiche un message avec une icône et des boutons de confirmation.
    """
    
    def __init__(self, parent, title, message, dialog_type="info"):
        """
        Initialise la boîte de dialogue.
        
        Args:
            parent: Fenêtre parente
            title (str): Titre de la boîte de dialogue
            message (str): Message à afficher
            dialog_type (str): Type de dialogue ("info", "warning", "error", "question", "success")
        """
        # Appel du constructeur de la classe parente Toplevel
        super().__init__(parent)
        # Définit le titre de la fenêtre
        self.title(title)
        # Empêche le redimensionnement de la fenêtre
        self.resizable(False, False)
        # Applique la couleur de fond du thème
        self.config(bg=tm.current_theme["bg"])
        # Initialise le résultat à None
        self.result = None
        
        # Rend la fenêtre modale (liée au parent)
        self.transient(parent)
        # Capture tous les événements (bloque l'interaction avec le parent)
        self.grab_set()
        
        # Conteneur principal avec le panneau thématisé
        container = tk.Frame(self, bg=tm.current_theme["panel"])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Dictionnaire des icônes selon le type de dialogue
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "question": "❓",
            "success": "✅"
        }
        # Récupère l'icône appropriée (info par défaut)
        icon = icons.get(dialog_type, "ℹ️")
        
        # Affiche l'icône en grand
        tk.Label(container, text=icon, font=("Arial", 32), 
                bg=tm.current_theme["panel"], fg=tm.current_theme["alive"]).pack(pady=10)
        
        # Affiche le titre en gras
        tk.Label(container, text=title, font=("Arial", 14, "bold"),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=5)
        
        # Affiche le message avec retour à la ligne automatique
        tk.Label(container, text=message, font=("Arial", 11), wraplength=300,
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=15)
        
        # Conteneur pour les boutons
        btn_frame = tk.Frame(container, bg=tm.current_theme["panel"])
        btn_frame.pack(pady=10)
        
        # Si c'est une question, affiche Oui/Non
        if dialog_type == "question":
            # Bouton Oui (retourne True)
            ModernButton(btn_frame, "✓ Oui", lambda: self.set_result(True), 
                        width=100, height=35, bg=tm.current_theme["panel"]).pack(side='left', padx=5)
            # Bouton Non (retourne False)
            ModernButton(btn_frame, "✗ Non", lambda: self.set_result(False), 
                        width=100, height=35, bg=tm.current_theme["panel"]).pack(side='left', padx=5)
        else:
            # Sinon, affiche seulement OK (retourne True)
            ModernButton(btn_frame, "OK", lambda: self.set_result(True), 
                        width=120, height=35, bg=tm.current_theme["panel"]).pack()
        
        # Centre la fenêtre sur l'écran
        self.update_idletasks()
        # Calcule la largeur et hauteur de la fenêtre
        width = self.winfo_width()
        height = self.winfo_height()
        # Calcule les coordonnées pour centrer
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        # Applique la position
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def set_result(self, value):
        """
        Définit le résultat et ferme la boîte de dialogue.
        
        Args:
            value (bool): Résultat de la sélection (True pour Oui/OK, False pour Non)
        """
        # Stocke le résultat
        self.result = value
        # Ferme la fenêtre
        self.destroy()

def show_custom_message(parent, title, message, dialog_type="info"):
    """
    Affiche un message personnalisé et retourne le résultat.
    
    Args:
        parent: Fenêtre parente
        title (str): Titre du message
        message (str): Contenu du message
        dialog_type (str): Type de dialogue
        
    Returns:
        bool/None: True pour Oui/OK, False pour Non, None si fermé
    """
    # Crée la boîte de dialogue
    dialog = CustomDialog(parent, title, message, dialog_type)
    # Attend que la fenêtre soit fermée avant de continuer
    parent.wait_window(dialog)
    # Retourne le résultat
    return dialog.result

class CustomInputDialog(tk.Toplevel):
    """
    Dialogue pour saisir du texte avec validation.
    Affiche un champ de saisie et des boutons OK/Annuler.
    """
    
    def __init__(self, parent, title, message, available_items=""):
        """
        Initialise le dialogue de saisie.
        
        Args:
            parent: Fenêtre parente
            title (str): Titre du dialogue
            message (str): Message d'instruction
            available_items (str): Liste des éléments disponibles (optionnel)
        """
        # Appel du constructeur de la classe parente
        super().__init__(parent)
        # Définit le titre
        self.title(title)
        # Empêche le redimensionnement
        self.resizable(False, False)
        # Applique le thème
        self.config(bg=tm.current_theme["bg"])
        # Initialise le résultat
        self.result = None
        
        # Rend la fenêtre modale
        self.transient(parent)
        self.grab_set()
        
        # Conteneur principal
        container = tk.Frame(self, bg=tm.current_theme["panel"])
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Affiche le titre
        tk.Label(container, text=title, font=("Arial", 14, "bold"),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=10)
        
        # Affiche la liste des éléments disponibles si fournie
        if available_items:
            tk.Label(container, text=available_items, font=("Arial", 10),
                    bg=tm.current_theme["panel"], fg=tm.current_theme["text"],
                    wraplength=350).pack(pady=5)
        
        # Affiche le message d'instruction
        tk.Label(container, text=message, font=("Arial", 11),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=10)
        
        # Champ de saisie de texte
        self.entry = tk.Entry(container, font=("Arial", 12), width=25,
                             bg=tm.current_theme["accent"], fg=tm.current_theme["text"])
        self.entry.pack(pady=10)
        # Place le curseur dans le champ
        self.entry.focus()
        # Permet de valider avec la touche Entrée
        self.entry.bind('<Return>', lambda e: self.confirm())
        
        # Conteneur pour les boutons
        btn_frame = tk.Frame(container, bg=tm.current_theme["panel"])
        btn_frame.pack(pady=15)
        
        # Bouton OK (valide la saisie)
        ModernButton(btn_frame, "✓ OK", self.confirm, 
                    width=100, height=35, bg=tm.current_theme["panel"]).pack(side='left', padx=5)
        # Bouton Annuler (ferme sans valider)
        ModernButton(btn_frame, "✗ Annuler", self.cancel, 
                    width=100, height=35, bg=tm.current_theme["panel"]).pack(side='left', padx=5)
        
        # Centre la fenêtre sur l'écran
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def confirm(self):
        """
        Valide la saisie et ferme le dialogue.
        Récupère le texte saisi et supprime les espaces superflus.
        """
        # Récupère et nettoie le texte saisi
        self.result = self.entry.get().strip()
        # Ferme la fenêtre
        self.destroy()
    
    def cancel(self):
        """
        Annule la saisie et ferme le dialogue.
        Le résultat reste None.
        """
        # Laisse le résultat à None
        self.result = None
        # Ferme la fenêtre
        self.destroy()

def show_custom_input(parent, title, message, available_items=""):
    """
    Affiche un dialogue de saisie de texte et retourne le résultat.
    
    Args:
        parent: Fenêtre parente
        title (str): Titre du dialogue
        message (str): Message d'instruction
        available_items (str): Liste des éléments disponibles
        
    Returns:
        str/None: Texte saisi ou None si annulé
    """
    # Crée le dialogue de saisie
    dialog = CustomInputDialog(parent, title, message, available_items)
    # Attend la fermeture du dialogue
    parent.wait_window(dialog)
    # Retourne le texte saisi
    return dialog.result

class CustomColorPicker(tk.Toplevel):
    """
    Sélecteur de couleur avancé avec gradient 2D et gestion des favoris.
    Permet de choisir une couleur via un gradient, une barre de teinte,
    ou en saisissant le code hexadécimal.
    """
    
    def __init__(self, parent, title, initial_color):
        """
        Initialise le sélecteur de couleur.
        
        Args:
            parent: Fenêtre parente
            title (str): Titre de la fenêtre
            initial_color (str): Couleur initiale au format #RRGGBB
        """
        # Appel du constructeur de la classe parente
        super().__init__(parent)
        self.title(title)
        
        # Configuration de la fenêtre
        self.geometry("700x620")
        self.resizable(False, False)
        self.config(bg=tm.current_theme["bg"])
        # Initialise la couleur sélectionnée
        self.selected_color = initial_color
        # Initialise le résultat
        self.result = None
        # Charge les couleurs favorites depuis le gestionnaire de thèmes
        self.custom_colors = tm.load_favorite_colors()
        # Initialise la teinte
        self.hue = 0
        
        # Rend la fenêtre modale
        self.transient(parent)
        self.grab_set()
        
        # Convertit la couleur initiale en HSV pour récupérer la teinte
        r, g, b = self.hex_to_rgb(initial_color)
        h, s, v = self.rgb_to_hsv(r/255, g/255, b/255)
        self.hue = h
        
        # Construit l'interface utilisateur
        self.create_ui()
        
        # Centre la fenêtre sur l'écran
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 350
        y = (self.winfo_screenheight() // 2) - 310
        self.geometry(f'700x620+{x}+{y}')
    
    def hex_to_rgb(self, hex_color):
        """
        Convertit une couleur hexadécimale en RGB.
        
        Args:
            hex_color (str): Couleur au format #RRGGBB
            
        Returns:
            tuple: (R, G, B) avec des valeurs 0-255
        """
        # Supprime le # si présent
        hex_color = hex_color.lstrip('#')
        # Convertit chaque paire de caractères en entier (base 16)
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, r, g, b):
        """
        Convertit des valeurs RGB en couleur hexadécimale.
        
        Args:
            r, g, b: Valeurs RGB (0-255)
            
        Returns:
            str: Couleur au format #RRGGBB
        """
        # Convertit chaque composante en hexadécimal sur 2 caractères
        return f'#{int(r):02x}{int(g):02x}{int(b):02x}'
    
    def rgb_to_hsv(self, r, g, b):
        """
        Convertit des valeurs RGB (0-1) en HSV.
        
        Args:
            r, g, b: Valeurs RGB normalisées (0.0 à 1.0)
            
        Returns:
            tuple: (H, S, V) avec des valeurs 0.0 à 1.0
        """
        import colorsys
        # Utilise la fonction de conversion de la bibliothèque standard
        return colorsys.rgb_to_hsv(r, g, b)
    
    def hsv_to_rgb(self, h, s, v):
        """
        Convertit des valeurs HSV en RGB (0-255).
        
        Args:
            h, s, v: Valeurs HSV (0.0 à 1.0)
            
        Returns:
            tuple: (R, G, B) avec des valeurs 0-255
        """
        import colorsys
        # Convertit HSV en RGB (0-1)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        # Convertit en valeurs 0-255
        return int(r * 255), int(g * 255), int(b * 255)
    
    def create_ui(self):
        """
        Construit l'interface du sélecteur de couleur.
        Crée le gradient 2D, la barre de teinte, l'aperçu et les contrôles.
        """
        # Conteneur principal
        container = tk.Frame(self, bg=tm.current_theme["panel"])
        container.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Titre du sélecteur
        tk.Label(container, text="🎨 Sélecteur de Couleur", font=("Arial", 14, "bold"),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=(0, 10))
        
        # Disposition principale (gauche et droite)
        main_layout = tk.Frame(container, bg=tm.current_theme["panel"])
        main_layout.pack(fill='both', expand=True)
        
        # Zone gauche : gradient et barre de teinte
        left_frame = tk.Frame(main_layout, bg=tm.current_theme["panel"])
        left_frame.pack(side='left', padx=10)
        
        # Label du gradient
        tk.Label(left_frame, text="Sélectionner une couleur :", font=("Arial", 10, "bold"),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=5)
        
        # Conteneur du gradient avec bordure
        gradient_frame = tk.Frame(left_frame, bg=tm.current_theme["accent"])
        gradient_frame.pack(pady=5)
        
        # Canvas du gradient 2D (saturation x valeur)
        self.gradient_canvas = tk.Canvas(gradient_frame, width=256, height=256,
                                        bg="white", highlightthickness=2,
                                        highlightbackground=tm.current_theme["text"],
                                        cursor="crosshair")
        self.gradient_canvas.pack(padx=3, pady=3)
        # Bindings pour le clic et le glissement
        self.gradient_canvas.bind('<Button-1>', self.on_gradient_click)
        self.gradient_canvas.bind('<B1-Motion>', self.on_gradient_click)
        
        # Dessine le gradient initial
        self.draw_gradient()
        
        # Label de la barre de teinte
        tk.Label(left_frame, text="Teinte :", font=("Arial", 9, "bold"),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=(10, 5))
        
        # Conteneur de la barre de teinte avec bordure
        hue_frame = tk.Frame(left_frame, bg=tm.current_theme["accent"])
        hue_frame.pack(pady=5)
        
        # Canvas de la barre de teinte horizontale
        self.hue_canvas = tk.Canvas(hue_frame, width=256, height=30,
                                   bg="white", highlightthickness=2,
                                   highlightbackground=tm.current_theme["text"],
                                   cursor="hand2")
        self.hue_canvas.pack(padx=3, pady=3)
        # Bindings pour le clic et le glissement
        self.hue_canvas.bind('<Button-1>', self.on_hue_click)
        self.hue_canvas.bind('<B1-Motion>', self.on_hue_click)
        
        # Dessine la barre de teinte
        self.draw_hue_bar()
        
        # Zone droite : aperçu et contrôles
        right_frame = tk.Frame(main_layout, bg=tm.current_theme["panel"])
        right_frame.pack(side='left', fill='both', expand=True, padx=10)
        
        # Label de l'aperçu
        tk.Label(right_frame, text="Aperçu :", font=("Arial", 10, "bold"),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=5)
        
        # Canvas d'aperçu de la couleur sélectionnée
        self.preview = tk.Canvas(right_frame, width=180, height=60, 
                                bg=self.selected_color, highlightthickness=2,
                                highlightbackground=tm.current_theme["text"])
        self.preview.pack(pady=5)
        
        # Label du code couleur
        tk.Label(right_frame, text="Code couleur :", font=("Arial", 10, "bold"),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=5)
        
        # Conteneur pour le champ de saisie et le bouton
        entry_frame = tk.Frame(right_frame, bg=tm.current_theme["panel"])
        entry_frame.pack(pady=5)
        
        # Champ de saisie du code hexadécimal
        self.color_entry = tk.Entry(entry_frame, font=("Arial", 11), width=10,
                                    bg=tm.current_theme["accent"], fg=tm.current_theme["text"],
                                    justify='center')
        self.color_entry.insert(0, self.selected_color)
        self.color_entry.pack(side='left', padx=3)
        # Permet de valider avec Entrée
        self.color_entry.bind('<Return>', lambda e: self.apply_manual_color())
        
        # Bouton pour appliquer la couleur saisie manuellement
        apply_btn = tk.Button(entry_frame, text="✓ Appliquer", 
                             command=self.apply_manual_color,
                             bg=tm.current_theme["button_bg"], 
                             fg=tm.current_theme["button_text"],
                             font=("Arial", 9, "bold"),
                             relief='flat', cursor="hand2",
                             padx=8, pady=2)
        apply_btn.pack(side='left', padx=3)
        
        # Bouton pour ajouter aux favoris
        ModernButton(right_frame, "⭐ Ajouter aux favoris", self.add_to_custom, 
                    width=180, height=30, bg=tm.current_theme["panel"]).pack(pady=10)
        
        # Label des couleurs favorites
        tk.Label(right_frame, text="💎 Mes couleurs :", font=("Arial", 9, "bold"),
                bg=tm.current_theme["panel"], fg=tm.current_theme["text"]).pack(pady=5)
        
        # Conteneur pour afficher les couleurs favorites
        self.custom_frame = tk.Frame(right_frame, bg=tm.current_theme["panel"])
        self.custom_frame.pack(fill='x', pady=5)
        # Affiche les couleurs favorites
        self.refresh_custom_colors()
        
        # Conteneur pour les boutons de validation
        btn_frame = tk.Frame(container, bg=tm.current_theme["panel"])
        btn_frame.pack(pady=15)
        
        # Bouton Valider
        ModernButton(btn_frame, "✓ Valider", self.confirm, 
                    width=180, height=40, bg=tm.current_theme["panel"]).pack(side='left', padx=5)
        # Bouton Annuler
        ModernButton(btn_frame, "✗ Annuler", self.cancel, 
                    width=120, height=40, bg=tm.current_theme["panel"]).pack(side='left', padx=5)
    
    def draw_gradient(self):
        """
        Dessine le gradient 2D de saturation et valeur pour la teinte actuelle.
        Utilise PIL si disponible pour un rendu rapide, sinon dessine avec des rectangles.
        """
        # Efface le contenu précédent
        self.gradient_canvas.delete('all')
        
        # Affiche un texte de chargement temporaire
        loading_text = self.gradient_canvas.create_text(128, 128, text="Chargement...",
                                                        font=("Arial", 12),
                                                        fill=tm.current_theme["text"])
        self.gradient_canvas.update()
        
        # Dimensions du gradient
        width = 256
        height = 256
        
        try:
            # Essaie d'utiliser PIL pour un rendu rapide et lisse
            from PIL import Image, ImageTk
            
            # Crée une image RGB
            img = Image.new('RGB', (width, height))
            pixels = img.load()
            
            # Génère chaque pixel du gradient
            for y in range(height):
                for x in range(width):
                    # Saturation augmente de gauche à droite (0 à 1)
                    saturation = x / width
                    # Valeur diminue de haut en bas (1 à 0)
                    value = 1 - (y / height)
                    # Convertit HSV en RGB
                    r, g, b = self.hsv_to_rgb(self.hue, saturation, value)
                    # Définit la couleur du pixel
                    pixels[x, y] = (r, g, b)
            
            # Supprime le texte de chargement
            self.gradient_canvas.delete(loading_text)
            # Convertit l'image en format Tkinter et l'affiche
            self.gradient_image = ImageTk.PhotoImage(img)
            self.gradient_canvas.create_image(0, 0, anchor='nw', image=self.gradient_image)
            
        except ImportError:
            # Si PIL n'est pas disponible, dessine avec des rectangles (plus lent)
            self.gradient_canvas.delete(loading_text)
            # Taille des blocs (compromise performance/qualité)
            block_size = 4
            
            # Dessine le gradient par blocs
            for y in range(0, height, block_size):
                for x in range(0, width, block_size):
                    # Calcule saturation et valeur pour ce bloc
                    saturation = x / width
                    value = 1 - (y / height)
                    # Convertit en RGB
                    r, g, b = self.hsv_to_rgb(self.hue, saturation, value)
                    color = self.rgb_to_hex(r, g, b)
                    # Dessine un rectangle de la couleur calculée
                    self.gradient_canvas.create_rectangle(x, y, x+block_size, y+block_size, 
                                                         fill=color, outline="")
    
    def draw_hue_bar(self):
        """
        Dessine la barre de teinte horizontale (arc-en-ciel).
        Affiche également un curseur sur la teinte actuelle.
        """
        # Efface le contenu précédent
        self.hue_canvas.delete('all')
        
        # Dimensions de la barre
        width = 256
        height = 30
        
        # Dessine une ligne verticale pour chaque valeur de teinte
        for x in range(width):
            # Calcule la teinte pour cette position (0.0 à 1.0)
            hue = x / width
            # Convertit en RGB à saturation et valeur maximales
            r, g, b = self.hsv_to_rgb(hue, 1.0, 1.0)
            color = self.rgb_to_hex(r, g, b)
            # Dessine une ligne verticale de cette couleur
            self.hue_canvas.create_line(x, 0, x, height, fill=color)
        
        # Dessine le curseur sur la teinte actuelle
        hue_x = int(self.hue * width)
        # Ligne blanche épaisse
        self.hue_canvas.create_line(hue_x, 0, hue_x, height, fill='white', width=3)
        # Ligne noire fine par-dessus pour le contraste
        self.hue_canvas.create_line(hue_x, 0, hue_x, height, fill='black', width=1)
    
    def on_gradient_click(self, event):
        """
        Gère le clic ou le glissement sur le gradient 2D.
        Met à jour la couleur sélectionnée selon la position.
        
        Args:
            event: Événement souris contenant les coordonnées
        """
        # Limite les coordonnées aux dimensions du canvas
        x = max(0, min(255, event.x))
        y = max(0, min(255, event.y))
        
        # Convertit la position en saturation et valeur
        saturation = x / 256
        value = 1 - (y / 256)
        
        # Convertit HSV en RGB avec la teinte actuelle
        r, g, b = self.hsv_to_rgb(self.hue, saturation, value)
        self.selected_color = self.rgb_to_hex(r, g, b)
        
        # Met à jour l'aperçu
        self.preview.config(bg=self.selected_color)
        # Met à jour le champ de saisie
        self.color_entry.delete(0, tk.END)
        self.color_entry.insert(0, self.selected_color)
    
    def on_hue_click(self, event):
        """
        Gère le clic ou le glissement sur la barre de teinte.
        Met à jour la teinte et redessine le gradient.
        
        Args:
            event: Événement souris contenant les coordonnées
        """
        # Limite les coordonnées
        x = max(0, min(255, event.x))
        # Convertit la position en teinte (0.0 à 1.0)
        self.hue = x / 256
        
        # Redessine le gradient avec la nouvelle teinte
        self.draw_gradient()
        # Redessine la barre avec le nouveau curseur
        self.draw_hue_bar()
        
        # Récupère la saturation et valeur actuelles de la couleur sélectionnée
        r, g, b = self.hex_to_rgb(self.selected_color)
        h, s, v = self.rgb_to_hsv(r/255, g/255, b/255)
        
        # Applique la nouvelle teinte avec les mêmes saturation et valeur
        r, g, b = self.hsv_to_rgb(self.hue, s, v)
        self.selected_color = self.rgb_to_hex(r, g, b)
        
        # Met à jour l'aperçu
        self.preview.config(bg=self.selected_color)
        # Met à jour le champ de saisie
        self.color_entry.delete(0, tk.END)
        self.color_entry.insert(0, self.selected_color)
    
    def apply_manual_color(self):
        """
        Applique une couleur saisie manuellement dans le champ de texte.
        Valide le format et met à jour le gradient et l'aperçu.
        """
        # Récupère le texte saisi
        color = self.color_entry.get().strip()
        
        # Ajoute le # si manquant
        if not color.startswith('#'):
            color = '#' + color
        
        # Vérifie que le format est valide (#RRGGBB = 7 caractères)
        if len(color) == 7:
            try:
                # Tente de convertir en RGB pour valider
                r, g, b = self.hex_to_rgb(color)
                # Convertit en HSV pour récupérer la teinte
                h, s, v = self.rgb_to_hsv(r/255, g/255, b/255)
                
                # Met à jour la teinte
                self.hue = h
                # Met à jour la couleur sélectionnée
                self.selected_color = color
                # Met à jour l'aperçu
                self.preview.config(bg=color)
                # Met à jour le champ de saisie avec le format normalisé
                self.color_entry.delete(0, tk.END)
                self.color_entry.insert(0, color)
                
                # Redessine le gradient et la barre de teinte
                self.draw_gradient()
                self.draw_hue_bar()
                
            except Exception as e:
                # Si la conversion échoue, affiche une erreur
                show_custom_message(self, "Erreur", 
                                  f"Code couleur invalide!\n{str(e)}", "error")
        else:
            # Format incorrect
            show_custom_message(self, "Erreur", 
                              "Format incorrect!\nUtilisez: #RRGGBB (ex: #ff0000)", "error")
    
    def add_to_custom(self):
        """
        Ajoute la couleur actuelle aux couleurs favorites.
        Sauvegarde dans le gestionnaire de thèmes.
        """
        color = self.selected_color
        # Vérifie que la couleur n'est pas déjà dans les favoris
        if color not in self.custom_colors:
            # Ajoute à la liste
            self.custom_colors.append(color)
            # Sauvegarde dans le fichier
            tm.save_favorite_colors(self.custom_colors)
            # Rafraîchit l'affichage
            self.refresh_custom_colors()
    
    def remove_from_custom(self, color):
        """
        Supprime une couleur des favoris.
        
        Args:
            color (str): Couleur à supprimer
        """
        # Vérifie que la couleur est dans les favoris
        if color in self.custom_colors:
            # Supprime de la liste
            self.custom_colors.remove(color)
            # Sauvegarde la nouvelle liste
            tm.save_favorite_colors(self.custom_colors)
            # Rafraîchit l'affichage
            self.refresh_custom_colors()
    
    def refresh_custom_colors(self):
        """
        Rafraîchit l'affichage des couleurs favorites.
        Crée un bouton pour chaque couleur avec un bouton de suppression.
        """
        # Supprime tous les widgets existants
        for widget in self.custom_frame.winfo_children():
            widget.destroy()
        
        # Si aucune couleur favorite
        if not self.custom_colors:
            # Affiche un message
            tk.Label(self.custom_frame, text="(Aucune couleur favorite)",
                    font=("Arial", 8, "italic"), bg=tm.current_theme["panel"],
                    fg=tm.current_theme["text"]).pack()
        else:
            # Conteneur en grille pour les couleurs
            colors_grid = tk.Frame(self.custom_frame, bg=tm.current_theme["panel"])
            colors_grid.pack()
            
            # Crée un bouton pour chaque couleur favorite
            for i, color in enumerate(self.custom_colors):
                # Conteneur pour le bouton et le X de suppression
                color_container = tk.Frame(colors_grid, bg=tm.current_theme["panel"])
                # Place en grille (6 colonnes maximum)
                color_container.grid(row=i//6, column=i%6, padx=2, pady=2)
                
                # Bouton de couleur (cliquable pour sélectionner)
                btn = tk.Button(color_container, bg=color, width=3, height=1,
                              relief='solid', bd=2, cursor="hand2",
                              command=lambda c=color: self.set_color(c))
                btn.pack()
                
                # Label X pour supprimer
                del_btn = tk.Label(color_container, text="✕", font=("Arial", 7),
                                  bg=tm.current_theme["panel"], fg=tm.current_theme["text"],
                                  cursor="hand2")
                del_btn.pack()
                # Binding du clic pour la suppression
                del_btn.bind("<Button-1>", lambda e, c=color: self.remove_from_custom(c))
    
    def set_color(self, color):
        """
        Applique une couleur favorite comme couleur sélectionnée.
        
        Args:
            color (str): Couleur à appliquer
        """
        # Met à jour la couleur sélectionnée
        self.selected_color = color
        # Met à jour l'aperçu
        self.preview.config(bg=color)
        # Met à jour le champ de saisie
        self.color_entry.delete(0, tk.END)
        self.color_entry.insert(0, color)
        
        # Convertit en HSV pour récupérer la teinte
        r, g, b = self.hex_to_rgb(color)
        h, s, v = self.rgb_to_hsv(r/255, g/255, b/255)
        self.hue = h
        
        # Redessine le gradient et la barre
        self.draw_gradient()
        self.draw_hue_bar()
    
    def confirm(self):
        """
        Valide la couleur sélectionnée et ferme le sélecteur.
        """
        self.result = self.selected_color
        self.destroy()
    
    def cancel(self):
        """
        Annule la sélection et ferme le sélecteur.
        """
        self.result = None
        self.destroy()

def show_color_picker(parent, title, initial_color):
    """
    Affiche le sélecteur de couleur et retourne la couleur choisie.
    
    Args:
        parent: Fenêtre parente
        title (str): Titre du sélecteur
        initial_color (str): Couleur initiale
        
    Returns:
        str/None: Couleur sélectionnée ou None si annulé
    """
    # Crée le sélecteur
    picker = CustomColorPicker(parent, title, initial_color)
    # Attend la fermeture
    parent.wait_window(picker)
    # Retourne le résultat
    return picker.result


class ModernButton(tk.Canvas):
    """
    Bouton avec style moderne et animations de survol.
    Hérite de Canvas pour permettre un dessin personnalisé avec coins arrondis.
    """
    
    def __init__(self, parent, text, command, **kwargs):
        """
        Initialise le bouton moderne.
        
        Args:
            parent: Widget parent
            text (str): Texte du bouton
            command: Fonction appelée au clic
            **kwargs: Arguments supplémentaires (width, height, bg)
        """
        # Appel du constructeur Canvas sans bordure
        super().__init__(parent, highlightthickness=0, **kwargs)
        # Stocke la fonction de callback
        self.command = command
        # Stocke le texte
        self.text = text
        # État de survol initialisé à False
        self.is_hover = False
        # État du bouton
        self.config_state = 'normal'
        
        # Configure les dimensions
        self.config(width=kwargs.get('width', 150), height=kwargs.get('height', 40))
        # Récupère les couleurs du thème
        self.bg_color = tm.current_theme["button_bg"] 
        self.hover_color = tm.current_theme["button_hover"]
        self.text_color = tm.current_theme["button_text"]
        
        # Dessine le bouton initial
        self.draw()
        
        # Bindings des événements souris
        self.bind("<Button-1>", lambda e: self.on_click())  # Clic
        self.bind("<Enter>", lambda e: self.on_enter())     # Entrée de la souris
        self.bind("<Leave>", lambda e: self.on_leave())     # Sortie de la souris

    def config(self, **kwargs):
        """
        Configure le bouton (override de la méthode Canvas).
        Gère spécialement l'état 'disabled'.
        
        Args:
            **kwargs: Arguments de configuration
        """
        # Si on change l'état du bouton
        if 'state' in kwargs:
            self.state = kwargs['state']
            if self.state == 'disabled':
                # Mode désactivé
                self.config_state = 'disabled'
                # Supprime les bindings d'événements
                self.unbind("<Button-1>")
                self.unbind("<Enter>")
                self.unbind("<Leave>")
                # Change le curseur
                self.configure(cursor="")
            else:
                # Mode normal
                self.config_state = 'normal'
                # Réactive les bindings
                self.bind("<Button-1>", lambda e: self.on_click())
                self.bind("<Enter>", lambda e: self.on_enter())
                self.bind("<Leave>", lambda e: self.on_leave())
                # Curseur main
                self.configure(cursor="hand2")
            # Redessine le bouton
            self.draw()
    
    def draw(self):
        """
        Dessine le bouton avec ses coins arrondis et son texte.
        Utilise la couleur de survol ou la couleur normale.
        """
        # Efface le dessin précédent
        self.delete("all")
        # Choisit la couleur selon l'état de survol
        color = self.hover_color if self.is_hover else self.bg_color
        
        # Récupère les dimensions
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        
        # Dessine le rectangle arrondi
        self.create_rounded_rect(2, 2, w-2, h-2, radius=12, fill=color, outline="")
        
        # Dessine le texte centré
        self.create_text(w//2, h//2, text=self.text, fill=self.text_color, 
                        font=("Arial", 10, "bold"))
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """
        Dessine un rectangle avec coins arrondis.
        
        Args:
            x1, y1: Coordonnées du coin supérieur gauche
            x2, y2: Coordonnées du coin inférieur droit
            radius: Rayon des coins arrondis
            **kwargs: Arguments pour create_polygon
            
        Returns:
            ID du polygone créé
        """
        # Liste des points pour créer un rectangle arrondi
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                 x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                 x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        # Crée un polygone lissé
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def on_enter(self):
        """
        Callback appelé quand la souris entre dans le bouton.
        Active l'état de survol et redessine.
        """
        self.is_hover = True
        self.draw()
    
    def on_leave(self):
        """
        Callback appelé quand la souris sort du bouton.
        Désactive l'état de survol et redessine.
        """
        self.is_hover = False
        self.draw()
    
    def on_click(self):
        """
        Callback appelé lors du clic sur le bouton.
        Exécute la fonction command si le bouton est actif.
        """
        # Vérifie que le bouton est actif et qu'une fonction est définie
        if self.command and self.config_state == 'normal':
            self.command()
        
    def update_colors(self):
        """
        Met à jour les couleurs du bouton selon le thème actuel.
        Utile après un changement de thème.
        """
        # Récupère les nouvelles couleurs du thème
        self.bg_color = tm.current_theme["button_bg"]
        self.hover_color = tm.current_theme["button_hover"]
        self.text_color = tm.current_theme["button_text"]
        # Redessine avec les nouvelles couleurs
        self.draw()

# CLASSE THEMEPREVIEW

class ThemePreview(tk.Canvas):
    """
    Aperçu visuel d'un thème avec exemples d'éléments.
    Affiche un mini panneau avec grille et bouton pour prévisualiser un thème.
    """
    
    def __init__(self, parent, theme_data, **kwargs):
        """
        Initialise l'aperçu de thème.
        
        Args:
            parent: Widget parent
            theme_data (dict): Dictionnaire des couleurs du thème
            **kwargs: Arguments supplémentaires (width, height)
        """
        # Appel du constructeur Canvas
        super().__init__(parent, highlightthickness=0, **kwargs)
        # Stocke les données du thème
        self.theme = theme_data
        # Configure les dimensions
        self.config(width=kwargs.get('width', 320), height=kwargs.get('height', 180))
        # Dessine l'aperçu
        self.draw_preview()
    
    def draw_preview(self):
        """
        Dessine l'aperçu du thème avec tous ses éléments.
        Affiche : fond, panneau, titre, grille exemple et bouton exemple.
        """
        # Efface le dessin précédent
        self.delete("all")
        # Dimensions de l'aperçu
        w, h = 320, 180
        
        # Dessine le fond
        self.create_rectangle(0, 0, w, h, fill=self.theme["bg"], outline="")
        
        # Dessine le panneau d'en-tête
        self.create_rectangle(10, 10, w-10, 60, fill=self.theme["panel"], outline="")
        # Titre centré
        self.create_text(w//2, 35, text="Aperçu du Thème", 
                        fill=self.theme["text"], font=("Arial", 12, "bold"))
        
        # Dessine une mini grille 5x5 comme exemple
        cell_size = 15
        start_x, start_y = 20, 80
        for i in range(5):
            for j in range(5):
                # Calcule la position de chaque cellule
                x0 = start_x + j * cell_size
                y0 = start_y + i * cell_size
                # Alterne les couleurs vivante/morte
                color = self.theme["alive"] if (i + j) % 2 == 0 else self.theme["dead"]
                # Dessine la cellule
                self.create_rectangle(x0, y0, x0+cell_size-2, y0+cell_size-2, 
                                    fill=color, outline=self.theme["bg"])
        
        # Dessine un bouton exemple
        btn_x, btn_y = 140, 100
        self.create_rounded_rect(btn_x, btn_y, btn_x+150, btn_y+40, 
                                radius=10, fill=self.theme["button_bg"], outline="")
        # Texte du bouton
        self.create_text(btn_x+75, btn_y+20, text="Bouton Exemple", 
                        fill=self.theme["button_text"], font=("Arial", 10, "bold"))
    
    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        """
        Dessine un rectangle avec coins arrondis.
        
        Args:
            x1, y1: Coordonnées du coin supérieur gauche
            x2, y2: Coordonnées du coin inférieur droit
            radius: Rayon des coins arrondis
            **kwargs: Arguments pour create_polygon
            
        Returns:
            ID du polygone créé
        """
        # Liste des points pour le rectangle arrondi
        points = [x1+radius, y1, x2-radius, y1, x2, y1, x2, y1+radius,
                 x2, y2-radius, x2, y2, x2-radius, y2, x1+radius, y2,
                 x1, y2, x1, y2-radius, x1, y1+radius, x1, y1]
        # Crée le polygone lissé
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def update_theme(self, theme_data):
        """
        Met à jour l'aperçu avec un nouveau thème.
        
        Args:
            theme_data (dict): Nouveau dictionnaire de thème
        """
        # Met à jour les données
        self.theme = theme_data
        # Redessine l'aperçu
        self.draw_preview()