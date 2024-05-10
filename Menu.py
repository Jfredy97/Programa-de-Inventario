from tkinter import Tk, Label, Button, Entry, messagebox, ttk, Frame, END

#############################Clase###########################################
class Producto:
    
    def __init__(self, idProducto, nombre, cantidad, precio):
        self.idProducto = idProducto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        return f"{self.idProducto},{self.nombre},{self.cantidad},{self.precio}"

################################## Funciones ###################################
def nuevo_producto():
    global id_producto
    
    nombre_producto = txtNombre.get()
    añadir_al_inventario = txtCantidad.get()
    precio_producto = txtPrecio.get()

    if not nombre_producto or not añadir_al_inventario or not precio_producto:
        messagebox.showinfo(title="Error", message="Campos obligatorios", parent=ventana)
        return 
    


    ########################## indice producto  ##############################
    with open("productos.txt", 'r') as archivoProductos:
        id_producto = len(archivoProductos.readlines()) + 1
    
    producto = Producto(id_producto, nombre_producto, añadir_al_inventario, precio_producto)
    tabla.insert("", "end", values=(id_producto, nombre_producto, añadir_al_inventario, f'$ {precio_producto}'))

    with open("productos.txt", 'a') as archivoProductos:
        archivoProductos.write(str(producto) + "\n")
        print("Agregado con éxito")
        
    txtNombre.delete(0, END)
    txtCantidad.delete(0, END)
    txtPrecio.delete(0, END)
################################Buscar Producto#########################################
def buscarProductos(nombre):
    with open("productos.txt", 'r') as lista_productos:
        datos = lista_productos.readlines()
    
    tabla.delete(*tabla.get_children())
    
    
    for producto in datos:
        campos = producto.split(",")
        if len(campos) >= 4:
            nombre_producto = campos[1]
            if nombre.lower() in nombre_producto.lower():
                tabla.insert("", "end", values=(campos[0], campos[1], campos[3], campos[2]))  # Insertar el producto en la tabla

    if not tabla.get_children():
        messagebox.showinfo(title="Error", message=f'El producto {nombre} no fue encontrado', parent=ventana)

def buscar():
    nombre = txtNombre.get()
    if not nombre:
        messagebox.showinfo(title="Error", message="El campo de búsqueda está vacío",parent=ventana)
        return
    buscarProductos(nombre)

###############################Lsitar Productos##########################################
def listar():
    tabla.delete(*tabla.get_children())

    with open("productos.txt", 'r') as archivo:
        for linea in archivo:
            campos = linea.strip().split(',')
            tabla.insert("", "end", values=campos)

#################################Editar#################################################
id_producto_actual = None
def cargar_datos_seleccionados():
    global id_producto_actual
    item_seleccionado = tabla.selection()
    if item_seleccionado:
        valores = tabla.item(item_seleccionado)['values']
        if len(valores) >= 4:
            id_producto_seleccionado = tabla.item(item_seleccionado)['values'][0]
            nombre_producto = tabla.item(item_seleccionado)['values'][1]
            cantidad_producto = tabla.item(item_seleccionado)['values'][2]
            precio_producto = tabla.item(item_seleccionado)['values'][3]
        
        # Asignar el ID del producto seleccionado a id_producto_actual
        id_producto_actual = id_producto_seleccionado

        txtNombre.delete(0, 'end')
        txtNombre.insert(0, nombre_producto)
        txtCantidad.delete(0, 'end')
        txtCantidad.insert(0, cantidad_producto)
        txtPrecio.delete(0, 'end')
        txtPrecio.insert(0, precio_producto)
        return id_producto_seleccionado, nombre_producto, cantidad_producto, precio_producto
    else:
        return None, "", "", ""

# Función para editar un producto
def editar():
    global id_producto_actual  # Utilizar la variable global id_producto_actual
    if id_producto_actual is not None:
        nuevo_nombre = txtNombre.get()
        nueva_cantidad = txtCantidad.get()
        nuevo_precio = txtPrecio.get()

        if nuevo_nombre and nueva_cantidad and nuevo_precio:
            try:
                # Leer el archivo y guardar los datos editados en una lista
                with open("productos.txt", 'r') as file:
                    lineas = file.readlines()

                # Modificar los datos del producto seleccionado en la lista
                for i, linea in enumerate(lineas):
                    campos = linea.strip().split(",")
                    if campos[0] == str(id_producto_actual):  # Utilizar id_producto_actual
                        lineas[i] = f"{id_producto_actual},{nuevo_nombre},{nueva_cantidad},{nuevo_precio}\n"

                # Escribir la lista actualizada en el archivo
                with open("productos.txt", 'w') as file:
                    file.writelines(lineas)

                messagebox.showinfo(title="Información", message="Producto editado exitosamente", parent=ventana)

                # Actualizar la tabla
                item_seleccionado = tabla.selection()[0]
                tabla.item(item_seleccionado, values=(id_producto_actual, nuevo_nombre, nueva_cantidad, nuevo_precio))

                # Limpiar los campos de entrada
                txtNombre.delete(0, END)
                txtCantidad.delete(0, END)
                txtPrecio.delete(0, END)
            except Exception as e:
                messagebox.showerror(title="Error", message=f"Error al editar el archivo: {e}", parent=ventana)



