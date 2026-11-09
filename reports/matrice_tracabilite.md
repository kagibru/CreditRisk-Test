# MATRICE DE TRAÇABILITÉ ENRICHIE — CreditRisk-Test

**Version :** 1.2 — 09 novembre 2026  
**Référence :** Évaluation Formative 2, Partie I, activité 1  
**Périmètre :** Prototype pédagogique FastAPI / scikit-learn, données synthétiques

## 1. Convention de lecture

Les identifiants **EX-01 à EX-20** conservent leur sens dans la matrice initiale du projet. Les identifiants **Sujet EX01 à EX07** désignent les sept exigences obligatoires du professeur : ils ne sont **pas équivalents** aux identifiants du projet. Les priorités et niveaux de risque ci-dessous constituent une **analyse proposée** pour ce prototype, non une notation fournie par l'enseignant.

- **P1 — Critique :** risque d'une réponse incorrecte, d'une donnée invalide acceptée ou d'une régression non détectée.
- **P2 — Élevée :** risque d'indisponibilité, d'incohérence ou de dégradation significative du service.
- **P3 — Normale :** traçabilité, observabilité ou qualité documentaire.
- **Vérifié :** un test ou une preuve a été rapporté comme réussi ; **Partiel :** une partie de l'exigence reste à démontrer ; **Non vérifié :** preuve insuffisante.

## 2. Correspondance des sept exigences obligatoires du professeur

| Exigence du sujet | Attente du professeur | Exigence(s) du projet | État de la preuve |
|---|---|---|---|
| Sujet EX01 | Âge dans l'intervalle autorisé ; rejet hors limites | EX-04 | Tests d'entrées invalides / limites rapportés réussis |
| Sujet EX02 | Revenu numérique et positif ; erreur contrôlée sinon | EX-04 | Tests `revenu_mensuel` rapportés réussis |
| Sujet EX03 | Durée entière valide ; rejet sinon | EX-04 | Test de durée non entière rapporté réussi |
| Sujet EX04 | Probabilité de prédiction comprise entre 0 et 1 | EX-03 | `test_prediction_valide` ; `test_probabilite_finie` |
| Sujet EX05 | Modèle disponible ; indisponibilité signalée correctement | EX-10 | `test_modele_indisponible_prediction` |
| Sujet EX06 | Entrée incomplète ; réponse d'erreur appropriée | EX-05 | `test_champ_obligatoire_absent` |
| Sujet EX07 | Nouvelle version sans dégradation des critères critiques | EX-13, EX-14, EX-19 | **Partiel** : baseline et dégradations simulées testées ; comparaison réelle de versions non démontrée |

Les exigences complémentaires du projet (au-delà des sept du sujet) comprennent notamment EX-01, EX-02, EX-06, EX-07, EX-08, EX-09, EX-11 et EX-12 : le minimum de cinq exigences supplémentaires est donc dépassé.

## 3. Matrice détaillée des exigences et cas de test

**Précondition commune :** environnement Python et dépendances installés ; pour les scénarios nécessitant une prédiction, application et modèle de test accessibles, sauf lorsque l'indisponibilité est précisément simulée. Les codes HTTP exacts et les messages de réponse doivent être confirmés à partir des assertions de `tests/test_api.py` avant remise ; ils ne sont pas inventés dans cette matrice.

