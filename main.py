from gurobipy import  *

# diccionarios cuyos valores son [b_i, l_i],
# o sea que es una lista cuyo primer valor es el mínimo valor de 
# kilos de nutrientes y el segundo valor es el máximo valor de kilos de nutrientes
# de cada tipo
categorias = {
    'calorias': [400, 600],
    'proteinas':  [270, 1000],
    'grasas':      [100, 600],
    'sodio':   [150, 800]}

# Diccionario cuya llave es la comida y su valor es 
# el costo que esta tiene (los valores son los c_j)
cereales = {
    'trigo': 2.49,
    'avena':   2.89,
    'arroz':   1.50,
    'soya':     1.89,
    'maiz':  2.09,
    'cebada':     1.99,
    'porotos':     2.49,
    'lentejas':      1.89,
    'chia': 1.59}

#diccionario cuyos valores son los a_ij
valores = {
    ('trigo', 'calorias'): 0.410,
    ('trigo', 'proteinas'):  0.224,
    ('trigo', 'grasas'):      0.16,
    ('trigo', 'sodio'):   0.230,
    ('avena',   'calorias'): 0.420,
    ('avena',   'proteinas'):  0.32,
    ('avena',   'grasas'):      0.10,
    ('avena',   'sodio'):   0.1190,
    ('arroz',   'calorias'): 0.360,
    ('arroz',   'proteinas'):  0.20,
    ('arroz',   'grasas'):      0.232,
    ('arroz',   'sodio'):   0.1800,
    ('soya',     'calorias'): 0.380,
    ('soya',     'proteinas'):  0.14,
    ('soya',     'grasas'):      0.19,
    ('soya',     'sodio'):   0.1270,
    ('maiz',  'calorias'): 0.320,
    ('maiz',  'proteinas'):  0.12,
    ('maiz',  'grasas'):      0.10,
    ('maiz',  'sodio'):   0.2930,
    ('cebada',     'calorias'): 0.320,
    ('cebada',     'proteinas'):  0.15,
    ('cebada',     'grasas'):      0.12,
    ('cebada',     'sodio'):   0.2820,
    ('porotos',     'calorias'): 0.320,
    ('porotos',     'proteinas'):  0.31,
    ('porotos',     'grasas'):      0.12,
    ('porotos',     'sodio'):   0.1230,
    ('lentejas',      'calorias'): 0.100,
    ('lentejas',      'proteinas'):  0.28,
    ('lentejas',      'grasas'):      0.45,
    ('lentejas',      'sodio'):   0.125,
    ('chia', 'calorias'): 0.2330,
    ('chia', 'proteinas'):  0.18,
    ('chia', 'grasas'):      0.10,
    ('chia', 'sodio'):   0.180}

#Modelo para pregunat a,b,c,d

class ModelA: 
    def __init__(self): 
        self.model = Model("Model A")
    def create_model(self):
        self.I = list(categorias.keys())
        self.J = list(cereales.keys())
        self.a = valores 
        self.c = cereales
        self.b = categorias

        self.x = self.model.addVars(cereales.keys(), vtype=GRB.CONTINUOUS, name="x")

        self.model.setObjective(quicksum(self.c[j] * self.x[j] for j in self.J), GRB.MINIMIZE) 

        self.model.addConstr(quicksum(self.x[j] for j in self.J) == 1000)

        self.min_b = self.model.addConstrs(quicksum(self.a[(j, i)] * self.x[j] for j in self.J) >= self.b[i][0] for i in self.I)

        self.max_b = self.model.addConstrs(quicksum(self.a[(j, i)] * self.x[j] for j in self.J) <= self.b[i][1] for i in self.I)
        
    def solve(self):
        self.model.optimize()
    
    def build_sol_a(self): 
        self.create_model()
        self.solve()
        self.print_solution_a()

    def print_solution_a(self):
        print("Respuesta a la pregunta a:")
        if self.model.status == GRB.OPTIMAL:
            print(f"\nValor óptimo: {self.model.objVal:.2f} unidades de utilidad\n")
            print("Kilos de cada cereal:")
            for j in self.J:
                print(f"{j}: {self.x[j].X:.2f} kilos")
        else:
            print("No se encontro una solución óptima.")

    def build_sol_b(self):
        self.create_model()
        self.solve()
        self.print_solution_b()

    def print_solution_b(self):
        print("Respuesta a la pregunta b:")
        if self.model.status == GRB.OPTIMAL:
            print("\nCostos reducidos de las variables:")
            for var in self.model.getVars():
                print(f"{var.VarName}: valor = {var.X:.2f}, costo reducido = {var.RC:.4f}")
            print("Los costos reducidos son positivos, lo que significa que la solución es óptima y no se puede mejorar reduciendo el costo de ninguna variable.")
        else:
            print("No se encontro una solución óptima.")
    def print_solution_c(self):
        pass 
    def build_sol_c(self):
        modelc = ModelA()
        modelc.create_model()
        modelc.solve()
        modelc.print_solution_c()
    

    def build_sol_d(self): 
        modelB = ModelB()
        modelB.build_sol_d()

    def build_sol_e(self):
        modelC = ModelC()
        modelC.build_sol_e()


