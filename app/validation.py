import math

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator


class CreditApplication(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    age: StrictInt = Field(ge=18, le=100)
    revenu_mensuel: float = Field(gt=0, le=100_000_000)
    montant_credit: float = Field(gt=0, le=1_000_000_000)
    duree_mois: StrictInt = Field(ge=1, le=360)
    anciennete_activite: float = Field(ge=0, le=80)

    @field_validator("revenu_mensuel", "montant_credit", "anciennete_activite", mode="before")
    @classmethod
    def numeric_only(cls, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("Une valeur numerique est requise")  # noqa: TRY004
        if not math.isfinite(value):
            raise ValueError("Valeur non finie interdite")
        return value
