class Paciente:
    def __init__(self):
        self.__nombre= ""
        self.__cedula= 0
        self.__genero= ""
        self.__servicio= ""
    def asigGen(self,genero):
          self.__genero= genero
    def asigNom(self,nombre):
         self.__nombre= nombre
    def asigSer(self,serv):
         self.__servicio= serv
    def asigCed(self,cc):
         self.__cedula= cc
    def verGen(self):
         return self.__genero
    def verNom(self):
         return self.__nombre
    def verSer(self):
         return self.__servicio
    def verCed(self):
         return self.__cedula
class Sistema:
     def __init__(self):
          self.__listpacientes= []
     def ingresarPac(self,pac):
          self.__listpacientes.append(pac)
     def verPac(self, v):
          for p in self.__listpacientes:
               if v== p.verCed():
                    return p
               else:
                    print ("No se ha encontrado el paciente en el sistema")
     def vercantPac(self):
          print ("En el sistema hay: " + str(len(self.__listpacientes)) + " pacientes")
def main():
     sis=Sistema()
     while True:
          op=int(input("""Ingrese: 
                       1. Nuevo Paciente 
                       2. Ver Paciente
                       3. Ver Cantidad de Pacientes
                       4. Salir
                       """))
          if op==1:
               print("""Datos del Paciente:
                     """)  
               nombre = input ("Ingrese el nombre: ")                        
               cedula = int(input ("Ingrese la cedula: "))
               genero = input ("Femenino o Masculino: ")                        
               servicio = input ("A que servicio ingresó: ")
               pac = Paciente()

               pac.asigNom(nombre)
               pac.asigCed(cedula)
               pac.asigGen(genero)
               pac.asigSer(servicio)

               sis.ingresarPac(pac)
          elif op==2:
               c=int(input("Ingrese la cédula del paciente "))
               p=sis.verPac(c)
               print("Nombre: "+ p.verNom())
               print("Cedula: "+ str(p.verCed()))
               print("Género: "+ p.verGen())
               print("Servicio: "+ p.verSer())
             ##  if c == pac.verCed:
             ##  else: 
            ##      print("Ingresó una cédula incorrecta. Vuelva a intentar")     
          elif op==3:
               sis.vercantPac()
               
          elif op==4:
               break
          else:
               break
if __name__ == "__main__":
     main()
