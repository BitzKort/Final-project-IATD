import customtkinter
import pyperclip
from tkinter import messagebox

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
        
        try:
            # Primero, procesamos los valores de entrada.
            N = int(input_data[0].strip())  # Número de productos
            M = int(input_data[1].strip())  # Número de materias primas

            # Listas para almacenar los datos de los productos y materias primas.
            productos = []
            precios = []
            cantidades_materias = []

            # Procesar los productos
            for i in range(2, 2 + N):
                data = input_data[i].strip().split()
                nombre_producto = data[0]
                precio_producto = int(data[1])
                cantidades = list(map(int, data[2:]))
                if len(cantidades) != M:
                    raise ValueError("El número de cantidades de materias primas no coincide con el número de materias primas.")
                productos.append(f'"{nombre_producto}"')  # Producto como string
                precios.append(precio_producto)
                cantidades_materias.append(cantidades)

            # Listas para almacenar los datos de las materias primas.
            materias = []
            costos = []
            disponibilidades = []

            # Procesar las materias primas
            for i in range(2 + N, 2 + N + M):
                data = input_data[i].strip().split()
                nombre_materia = data[0]
                costo_materia = int(data[1])
                disponibilidad_materia = int(data[2])
                if len(data) != 3:
                    raise ValueError("Faltan datos para una materia prima.")
                materias.append(f'"{nombre_materia}"')  # Materia prima como string
                costos.append(costo_materia)
                disponibilidades.append(disponibilidad_materia)

            # Procesar las demandas mínimas y máximas
            demandas_minimas = [0] * N
            demandas_maximas = [100000] * N  # Valor alto como "infinito" para máximas

            for i in range(2 + N + M, len(input_data)):
                data = input_data[i].strip().split()
                producto = data[0]
                tipo_demanda = data[1]
                valor_demanda = int(data[2])

                # Encontrar el índice del producto
                index_producto = productos.index(f'"{producto}"')
                if tipo_demanda == "minimo":
                    demandas_minimas[index_producto] = valor_demanda
                elif tipo_demanda == "maximo":
                    demandas_maximas[index_producto] = valor_demanda

            # Generar código MiniZinc en el formato solicitado
            minizinc_code = ""

            for i in range(N):
                minizinc_code += f"var int: x{i+1}; %{productos[i]}\n"
            
            minizinc_code += "\n"

            # Definición de la variable z para los costos
            minizinc_code += "var int: z;\n\n"

            # Restricción de costos
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
            for i in range(N):
                minizinc_code += f"constraint x{i+1} >= {demandas_minimas[i]} /\ x{i+1} <= {demandas_maximas[i]};  % Demanda de {productos[i]}\n"

            # Solución
            minizinc_code += "\nsolve maximize z;\n\n"
            minizinc_code += 'output [\n'
            for i in range(N):
                minizinc_code += f'"{productos[i]}=" , show(x{i+1}), "\\n"\n' if i < N - 1 else f'"{productos[i]}=" , show(x{i+1}), "\\n", "Costo=", show(z) \n'
            minizinc_code += '];\n'

            # Mostrar el código en el textbox2
            self.textbox2.configure(state="normal")
            self.textbox2.delete("0.0", "end")
            self.textbox2.insert("0.0", minizinc_code)
            self.textbox2.configure(state="disabled")

        except ValueError as e:
            # Mostrar un mensaje de error si hay algún problema con los datos de entrada
            messagebox.showerror("Error", f"Entrada incorrecta: {str(e)}")

    def copiar(self):
        # Copiar el código generado al portapapeles
        code = self.textbox2.get("0.0", "end-1c")
        pyperclip.copy(code)

app = App()
app.mainloop()
