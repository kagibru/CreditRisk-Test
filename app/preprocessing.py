import numpy as np

FEATURES = ["age", "revenu_mensuel", "montant_credit", "duree_mois", "anciennete_activite"]


def to_features(application):
    row = np.array([[getattr(application, key) for key in FEATURES]], dtype=float)
    if row.shape != (1, 5) or not np.isfinite(row).all():
        raise ValueError("Dimensions ou valeurs invalides")
    return row
