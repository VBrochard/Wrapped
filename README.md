# Wrapped



Plan de Projet : Outil de Chiffrement de PDF en Python

Voici un plan détaillé pour créer un script Python capable de chiffrer et déchiffrer des fichiers (comme des PDF) de manière sécurisée à l'aide d'un mot de passe.

L'objectif est de rendre le fichier illisible sans le mot de passe correct. Nous n'allons pas utiliser de "seed" manuelle, mais un concept cryptographique bien plus robuste appelé "Salt" (Sel), qui correspond à votre idée de "seed unique" et qui est généré automatiquement.

1. Concepts Clés

Avant de commencer, voici les concepts que nous allons utiliser :

Chiffrement Symétrique (AES) : Nous utiliserons l'algorithme AES (Advanced Encryption Standard). C'est la norme mondiale actuelle, utilisée par les gouvernements et les banques. Il est considéré comme "incourtable" s'il est bien implémenté. Nous utiliserons le mode GCM (Galois/Counter Mode), qui non seulement chiffre les données, mais vérifie aussi qu'elles n'ont pas été modifiées (authentification).

Dérivation de Clé (PBKDF2) : Un mot de passe (ex: "monMotDePasse123") n'est pas une bonne clé de chiffrement. Nous devons le transformer en une clé binaire sécurisée. Pour cela, nous utilisons une "Fonction de Dérivation de Clé Basée sur un Mot de Passe" comme PBKDF2.

Sel (Salt) : C'est là que votre "seed unique" entre en jeu. Pour qu'un même mot de passe ne génère pas toujours la même clé (ce qui est une faille de sécurité), on lui ajoute un "Sel" : une petite donnée aléatoire unique générée pour chaque chiffrement. Ce "Sel" n'est pas secret et est stocké avec le fichier chiffré. Il garantit que si vous chiffrez deux fichiers identiques avec le même mot de passe, les fichiers chiffrés résultants seront totalement différents.

Nonce (IV) : Une autre donnée aléatoire, similaire au Sel, mais utilisée par l'algorithme AES-GCM lui-même pour garantir que le chiffrement est unique à chaque fois. Il est également stocké avec le fichier chiffré.

[Image d'un diagramme de chiffrement symétrique avec dérivation de clé]

2. Bibliothèques Python Requises

La seule bibliothèque externe dont vous aurez besoin est cryptography. C'est la bibliothèque de référence en Python pour toutes les opérations cryptographiques.

Vous pouvez l'installer avec pip :

pip install cryptography


Nous utiliserons aussi des modules intégrés :

os : Pour générer des données aléatoires sécurisées (os.urandom).

getpass : Pour demander un mot de passe à l'utilisateur de manière sécurisée (sans l'afficher à l'écran).

argparse : (Optionnel) Pour créer une interface en ligne de commande propre (ex: python mon_script.py --chiffrer mon_fichier.pdf).

3. Structure du Fichier Chiffré

Pour pouvoir déchiffrer le fichier, nous devons stocker les informations non secrètes avec les données chiffrées. Un fichier chiffré (.enc) ressemblera à ceci :

[ 16 octets de SEL ] + [ 12 octets de NONCE ] + [ X octets de TAG GCM ] + [ Y octets de DONNÉES CHIFFRÉES ]

4. Plan d'Action : Fonction de Chiffrement

Voici les étapes pour la fonction chiffrer(fichier_entree, fichier_sortie, mot_de_passe) :

Lire les données : Lire le contenu complet du fichier PDF (fichier_entree) en mode binaire ('rb').

Générer le Sel : Créer un "Sel" aléatoire de 16 octets : salt = os.urandom(16).

Dériver la Clé :

Utiliser PBKDF2HMAC (de cryptography.hazmat.primitives.kdf.pbkdf2) avec :

Le mot_de_passe (encodé en UTF-8).

Le salt généré.

Un grand nombre d'itérations (ex: 480 000) pour ralentir les attaques par force brute.

Algorithme de hachage SHA256.

Cela vous donnera une clé de 32 octets (256 bits) parfaite pour AES.

Générer le Nonce : Créer un "Nonce" (ou IV) aléatoire de 12 octets : nonce = os.urandom(12).

Chiffrer (AES-GCM) :

Initialiser un objet AESGCM (de cryptography.hazmat.primitives.ciphers.aead) avec la clé dérivée.

Chiffrer les données du PDF en utilisant le nonce.

Le chiffrement produira deux choses : les donnees_chiffrees et un tag d'authentification (généralement 16 octets).

Écrire le Fichier de Sortie :

Ouvrir fichier_sortie en mode écriture binaire ('wb').

Écrire dans l'ordre : salt + nonce + tag + donnees_chiffrees.

5. Plan d'Action : Fonction de Déchiffrement

Voici les étapes pour la fonction dechiffrer(fichier_entree, fichier_sortie, mot_de_passe) :

Lire le Fichier Chiffré : Lire le contenu complet du fichier_entree (.enc) en mode binaire ('rb').

Extraire les Composants :

salt = 16 premiers octets.

nonce = 12 octets suivants.

tag = 16 octets suivants.

donnees_chiffrees = Tout le reste.

Dériver la Clé :

IMPORTANT : Utiliser exactement la même méthode PBKDF2 que pour le chiffrement :

Le mot_de_passe fourni par l'utilisateur.

Le salt lu depuis le fichier.

Le même nombre d'itérations (480 000) et SHA256.

Déchiffrer (AES-GCM) :

Initialiser un objet AESGCM avec la clé re-dérivée.

Tenter de déchiffrer les donnees_chiffrees en utilisant le nonce et le tag.

Gestion des erreurs : C'est la partie magique. Si le mot de passe est incorrect, la clé dérivée sera fausse. AES-GCM s'en rendra compte (le tag ne correspondra pas) et lèvera une exception InvalidTag (de cryptography.exceptions).

Vous devez intercepter cette exception (try...except InvalidTag:) et afficher "Erreur : Mot de passe incorrect ou fichier corrompu."

Écrire le Fichier de Sortie :

Si le déchiffrement réussit (aucune exception n'est levée), écrire les donnees_dechiffrees dans le fichier_sortie.

6. Interface Utilisateur (Main)

Utilisez argparse pour permettre à l'utilisateur de choisir entre --chiffrer (-c) et --dechiffrer (-d).

Demandez le fichier d'entrée et le fichier de sortie.

Utilisez getpass.getpass("Entrez votre mot de passe : ") pour demander le mot de passe de manière sécurisée. Pour le chiffrement, demandez-le deux fois pour confirmation.

Appelez la fonction appropriée (chiffrer ou dechiffrer) avec les bons arguments.

Ce plan vous donne une base extrêmement solide et sécurisée, bien au-delà de ce que la plupart des tutoriels simples proposent. Bon courage pour le codage !



#N.B

- Pour l'instant pas d'interface graphique stylée 