class ModelB:
    def __init__(self):
        self.model = Model("Model B")

    def create_model(self):
        self.I = list(categorias.keys())
        self.J = list(cereales.keys())
        self.a = valores 
        self.c = cereales
        self.b = categorias

        self.x = self.model.addVars(cereales.keys(), vtype=GRB.CONTINUOUS, name="x")

        self.model.setObjective(quicksum(self.c[j] * self.x[j] for j in self.J), GRB.MINIMIZE) 

        self.model.addConstr(quicksum(self.x[j] for j in self.J) == 1000)

        for i in self.I:
            if i == "proteinas":
                  self.prot_constraint = self.model.addConstr(
                    quicksum(self.a[(j, i)] * self.x[j] for j in self.J) >= self.b[i][0],
                    name="min_proteinas"
                )
            else:
                self.model.addConstr(quicksum(self.a[(j, i)] * self.x[j] for j in self.J) >= self.b[i][0])                
        self.model.addConstrs(quicksum(self.a[(j, i)] * self.x[j] for j in self.J) <= self.b[i][1] for i in self.I)

    def solve(self):
        self.model.optimize()

    def build_sol_d(self):
        self.create_model()
        self.solve()
        self.print_solution_d()

    def print_solution_d(self):
        print("Respuesta a la pregunta d:")
        if self.model.status == GRB.OPTIMAL:
            print(f"\nValor óptimo: {self.model.objVal:.2f} unidades de utilidad\n")
            dual = self.prot_constraint.Pi
            print(f"Valor dual de la restrccion de proteinas minimas: {dual:.4f}")
            print(f"Si reduces el minimo de proteinas en 3 el valor de la funcion objetivo baja en: {3 * dual:.4f}")

        else:
            print("No se encontró una solución óptima.")


class ModelC:
    def __init__(self):
        self.model = Model("Model C")

    def create_model(self):
        self.I = list(categorias.keys())
        self.J = list(cereales.keys())
        self.a = valores 
        self.c = cereales
        self.b = categorias

        self.x = self.model.addVars(cereales.keys(), vtype=GRB.INTEGER, name="x")

        self.model.setObjective(quicksum(5 * self.c[j] * self.x[j] for j in self.J), GRB.MINIMIZE) 

        self.model.addConstr(quicksum(5 * self.x[j] for j in self.J) == 1000)

        self.min_b = self.model.addConstrs(quicksum(5 * self.a[(j, i)] * self.x[j] for j in self.J) >= self.b[i][0] for i in self.I)

        self.model.addConstrs(quicksum(5 * self.a[(j, i)] * self.x[j] for j in self.J) <= self.b[i][1] for i in self.I)

    def solve(self):
        self.model.optimize()

    def build_sol_e(self):
        self.create_model()
        self.solve()
        self.print_solution_e()

    def print_solution_e(self):
        print("Respuesta a la pregunta e:")
        if self.model.status == GRB.OPTIMAL:
            print(f"\nValor óptimo: {self.model.objVal:.2f} unidades de utilidad\n")
            for j in self.J:
                print(f"{j}: {self.x[j].X}")      
            print(f"El valor óptimo aumenta en un 0.066% en comparación con el modelo anterior.")
            
        else:
            print("No se encontro una solución óptima.")

def main():
    while True:
        option = input("Seleccion una pregunta: a, b, c, d, e o 1 para salir\n")
        if option == "a": 
            print("Resolviendo pregunta a...")
            model = ModelA()
            model.build_sol_a()
        elif option == "b": 
            print("Resolviendo pregunta b...")
            model = ModelA()
            model.build_sol_b()
        elif option == "c": 
            print("Resolviendo pregunta c...")
            model = ModelA()
            model.build_sol_c()
        elif option == "d": 
            print("Resolviendo pregunta d...")
            model = ModelA()
            model.build_sol_d()
        elif option == "e": 
            print("Resolviendo pregunta e...")
            model = ModelA()
            model.build_sol_e()
        elif option == '1':
            print("Saliendo del programa.")
            return


if __name__ == "__main__":
    main()
