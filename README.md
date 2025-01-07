## Unités (utiliser uniquement celles-ci)

- u
- ml
- g
- kg
- l
- cl
- cuillière(s) à soupe
- cuillière(s) à café

## Structure des fichiers JSON

```
{
    "nom_recette": "Nom avec majuscule au début",
    "ingredients_recette": [
        {
        "nom_ingredient": "Nom de l'ingrédient uniquement, avec majuscule au début",
        "unite_ingredient": "Unité parmi la liste ci-dessus",
        "quantite_ingredient": Nombre (sans ""),
        //Facultatif ↓
        "etape_ingredient": "Nom de l'étape"
        },
        //Répéter autant que d'ingrédients
    ],
    "instructions_recette": [
        "Texte court qui décrit chaque étape",
    ],
    "mots_cles_recette": [
      "texte (sans majuscule)"
    ],
    "unite_recette": "Unité parmi la liste ci-dessus",
    "variantes_recette": ["Éléments qui peuvent être modifiés, ajoutés ou supprimés dans la recette"],
    "quantite_recette": Nombre (correspond à la quantité totale finale de la recette),
    "type_recette": "dessert, plat, boulangerie, sauce, pâtisserie, autre"
}

```
