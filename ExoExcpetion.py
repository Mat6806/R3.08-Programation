'''
#Ex1
if __name__ == '__main__':
    def divEntier(x: int, y: int) -> int:
        try :
            if x < y:
             return 0     
            else:        
              x = x - y 
        except ValueError as err :
          print(f"problem de : {err}") 
        except ZeroDivisionError as err:
            print(f"problem de : {err}") 
        else :
         return divEntier(x, y) + 1 

print(divEntier(2,2))



#Exmpl cours du prof 
if __name__ == '__main__': 
    try: 
        a = float(input("a: ")) 
        b = float(input("b: "))
        res = a/b 
    except ValueError: 
        print("Please enter a float") 
    except ZeroDivisionError: 
        print("b should not be 0") 
    else: 
        print(res)


if __name__ == '__main__':
   try: 
     a = float(input("a: ")) 
     b = float(input("b: "))
     res = a/b 
   except ValueError as err: 
    print(f"Please enter a float: {err}") # le err => affiche le message d'érreur de la valuerror
   except ZeroDivisionError as err: 
    print("b should not be 0: {err}") 
   else: 
     print(res)

if __name__ == '__main__':
    a = int(input("Enter a positive number:"))
    if a <= 0:
        raise ValueError("It’s not a positive number")  #raise permet de lever l'excepetion 
'''

#Ex2
nom_fichier = "Test.txt"

try:
    with open(nom_fichier, "r") as fichier:
        for ligne in fichier:
            print(ligne.rstrip())            
except FileNotFoundError:
    print(f"Le fichier '{nom_fichier}' n'a pas été trouvé.")
except IOError:
    print(f"Une erreur est survenue lors de l'ouverture du fichier '{nom_fichier}'.")
except PermissionError:
    print(f"Vous n'avez pas les permission pour le fichier suivant:{nom_fichier}.")

