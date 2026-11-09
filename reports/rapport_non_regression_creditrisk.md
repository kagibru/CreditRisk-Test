# Rapport de tests de non-régression — CreditRisk-Test

**Date :** 9 novembre 2026  
**Environnement :** Windows, Python 3.13.2, Pytest 9.2.0  
**Commande :** `python -m pytest tests/test_model_metrics.py -v -s`  
**Résultat :** 1 test réussi en 4,32 secondes.

## 1. Objectif et périmètre

Vérifier automatiquement que les métriques du modèle chargé par `get_model()` ne sont pas inférieures aux métriques de référence au-delà d'une tolérance absolue de 0,02. Les métriques surveillées sont le rappel (recall) et le F1-score.

## 2. Méthode

Le test `test_model_metrics_against_baseline` charge `reports/baseline.json`, régénère un jeu de validation synthétique avec une graine fixe (`seed=42`), puis évalue le modèle courant sur 1 000 observations. Les prédictions sont comparées aux étiquettes synthétiques avec `recall_score` et `f1_score` de scikit-learn (`zero_division=0`).

Les seuils de conformité sont :

- `recall_actuel >= recall_baseline - 0.02`
- `f1_actuel >= f1_baseline - 0.02`

Cette tolérance est un **choix de test** ; elle ne constitue pas une justification métier de l'acceptabilité du risque.

## 3. Résultats

| Indicateur | Référence | Courant (affiché par le test) | Seuil minimal | Décision |
|---|---:|---:|---:|---|
| Recall | 0,1464968153 | 0,1465 | 0,1264968153 | Conforme |
| F1-score | 0,2473118280 | 0,2473 | 0,2273118280 | Conforme |

**Trace d'exécution communiquée :**

```text
Recall actuel : 0.1465
Recall baseline : 0.1465
F1 actuel : 0.2473
F1 baseline : 0.2473
PASSED
1 passed in 4.32s
```

Le fichier `reports/current_metrics.json` transmis contient les mêmes valeurs que la référence, mais le test montré recalcule directement les métriques du modèle courant : il ne lit pas `current_metrics.json`.

## 4. Analyse et limites

**Conclusion du contrôle :** aucune dégradation au-delà de la tolérance définie n'a été détectée lors de cette exécution.

**Limites :**

1. Les données de validation sont **synthétiques** ; elles ne démontrent pas la performance sur des demandes de crédit réelles.
2. Le test ne démontre pas à lui seul qu'une **nouvelle version distincte** du modèle a été déployée ou comparée : les identifiants/empreintes des deux artefacts ne sont pas consignés.
3. Les valeurs courantes sont affichées à quatre décimales ; l'égalité exacte avec la baseline ne peut pas être déduite de cet affichage seul, même si les fichiers JSON transmis sont identiques.
4. Le rappel de référence (~14,65 %) est faible ; la conformité à une baseline faible n'établit pas l'aptitude à une utilisation décisionnelle en production.
5. Le test fourni ne vérifie pas explicitement la cohérence du rechargement du modèle ; cette exigence doit être démontrée par une preuve distincte si elle figure dans l'énoncé.

## 5. Décision et recommandations

**Décision :** contrôle de non-régression **réussi**, avec réserves concernant la représentativité des données et l'absence de preuve d'une comparaison entre deux versions distinctes.

**Actions recommandées :**

- Conserver les versions/empreintes des artefacts modèle et leur historique de métriques.
- Évaluer une version candidate distincte sur le même jeu de validation figé avant déploiement.
- Documenter le choix des seuils en fonction du coût métier des faux négatifs.
- Compléter par une évaluation sur données réelles, une analyse par sous-populations et un contrôle de calibration.
- Vérifier et consigner séparément le comportement après rechargement du modèle.

## 6. Traçabilité

- **Exigence concernée :** EX07 du sujet (absence de dégradation des critères critiques), et EX-19 de l'ancienne matrice projet.
- **Test :** `tests/test_model_metrics.py::test_model_metrics_against_baseline`.
- **Référence :** `reports/baseline.json`.
- **Données métriques courantes enregistrées :** `reports/current_metrics.json`.
- **Preuve d'exécution :** sortie Pytest du 9 novembre 2026 communiquée dans la conversation.
