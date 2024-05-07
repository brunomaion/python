import tkinter as tk
from tkinter import colorchooser

class Triangulo:
    def __init__(self, vertices, cor):
        self.vertices = vertices
        self.cor = cor
        self.id = None

    def obter_vertices(self):
        return self.vertices

class Interface:
    def __init__(self, master):
        self.master = master
        self.master.title("Editor de Triângulos")

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg='white')
        self.canvas.pack(side=tk.LEFT)

        self.frame_right = tk.Frame(self.master)
        self.frame_right.pack(side=tk.RIGHT, padx=10)

        self.botao_adicionar = tk.Button(self.frame_right, text="Adicionar Triângulo", command=self.iniciar_selecao)
        self.botao_adicionar.pack(pady=5)

        self.lista_triangulos = tk.Listbox(self.frame_right, selectmode=tk.SINGLE)
        self.lista_triangulos.pack(pady=5)

        self.botao_mudar_cor = tk.Button(self.frame_right, text="Mudar Cor", command=self.mudar_cor_triangulo)
        self.botao_mudar_cor.pack(pady=5)

        self.botao_ocultar = tk.Button(self.frame_right, text="Ocultar Triângulo", command=self.ocultar_triangulo)
        self.botao_ocultar.pack(pady=5)

        self.botao_excluir = tk.Button(self.frame_right, text="Excluir Triângulo", command=self.excluir_triangulo)
        self.botao_excluir.pack(pady=5)

        self.botao_mostrar = tk.Button(self.frame_right, text="Mostrar Triângulos Ocultos", command=self.mostrar_triangulo_oculto)
        self.botao_mostrar.pack(pady=5)

        self.triangulos = []

        self.vertices = []
        self.selecionando = False

    def iniciar_selecao(self):
        self.selecionando = True
        self.vertices = []

    def finalizar_selecao(self):
        self.selecionando = False
        if len(self.vertices) == 6:  # Verifica se foram selecionados três pontos
            cor = "#FF0000"  # Cor padrão é vermelho
            triangulo = Triangulo(self.vertices, cor)
            self.desenhar_triangulo(triangulo)
            self.triangulos.append(triangulo)
            self.atualizar_lista_triangulos()
            self.vertices = []  # Limpar lista de vértices para o próximo triângulo
        else:
            print("Selecione 3 pontos na viewport para definir os vértices do triângulo.")

    def desenhar_triangulo(self, triangulo):
        triangulo.id = self.canvas.create_polygon(triangulo.vertices, fill=triangulo.cor, state='normal')

    def registrar_clicar(self, event):
        if self.selecionando:
            x, y = event.x, event.y
            self.vertices.append(x)
            self.vertices.append(y)
            if len(self.vertices) == 6:
                self.finalizar_selecao()

    def atualizar_lista_triangulos(self):
        self.lista_triangulos.delete(0, tk.END)
        for i, triangulo in enumerate(self.triangulos):
            estado = "Oculto" if self.canvas.itemcget(triangulo.id, "state") == "hidden" else "Visível"
            self.lista_triangulos.insert(tk.END, f"Triângulo {i+1} - {estado}")

    def mudar_cor_triangulo(self):
        indice = self.lista_triangulos.curselection()
        if indice:
            indice = int(indice[0])
            cor_nova = colorchooser.askcolor()[1]
            if cor_nova:
                triangulo = self.triangulos[indice]
                self.canvas.itemconfig(triangulo.id, fill=cor_nova)
                triangulo.cor = cor_nova
                print("Cor do triângulo atualizada com sucesso.")
            else:
                print("Nenhuma cor selecionada.")
        else:
            print("Selecione um triângulo na lista.")

    def ocultar_triangulo(self):
        indice = self.lista_triangulos.curselection()
        if indice:
            indice = int(indice[0])
            triangulo = self.triangulos[indice]
            estado_atual = self.canvas.itemcget(triangulo.id, "state")
            novo_estado = "normal" if estado_atual == "hidden" else "hidden"
            self.canvas.itemconfig(triangulo.id, state=novo_estado)
            self.atualizar_lista_triangulos()
        else:
            print("Selecione um triângulo na lista.")

    def excluir_triangulo(self):
        indice = self.lista_triangulos.curselection()
        if indice:
            indice = int(indice[0])
            triangulo = self.triangulos.pop(indice)
            self.canvas.delete(triangulo.id)
            self.atualizar_lista_triangulos()
        else:
            print("Selecione um triângulo na lista.")

    def mostrar_triangulo_oculto(self):
        for triangulo in self.triangulos:
            estado = self.canvas.itemcget(triangulo.id, "state")
            if estado == "hidden":
                self.canvas.itemconfig(triangulo.id, state="normal")
        self.atualizar_lista_triangulos()

    def obter_vertices_triangulo(self):
        indice = self.lista_triangulos.curselection()
        if indice:
            indice = int(indice[0])
            triangulo = self.triangulos[indice]
            return triangulo.obter_vertices()
        else:
            print("Selecione um triângulo na lista.")

def main():
    root = tk.Tk()
    app = Interface(root)
    root.bind("<Button-1>", app.registrar_clicar)
    root.mainloop()

if __name__ == "__main__":
    main()
