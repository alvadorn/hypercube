

class DataStructure:
    def __init__(self):
        self.nodes = []
        self.unique = 0

    def add_node(self, common_id, parent_id):
        self.nodes.append(Node(self.unique, common_id, parent_id))
        self.unique += 1
        return self.unique - 1

    def find_path(self, last_father):
        print("len total: %s", len(self.nodes))
        father = last_father
        path = []
        n = Node(-1, -1,-1)
        while father is not None:
            print("step father is: %s", father)
            n.unique = father
            ref = self.nodes.index(n)
            print("ref: %s", ref)
            if ref is not None:
                path.append(self.nodes[ref].common)
                father = self.nodes[ref].parent
            else:
                father = None
        print(len(path))
        return path


        #for x in self.nodes.reverse():

    def count(self):
        return len(self.nodes)


class Node:
    """
        Node class that receives an unique id for a new node, a common id and
        the parent's common id. If parent's id is None, so the node is the root.
    """
    def __init__(self, unique_id, common_id, parent_id=None, parent_unique_id=None):
        self.unique = unique_id
        self.common = common_id
        self.parent = parent_id
        self.parent_unique = parent_unique_id

    def __eq__(self, other_node):
        return self.unique == other_node.unique

    def __ne__(self, other_node):
        return not self.__eq__(self, other_node)

    def is_parent(self, other_node):
        return (self.common == other_node.parent) and (self.parent_unique == other_node.parent_unique)

    def is_child(self, other_node):
        return self.parent == other_node.common
