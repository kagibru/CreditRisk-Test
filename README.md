# CreditRisk-Test

Prototype pedagogique de QA pour une API de risque de credit. **Donnees synthetiques, modele non adapte aux decisions bancaires reelles.**

## Windows / PowerShell

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts\train_model.py
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Ouvrir http://127.0.0.1:8000/docs pour essayer l'API.

Exemple POST /predict :
```json
{"age":35,"revenu_mensuel":250000,"montant_credit":1000000,"duree_mois":12,"anciennete_activite":4}
```

Le modele doit etre entraine localement avant de lancer l'API. Le jeu synthetique n'est pas une preuve de precision ni d'equite en conditions reelles.
