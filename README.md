
# CreditRisk-Test

## 1. Présentation

CreditRisk-Test est un prototype pédagogique destiné à l'évaluation de la qualité logicielle d'un système d'intelligence artificielle de prédiction du risque de défaut de crédit.

Le projet met en œuvre une API REST développée avec FastAPI, un modèle de Machine Learning utilisant scikit-learn et une démarche structurée d'assurance qualité logicielle.

**Important :** les données utilisées sont synthétiques. Le modèle n'est pas qualifié pour prendre des décisions bancaires réelles.

## 2. Objectifs

- Définir les exigences fonctionnelles et leur traçabilité.
- Automatiser les tests fonctionnels et d'intégration.
- Évaluer la robustesse de l'API.
- Vérifier la non-régression des performances du modèle.
- Mesurer les performances de l'API sous charge.
- Automatiser les contrôles qualité avec GitHub Actions.
- Produire un rapport final de qualification.

## 3. Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python | Développement et tests |
| FastAPI | API REST |
| scikit-learn | Modèle prédictif |
| Pytest | Tests automatisés |
| pytest-cov | Couverture du code |
| Ruff | Analyse statique |
| Locust | Tests de charge |
| GitHub Actions | Intégration continue |
| Joblib | Sérialisation du modèle |

## 4. Architecture fonctionnelle

Le système suit le processus :

Requête HTTP → Validation des données → Prétraitement → Modèle de Machine Learning → Réponse JSON.

Principaux modules :

- `app/main.py` : endpoints FastAPI.
- `app/validation.py` : validation des données.
- `app/preprocessing.py` : préparation des variables.
- `app/prediction.py` : chargement du modèle et prédiction.
- `scripts/train_model.py` : entraînement du modèle synthétique.

## 5. Installation et démarrage

### Windows / PowerShell

Créer et activer l'environnement virtuel :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Installer les dépendances :

```powershell
python -m pip install -r requirements.txt
```

Entraîner le modèle :

```powershell
python scripts/train_model.py
```

Démarrer l'API :

```powershell
python -m uvicorn app.main:app --reload
```

Documentation interactive :

http://127.0.0.1:8000/docs

## 6. Exemple de prédiction

Endpoint : `POST /predict`

```json
{
  "age": 35,
  "revenu_mensuel": 250000,
  "montant_credit": 1000000,
  "duree_mois": 12,
  "anciennete_activite": 4
}
```

La réponse contient notamment la probabilité estimée de défaut de crédit et la version du modèle.

Autres endpoints :

- `GET /health`
- `GET /model-info`

## 7. Stratégie de test

Le projet comprend **80 tests automatisés**, dont **41 tests fonctionnels**, couvrant :

| Catégorie | Fichier |
|---|---|
| Tests fonctionnels | `tests/test_api.py` |
| Tests d'intégration | `tests/test_integration.py` |
| Tests de robustesse | `tests/test_robustness.py` |
| Tests de non-régression | `tests/test_regression.py` |
| Comparaison des métriques | `tests/test_model_metrics.py` |
| Tests de performance | `tests/test_performance.py` |

### Exécution

```powershell
python -m pytest tests/ -v
```

Résultat de la dernière validation locale :

**80 tests réussis, 0 échec** (dont 24 scénarios supplémentaires de validation aux limites).

### Analyse statique

```powershell
python -m ruff check app scripts tests
```

Résultat : `All checks passed!`

### Couverture du code

```powershell
python -m pytest tests/ --cov=app --cov-report=term-missing
```

Couverture documentée : **91 %** (dernière exécution locale de la suite à 80 tests).

## 8. Tests de non-régression

Le projet compare les métriques du modèle courant à une baseline enregistrée dans `reports/baseline.json`.

Les critères suivis comprennent :

- Recall.
- F1-score.
- Reproductibilité des prédictions.
- Cohérence après rechargement du modèle.

Résultats observés :

| Indicateur | Baseline | Modèle courant |
|---|---:|---:|
| Recall | 14,65 % | 14,65 % |
| F1-score | 24,73 % | 24,73 % |

Tolérance maximale autorisée : **2 points de pourcentage de dégradation par métrique**.

Les huit tests de non-régression ont réussi.

La comparaison automatique des métriques du modèle courant à la baseline est vérifiée ; en revanche, la comparaison expérimentale de deux versions distinctes du modèle sur un même jeu de validation reste non démontrée.

## 9. Tests de performance

Quatre campagnes de charge ont été réalisées avec Locust.

| Utilisateurs virtuels | Requêtes | Échecs | P95 | Débit |
|---:|---:|---:|---:|---:|
| 5 | 191 | 0 | 20 ms | 3,24 req/s |
| 20 | 767 | 0 | 20 ms | 12,90 req/s |
| 50 | 1 895 | 0 | 21 ms | 31,88 req/s |
| 100 | 7 565 | 0 | 20 ms | 63,62 req/s |

**Total : 10 418 requêtes, aucun échec.**

Environnement local :

- Windows 11 Pro 64 bits.
- Intel Core Ultra 7 165H.
- 16 cœurs et 22 processeurs logiques.
- 63,45 Go de RAM.
- Python 3.13.2.
- Locust 2.47.0.

Les résultats ne constituent pas une garantie de performance en production.

## 10. Intégration continue

Le workflow `.github/workflows/tests.yml` s'exécute lors des push, des Pull Requests et des déclenchements manuels.

Il assure :

1. L'installation de Python et des dépendances.
2. L'entraînement du modèle synthétique.
3. La vérification du code avec Ruff.
4. L'exécution des tests Pytest.
5. La mesure de couverture.
6. L'archivage des rapports XML.

Une démonstration contrôlée a confirmé qu'un test Pytest volontairement défaillant provoque l'échec du pipeline.

Preuve :
https://github.com/kagibru/CreditRisk-Test/actions/runs/42700994044

La branche de démonstration n'est pas destinée à être fusionnée dans `main`.

## 11. Livrables

Les principaux documents sont disponibles dans `reports/` :

| Livrable | Fichier |
|---|---|
| Plan de test | `plan_de_test.md` |
| Matrice de traçabilité | `matrice_tracabilite.md` |
| Registre d'anomalies | `registre_anomalies_robustesse.md` |
| Rapport de non-régression | `rapport_non_regression_creditrisk.md` |
| Rapport de performance | `rapport_performance_creditrisk.md` |
| Rapport final de qualification | `rapport_final_qualification_creditrisk.pdf` |
| Résultats Pytest | `pytest_results.xml` |
| Couverture | `coverage.xml` |
| Résultats Locust | `load_*_stats.csv` et fichiers associés |

## 12. Limites et décision de qualification

Les contrôles techniques réalisés sont satisfaisants dans le périmètre pédagogique.

Cependant, le modèle présente un recall faible (14,65 %) sur les données synthétiques de validation, ce qui traduit un risque important de défauts de crédit non détectés.

Les données synthétiques ne permettent pas non plus de démontrer la fiabilité, l'équité ou la généralisation du modèle en conditions réelles.

**Décision : favorable à une démonstration pédagogique et à un pilote technique contrôlé sans décision financière réelle ; défavorable à une mise en production bancaire.**

Des validations complémentaires sur données réelles représentatives, ainsi que des analyses de biais, de calibration et de risques métier, seraient indispensables avant toute utilisation opérationnelle.
