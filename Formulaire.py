import tkinter as tk
from tkinter import ttk, messagebox
import json

# Predefined options for units
UNIT_OPTIONS = [
    "kg",
    "ml",
    "g",
    "u",
    "litre(s)",
    "cuillère(s) à café",
    "cuillère(s) à soupe",
]

# Data structure to hold the JSON content
json_data = {
    "nom_recette": "",
    "ingredients_recette": [],
    "instructions_recette": [],
    "mots_cles_recette": [],
    "unite_recette": "",
    "variantes_recette": [],
    "quantite_recette": 0,
    "type_recette": "",
}


# Save JSON to file
def save_to_json():
    try:
        # Ensure "nom_recette" is not empty
        nom_recette = json_data.get("nom_recette", "").strip()
        if not nom_recette:
            messagebox.showerror("Error", "Nom Recette cannot be empty.")
            return

        # Create filename from "nom_recette"
        filename = f"{nom_recette.replace(' ', '_')}.json"

        # Save the JSON data to the file
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(json_data, file, indent=4, ensure_ascii=False)

        messagebox.showinfo("Success", f"Data saved to {filename}!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# Add ingredient
def add_ingredient():
    ingredient_window = tk.Toplevel(root)
    ingredient_window.title("Add Ingredient")

    tk.Label(ingredient_window, text="Nom:").grid(row=0, column=0, padx=10, pady=5)
    nom_entry = tk.Entry(ingredient_window, width=30)
    nom_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ingredient_window, text="Unité:").grid(row=1, column=0, padx=10, pady=5)
    unite_var = tk.StringVar(ingredient_window)
    unite_var.set(UNIT_OPTIONS[0])  # Default to first option
    unite_menu = ttk.Combobox(
        ingredient_window, textvariable=unite_var, values=UNIT_OPTIONS, state="readonly"
    )
    unite_menu.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ingredient_window, text="Quantité:").grid(row=2, column=0, padx=10, pady=5)
    quantite_entry = tk.Entry(ingredient_window, width=30)
    quantite_entry.grid(row=2, column=1, padx=10, pady=5)

    def save_ingredient():
        try:
            ingredient = {
                "nom_ingredient": nom_entry.get().strip(),
                "unite_ingredient": unite_var.get(),
                "quantite_ingredient": int(quantite_entry.get().strip()),
            }
            json_data["ingredients_recette"].append(ingredient)
            refresh_ingredient_list()
            ingredient_window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Quantité must be a valid number.")

    save_button = tk.Button(ingredient_window, text="Add", command=save_ingredient)
    save_button.grid(row=3, column=0, columnspan=2, pady=10)


# Refresh ingredient list
def refresh_ingredient_list():
    for widget in ingredient_frame.winfo_children():
        widget.destroy()

    for idx, ingredient in enumerate(json_data["ingredients_recette"]):
        tk.Label(
            ingredient_frame,
            text=f"{idx + 1}. {ingredient['nom_ingredient']} ({ingredient['quantite_ingredient']} {ingredient['unite_ingredient']})",
        ).pack()


# Add instruction or keyword
def add_to_list(key, prompt):
    list_window = tk.Toplevel(root)
    list_window.title(f"Add {prompt}")

    tk.Label(list_window, text=f"New {prompt}:").grid(row=0, column=0, padx=10, pady=10)
    entry = tk.Entry(list_window, width=40)
    entry.grid(row=0, column=1, padx=10, pady=10)

    def save_item():
        value = entry.get().strip()
        if value:
            json_data[key].append(value)
            refresh_lists()
            list_window.destroy()

    save_button = tk.Button(list_window, text="Add", command=save_item)
    save_button.grid(row=1, column=0, columnspan=2, pady=10)


# Refresh dynamic lists
def refresh_lists():
    for widget in instruction_frame.winfo_children():
        widget.destroy()

    for idx, instruction in enumerate(json_data["instructions_recette"]):
        tk.Label(instruction_frame, text=f"{idx + 1}. {instruction}").pack()

    for widget in keyword_frame.winfo_children():
        widget.destroy()

    for idx, keyword in enumerate(json_data["mots_cles_recette"]):
        tk.Label(keyword_frame, text=f"{idx + 1}. {keyword}").pack()


# Main GUI setup
root = tk.Tk()
root.title("Recipe JSON Creator")

# Static Fields
tk.Label(root, text="Nom Recette:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
nom_recette_entry = tk.Entry(root, width=40)
nom_recette_entry.grid(row=0, column=1, padx=10, pady=5)
nom_recette_entry.bind(
    "<FocusOut>", lambda _: json_data.update({"nom_recette": nom_recette_entry.get()})
)

tk.Label(root, text="Quantité Recette:").grid(
    row=1, column=0, padx=10, pady=5, sticky="w"
)
quantite_entry = tk.Entry(root, width=40)
quantite_entry.grid(row=1, column=1, padx=10, pady=5)
quantite_entry.bind(
    "<FocusOut>",
    lambda _: json_data.update({"quantite_recette": int(quantite_entry.get())}),
)

tk.Label(root, text="Unité Recette:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
unite_recette_var = tk.StringVar(root)
unite_recette_var.set(UNIT_OPTIONS[0])  # Default to first option
unite_recette_menu = ttk.Combobox(
    root, textvariable=unite_recette_var, values=UNIT_OPTIONS, state="readonly"
)
unite_recette_menu.grid(row=2, column=1, padx=10, pady=5)
unite_recette_menu.bind(
    "<<ComboboxSelected>>",
    lambda _: json_data.update({"unite_recette": unite_recette_var.get()}),
)

# Ingredients Section
tk.Label(root, text="Ingredients:").grid(
    row=3, column=0, columnspan=2, pady=10, sticky="w"
)
ingredient_frame = tk.Frame(root)
ingredient_frame.grid(row=4, column=0, columnspan=2)
add_ingredient_button = tk.Button(root, text="Add Ingredient", command=add_ingredient)
add_ingredient_button.grid(row=5, column=0, columnspan=2, pady=5)

# Instructions Section
tk.Label(root, text="Instructions:").grid(
    row=6, column=0, columnspan=2, pady=10, sticky="w"
)
instruction_frame = tk.Frame(root)
instruction_frame.grid(row=7, column=0, columnspan=2)
add_instruction_button = tk.Button(
    root,
    text="Add Instruction",
    command=lambda: add_to_list("instructions_recette", "Instruction"),
)
add_instruction_button.grid(row=8, column=0, columnspan=2, pady=5)

# Keywords Section
tk.Label(root, text="Keywords:").grid(
    row=9, column=0, columnspan=2, pady=10, sticky="w"
)
keyword_frame = tk.Frame(root)
keyword_frame.grid(row=10, column=0, columnspan=2)
add_keyword_button = tk.Button(
    root,
    text="Add Keyword",
    command=lambda: add_to_list("mots_cles_recette", "Keyword"),
)
add_keyword_button.grid(row=11, column=0, columnspan=2, pady=5)

# Save Button
save_button = tk.Button(root, text="Save to JSON", command=save_to_json)
save_button.grid(row=12, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()
