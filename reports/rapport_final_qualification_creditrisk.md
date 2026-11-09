# RAPPORT FINAL DE QUALIFICATION — CreditRisk-Test

**Projet :** API de prédiction du risque de défaut de crédit  
**Version du rapport :** 1.0 — 9 novembre 2026  
**Cadre :** projet pédagogique de tests logiciels  
**Décision :** qualification technique pour démonstration pédagogique uniquement, avec réserves

## 1. Synthèse exécutive

La campagne de qualification a évalué les fonctions de l'API, la validation des entrées, l'intégration du pipeline de prédiction, la robustesse, la non-régression, les performances et l'automatisation des contrôles. La dernière exécution communiquée de Pytest sous WSL a abouti à **56 tests réussis sur 56**, sans échec et avec un avertissement de dépréciation non bloquant. La couverture globale **documentée** est de **91 %**, au-dessus du seuil pédagogique retenu de 80 %. Une exécution GitHub Actions a également été signalée comme réussie.

Quatre campagnes de charge Locust, à 5, 20, 50 et 100 utilisateurs simulés, totalisent **10 418 requêtes**, sans échec enregistré. Le P95 est compris entre **20 et 21 ms** selon le scénario. Ces résultats attestent d'un comportement satisfaisant **dans l'environnement local et avec les entrées testées** ; ils ne prouvent ni l'aptitude à la production ni la qualité prédictive du modèle en contexte réel.

**Avis : favorable pour une démonstration pédagogique ; défavorable à une mise en production ou à l'utilisation pour des décisions financières réelles.**

## 2. Système évalué et périmètre

Le système est une API développée avec **FastAPI** et **scikit-learn**, reposant sur une régression logistique entraînée sur des **données synthétiques reproductibles**. Les endpoints examinés sont `/health`, `/model-info` et `/predict`.

Le périmètre couvre : validation des champs et des types ; gestion des requêtes invalides ; prétraitement et cohérence des dimensions ; appel au modèle et gestion de ses indisponibilités ; reproductibilité ; contrôle des métriques de référence ; détection de régressions simulées ; mesures de latence et campagnes de charge ; intégration continue.

Le périmètre ne couvre pas la validation métier sur une population réelle, une analyse complète d'équité, la calibration, la dérive, la sécurité opérationnelle ni les essais d'endurance.

## 3. Environnement, méthode et preuves

| Domaine | Outils / environnement | Preuves documentées |
|---|---|---|
| Tests automatisés | Pytest, FastAPI TestClient | Exécution de 56 tests ; fichiers XML sous `reports/` |
| Couverture | pytest-cov | `reports/coverage.xml` ; couverture globale documentée de 91 % |
| Intégration continue | GitHub Actions, Python 3.12, Ruff | Exécution n° 42604536298 signalée réussie ; `reports/github-actions/` |
| Environnement local | Windows 11, Python 3.13.2 ; contrôle final sous WSL, Python 3.11.9 | Sortie terminal Pytest communiquée |
| Charge HTTP | Locust, Uvicorn local, endpoint `POST /predict` | `reports/load_*_stats.csv` et `reports/rapport_performance_creditrisk.md` |
| Traçabilité | Matrice EX-01 à EX-20 | `reports/matrice_tracabilite.md` |

Les mesures TestClient et les mesures Locust sont deux campagnes distinctes et ne doivent pas être comparées comme si elles reposaient sur un protocole identique.

## 4. Résultats des tests automatisés

| Catégorie | Tests réussis | Échecs |
|---|---:|---:|
| Fonctionnels | 17 | 0 |
| Intégration | 11 | 0 |
| Robustesse | 18 | 0 |
| Non-régression | 7 | 0 |
| Performance automatisée | 2 | 0 |
| Métriques du modèle | 1 | 0 |
| **Total** | **56** | **0** |

Ce décompte est celui du plan de test actualisé. La dernière exécution communiquée confirme le total de 56 tests réussis. Un avertissement `StarletteDeprecationWarning` concernant l'utilisation de `httpx` avec `starlette.testclient` a été observé ; il n'a pas provoqué d'échec.

**Couverture :** 91 % documentés. Ce taux reflète l'exécution de code par les tests, pas la preuve que tous les comportements ou risques métier ont été vérifiés. La couverture du prétraitement comporte notamment une branche de levée d'exception non couverte lors des vérifications précédentes.

## 5. Résultats de performance

### 5.1 Mesures locales avec TestClient

| Indicateur | Mesure |
|---|---:|
| Latence API moyenne | 4,75 ms |
| Latence API P95 | 5,53 ms |
| Débit séquentiel estimé | 210,60 requêtes/s |
| Latence d'inférence P95 | 0,36 ms |

Ces résultats proviennent de mesures locales et ne représentent pas un débit soutenable en production.

### 5.2 Charge HTTP avec Locust

| Utilisateurs simulés | Requêtes | Échecs | Débit (req/s) | P95 (ms) | P99 (ms) |
|---:|---:|---:|---:|---:|---:|
| 5 | 191 | 0 | 3,24 | 20 | 810 |
| 20 | 767 | 0 | 12,90 | 20 | 24 |
| 50 | 1 895 | 0 | 31,88 | 21 | 31 |
| 100 | 7 565 | 0 | 63,62 | 20 | 30 |
| **Total** | **10 418** | **0** | — | — | — |

