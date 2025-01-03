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
        item_text = f"{idx + 1}. {ingredient['nom_ingredient']} ({ingredient['quantite_ingredient']} {ingredient['unite_ingredient']})"
        item_label = tk.Label(ingredient_frame, text=item_text)
        item_label.pack(side="left", padx=5, pady=2)

        delete_button = tk.Button(
            ingredient_frame,
            text="Delete",
            command=lambda i=idx: remove_ingredient(i),
        )
        delete_button.pack(side="left", padx=5, pady=2)


# Function to remove an ingredient
def remove_ingredient(idx):
    del json_data["ingredients_recette"][idx]
    refresh_ingredient_list()  # Refresh the list after removal


# Add multi-line instructions
def add_variantes():
    variantes_window = tk.Toplevel(root)
    variantes_window.title("Add variantes")

    tk.Label(variantes_window, text="Variantes (une par ligne):").grid(
        row=0, column=0, padx=10, pady=10
    )
    text_area = tk.Text(variantes_window, width=50, height=10)
    text_area.grid(row=1, column=0, padx=10, pady=10)

    def save_variantes():
        variantes = text_area.get("1.0", tk.END).strip().splitlines()
        json_data["variantes_recette"].extend(
            [vari.strip() for vari in variantes if vari.strip()]
        )
        refresh_lists()
        variantes_window.destroy()

    save_button = tk.Button(variantes_window, text="Ajouter", command=save_variantes)
    save_button.grid(row=2, column=0, pady=10)


def add_instructions():
    instruction_window = tk.Toplevel(root)
    instruction_window.title("Add Instructions")

    tk.Label(instruction_window, text="Instructions (one per line):").grid(
        row=0, column=0, padx=10, pady=10
    )
    text_area = tk.Text(instruction_window, width=50, height=10)
    text_area.grid(row=1, column=0, padx=10, pady=10)

    def save_instructions():
        instructions = text_area.get("1.0", tk.END).strip().splitlines()
        json_data["instructions_recette"].extend(
            [instr.strip() for instr in instructions if instr.strip()]
        )
        refresh_lists()
        instruction_window.destroy()

    save_button = tk.Button(instruction_window, text="Save", command=save_instructions)
    save_button.grid(row=2, column=0, pady=10)


# Add keyword
def add_keyword():
    keyword_window = tk.Toplevel(root)
    keyword_window.title("Add Keyword")

    tk.Label(keyword_window, text="New Keyword:").grid(
        row=0, column=0, padx=10, pady=10
    )
    keyword_entry = tk.Entry(keyword_window, width=40)
    keyword_entry.grid(row=0, column=1, padx=10, pady=10)

    def save_keyword():
        value = keyword_entry.get().strip()
        if value:
            json_data["mots_cles_recette"].append(value)
            refresh_lists()
            keyword_window.destroy()

    save_button = tk.Button(keyword_window, text="Add", command=save_keyword)
    save_button.grid(row=1, column=0, columnspan=2, pady=10)


# Refresh dynamic lists including instructions, keywords, and variants
def refresh_lists():
    # Refresh instructions section
    for widget in instruction_frame.winfo_children():
        widget.destroy()

    for idx, instruction in enumerate(json_data["instructions_recette"]):
        item_text = f"{idx + 1}. {instruction}"
        item_label = tk.Label(instruction_frame, text=item_text)
        item_label.pack(side="left", padx=5, pady=2)

        delete_button = tk.Button(
            instruction_frame,
            text="Delete",
            command=lambda i=idx: remove_instruction(i),
        )
        delete_button.pack(side="left", padx=5, pady=2)

    # Refresh keywords section
    for widget in keyword_frame.winfo_children():
        widget.destroy()

    for idx, keyword in enumerate(json_data["mots_cles_recette"]):
        item_text = f"{idx + 1}. {keyword}"
        item_label = tk.Label(keyword_frame, text=item_text)
        item_label.pack(side="left", padx=5, pady=2)

        delete_button = tk.Button(
            keyword_frame, text="Delete", command=lambda i=idx: remove_keyword(i)
        )
        delete_button.pack(side="left", padx=5, pady=2)

    # Refresh variantes section
    for widget in variantes_frame.winfo_children():
        widget.destroy()

    for idx, variante in enumerate(json_data["variantes_recette"]):
        item_text = f"{idx + 1}. {variante}"
        item_label = tk.Label(variantes_frame, text=item_text)
        item_label.pack(side="left", padx=5, pady=2)

        delete_button = tk.Button(
            variantes_frame, text="Delete", command=lambda i=idx: remove_variante(i)
        )
        delete_button.pack(side="left", padx=5, pady=2)


# Function to remove an instruction
def remove_instruction(idx):
    del json_data["instructions_recette"][idx]
    refresh_lists()


# Function to remove a keyword
def remove_keyword(idx):
    del json_data["mots_cles_recette"][idx]
    refresh_lists()


# Function to remove a variant
def remove_variante(idx):
    del json_data["variantes_recette"][idx]
    refresh_lists()


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
    root, text="Add Instructions", command=add_instructions
)
add_instruction_button.grid(row=8, column=0, columnspan=2, pady=5)

# Variantes Section
tk.Label(root, text="Variantes :").grid(
    row=9, column=0, columnspan=2, pady=10, sticky="w"
)
variantes_frame = tk.Frame(root)
variantes_frame.grid(row=10, column=0, columnspan=2)
add_variantes_button = tk.Button(root, text="Add Variantes", command=add_variantes)
add_variantes_button.grid(row=11, column=0, columnspan=2, pady=5)

# Keywords Section
tk.Label(root, text="Keywords:").grid(
    row=12, column=0, columnspan=2, pady=10, sticky="w"
)
keyword_frame = tk.Frame(root)
keyword_frame.grid(row=13, column=0, columnspan=2)
add_keyword_button = tk.Button(
    root,
    text="Add Keyword",
    command=add_keyword,
)
add_keyword_button.grid(row=14, column=0, columnspan=2, pady=5)

# Save Button
save_button = tk.Button(root, text="Save to JSON", command=save_to_json)
save_button.grid(row=15, column=0, columnspan=2, pady=20)

# Run the application
root.mainloop()
