# PLAN DE TEST — CreditRisk-Test

**Projet :** Système IA de prédiction du risque de crédit  
**Version :** 1.0  
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
- L'exécution automatisée des tests avec GitHub Actions.

## 3. Stratégie de test

Les tests sont développés avec Pytest et FastAPI TestClient.

L'intégration continue repose sur GitHub Actions et comprend l'installation des dépendances, l'entraînement du modèle, Ruff, Pytest et la production des rapports de couverture.

## 4. Résultats observés

| Catégorie | Tests réussis | Échecs |
|---|---:|---:|
| Tests fonctionnels | 17 | 0 |
| Tests d'intégration | 11 | 0 |
| Tests de robustesse | 18 | 0 |
| Tests de non-régression | 7 | 0 |
| Tests de performance | 2 | 0 |
| **Total** | **55** | **0** |

Couverture locale mesurée : **91 %**.

L'exécution GitHub Actions n° 42604536298 s'est terminée avec succès après correction des anomalies Ruff.

## 5. Performances observées

| Indicateur | Résultat |
|---|---:|
| Latence API moyenne | 4,75 ms |
| Latence API P95 | 5,53 ms |
| Débit séquentiel estimé | 210,60 requêtes/s |
| Latence inférence P95 | 0,36 ms |

Ces mesures ont été obtenues localement avec TestClient. Elles ne constituent pas un test de charge en conditions de production.

## 6. Critères de qualification

Les critères techniques retenus sont :

- Absence d'échec dans la suite de tests.
- Exécution réussie du workflow CI.
- Couverture du code supérieure ou égale à 80 %.
- Réponses HTTP conformes aux scénarios testés.
- Absence de valeurs de probabilité non finies dans les scénarios valides.
- Documentation des anomalies et des limites.

Ces critères techniques ne suffisent pas à autoriser l'utilisation réelle du modèle pour des décisions de crédit.

## 7. Limites

Le modèle utilise des données synthétiques. Son rappel de référence est de 14,65 % et son F1-score de 24,73 %.

Les tests de non-régression actuels vérifient la détection de dégradations simulées, mais ne recalculent pas encore les métriques d'une nouvelle version sur un jeu de validation figé.

Aucune validation sur des données réelles représentatives, ni analyse complète des biais, de la calibration ou de la dérive des données, n'a été effectuée.

## 8. Conclusion

Le système satisfait les contrôles techniques automatisés exécutés à ce stade.

Il est qualifié pour une démonstration pédagogique, mais **n'est pas qualifié pour une utilisation en production dans une institution financière**.