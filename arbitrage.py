def calculMise(coefarbitrage, cote1, cote2, mise_totale=100):
    # Calcul des mises proportionnelles pour obtenir un gain égal
    miseA = (mise_totale * (1/cote1)) / coefarbitrage
    miseB = (mise_totale * (1/cote2)) / coefarbitrage
    
    # Calcul du gain
    gain = (miseA * cote1) - (miseA + miseB)
    
    return miseA, miseB, gain

def possible(matchtab1, nomtableau1, matchtab2, nomtableau2, mise_totale=100):
    #Est-ce qu'ils sont à la même date ?
    datematch1 = matchtab1[4]
    datematch2 = matchtab2[4]
    if datematch1 != datematch2:
        return None
    
    # Première combinaison : cote1 match1 avec cote2 match2
    cotematch1e1 = float(str(matchtab1[1]).replace(",", "."))  # Force en str avant replace
    cotematch2e2 = float(str(matchtab2[3]).replace(",", "."))  # Force en str avant replace
    
    # pour debbug print(f"Arbitrage entre {matchtab1[0]} à {cotematch1e1} sur {nomtableau1} et {matchtab2[2]} à {cotematch2e2} sur {nomtableau2}")
    coefarbitrage = (1/cotematch1e1) + (1/cotematch2e2)
    if coefarbitrage < 1:
        miseA, miseB, gain = calculMise(coefarbitrage, cotematch1e1, cotematch2e2, mise_totale)
        return {
            "combinaison": f"Arbitrage entre {matchtab1[0]} à {cotematch1e1} sur {nomtableau1} et {matchtab2[2]} à {cotematch2e2} sur {nomtableau2}",
            "miseA": round(miseA, 2),
            "miseB": round(miseB, 2),
            "gain": round(gain, 2),
            "ROI": round((gain / mise_totale) * 100, 2)
        }
    
    # Deuxième combinaison : cote2 match1 avec cote1 match2
    cotematch2e1 = float(str(matchtab2[1]).replace(",", "."))
    cotematch1e2 = float(str(matchtab1[3]).replace(",", "."))
    
    coefarbitrage = (1/cotematch2e1) + (1/cotematch1e2)
    if coefarbitrage < 1:
        miseA, miseB, gain = calculMise(coefarbitrage, cotematch2e1, cotematch1e2, mise_totale)
        return {
            "combinaison": f"Arbitrage entre {matchtab1[2]} à {cotematch1e2} sur {nomtableau1} et {matchtab2[0]} à {cotematch2e1} sur {nomtableau2}",
            "miseA": round(miseA, 2),
            "miseB": round(miseB, 2),
            "gain": round(gain, 2),
            "ROI": round((gain / mise_totale) * 100, 2)
        }
    
    return None