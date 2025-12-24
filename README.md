# 🧬 Jeu de la Vie - Version Moderne

**Auteur :** LAM Hoang Anh Harry

> Simulation interactive du Game of Life de Conway avec interface graphique moderne et calculs parallélisés

---

## 📋 Table des matières

- [Présentation](#-présentation)
- [Fonctionnalités](#-fonctionnalités)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Architecture](#-architecture)
- [Structure du projet](#-structure-du-projet)
- [Technologies utilisées](#-technologies-utilisées)

---

## 🎮 Présentation

Le **Jeu de la Vie** est un automate cellulaire imaginé par le mathématicien John Conway en 1970. Cette implémentation moderne propose :

- ⚡ **Calculs parallèles** avec multi-threading (un thread par cellule)
- 🎨 **Interface graphique moderne** développée avec Tkinter
- 🎮 **Contrôles interactifs** pour explorer les patterns
- 💾 **Sauvegarde automatique** de vos simulations

### Les règles du jeu

Le jeu évolue selon des règles simples appliquées à chaque génération :

1. **Survie** : Une cellule vivante avec 2 ou 3 voisins survit
2. **Mort** : Une cellule vivante avec <2 ou >3 voisins meurt (sous-population ou surpopulation)
3. **Naissance** : Une cellule morte avec exactement 3 voisins naît

Les 8 cases adjacentes (horizontales, verticales et diagonales) sont considérées comme voisines.

---

## ✨ Fonctionnalités

### 🎯 Simulation avancée

- ⚡ **Multi-threading haute performance** : Chaque cellule possède son propre thread pour des calculs parallèles
- 🔄 **Synchronisation par barrière** : Tous les threads se synchronisent entre chaque génération
- 🎮 **Contrôles en temps réel** : Play/Pause, avance pas à pas, vitesse variable (1-30 gen/s)
- 📊 **Grilles adaptatives** : Taille configurable de 5×5 à 80×80 cellules
- ↩️ **Historique complet** : Naviguez dans les 100 dernières générations (Undo/Redo)

### 🎨 Personnalisation visuelle

#### Thèmes prédéfinis
- **Dark** : Sombre et élégant (par défaut)
- **Neon** : Couleurs vives et énergiques
- **Ocean** : Tons bleus apaisants
- **Sunset** : Ambiance chaude et rosée

#### Créateur de thèmes personnalisés
- 🎨 **Sélecteur de couleurs 2D** (saturation × valeur)
- 🌈 **Barre de teinte** pour choisir la couleur de base
- ⭐ **Gestion des couleurs favorites**
- 👁️ **Aperçu en temps réel**
- 💾 **Sauvegarde automatique** de vos créations

### 🖱️ Interaction directe

- **Clic simple** : Inverse l'état d'une cellule (morte ↔ vivante)
- **Clic + Glissement** : Dessinez ou effacez en continu
- **Mode intelligent** : Le premier clic détermine automatiquement le mode (dessiner/effacer)
- **Édition en pause** : Modifiez la grille à tout moment

### 💾 Reprise de session

- **Sauvegarde automatique** : Votre session est sauvegardée à chaque fermeture
- **Message de reprise** : Au redémarrage, un message vous propose de :
  - **Reprendre** : Continue exactement où vous vous êtes arrêté
  - **Recommencer** : Génère une nouvelle grille aléatoire
- **État préservé** : La génération, la vitesse et l'état (pause/lecture) sont conservés

### 📚 Tutoriel intégré

- **Guide interactif** : 12 pages explicatives avec exemples visuels
- **Patterns classiques** : Block, Blinker, Glider avec explications détaillées
- **Navigation intuitive** : Précédent/Suivant avec indicateur de progression

---

## 📦 Installation

### Prérequis

- **Python 3.7 ou supérieur**
- **Tkinter** (inclus par défaut avec Python)
- **PIL/Pillow** (optionnel, pour de meilleures performances graphiques)

### Installation rapide

```bash
# Cloner le dépôt depuis GitHub
git clone https://github.com/LAM-Harry/jeu-de-la-vie.git

# Se déplacer dans le dossier du projet
cd jeu-de-la-vie

# (Optionnel) Installer Pillow pour de meilleures performances
pip install Pillow

# Lancer l'application
python main.py
```

### Sans Pillow

Le projet fonctionne parfaitement sans Pillow, mais le sélecteur de couleurs sera légèrement plus lent au rendu.

---

## 🎯 Utilisation

### Démarrage rapide

1. **Lancez l'application** : `python main.py`
2. Cliquez sur **"▶ JOUER"** dans le menu principal
3. Générez une grille aléatoire avec **🎲 Aléatoire**
4. Lancez la simulation avec **▶ Démarrer**
5. Ajustez la vitesse avec le curseur **⚡ Vitesse**

### Contrôles de simulation

| Bouton | Action |
|--------|--------|
| **▶ Démarrer** | Lance la simulation automatique |
| **⏸ Pause** | Met en pause la simulation |
| **⏩ +1 Gen** | Avance d'une seule génération (mode pas à pas) |
| **🎲 Aléatoire** | Génère une grille aléatoire (~25% de cellules vivantes) |
| **🗑️ Effacer** | Vide complètement la grille |
| **◀ Précédent** | Revient à la génération précédente (Undo) |
| **▶ Suivant** | Avance à la génération suivante (Redo) |
| **⚡ Curseur** | Ajuste la vitesse (1-30 générations/seconde) |

### Dessiner vos propres patterns

1. Cliquez sur **🗑️ Effacer** pour partir d'une grille vide
2. **Cliquez** sur les cellules pour les activer/désactiver
3. **Maintenez + Glissez** pour dessiner en continu
4. Lancez la simulation pour voir votre création évoluer

### Patterns classiques à essayer

#### 🟦 Block (Nature morte)
```
██
██
```
Formation carrée 2×2 qui reste stable indéfiniment.

#### 〰️ Blinker (Oscillateur)
```
███
```
Oscille entre vertical et horizontal avec une période de 2 générations.

#### ✈️ Glider (Vaisseau spatial)
```
 █ 
  █
███
```
Se déplace en diagonale sur toute la grille.

> 💡 **Astuce** : Consultez le tutoriel intégré (**📚 TUTORIEL**) pour découvrir d'autres patterns fascinants !

### Créer un thème personnalisé

1. Cliquez sur **➕ Créer** dans la section Thèmes
2. Choisissez vos couleurs avec le sélecteur 2D et la barre de teinte
3. Donnez un nom à votre thème
4. Cliquez sur **💾 Enregistrer**
5. Votre thème apparaît immédiatement dans la liste !

---

## 🏗️ Architecture

### Vue d'ensemble du système

```
┌─────────────────────────────────────────────────────────┐
│                        main.py                          │
│                   (Point d'entrée)                      │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                   gui_windows.py                        │
│         (Menu principal, Tutoriel, Créateur)            │
└─────┬──────────────────────────────────────────────┬────┘
      │                                              │
┌─────▼──────────────────┐                  ┌────────▼──────┐
│    gui_game.py         │                  │ gui_components│
│ (Fenêtre simulation)   │◄─────────────────│   (Widgets)   │
└─────┬──────────────────┘                  └───────────────┘
      │
┌─────▼──────────────────┬────────────────┬─────────────────┐
│  gamelife_core.py      │ theme_manager  │ history_manager │
│  (Threads, règles)     │   (Thèmes)     │  (Undo/Redo)    │
└────────────────────────┴────────────────┴─────────────────┘
```

**Flux de dépendances** :
- `main.py` → Initialise le menu principal
- `gui_windows.py` → Gère toutes les fenêtres de l'application
- `gui_game.py` → Fenêtre de simulation utilisant les composants réutilisables
- `gui_components.py` → Bibliothèque de widgets personnalisés
- **Couche inférieure** : Moteur de jeu + Gestionnaires (indépendants de l'UI)

### Composants principaux

#### 1. Moteur de simulation (`gamelife_core.py`)

**Grilles doubles** : Technique du double buffering
- `T` : Grille actuelle de taille `(n+2) × (n+2)`
- `Tnext` : Grille calculée pour la génération suivante
- Bordures `+2` : Simplifient le calcul des voisins (pas de cas spéciaux aux bords)

**Pool de threads** : Calculs parallélisés
```python
# Un thread créé pour chaque cellule
for i in range(1, n+1):
    for j in range(1, n+1):
        thread = Thread(target=cell_thread, args=(i, j))
        thread.start()
```

**Barrière de synchronisation** : Coordination globale
```python
barrier = threading.Barrier(n * n, action=barrier_action)

# Dans chaque thread
barrier.wait()  # Bloque jusqu'à ce que tous les threads arrivent
```

La barrière garantit que :
- Aucun thread ne commence la génération N+1 avant que tous aient fini N
- Le dernier thread déclenche automatiquement `barrier_action()` pour échanger les grilles

**Événements de contrôle** :
- `running` : Active/désactive la simulation
- `stop_event` : Arrêt complet des threads
- `step_event` : Mode pas à pas (une seule génération)
- `redraw_event` : Déclenche le rafraîchissement graphique

#### 2. Gestion de l'historique (`history_manager.py`)

**Système de snapshots** :
```python
generation_history = {
    0: [[grille_gen_0]],
    1: [[grille_gen_1]],
    2: [[grille_gen_2]],
    # ...
}
```

**Fonctionnalités** :
- Sauvegarde automatique après chaque génération
- Navigation Undo/Redo instantanée
- Limite mémoire : 100 dernières générations conservées
- Persistance sur disque au format JSON

#### 3. Système de thèmes (`theme_manager.py`)

**Structure d'un thème** :
```python
theme = {
    "bg": "#1a1a2e",           # Arrière-plan
    "panel": "#16213e",         # Panneaux
    "accent": "#0f3460",        # Accent
    "alive": "#00ff88",         # Cellules vivantes
    "dead": "#2d3561",          # Cellules mortes
    "text": "#eeeeee",          # Texte
    "button_bg": "#0f3460",     # Boutons
    "button_hover": "#1e5f8c",  # Survol
    "button_text": "#ffffff"    # Texte boutons
}
```

**Gestion** :
- 4 thèmes prédéfinis non modifiables
- Thèmes personnalisés stockés dans `custom_themes.json`
- Changement de thème instantané sans redémarrage

#### 4. Interface graphique

**Fenêtre principale** (`gui_game.py`)
- Canvas adaptatif avec redimensionnement automatique
- Gestion du clic et du glissement pour dessiner
- Boucle de rafraîchissement à 30 FPS
- Synchronisation avec le moteur via événements

**Composants réutilisables** (`gui_components.py`)
- `ModernButton` : Boutons avec animation de survol
- `CustomDialog` : Dialogues personnalisés
- `CustomColorPicker` : Sélecteur de couleurs HSV complet
- `ThemePreview` : Aperçu miniature des thèmes

**Fenêtres secondaires** (`gui_windows.py`)
- `ModernMainMenu` : Menu principal avec sélection de thèmes
- `ModernTutorialWindow` : Tutoriel interactif 12 pages
- `ThemeCreatorWindow` : Éditeur de thèmes avec aperçu temps réel

### Flux d'exécution détaillé

```
1. DÉMARRAGE
   main.py
     │
     └─→ ModernMainMenu affiche le menu
           │
           └─→ Charge configuration (thème, vitesse, état)

2. LANCEMENT DU JEU
   Clic sur "JOUER"
     │
     └─→ ModernApp (gui_game.py)
           │
           ├─→ Initialise grilles T et Tnext
           ├─→ start_workers() crée n×n threads
           ├─→ Charge historique depuis disque
           └─→ Lance ui_loop() (boucle 30ms)

3. SIMULATION EN COURS
   Threads en parallèle
     │
     ├─→ Chaque thread exécute cell_thread(i, j)
     │     │
     │     ├─→ Attend running.set()
     │     ├─→ Compte les voisins vivants
     │     ├─→ Applique règles de Conway
     │     └─→ barrier.wait()
     │
     └─→ Dernier thread → barrier_action()
           │
           ├─→ Échange T ↔ Tnext (swap atomique)
           ├─→ Incrémente gen_counter
           ├─→ Sauvegarde snapshot dans historique
           ├─→ Déclenche redraw_event
           └─→ Applique délai selon vitesse

4. RAFRAÎCHISSEMENT INTERFACE
   ui_loop() vérifie redraw_event
     │
     └─→ redraw() met à jour tous les rectangles du canvas
           │
           └─→ Boucle continue toutes les 30ms...
```

### Synchronisation des threads

**Attente de démarrage** :
```python
while not (running.is_set() or stop_event.is_set()):
    time.sleep(0.01)  # Vérifie toutes les 10ms
```

**Calcul de l'état suivant** :
```python
# Compte les 8 voisins
neighbors = (
    T[i-1][j-1] + T[i-1][j] + T[i-1][j+1] +
    T[i][j-1] + T[i][j+1] +
    T[i+1][j-1] + T[i+1][j] + T[i+1][j+1]
)

# Règles de Conway
if T[i][j] == 1:
    Tnext[i][j] = 1 if neighbors in (2, 3) else 0
else:
    Tnext[i][j] = 1 if neighbors == 3 else 0
```

**Point de synchronisation** :
```python
barrier.wait()  # Tous les threads se rejoignent ici
# Le dernier arrivé exécute automatiquement barrier_action()
```

---

## 📁 Structure du projet

```
jeu-de-la-vie/
│
├── main.py                      # Point d'entrée
│
├── gamelife_core.py             # Moteur de simulation
│   ├── Grilles T et Tnext
│   ├── Gestion des threads
│   ├── Barrière de synchronisation
│   ├── Règles de Conway
│   └── Événements de contrôle
│
├── history_manager.py           # Gestion de l'historique
│   ├── Snapshots des générations
│   ├── Navigation Undo/Redo
│   ├── Limite à 100 générations
│   └── Sauvegarde JSON
│
├── theme_manager.py             # Système de thèmes
│   ├── 4 thèmes prédéfinis
│   ├── Thèmes personnalisés
│   ├── Configuration globale
│   └── Persistance
│
├── gui_game.py                  # Fenêtre principale
│   ├── Canvas adaptatif
│   ├── Panneau de contrôle
│   ├── Panneau de configuration
│   ├── Interaction souris
│   └── Boucle de rafraîchissement
│
├── gui_windows.py               # Fenêtres secondaires
│   ├── ModernMainMenu
│   ├── ModernTutorialWindow
│   └── ThemeCreatorWindow
│
├── gui_components.py            # Composants UI
│   ├── ModernButton
│   ├── CustomDialog
│   ├── CustomInputDialog
│   ├── CustomColorPicker
│   └── ThemePreview
│
├── gamelife_config.json         # Configuration (auto-généré)
├── custom_themes.json           # Thèmes perso (auto-généré)
├── favorite_colors.json         # Couleurs favorites (auto-généré)
├── gamelife_history.json        # Historique (auto-généré)
│
└── README.md                    # Documentation
```

### Fichiers générés automatiquement

Ces fichiers sont créés lors de l'utilisation :

- **`gamelife_config.json`** : Préférences (thème, vitesse, état pause/lecture)
- **`custom_themes.json`** : Thèmes créés par l'utilisateur
- **`favorite_colors.json`** : Couleurs favorites du sélecteur
- **`gamelife_history.json`** : Dernière session sauvegardée

---

## 🛠️ Technologies utilisées

### Bibliothèques Python

| Bibliothèque | Usage | Statut |
|--------------|-------|--------|
| **Tkinter** | Interface graphique | Obligatoire (inclus) |
| **Threading** | Calculs parallèles | Obligatoire (inclus) |
| **JSON** | Sauvegarde données | Obligatoire (inclus) |
| **Pillow (PIL)** | Rendu graphique | Optionnel |

### Concepts de programmation

- **Multi-threading** : Un thread par cellule pour calculs parallèles
- **Barrière de synchronisation** : Coordination de n×n threads
- **Double buffering** : Grilles T et Tnext pour éviter les conflits
- **Architecture modulaire** : Séparation claire des responsabilités
- **Programmation événementielle** : Interface réactive
- **Design patterns** : Observer (événements), Singleton (configuration)

### Performances

- **Grille 30×30** : 900 threads simultanés
- **Grille 50×50** : 2500 threads simultanés
- **Grille 80×80** : 6400 threads simultanés (maximum)
- **Rafraîchissement** : 30 FPS (interface)
- **Vitesse simulation** : 1-30 générations/seconde (configurable)

---

## 📖 Guide avancé

### Optimisation des performances

**Pour les grandes grilles (60×60+)** :
- Réduisez la vitesse à 5-10 gen/s
- Installez Pillow pour un rendu plus rapide
- Fermez les applications gourmandes en ressources

**Pour l'analyse détaillée** :
- Utilisez le mode **⏩ +1 Gen** (pas à pas)
- Naviguez avec **◀ Précédent** et **▶ Suivant**
- Ajustez le zoom de votre écran si nécessaire

### Patterns avancés

**Pentadecathlon** (Oscillateur période 15) :
```
  ████  
██    ██
  ████  
```

**Glider Gun** (Générateur de Gliders) :
Structure complexe qui émet des Gliders en continu.
Cherchez "Gosper Glider Gun" pour le pattern complet.

**Puffer Train** :
Vaisseau spatial qui laisse une traînée de débris.

> 🔍 **Ressources** : Consultez [LifeWiki](https://www.conwaylife.com/) pour découvrir des milliers de patterns fascinants !

### Résolution de problèmes

**L'application ne démarre pas** :
```bash
# Vérifiez la version de Python
python --version  # Doit être 3.7+

# Vérifiez que Tkinter est installé
python -m tkinter
```

**Interface lente sur grandes grilles** :
```bash
# Installez Pillow pour améliorer les performances
pip install Pillow
```

**Les thèmes ne se sauvegardent pas** :
- Vérifiez les permissions d'écriture dans le dossier
- Les fichiers JSON doivent être accessibles en écriture