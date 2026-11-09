# Registre des anomalies et des risques — CreditRisk-Test

Date : 09 novembre 2026
Environnement : Windows / Python 3.13.2
Suite : tests/test_robustness.py

## Résultat global

- Tests exécutés : 18
- Tests réussis : 18
- Tests échoués : 0
- Avertissements : 1
- Durée : 11,38 secondes

## Scénarios vérifiés

| ID | Risque visé | Comportement attendu | Résultat observé | Gravité potentielle | Correction recommandée |
|---|---|---|---|---|---|
| ROB-01 | Données nulles ou invalides | HTTP 422 | 10 tests réussis | Majeure | Aucune correction requise sur les cas testés |
| ROB-02 | Valeurs hors limites | HTTP 422 | 4 tests réussis | Majeure | Aucune correction requise sur les cas testés |
| ROB-03 | Schéma incorrect | HTTP 422 | 1 test réussi | Majeure | Aucune correction requise sur le cas testé |
| ROB-04 | Probabilité invalide | HTTP 200 et probabilité finie dans [0,1] | 1 test réussi | Critique | Maintenir le contrôle du contrat |
| ROB-05 | Prédictions non reproductibles | Probabilités égales à 1e-12 près | 1 test réussi | Majeure | Maintenir le contrôle de reproductibilité |
| ROB-06 | Montant extrême | HTTP 200 avec probabilité valide, ou HTTP 422 | 1 test réussi | Majeure | Documenter le code HTTP effectivement observé et préciser la règle métier |

## Observations techniques

OBS-01 : StarletteDeprecationWarning relatif à l'utilisation de httpx avec starlette.testclient.

Statut : avertissement non bloquant.
Recommandation : examiner la compatibilité des dépendances lors d'une prochaine mise à jour.

## Conclusion

Aucune anomalie fonctionnelle n'a été détectée par les 18 tests exécutés.

Cette conclusion est limitée aux scénarios et assertions effectivement testés.
Elle ne garantit pas l'absence de défauts dans d'autres conditions.