#################################Eliminar#################################################
def eliminar_producto():
    item_seleccionado = tabla.selection()
    if item_seleccionado:
        id_producto = tabla.item(item_seleccionado)['values'][0]

        with open("productos.txt", 'r') as archivo:
            lineas = archivo.readlines()

        with open("productos.txt", 'w') as archivo:
            for linea in lineas:
                campos = linea.split(",")
                if campos[0] != str(id_producto):
                    archivo.write(linea)

        tabla.delete(item_seleccionado)
        messagebox.showinfo(title="Información", message="Producto eliminado exitosamente")
    else:
        messagebox.showinfo(title="Error", message="Por favor seleccione un producto para eliminar")





ventana = Tk()
ventana.columnconfigure(0, weight=1)
ventana.title("Inventario")
ventana.geometry("850x600")
ventana.resizable(False, False)

frame_titulo = Frame(ventana, bd=2, pady=20)
frame_titulo.grid(column=0, row=0)

frame_botones = Frame(ventana, bd=2)
frame_botones.grid(column=0, row=1, pady=(170, 0))

frame_tabla = Frame(ventana, bd=2, background="black")
frame_tabla.grid(column=0, row=2, pady=(20, 0))

lblTitulo = Label(frame_titulo, text=" PROGRAMA DE INVENTARIO ", font=("Arial", 25))
lblTitulo.grid(column=0, row=0)

lblNombre = Label(ventana, text="Nombre: ")
lblNombre.place(relx=0.2, rely=0.20, relwidth=0.100, height=30)

txtNombre = Entry(ventana)
txtNombre.place(relx=0.3, rely=0.20, relwidth=0.480, height=30)


lblCantidad = Label(ventana, text="Cantidad: ")
lblCantidad.place(relx=0.2, rely=0.28, relwidth=0.100, height=30)

txtCantidad = Entry(ventana)
txtCantidad.place(relx=0.3, rely=0.28, relwidth=0.480, height=30)

lblPrecio = Label(ventana, text="Precio: ")
lblPrecio.place(relx=0.2, rely=0.36, relwidth=0.100, height=30)

txtPrecio = Entry(ventana)
txtPrecio.place(relx=0.3, rely=0.36, relwidth=0.480, height=30)

# Boton Añadir
botonAñadir = Button(frame_botones, text="Añadir", width=15, background="#FF3B3F", command=nuevo_producto)
botonAñadir.grid(row=0, column=0, padx=15)

# Boton Buscar producto
botonBuscar = Button(frame_botones, text="Buscar producto", width=15, background="#3A9FE9",command=buscar)
botonBuscar.grid(row=0, column=1, padx=15)

# Boton Editar
botonEditar = Button(frame_botones, text="Editar", width=15, background="#A9A9A9",command=editar)
botonEditar.grid(row=0, column=2, padx=15)

# Boton Listar
botonListar = Button(frame_botones, text="Listar", width=15, background="#D7BC5B", command=listar)
botonListar.grid(row=0, column=3, padx=10)

# Botn Eliminar
botonEliminar = Button(frame_botones, text="Eliminar", width=15, background="#83D75B",command=eliminar_producto)
botonEliminar.grid(row=0, column=4, padx=10)

# Crear la tabla
tabla = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Precio", "Cantidad"))
tabla.heading('#0')
tabla.heading('#1', text="ID")
tabla.heading('#2', text="Nombre")
tabla.heading('#3', text="Cantidad")
tabla.heading('#4', text="Precio")
tabla.column('#0', width=0)
tabla.column('#1', width=50)
tabla.column('#2', width=200)
tabla.column('#3', width=200)
tabla.column('#4', width=200)
tabla.grid(column=0, row=0)
tabla.bind("<Double-1>", lambda event: cargar_datos_seleccionados())


ventana.mainloop()


