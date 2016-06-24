import unittest
import sys

from hypercube.algorithm import DataStructure, Node

class NodesFactory(unittest.TestCase):
    def setUp(self):
        self.node1 = Node(1, 1, None, None)
        self.node2 = Node(2, 1, None, None)
        self.node3 = Node(3, 2, 1, 1)
        self.node4 = Node(4, 3, 1, 1)
        self.node5 = Node(5, 4, 2, 3)
        self.node6 = Node(6, 5, 4, 5)

class NodeTest(NodesFactory):
    def test_nodes_have_same_id(self):
        self.assertEqual(self.node1, self.node2)

    def test_nodes_have_different_id(self):
        self.assertFalse(self.node1 == self.node3)

    def test_node_is_child(self):
        self.assertTrue(self.node3.is_child(self.node1))

    def test_node_isnt_child(self):
        self.assertFalse(self.node1.is_child(self.node3))

    def test_node_is_parent(self):
        self.assertTrue(self.node5.is_parent(self.node6))

    def test_node_isnt_parent(self):
        self.assertFalse(self.node4.is_parent(self.node2))


class DataStructureTest(NodesFactory):
    def setUp(self):
        self.data = DataStructure()

    def is_equal(self, l1, l2):
        if len(l1) != len(l2):
            return False
        else:
            for i in range(len(l1)):
                if l1[i] != l2[i]:
                    return False
        return True

    def test_data_cleaned(self):
        self.assertEqual(self.data.count(), 0)

    def test_data_after_one_add(self):
        self.data.add_node(1, None)
        self.assertEqual(self.data.count(), 1)

    def test_data_multiple_add_and_verify_path(self):
        self.data.add_node(1, None)
        self.data.add_node(2, 1)
        self.data.add_node(3, 2)
        self.data.add_node(4, 3)
        path = self.data.find_path()
        self.assertTrue(self.is_equal(path, [1, 2, 3, 4]))
