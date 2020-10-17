import copy

class Graphe:
    L = []
    P = []
    nombre_sommets = None
    a_cycle_absorbant = False
    floyd_done = False

    def __init__(self, path):
        lines = []
        with open(path, "r") as file:  # On récupère les lignes du fichier pour pouvoir créer le graphe
            for line in file.readlines():
                lines.append(line.strip("\n"))

        self.nombre_sommets = int(lines.pop(0))
        for i in range(0, self.nombre_sommets):  # On crée la matrice vide que l'on viendra remplir plus tard
            self.L.append([])
            self.P.append([])
            for n in range(0, self.nombre_sommets):
                if n == i:
                    self.L[-1].append(0)
                    self.P[-1].append(i+1)
                else:
                    self.L[-1].append(None)
                    self.P[-1].append(None)

        lines.pop(0)  # On se débarasse de la ligne contenant le nombre d'arcs car elle ne nous importe pas

        try:
            for line in lines:
                line = line.split(" ")
                line = list(map(int, line))
                self.L[line[0]-1][line[1]-1] = line[2]  # On entre dans la matrice d'adjacence chaque arête du fichier
                self.P[line[0]-1][line[1]-1] = line[0]  # On entre aussi la matrice des prédécesseurs
        except IndexError:
            print("Le nombre de sommets et les bornes d'une des arêtes ne correspondent pas.")
        except TypeError:
            print("Le fichier source est mal formatté (les noms des sommets doivent être des nombres).")

    def afficher_adja(self):
        """
        Affiche la table L à l'aide de self.afficher
        :return:
        """
        print("Matrice d'adjascence")
        self.afficher(self.L)

    def afficher_pred(self):
        """
        Affiche la table P à l'aide de self.afficher
        :return:
        """
        print("Matrice des prédécésseurs")
        self.afficher(self.P)

    def afficher(self, table):
        """
        Affiche la table passée en paramètre de façon bien formatée
        :param table:
        :return:
        """

        properly_formated_array = copy.deepcopy(table)
        # On insère le numéro du sommet dans chaque ligne
        # Pour cela on insère le numéro du sommet auquel correspond la ligne en première position de chaque ligne
        i = 0
        for line in properly_formated_array:
            for index, cell in enumerate(line):  # On en profite pour remplacer les "None" par un symbole infini
                if cell is None:
                    properly_formated_array[i][index] = "∞"
            line.insert(0, i+1)
            i += 1
        # Puis on crée une ligne tout en haut pour les numéros de colonnes
        properly_formated_array.insert(0, [i for i in range(0, self.nombre_sommets+1)])
        properly_formated_array[0][0] = ""  # On supprime le premier élément de cette ligne car c'est la case inutile de la légende

        stringed_values = [[str(e) for e in row] for row in properly_formated_array]  # On converti chaque ligne en string pour pouvoir récupérer la longueur des nombres plus tard
        long_max = [max(map(len, col)) for col in zip(*stringed_values)]  # On récupère la longueur maximale de chaque colonne
        format_param = ' | '.join(f'{{:{x}}}' for x in long_max)  # On prépare les paramètres des chaines de formats pour l'étape suivante, et on insère les séparateurs de colonnes
        table = [format_param.format(*row).replace("|","║",1) for row in stringed_values]  # On insère les valeurs entourées du bon nombre d'espaces, et on remplace le premier "|" par un "║"
        table.insert(1, "".join(["=" for _ in range(0, len(table[0]))]))  # On insère une ligne de "=" pour la séparation
        table[1] = table[1][:long_max[0]+1] + "╬" + table[1][long_max[0]+2:]  # On termine la construction des barres
        print('\n'.join(table))  # On affiche les lignes

    def floydWarshall(self, display=True):
        """
        Éxécute l'algorithme de Floyd-Warshall sur le graphe
        :return:
        """

        for k in range(0, self.nombre_sommets):
            if display:
                print("\nK =", k)
                self.afficher_adja()
                self.afficher_pred()
            for i in range(0, self.nombre_sommets):
                for j in range(0, self.nombre_sommets):
                    if self.L[i][k] is None or self.L[k][j] is None:  # Si l'un des chemins par lesquels on veut passer n'existe pas, on passe
                        continue
                    elif self.L[i][j] is None:  # L'arête n'existe pas, mais on a trouvé un autre chemin, alors on ajoute le nouveau chemin
                        self.L[i][j] = self.L[i][k] + self.L[k][j]
                        self.P[i][j] = self.P[k][j]
                    elif self.L[i][k] + self.L[k][j] < self.L[i][j]:  # Si on a bien deux chemins à comparer, alors on procède comme d'habitude
                        self.L[i][j] = self.L[i][k] + self.L[k][j]
                        self.P[i][j] = self.P[k][j]

                    if i == j and self.L[i][j] < 0:
                        self.a_cycle_absorbant = True  # Le seul moyen d'améliorer le trajet d'un sommet vers lui-même est via un cycle absorbant
                        return
        self.floyd_done = True

    def plusCourtChemin(self, src, dest):
        """
        Renvoie la liste des sommets du plus court chemin de src à dest.
        :return:
        """

        if not self.floyd_done:  # Si on a pas encore fait l'algorithme, on le fait sans afficher ses étapes
            self.floydWarshall(False)

        if self.P[src-1][dest-1] is None or self.a_cycle_absorbant:
            return []  # Si on a pas de point de départ au chemin de src vers dest alors on peut renvoyer directement un ensemble vide. Idem s'il y a des cycles absorbants
        else:
            chemin = [dest]
            while src != dest:
                # On n'oublie pas de convertir src et dest qui sont dans [1,n] pour les humains vers [0,n-1] pour l'ordinateur lors de la lecture
                dest = self.P[src-1][dest-1]  # On remonte les prédécesseurs jusqu'à retomber sur le sommet initial
                chemin.append(dest)  # On devrait ajouter le prédécesseur au début puisqu'on part de la fin, cependant on inversera juste la liste à la fin de la boucle
            chemin.reverse()  # Plus efficace que d'ajouter au début de la liste à chaque tour de boucle
            return chemin





