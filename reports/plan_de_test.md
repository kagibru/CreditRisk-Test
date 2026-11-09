# PLAN DE TEST — CreditRisk-Test

**Projet :** Système IA de prédiction du risque de crédit  
**Version :** 1.1  
**Date :** 09 novembre 2026  
**Environnement :** Windows 11 / Python 3.13.2, GitHub Actions / Python 3.12

## 1. Objectif

Ce plan vise à vérifier la conformité fonctionnelle, la fiabilité technique, la robustesse et les performances d'une API de prédiction du risque de défaut de crédit.

Le système est développé avec FastAPI et scikit-learn. Il utilise une régression logistique entraînée sur des données synthétiques reproductibles.

## 2. Périmètre des tests

Les tests couvrent :

- La validation des données saisies par le demandeur.
- Les endpoints `/health`, `/model-info` et `/predict`.
- L'intégration entre validation, prétraitement et prédiction.
- La gestion des erreurs et des entrées invalides.
- La répétabilité des prédictions.
- La détection de dégradations simulées des métriques.
- Les performances locales de l'API et de l'inférence.
- La tenue en charge locale de `POST /predict` avec Locust (5, 20, 50 et 100 utilisateurs simulés).
- L'exécution automatisée des tests avec GitHub Actions.

## 3. Stratégie de test

Les tests automatisés sont développés avec Pytest et FastAPI TestClient. Les campagnes de charge HTTP sont réalisées séparément avec Locust sur un serveur Uvicorn local.

L'intégration continue repose sur GitHub Actions et comprend l'installation des dépendances, l'entraînement du modèle, Ruff, Pytest et la production des rapports de couverture.

## 4. Résultats observés

| Catégorie | Tests réussis | Échecs |
|---|---:|---:|
| Tests fonctionnels | 17 | 0 |
| Tests d'intégration | 11 | 0 |
| Tests de robustesse | 18 | 0 |
| Tests de non-régression | 7 | 0 |
| Tests de performance | 2 | 0 |
| Test des métriques du modèle | 1 | 0 |
| **Total** | **56** | **0** |

Couverture locale documentée : **91 %**. La dernière exécution Pytest sous WSL a confirmé **56 tests réussis**, sans échec (un avertissement de dépréciation non bloquant).

L'exécution GitHub Actions n° 42604536298 s'est terminée avec succès après correction des anomalies Ruff.

## 5. Performances observées

| Indicateur | Résultat |
|---|---:|
| Latence API moyenne | 4,75 ms |
| Latence API P95 | 5,53 ms |
| Débit séquentiel estimé | 210,60 requêtes/s |
| Latence inférence P95 | 0,36 ms |

Ces mesures ont été obtenues localement avec TestClient. Elles sont distinctes des essais de charge Locust ci-dessous.

### Campagnes de charge Locust

| Utilisateurs simulés | Requêtes | Échecs | Débit (req/s) | P95 (ms) |
|---:|---:|---:|---:|---:|
| 5 | 191 | 0 | 3,24 | 20 |
| 20 | 767 | 0 | 12,90 | 20 |
| 50 | 1 895 | 0 | 31,88 | 21 |
| 100 | 7 565 | 0 | 63,62 | 20 |
| **Total** | **10 418** | **0** | — | — |

Les débits et latences sont propres à chaque scénario : ils ne s’additionnent pas. Le P95 reste de 20 à 21 ms. Un maximum atypique de **1 818,21 ms** a été enregistré à 5 utilisateurs ; son origine n’est pas établie. Les essais ont été réalisés sur une machine locale avec un seul dossier synthétique, sans mesure d’endurance ni suivi des ressources système. Voir `reports/rapport_performance_creditrisk.md` et les fichiers `reports/load_*_stats.csv`. Ces essais ne constituent pas une qualification en conditions de production.

## 6. Critères de qualification

Les critères techniques retenus sont :

- Absence d'échec dans la suite de tests.
- Exécution réussie du workflow CI.
- Couverture du code supérieure ou égale à 80 %.
- Réponses HTTP conformes aux scénarios testés.
- Absence de valeurs de probabilité non finies dans les scénarios valides.
- Documentation des anomalies et des limites.
- Pour les essais de charge locaux, absence d’échec enregistré et P95 inférieur à 100 ms (seuils pédagogiques proposés, non contractuels).

Ces critères techniques ne suffisent pas à autoriser l'utilisation réelle du modèle pour des décisions de crédit.

## 7. Limites

Le modèle utilise des données synthétiques. Son rappel de référence est de 14,65 % et son F1-score de 24,73 %.

Les tests de non-régression actuels vérifient la détection de dégradations simulées, mais ne recalculent pas encore les métriques d'une nouvelle version sur un jeu de validation figé.

Aucune validation sur des données réelles représentatives, ni analyse complète des biais, de la calibration ou de la dérive des données, n'a été effectuée. Les essais Locust ne couvrent ni l’endurance, ni les charges plus élevées, ni une infrastructure représentative de production.

## 8. Conclusion

Le système satisfait les contrôles techniques automatisés exécutés à ce stade.

Il est qualifié pour une démonstration pédagogique, mais **n'est pas qualifié pour une utilisation en production dans une institution financière**.