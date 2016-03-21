
class Structure:
  def __init__(self):
    self.nodes = []

  def add_node(self, id, unique, father):
    node = Node(id, unique, father)
    
    if father is not None:
      father_ref = self._search_father(father)
      father_ref.add_child(unique)

    self.nodes.append(node)


  def _search_father(self, node_id):
    index = self.nodes.index(node_id) # may cause errors here, pay attention
    return self.nodes[index]


class Node:
  def __init__(self, id, unique, father):
    self.unique = unique
    self.id = id
    self.father = father
    self.children = []

  def add_child(self, child):
    self.children.append(child)

  def __eq__(self, other):
    return self.unique == other

