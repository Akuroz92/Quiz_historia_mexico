import tkinter as tk
from tkinter import messagebox
import csv
import random

class QuizMexico:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Quiz de Historia de México")
        self.root.geometry("850x600")
        self.root.configure(bg="#0f172a")
        
        self.nombre_jugador = ""
        self.preguntas = []
        self.preguntas_seleccionadas = []
        self.indice_actual = 0
        self.puntaje = 0
        self.vidas = 3
        self.respuesta_seleccionada = tk.StringVar()
        
        self.mostrar_pantalla_inicio()
    
    def mostrar_pantalla_inicio(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="QUIZ DE HISTORIA DE MÉXICO", 
                font=("Times New Roman", 32, "bold"), bg="#0f172a", fg="#eab308").pack(pady=100)
        
        tk.Label(self.root, text="Ingresa tu nombre:", 
                font=("Arial", 16), bg="#0f172a", fg="white").pack(pady=10)
        
        self.entry_nombre = tk.Entry(self.root, font=("Arial", 14), width=35, justify="center", 
                                    bg="#1e2937", fg="white", insertbackground="white")
        self.entry_nombre.pack(pady=15)
        
        tk.Button(self.root, text="COMENZAR", font=("Arial", 14, "bold"), bg="#eab308", fg="black", width=25, height=2,
                command=self.iniciar_juego).pack(pady=50)
    
    def iniciar_juego(self):
        self.nombre_jugador = self.entry_nombre.get().strip()
        if not self.nombre_jugador:
            messagebox.showwarning("Advertencia", "Por favor ingresa tu nombre.")
            return
        self.cargar_preguntas()
    
    def cargar_preguntas(self):
        try:
            with open("preguntas.csv", newline="", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                self.preguntas = list(reader)
            
            if len(self.preguntas) < 5:
                messagebox.showerror("Error", "El archivo debe tener al menos 5 preguntas.")
                return
            
            self.preguntas_seleccionadas = random.sample(self.preguntas, 5)
            self.indice_actual = 0
            self.puntaje = 0
            self.vidas = 3
            self.mostrar_pantalla_juego()
            
        except FileNotFoundError:
            messagebox.showerror("Error", "No se encontró el archivo preguntas.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Error al leer el archivo:\n{e}")
    
    def mostrar_pantalla_juego(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Para la barra superior
        top_frame = tk.Frame(self.root, bg="#1e2937")
        top_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(top_frame, text=f"Jugador: {self.nombre_jugador}", font=("Arial", 12), bg="#1e2937", fg="white").pack(side="left", padx=20)
        tk.Label(top_frame, text=f"Puntaje: {self.puntaje}", font=("Arial", 12), bg="#1e2937", fg="#eab308").pack(side="left", padx=20)
        tk.Label(top_frame, text=f"Vidas: {'❤️' * self.vidas}", font=("Arial", 12), bg="#1e2937", fg="#ef4444").pack(side="right", padx=20)
        
        # Para las reguntas
        pregunta_actual = self.preguntas_seleccionadas[self.indice_actual]
        tk.Label(self.root, text=pregunta_actual[0], font=("Times New Roman", 18, "bold"), 
                bg="#0f172a", fg="white", wraplength=750).pack(pady=40)
        
        # Para que se resalten las opciones
        self.respuesta_seleccionada.set(None)
        options_frame = tk.Frame(self.root, bg="#0f172a")
        options_frame.pack(pady=20)
        
        for i in range(1, 5):
            rb = tk.Radiobutton(options_frame, text=pregunta_actual[i], variable=self.respuesta_seleccionada, 
                            value=pregunta_actual[i], font=("Arial", 13), bg="#0f172a", fg="#e2e8f0",
                            selectcolor="#eab308", activebackground="#1e2937", activeforeground="#ffffff",
                            indicatoron=True)
            # Un estilo adicional para resaltar la selección
            rb.configure(selectcolor="#eab308", fg="#e2e8f0")
            rb.pack(anchor="w", padx=80, pady=12)
        
        # Para botones
        btn_frame = tk.Frame(self.root, bg="#0f172a")
        btn_frame.pack(pady=40)
        
        tk.Button(btn_frame, text="RESPONDER", font=("Arial", 13, "bold"), bg="#eab308", fg="black", width=18, height=2,
                command=self.verificar_respuesta).pack(side="left", padx=25)
        
        tk.Button(btn_frame, text="SALIR", font=("Arial", 12), bg="#ef4444", fg="white", width=12, height=2,
                command=self.root.quit).pack(side="left", padx=25)
    
    def verificar_respuesta(self):
        if not self.respuesta_seleccionada.get():
            messagebox.showwarning("Atención", "Selecciona una respuesta.")
            return
        
        pregunta_actual = self.preguntas_seleccionadas[self.indice_actual]
        correcta = pregunta_actual[5]
        
        if self.respuesta_seleccionada.get() == correcta:
            self.puntaje += 10
            messagebox.showinfo("¡Correcto!", "¡Muy bien!")
        else:
            self.vidas -= 1
            messagebox.showerror("Incorrecto", f"La respuesta correcta era:\n{correcta}")
        
        self.indice_actual += 1
        
        if self.vidas <= 0 or self.indice_actual >= len(self.preguntas_seleccionadas):
            self.mostrar_resultados()
        else:
            self.mostrar_pantalla_juego()
    
    def mostrar_resultados(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        tk.Label(self.root, text="¡FIN DEL JUEGO!", font=("Times New Roman", 28, "bold"), bg="#0f172a", fg="#eab308").pack(pady=60)
        tk.Label(self.root, text=f"Jugador: {self.nombre_jugador}", font=("Arial", 16), bg="#0f172a", fg="white").pack(pady=10)
        tk.Label(self.root, text=f"Puntaje Final: {self.puntaje} puntos", font=("Arial", 20, "bold"), bg="#0f172a", fg="#eab308").pack(pady=20)
        tk.Label(self.root, text=f"Vidas restantes: {self.vidas}", font=("Arial", 14), bg="#0f172a", fg="#ef4444").pack(pady=10)
        
        tk.Button(self.root, text="JUGAR DE NUEVO", font=("Arial", 14, "bold"), bg="#22c55e", fg="black", width=25, height=2,
                command=self.mostrar_pantalla_inicio).pack(pady=50)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = QuizMexico()
    app.run()