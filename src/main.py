import customtkinter



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.fuente = "Times New Roman"
        self.title("Proyecto Final complejidad 2024-2")
        self.grid_columnconfigure(0, weight=1)
        self.tittle = customtkinter.CTkLabel(master=self, text="Empresas yo soy el peligro", font=(self.fuente, 20))
        self.tittle.grid(row=0, column=0, padx=20, pady=20, sticky="n", columnspan=2)

        self.info = """Por favor antes de escribir, tenga encuenta: 
            1. Verificar la veracidad de sus datos segun el problema.
            2. Verificar la correcta escritura de los datos.
            3. Recuerde que el formato de escritura es separado solamente por espacios"""

        self.infoTextBox = customtkinter.CTkLabel(master=self, text=self.info, font=(self.fuente, 15), justify= "left")
        self.infoTextBox.grid(row=1, column=0, padx=10, pady=20, sticky="w")

        self.textbox1 = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox1.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")

        self.textbox2 = customtkinter.CTkTextbox(master=self, width=400, corner_radius=0)
        self.textbox2.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
        self.textbox2.insert("0.0", "aqui aparecera la respuesta")
        self.textbox2.configure(state="disabled")

        self.traducir = customtkinter.CTkButton(master=self, text="Traducir a minizinc", command=self.traducirMinizinc)
        self.traducir.grid(row=3, column=0, padx=20, pady=20)

        self.copiarButton = customtkinter.CTkButton(master=self, text="Copiar", command=self.copiar)
        self.copiarButton.grid(row=3, column=1, padx=20, pady=20)
    
    def traducirMinizinc(self):
        #aqui es la logica que en donde tienes que traducir lo que ingresa el usuario en codgio de minizinc
        pass


    def copiar(self):
        #aqui añade la logica para copiar la respuesta que se manda a minizinc
        pass



app = App()
app.mainloop()