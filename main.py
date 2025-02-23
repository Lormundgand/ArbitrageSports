import sys
import logging
import winamax
import betclic
import arbitrage

sys.stdout.reconfigure(encoding='utf-8')
# On fait un gros caca et on retire le logging pour les perfs
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
"""
Fonctionnement du code:
1. Les fichiers Bookmakers crééent chacun un dictionnaire xxx_games quand on les import, pour lesquels on associe 
    aux clés des tableaux sous la forme [equipe1, coteequipe1, equipe2, coteequipe2, date, sport]. 
    
2. Une fois chacun des dictionnaires récupérés, il faut les parcourir et comparer. 
    arbitrage.possible fonctionne super bien. Claude.ai est le goat. Il ne reste qu'à ajuster au bon format de tableaux que l'on utilisera puis a lui faire parcourir les tableaux des bookmakers.
"""

#####################################################################
#crawling de betclic
betclic_games = {}
urls_betclic = [ "https://www.betclic.fr/mma-s23"
      ,"https://www.betclic.fr/boxe-s16"
      ,"https://www.betclic.fr/basketball-s4"
      ]
for url in urls_betclic:
    sport = url.split('/')[-1].split('-')[0] #prend le sport (basketball, boxe, mma)
    results = betclic.scrape_betclic(url)
    betclic_games[sport] = results
    #Pour print les matchs et cotes
    # print(" ")
    # for element in results:
    #     print(element)
print("betclic crawled")
print(len(betclic_games["mma"]))

#crawling de winamax
winamax_games = {}
sports_winamax = {
    "boxe": "https://www.winamax.fr/paris-sportifs/sports/10",
    "mma": "https://www.winamax.fr/paris-sportifs/sports/117",
    "basket": "https://www.winamax.fr/paris-sportifs/sports/2"
}
for sport, url in sports_winamax.items():
    winamax_games[sport] = winamax.getGames(url, sport)
print("winamax crawled")
print(len(winamax_games["mma"]))



#####################################################################
#arbitrage
def comparer_winamax_betclic(winamax_games, betclic_games):
    """
    Compare tous les matchs entre Winamax et Betclic pour trouver les opportunités d'arbitrage.
    
    Args:
        winamax_games: Dictionnaire des matchs Winamax
        betclic_games: Dictionnaire des matchs Betclic
    
    Returns:
        Liste des opportunités d'arbitrage trouvées
    """
    opportunities = []
    
    # Parcours de tous les matchs Winamax
    betclic_dict = {}
    nb_comparaisons = 0

    for match_id_betclic, match_list in betclic_games.items():
        for match in match_list:
            key = (match[0], match[2], match[4])  # (équipe1, équipe2, date)
            betclic_dict[key] = match  # Associe chaque match à sa clé unique

    # Parcours des matchs de Winamax
    for match_id_winamax, match_list in winamax_games.items():
        for match in match_list:
            key = (match[0], match[2], match[4])  # Même clé unique

            if key in betclic_dict:  # Vérifie si un match correspondant 
                nb_comparaisons += 1
                opportunity = arbitrage.possible(match, "Winamax", betclic_dict[key], "Betclic")
            
                # Si une opportunité est trouvée, on l'ajoute à la liste
                if opportunity:
                    opportunity['match_ids'] = (match_id_winamax, match_id_betclic)
                    opportunities.append(opportunity)
    
    print(f"nb_comparaisons : {nb_comparaisons}")
    return opportunities

# Chercher les opportunités
opportunities = comparer_winamax_betclic(winamax_games, betclic_games)
    
# Afficher les résultats
print(f"Nombre d'opportunités trouvées : {len(opportunities)}")
for opp in opportunities:
    print(f"Opportunité: {opp}")
"""
On peut arbitrer, voici les deux cas de figure.
Exemple winamax vs betclic où Arbitrage possible :
"""


winamaxpos = ["brest", 2.10 , "nantes", 1.9, 10/20/2025, "basketball"]
betclicpos = ["brest", 1.85, "nantes", 2.2, 10/20/2025, "basketball"]
#On devrait gagner 7$43 en mettant 51.16 sur brest et 48.84 sur nantes
resultat=(arbitrage.possible(winamaxpos, "winamax", betclicpos, "betclic"))
# if resultat:
#     print(f"Opportunité trouvée !")
#     print(f"Combinaison : {resultat['combinaison']}")
#     print(f"Mise A : {resultat['miseA']}€")
#     print(f"Mise B : {resultat['miseB']}€")
#     print(f"Gain potentiel : {resultat['gain']}€")
#     print(f"ROI : {resultat['ROI']}%")
# print(resultat)

"""
Exemple winamax vs betclic où Arbitrage impossible""" 
winamaximpos = ["brest", 1.9 , "nantes", 2, 10/20/2025, "basketball"]
betclicimpos = ["brest", 1.85, "nantes", 2.05, 10/20/2025, "basketball"]
#on devrait perdre dans tous les cas
resultat=arbitrage.possible(winamaximpos, "winamax", betclicimpos, "betclic")
# print(resultat)