| ID projet | Exigence | Préconditions spécifiques | Données d'entrée / scénario | Résultat attendu | Test ou preuve | Risque en cas d'échec | Priorité | Statut |
|---|---|---|---|---|---|---|---|---|
| EX-01 | Disponibilité de l'API | Service démarré | `GET /health` | Réponse de disponibilité conforme au contrat | `test_health` | Panne non détectée | P2 | Vérifié |
| EX-02 | Informations du modèle | Modèle chargé | `GET /model-info` | Métadonnées de modèle conformes au contrat | `test_model_info` | Version de modèle mal identifiée | P2 | Vérifié |
| EX-03 | Prédiction valide (Sujet EX04) | Modèle disponible | Dossier valide : âge 35, revenu 250000, crédit 1000000, durée 12, ancienneté 4 | Réponse conforme ; probabilité finie dans [0, 1] | `test_prediction_valide`, `test_probabilite_finie` | Résultat numérique incohérent | P1 | Vérifié |
| EX-04 | Rejet des valeurs incorrectes (Sujet EX01–EX03) | Validation active | Âge négatif/hors limites ; revenu texte, nul ou négatif ; durée non entière ; montant nul ou négatif | Rejet contrôlé, sans prédiction trompeuse | `test_entrees_invalides`, `test_valeurs_hors_limites` | Données invalides acceptées | P1 | Vérifié |
| EX-05 | Champs obligatoires (Sujet EX06) | Schéma d'entrée défini | Retirer successivement un des cinq champs requis | Erreur de validation contrôlée | `test_champ_obligatoire_absent` | Prédiction sur dossier incomplet | P1 | Vérifié |
| EX-06 | Champs supplémentaires | Schéma d'entrée défini | Ajouter un champ non autorisé | Rejet conforme au contrat d'entrée | `test_champ_supplementaire` | Contrat API non respecté | P2 | Vérifié |
| EX-07 | JSON mal formé | Endpoint disponible | Corps de requête JSON syntaxiquement invalide | Réponse d'erreur contrôlée, sans trace sensible | `test_json_mal_forme` | Erreur serveur ou fuite technique | P2 | Vérifié |
| EX-08 | Dimensions du prétraitement | Fonction de transformation disponible | Dossier valide à cinq variables | Matrice numérique de forme attendue (1, 5) | `test_dimensions_preprocessing` | Incompatibilité avec le modèle | P1 | Vérifié |
| EX-09 | Cohérence API / modèle | Modèle et API disponibles | Même dossier envoyé directement et via l'API | Prédictions cohérentes selon le contrat | `test_prediction_directe_et_api` | Divergence entre couches | P1 | Vérifié |
| EX-10 | Indisponibilité du modèle (Sujet EX05) | Indisponibilité simulée | Requête de prédiction sans modèle chargé | Erreur contrôlée ; aucune fausse prédiction | `test_modele_indisponible_prediction` | Résultat trompeur ou panne non maîtrisée | P1 | Vérifié |
| EX-11 | Erreur interne de prédiction | Erreur du modèle simulée | Requête valide provoquant une exception interne | Gestion contrôlée, sans détail sensible exposé | `test_erreur_prediction_interne` | Fuite technique / interruption | P1 | Vérifié |
| EX-12 | Reproductibilité | Modèle et entrée inchangés | Répéter une même requête valide | Résultats identiques ou conformes à la tolérance prévue | `test_prediction_repetable` | Décisions incohérentes | P2 | Vérifié |
| EX-13 | Intégrité de la baseline (Sujet EX07) | `reports/baseline.json` présent | Charger et valider les métriques de référence | Référence disponible et structurée correctement | `test_baseline_valide` | Référence invalide pour les comparaisons | P1 | Vérifié |
| EX-14 | Détection de régressions simulées (Sujet EX07) | Baseline et seuils de contrôle disponibles | Injecter une baisse simulée du rappel ou du F1 | Le contrôle signale la dégradation | `test_detection_regression_recall`, `test_detection_regression_f1` | Dégradation non détectée | P1 | Vérifié pour simulation |
| EX-15 | Performance de l'API | Environnement local de mesure | Requêtes valides chronométrées | Latence et débit mesurés et documentés | `test_performance_api` ; rapport de performance | Lenteur non caractérisée | P2 | Vérifié |
| EX-16 | Performance de l'inférence | Modèle chargé | Inférences répétées chronométrées | Latence d'inférence et P95 mesurés | `test_performance_inference` | Goulot d'étranglement ignoré | P2 | Vérifié |
| EX-17 | Automatisation CI | Dépôt et workflow configurés | Exécution GitHub Actions sur code du projet | Workflow exécutant les contrôles et signalant les échecs | Run 42604536298 ; exports CI | Régressions non bloquées | P2 | Vérifié pour exécution réussie ; scénario d'échec volontaire à confirmer |
| EX-18 | Couverture du code | Suite Pytest exécutée avec pytest-cov | Exécution avec mesure de couverture | Rapport disponible ; seuil pédagogique ≥ 80 % | `coverage.xml` ; couverture annoncée 91 % | Zones non testées ignorées | P2 | Vérifié selon rapport existant |
| EX-19 | Comparaison réelle d'une nouvelle version à la baseline (Sujet EX07) | Jeu de validation figé ; deux versions et tolérances documentées | Calculer rappel/F1 sur les mêmes observations pour les deux versions | Comparaison chiffrée et décision selon les seuils prédéfinis | **Rapport comparatif à produire** | Régression réelle du modèle non détectée | P1 | **Non vérifié** |
| EX-20 | Tenue sous charge progressive | Uvicorn local et Locust configurés | 5, 20, 50 et 100 utilisateurs simulés ; `POST /predict` | Mesurer débit, P95 et échecs ; interpréter les limites | `rapport_performance_creditrisk.md` et `load_*_stats.csv` | Saturation ou erreurs sous charge non identifiées | P2 | Vérifié pour les scénarios locaux |

## 4. Synthèse et réserves

- **20 exigences techniques** sont documentées ; les **sept exigences du professeur** sont explicitement mises en correspondance.
- **19 exigences** disposent d'au moins une preuve de vérification rapportée ; **EX-19** reste non vérifiée. Ce décompte ne signifie pas que toutes les sous-obligations du sujet sont entièrement satisfaites.
- La suite actuelle a été exécutée avec **56 tests réussis**. La couverture annoncée dans le plan est **91 %** ; elle doit rester associée à son rapport et à son environnement d'exécution.
- Les campagnes Locust totalisent **10 418 requêtes et zéro échec observé**, avec un P95 de **20 à 21 ms** selon les scénarios. Il s'agit de tests locaux, non d'une qualification de production.
- **À confirmer pour la Partie VII :** une preuve explicite qu'un test volontairement défaillant fait échouer GitHub Actions ; le succès du workflow seul ne le démontre pas.
- **À produire pour la Partie V :** un rapport comparatif entre une version de référence et une nouvelle version, avec métriques recalculées et tolérances fixées à l'avance.
- **À enrichir pour la Partie IV :** un registre des anomalies précisant risque, comportement attendu, résultat observé, gravité et correction recommandée.

## 5. Références des preuves

- `tests/test_api.py`, `tests/test_integration.py`, `tests/test_robustness.py`, `tests/test_regression.py`, `tests/test_performance.py`, `tests/test_model_metrics.py`.
- `reports/plan_de_test.md`, `reports/baseline.json`, `reports/coverage.xml`, `reports/rapport_performance_creditrisk.md`.
- `reports/load_5_stats.csv`, `reports/load_20_stats.csv`, `reports/load_50_stats.csv`, `reports/load_100_stats.csv`.
- `reports/github-actions/creditrisk-test-reports/coverage.xml`, `reports/github-actions/creditrisk-test-reports/pytest_results.xml`.

**Décision documentaire :** matrice enrichie pour la Partie I. Les états des preuves doivent être reconfirmés si le code, les tests ou les rapports sont modifiés avant remise. La validation technique du prototype ne vaut pas autorisation d'utilisation pour des décisions de crédit réelles.
