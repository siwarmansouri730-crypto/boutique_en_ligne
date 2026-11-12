import io
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import urllib.request


class BoutiquePythonApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Boutique en Ligne - Python & VS Code")
    self.root.geometry("650x720")
    self.root.config(bg="#f8fafc")

    # Title Banner
    title_label = tk.Label(
        root,
        text="Boutique en Ligne (Python App)",
        font=("Arial", 16, "bold"),
        bg="#4f46e5",
        fg="white",
        pady=12,
    )
    title_label.pack(fill=tk.X)

    # Produits data (Nom, Prix, URL mta3 el taswira)
    self.products = {
        "Chaussures (120 DT)": {
            "price": 120,
            "url": (
                "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=200&auto=format&fit=crop&q=60"
            ),
        },
        "Manteau (180 DT)": {
            "price": 180,
            "url": (
                "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=200&auto=format&fit=crop&q=60"
            ),
        },
        "Pantalon (75 DT)": {
            "price": 75,
            "url": (
                "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=200&auto=format&fit=crop&q=60"
            ),
        },
        "Lunettes (50 DT)": {
            "price": 50,
            "url": (
                "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=200&auto=format&fit=crop&q=60"
            ),
        },
        "T-Shirt (35 DT)": {
            "price": 35,
            "url": (
                "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=200&auto=format&fit=crop&q=60"
            ),
        },
        "Maquillage (60 DT)": {
            "price": 60,
            "url": (
                "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=200&auto=format&fit=crop&q=60"
            ),
        },
    }

    # Frame for Inputs
    frame = tk.Frame(root, bg="#f8fafc", pady=10)
    frame.pack()

    # Client Name
    tk.Label(
        frame,
        text="Nom et Prénom:",
        font=("Arial", 11, "bold"),
        bg="#f8fafc",
        fg="#1e293b",
    ).grid(row=0, column=1, sticky="e", padx=5, pady=5)
    self.name_entry = tk.Entry(frame, font=("Arial", 11), width=22)
    self.name_entry.grid(row=0, column=0, padx=5, pady=5)

    # Product Selection
    tk.Label(
        frame,
        text="Sélectionner Article:",
        font=("Arial", 11, "bold"),
        bg="#f8fafc",
        fg="#1e293b",
    ).grid(row=1, column=1, sticky="e", padx=5, pady=5)

    self.prod_combo = ttk.Combobox(
        frame,
        values=list(self.products.keys()),
        width=20,
        state="readonly",
        font=("Arial", 10),
    )
    self.prod_combo.grid(row=1, column=0, padx=5, pady=5)
    self.prod_combo.current(0)
    self.prod_combo.bind("<<ComboboxSelected>>", self.update_image)

    # Quantity
    tk.Label(
        frame,
        text="Quantité:",
        font=("Arial", 11, "bold"),
        bg="#f8fafc",
        fg="#1e293b",
    ).grid(row=2, column=1, sticky="e", padx=5, pady=5)
    self.qty_entry = tk.Entry(frame, font=("Arial", 11), width=22)
    self.qty_entry.insert(0, "1")
    self.qty_entry.grid(row=2, column=0, padx=5, pady=5)

    # Image Display Frame
    self.img_label = tk.Label(root, bg="#f8fafc")
    self.img_label.pack(pady=5)
    self.load_initial_image()

    # Add Button
    order_btn = tk.Button(
        root,
        text="Ajouter au Panier",
        font=("Arial", 11, "bold"),
        bg="#10b981",
        fg="white",
        padx=20,
        pady=6,
        command=self.add_order,
    )
    order_btn.pack(pady=5)

    # Table of Orders (Treeview)
    self.tree = ttk.Treeview(
        root,
        columns=("Client", "Product", "Qty", "Total"),
        show="headings",
        height=6,
    )
    self.tree.heading("Client", text="Client")
    self.tree.heading("Product", text="Article")
    self.tree.heading("Qty", text="Quantité")
    self.tree.heading("Total", text="Total")

    self.tree.column("Client", width=120, anchor="center")
    self.tree.column("Product", width=190, anchor="center")
    self.tree.column("Qty", width=60, anchor="center")
    self.tree.column("Total", width=90, anchor="center")

    self.tree.pack(pady=10)

  def load_image_from_url(self, url):
    try:
      with urllib.request.urlopen(url) as connection:
        raw_data = connection.read()
      image = Image.open(io.BytesIO(raw_data))
      image = image.resize((120, 120))
      return ImageTk.PhotoImage(image)
    except Exception:
      return None

  def load_initial_image(self):
    first_key = list(self.products.keys())[0]
    url = self.products[first_key]["url"]
    self.current_img = self.load_image_from_url(url)
    if self.current_img:
      self.img_label.config(image=self.current_img)

  def update_image(self, event):
    selected = self.prod_combo.get()
    url = self.products[selected]["url"]
    self.current_img = self.load_image_from_url(url)
    if self.current_img:
      self.img_label.config(image=self.current_img)

  def add_order(self):
    client = self.name_entry.get().strip()
    selected_prod = self.prod_combo.get()
    qty_str = self.qty_entry.get().strip()

    if not client or not qty_str:
      messagebox.showerror(
          "Erreur", "Veuillez remplir le nom et la quantité !"
      )
      return

    try:
      qty = int(qty_str)
      if qty <= 0:
        raise ValueError()
    except ValueError:
      messagebox.showerror("Erreur", "La quantité doit être un nombre valide !")
      return

    unit_price = self.products[selected_prod]["price"]
    total_price = unit_price * qty

    self.tree.insert(
        "", tk.END, values=(client, selected_prod, qty, f"{total_price} DT")
    )

    self.name_entry.delete(0, tk.END)
    self.qty_entry.delete(0, tk.END)
    self.qty_entry.insert(0, "1")

    messagebox.showinfo(
        "Succès",
        f"Commande de {client} enregistrée avec succès pour un total de"
        f" {total_price} DT !",
    )


if __name__ == "__main__":
  root = tk.Tk()
  app = BoutiquePythonApp(root)
  root.mainloop()