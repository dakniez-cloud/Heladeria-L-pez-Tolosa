import tkinter as tk
from tkinter import messagebox


carrito_items = []

def agregar_al_carrito():
    opcion = var_opcion.get()
    
    #límite de sabores 
    limites_sabores = {
        "1 Bocha": 1, "2 Bochas": 2, "3 Bochas": 3,
        "1/4 Kilo": 3, "1/2 Kilo": 4, "1 Kilo": 4, 
        "2 Kilos": 5
    }
    
    tarifas = {
        "1 Bocha": 1500, "2 Bochas": 2000, "3 Bochas": 2500,
        "1/4 Kilo": 7500, "1/2 Kilo": 5000, "1 Kilo": 8000, 
        "2 Kilos": 18000
    }
    
    precio_base = tarifas.get(opcion, 0)
    limite = limites_sabores.get(opcion, 1)
    
    seleccionados = [sabor for sabor, var in check_sabores.items() if var.get()]
    toppings_elegidos = [top for top, var in check_toppings.items() if var.get()]
   
    if not seleccionados:
        messagebox.showwarning("Atención", "Debe elegir al menos un sabor.")
        return

    # Nueva validación de límite de sabores
    if len(seleccionados) > limite:
        messagebox.showwarning("Límite excedido", 
                               f"La opción '{opcion}' solo permite hasta {limite} sabor(es).\n"
                               f"Has seleccionado {len(seleccionados)}.")
        return
    

    adicional_toppings = len(toppings_elegidos) * 200
    total_item = precio_base + adicional_toppings
    
    descripcion = f"{opcion}: {', '.join(seleccionados)}"
    if toppings_elegidos:
        descripcion += f" (+{len(toppings_elegidos)} top.)"
    
    carrito_items.append({"desc": descripcion, "precio": total_item})
    actualizar_lista_visual()
    limpiar_campos()

def actualizar_lista_visual():
    listbox_pedido.delete(0, tk.END)
    total_acumulado = 0
    for item in carrito_items:
        listbox_pedido.insert(tk.END, f"{item['desc']} - ${item['precio']}")
        total_acumulado += item['precio']
    lbl_total_valor.config(text=f"${total_acumulado}")

def eliminar_seleccionado():
    seleccion = listbox_pedido.curselection()
    
    if seleccion:
        indice = seleccion[0]
        carrito_items.pop(indice)
        actualizar_lista_visual()
    else:
         messagebox.showwarning("Atención", "Seleccione un artículo de la lista para eliminarlo.")

def finalizar_venta():
    if not carrito_items:
        messagebox.showwarning("Atención", "El carrito está vacío.")
        return
    
    total = sum(item['precio'] for item in carrito_items)
    messagebox.showinfo("Venta Exitosa", f"Venta finalizada.\nTotal a cobrar: ${total}")
    carrito_items.clear()
    actualizar_lista_visual()

def limpiar_campos():
    var_opcion.set("1 Bocha")
    for var in check_sabores.values(): var.set(False)
    for var in check_toppings.values(): var.set(False)


app = tk.Tk()
app.title("Dulce Frío - Punto de Venta")
app.geometry("1500x800")
app.config(bg="#F8F9FA")

tk.Label(app, text="DULCE FRÍO 🍦", font=("Helvetica", 30, "bold"), 
         bg="#F8F9FA", fg="#A6D3E9").pack(pady=10)

paneles = tk.Frame(app, bg="#F8F9FA")
paneles.pack(fill="both", expand=True, padx=20)

col_menu = tk.Frame(paneles, bg="#F8F9FA")
col_menu.pack(side="left", fill="both", expand=True)

