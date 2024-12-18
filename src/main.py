import customtkinter
import pyperclip

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.fuente = "Times New Roman"
        self.title("Proyecto Final complejidad 2024-2")
        self.grid_columnconfigure(0, weight=1)
        self.tittle = customtkinter.CTkLabel(master=self, text="Empresas yo soy el peligro", font=(self.fuente, 20))
        self.tittle.grid(row=0, column=0, padx=20, pady=20, sticky="n", columnspan=2)

        self.info = """Por favor antes de escribir, tenga en cuenta: 
            1. Verificar la veracidad de sus datos según el problema.
            2. Verificar la correcta escritura de los datos.
            3. Recuerde que el formato de escritura es separado solamente por espacios"""

        self.infoTextBox = customtkinter.CTkLabel(master=self, text=self.info, font=(self.fuente, 15), justify="left")
        self.infoTextBox.grid(row=1, column=0, padx=10, pady=20, sticky="w")

        self.textbox1 = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox1.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        self.textbox2 = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox2.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
        self.textbox2.insert("0.0", "Aquí aparecerá la respuesta")
        self.textbox2.configure(state="disabled")

        self.traducir = customtkinter.CTkButton(master=self, text="Traducir a minizinc", command=self.traducirMinizinc)
        self.traducir.grid(row=3, column=0, padx=20, pady=20)

        self.copiarButton = customtkinter.CTkButton(master=self, text="Copiar", command=self.copiar)
        self.copiarButton.grid(row=3, column=1, padx=20, pady=20)
    


    def traducirMinizinc(self):
        input_data = self.textbox1.get("0.0", "end-1c").strip().split("\n")

        print(input_data)
        
        # Primero, procesamos los valores de entrada.
        N = int(input_data[0].strip())  # Número de productos (numero de variables)
        M = int(input_data[1].strip())  # Número de materias primas (restricciones del problema)

        # Listas para almacenar los datos de los productos y materias primas.
        productos = {}
        listProductosKeys = []
        precios = []
        cantidades_materias = []

        # Procesar los productos
        for i in range(2, 2 + N):
            producto = input_data[i].strip().split()
            nombre_producto = producto[0]
            precio_producto = int(producto[1])
            cantidadesProductoPorMateria = list(map(int, producto[2:]))
            productos[nombre_producto] = f"x{i-1}"  # Producto como string
            precios.append(precio_producto)
            cantidades_materias.append(cantidadesProductoPorMateria)

        print("datos de productos")
        print(productos)
        listProductosKeys = list(productos.keys())
        print(precios)
        print(cantidades_materias)

        # Listas para almacenar los datos de las materias primas.
        materias = []
        costos = []
        disponibilidades = []

        # Procesar las materias primas
        for i in range(2 + N, 2 + N + M):
            materiaPrima = input_data[i].strip().split()
            nombre_materia = materiaPrima[0]
            costo_materia = int(materiaPrima[1])
            disponibilidad_materia = int(materiaPrima[2])
            materias.append(f'"{nombre_materia}"')  # Materia prima como string
            costos.append(costo_materia)
            disponibilidades.append(disponibilidad_materia)

        # Procesar las demandas mínimas y máximas
        listaDemandas = [] # Valor alto como "infinito" para máximas

        iter = 2 + N + M #nos aseguramos de estar en la primer linea de las restricciones de demandas
        while True:

            try:
                
                demandas = input_data[iter].strip().split()
                print(demandas)
                demandaNombreProducto = demandas[0]
                tipo_demanda = demandas[1]
                valor_demanda = int(demandas[2])
                
                if tipo_demanda == "minimo":
                    listaDemandas.append([productos[demandaNombreProducto], ">=", valor_demanda])
                elif tipo_demanda == "maximo":
                    listaDemandas.append([productos[demandaNombreProducto], "<=", valor_demanda])

                iter +=1
            
            except Exception:
                
                print("no hay mas lineas por traducir")
                break
        print("liesta de cosas")
        print(listaDemandas)

        # Generar código MiniZinc en el formato solicitado
        minizinc_code = ""

        #Primero se generan las variables
        for i in range(N):
            minizinc_code += f"var int: x{i+1}; %{listProductosKeys[i]}\n"
        
        minizinc_code += "\n"

        # Definición de la variable z para los costos
        minizinc_code += "var int: z;\n\n"

        # Restricción de costos (funcion objetivo)
        minizinc_code += "constraint z = "
        for i in range(N):
            minizinc_code += f"{precios[i]} * x{i+1} + " if i < N - 1 else f"{precios[i]} * x{i+1};  %Costo a minimizar\n"

        # Restricciones de cantidad no negativa
        for i in range(N):
            minizinc_code += f"constraint x{i+1} >= 0;\n"
        
        # Restricciones de materias primas (disponibilidad)
        for j in range(M):
            minizinc_code += f"constraint "
            for i in range(N):
                minizinc_code += f"{cantidades_materias[i][j]} * x{i+1} + " if i < N - 1 else f"{cantidades_materias[i][j]} * x{i+1} "
            minizinc_code += f"<= {disponibilidades[j]};  % Materia prima {materias[j]}\n"
        
        # Restricciones de demanda

        if len(listaDemandas) != 0: #Es decir, si existe al menos una demanda en alguno de los dos


            for demanda in listaDemandas:

                minizinc_code += f"constraint {demanda[0]} {demanda[1]} {demanda[2]}; \n"
        
        else:
            print("no hay demandas")
            

        # Solución
        minizinc_code += "\nsolve maximize z;\n\n"
        minizinc_code += 'output [\n'

        for i in range(N):
            if i < N - 1:
                minizinc_code += '"{}=", show(x{}), "\\n",\n'.format(listProductosKeys[i], i + 1)
            else:
                minizinc_code += '"{}=", show(x{}), "\\n", "Costo=", show(z)\n'.format(listProductosKeys[i], i + 1)
        minizinc_code += '];\n'

        # Mostrar el código en el textbox2
        self.textbox2.configure(state="normal")
        self.textbox2.delete("0.0", "end")
        self.textbox2.insert("0.0", minizinc_code)
        self.textbox2.configure(state="disabled")

    def copiar(self):
        # Copiar el código generado al portapapeles
        code = self.textbox2.get("0.0", "end-1c")
        pyperclip.copy(code)

app = App()
app.mainloop()