# Interface CLI
print("Bienvenue dans le projet de Théorie des Graphes d'Enzo Filangi, Adrien Girard et Josian Boyaram")
while True:
    while True:
        nbr_graphe = input("Entrez le numéro du graphe voulu: \n")
        try:  # on verifie que l'utilisateur a bien rentré un numero existant
            graphe = Graphe("graphes/test-" + nbr_graphe + ".txt")
            break
        except:
            print("Ce graphe n'existe pas, veuillez entrer un autre numéro.")

    print(f"\n\n### Le graphe {nbr_graphe} a bien été chargé ###\n")
    graphe.afficher_adja()
    graphe.afficher_pred()
    print("\n\n### Algorithme de Floyd-Warshall ###\n")
    graphe.floydWarshall()
    if graphe.a_cycle_absorbant:
        print("\n\nImpossible de mener à bien l'algorithme car le graphe contient des cycles absorbants.")
    else:
        print("\n\nRésultats finaux :\n")
        graphe.afficher_adja()
        graphe.afficher_pred()
        print("\n\nChemin le plus court :\n")
        while True:
            while True:  # Validation des entrées utilisateur
                try:
                    src = int(input("Sommet source :\n"))
                    dest = int(input("Somme destination : \n"))
                    assert 0 < src <= graphe.nombre_sommets and 0 < dest <= graphe.nombre_sommets
                    break
                except ValueError:
                    print("Veuillez entrer des nombres entiers.")
                except AssertionError:
                    print("Veuillez sélectionner des sommets existants.")
            print(f"\nPlus court chemin de {src} à {dest}:\n")
            print(graphe.plusCourtChemin(src, dest))
            if input("Voulez vous consulter un chemin différent ? (o/n)\n").lower() not in ["o", "oui"]:
                break
            else:
                print("\n### Autre chemin ###\n")

    if input("Voulez vous traiter un autre graphe ? (o/n)\n").lower() not in ["o", "oui"]:
        break
    else:
        print("\n\n#################################\n\n")