# Bochas
frame_bochas = tk.LabelFrame(col_menu, text=" Opciones por Bochas ", font=("Arial", 10, "bold"), padx=5, pady=5)
frame_bochas.pack(fill="x", pady=5)
var_opcion = tk.StringVar(value="1 Bocha")
opciones_bochas = [("1 Bocha", "$1500"), ("2 Bochas", "$2000"), ("3 Bochas", "$2500")]
for texto, precio in opciones_bochas:
    tk.Radiobutton(frame_bochas, text=f"{texto}", variable=var_opcion, value=texto).pack(side="left", padx=10)

#Kilos
frame_kilos = tk.LabelFrame(col_menu, text=" Opciones por Kilo ", font=("Arial", 10, "bold"), padx=10, pady=5)
frame_kilos.pack(fill="x", pady=5)
opciones_kilos = [("1/4 Kilo", "$7500"), ("1/2 Kilo", "$5000"), ("1 Kilo", "$8000"), ("2 Kilos", "$18000")]
for i, (texto, precio) in enumerate(opciones_kilos):
    tk.Radiobutton(frame_kilos, text=texto, variable=var_opcion, value=texto).grid(row=i//3, column=i%3, sticky="w", padx=5)

#Sabores
frame_sabores = tk.LabelFrame(col_menu, text=" Sabores ", font=("Arial", 10, "bold"), padx=10, pady=5)
frame_sabores.pack(fill="x", pady=5)
sabores = ["Chocolate", "Vainilla", "Frutilla", "Dulce de Leche", "Menta", "Tramontana","Limon","Granizado","Frutos del bosque","Super Gridito"]
check_sabores = {}
for i, sabor in enumerate(sabores):
    var = tk.BooleanVar()
    check_sabores[sabor] = var
    tk.Checkbutton(frame_sabores, text=sabor, variable=var).grid(row=i//3, column=i%3, sticky="w", padx=20)

# Sección Toppings
frame_toppings = tk.LabelFrame(col_menu, text=" Toppings (+$200) ", font=("Arial", 10, "bold"), padx=10, pady=5)
frame_toppings.pack(fill="x", pady=5)
lista_toppings = ["Baño de Chocolate", "Almendras", "Granas", "Salsa de Frutilla"]
check_toppings = {}
for i, top in enumerate(lista_toppings):
    var = tk.BooleanVar()
    check_toppings[top] = var
    tk.Checkbutton(frame_toppings, text=top, variable=var).grid(row=i//2, column=i%2, sticky="w", padx=20)

btn_agregar = tk.Button(col_menu, text="AGREGAR AL PEDIDO ➔", command=agregar_al_carrito, 
                        bg="#A6D3E9", fg="white", font=("Arial", 12, "bold"), height=2)
btn_agregar.pack(pady=15, fill="x")

col_carrito = tk.LabelFrame(paneles, text=" Detalle del Pedido Actual ", font=("Arial", 12, "bold"), bg="white", padx=10, pady=10)
col_carrito.pack(side="right", fill="both", padx=(20, 0))

listbox_pedido = tk.Listbox(col_carrito, font=("Arial", 10), width=45, height=20)
listbox_pedido.pack(pady=5)

btn_quitar = tk.Button(col_carrito, text="QUITAR ARTÍCULO", command=eliminar_seleccionado, 
                       bg="#E74C3C", fg="white", font=("Arial", 9, "bold"))
btn_quitar.pack(fill="x", pady=5)

frame_total = tk.Frame(col_carrito, bg="white")
frame_total.pack(fill="x", pady=10)
tk.Label(frame_total, text="TOTAL:", font=("Arial", 16, "bold"), bg="white").pack(side="left")
lbl_total_valor = tk.Label(frame_total, text="$0", font=("Arial", 16, "bold", "italic"), bg="white", fg="#27ae9c")
lbl_total_valor.pack(side="right")

btn_cobrar = tk.Button(col_carrito, text="FINALIZAR VENTA", command=finalizar_venta, 
                       bg="#27ae9c", fg="white", font=("Arial", 14, "bold"), height=2)
btn_cobrar.pack(side="bottom", fill="x")

app.mainloop()