# MATRICE DE TRAÇABILITÉ — CreditRisk-Test

| ID | Exigence vérifiée | Test ou preuve | Résultat |
|---|---|---|---|
| EX-01 | Disponibilité de l'API | `test_health` | Réussi |
| EX-02 | Informations du modèle | `test_model_info` | Réussi |
| EX-03 | Prédiction valide | `test_prediction_valide` | Réussi |
| EX-04 | Rejet des valeurs incorrectes | `test_entrees_invalides` | Réussi |
| EX-05 | Contrôle des champs obligatoires | `test_champ_obligatoire_absent` | Réussi |
| EX-06 | Contrôle des champs supplémentaires | `test_champ_supplementaire` | Réussi |
| EX-07 | Gestion du JSON mal formé | `test_json_mal_forme` | Réussi |
| EX-08 | Cohérence des dimensions | `test_dimensions_preprocessing` | Réussi |
| EX-09 | Cohérence API et modèle | `test_prediction_directe_et_api` | Réussi |
| EX-10 | Gestion du modèle indisponible | `test_modele_indisponible_prediction` | Réussi |
| EX-11 | Gestion des erreurs internes | `test_erreur_prediction_interne` | Réussi |
| EX-12 | Reproductibilité des prédictions | `test_prediction_repetable` | Réussi |
| EX-13 | Contrôle de la baseline | `test_baseline_valide` | Réussi |
| EX-14 | Détection d'une régression simulée | `test_detection_regression_recall` et `test_detection_regression_f1` | Réussi |
| EX-15 | Mesure des performances API | `test_performance_api` | Réussi |
| EX-16 | Mesure des performances d'inférence | `test_performance_inference` | Réussi |
| EX-17 | Exécution automatisée | GitHub Actions, run 42604536298 | Réussi |
| EX-18 | Couverture du code | Rapport pytest-cov | 91 % |
| EX-19 | Comparaison réelle avec une baseline | À implémenter | Non vérifié |
| EX-20 | Tests sous charge concurrente | Locust : `reports/load_5_stats.csv`, `load_20_stats.csv`, `load_50_stats.csv`, `load_100_stats.csv` ; `reports/rapport_performance_creditrisk.md` | Réussi pour les scénarios locaux : 10 418 requêtes, 0 échec, P95 de 20 à 21 ms |

**Bilan :** 19 exigences disposent d’une preuve de vérification ; EX-19 reste non vérifiée. La couverture de 91 % correspond au résultat documenté. Les tests de charge sont limités aux scénarios locaux décrits dans le rapport de performance.

**Note :** cette matrice relie les exigences techniques retenues aux tests réalisés. Elle devra être confrontée à l'énoncé complet avant la remise définitive.