Les scénarios utilisaient un temps d'attente aléatoire de 1 à 2 secondes entre requêtes par utilisateur. Les essais de 5, 20 et 50 utilisateurs étaient programmés pour 60 secondes, celui de 100 pour 120 secondes. Les taux de requêtes sont propres à chaque scénario et ne s'additionnent pas.

Le P95 demeure stable entre 20 et 21 ms, mais un maximum atypique de **1 818,21 ms** a été observé à cinq utilisateurs, avec un P99 de 810 ms. Sa cause n'est pas établie. Aucun échec n'a été enregistré dans les exports, sans que cela garantisse la fiabilité sur des charges ou durées supérieures.

Les seuils de **0 % d'échec** et de **P95 inférieur à 100 ms** sont des critères pédagogiques proposés, et non des exigences contractuelles confirmées.

## 6. Traçabilité des exigences

La matrice comporte **20 exigences techniques**. **19** disposent d'une preuve de vérification dans les documents fournis. L'exigence **EX-20** (charge concurrente) est désormais documentée par les quatre campagnes Locust. L'exigence **EX-19** (comparaison réelle d'une nouvelle version du modèle avec la baseline sur un jeu de validation figé) demeure **non vérifiée**.

Ce bilan ne constitue pas une attestation de conformité à l'énoncé du professeur : la confrontation finale avec l'énoncé complet reste à effectuer.

## 7. Anomalies, risques et réserves

| Point | Constat | Conséquence / suite |
|---|---|---|
| Avertissement de dépendance | Dépréciation Starlette/TestClient | Non bloquant ; surveiller les évolutions de dépendances |
| Pic de latence | Maximum de 1 818,21 ms à 5 utilisateurs | Investiguer la reproductibilité et la cause avant toute conclusion opérationnelle |
| Régression réelle EX-19 | Non implémentée / non vérifiée dans la matrice | Compléter si exigé ; ne pas la déclarer couverte |
| Validation prédictive | Données synthétiques ; rappel de référence 14,65 %, F1-score 24,73 % | Performances prédictives insuffisamment établies pour l'usage bancaire réel |
| Charge | Machine locale, un dossier synthétique, absence de suivi CPU/RAM et d'endurance | Généralisation à la production impossible |
| Couverture | 91 % globale documentée ; certaines branches non couvertes | Une couverture élevée ne supprime pas les risques résiduels |

Les journaux de CI et les résultats XML doivent être conservés avec le dossier de remise pour permettre la vérification des preuves.

## 8. Décision de qualification

| Critère pédagogique | Résultat | Appréciation |
|---|---|---|
| Suite Pytest sans échec | 56/56 | Satisfait |
| Couverture globale ≥ 80 % | 91 % documentés | Satisfait |
| CI signalée réussie | Run n° 42604536298 | Satisfait selon les preuves documentées |
| Tests de charge locaux sans échec | 10 418 requêtes, 0 échec | Satisfait pour les scénarios exécutés |
| P95 Locust inférieur à 100 ms | 20–21 ms | Satisfait pour les scénarios exécutés |
| Comparaison réelle à la baseline | EX-19 non vérifiée | Réserve ouverte |
| Aptitude à la production bancaire | Non évaluée sur données réelles ni infrastructure représentative | Non qualifiée |

**Décision finale :** le système est **qualifié pour une démonstration pédagogique sous réserve des limites exposées**. Il **n'est pas qualifié pour une utilisation en production dans une institution financière**. Les résultats de test technique ne constituent pas une validation de la pertinence des décisions de crédit.

## 9. Recommandations et clôture

1. Confronter la matrice et les livrables à l'énoncé intégral du professeur avant remise.
2. Conserver les fichiers XML, CSV, graphiques et journaux CI dans `reports/` avec une nomenclature stable.
3. Ne pas présenter EX-19 comme réalisée ; si nécessaire, comparer les métriques d'une nouvelle version sur un jeu de validation figé.
4. Pour tout prolongement opérationnel, compléter les essais d'endurance, l'observabilité système, la variété des entrées, l'analyse des biais et la validation sur données représentatives.
5. Investiguer le pic de latence observé à cinq utilisateurs.

### Références internes

- `reports/plan_de_test.md` — version 1.1.
- `reports/matrice_tracabilite.md` — exigences EX-01 à EX-20.
- `reports/rapport_performance_creditrisk.md` — protocole et analyse Locust.
- `reports/load_5_stats.csv`, `load_20_stats.csv`, `load_50_stats.csv`, `load_100_stats.csv` — mesures agrégées.
- `reports/coverage.xml` et rapports XML Pytest — preuves automatisées.
- `reports/github-actions/` — éléments d'exécution CI.

*Rapport établi à partir des résultats et documents communiqués. Les métriques n'ont pas été recalculées indépendamment à partir de l'ensemble des artefacts bruts.*
