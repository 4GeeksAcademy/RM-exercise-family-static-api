
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name): #__init__: Es el constructor de la clase. Se ejecuta cuando se crea una nueva instancia de FamilyStructure.
        self.last_name = last_name
        self._next_id = 1
        self._members = [
                        
                        {'id':1, 'first_name':'Jhon','age':33,'lucky_numbers':[7,13,22]},
                        {'id':2,'first_name':'Jane','age':35,'lucky_numbers':[10,14,3]},
                        {'id':3,'first_name':'Jimmy','age':5,'lucky_numbers':[1]},
        ]

     # Este método genera un 'id' único al agregar miembros a la lista (no debes modificar esta función)
    def _generate_id(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_member(self, member): ##member es el nuevo miembro que se desea agregar a la familia
        ## Debes implementar este método
        member['id'] = self._generateId()  # Genera un ID único
        self._members.append(member)  ## Agrega un nuevo miembro a la lista de _members
        pass

    def delete_member(self, id):
        ## Debes implementar este método
        ## Recorre la lista y elimina el miembro con el id proporcionado
        new_members=[]
        for member in self._members:
            if member['id'] !=id:
                new_members.append(member)
        self._members=new_members
        pass

    def get_member(self, id):
        ## Debes implementar este método
        ## Recorre la lista y elimina el miembro con el id proporcionado

        pass

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
