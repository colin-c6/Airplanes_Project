import unittest
from airplanes_project import data_structures


class Test_Graph(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        ''' Setting up an empty graph'''
        
        self.graph_obj = data_structures.Graph()
        
    def test_addVertex(self):
        
        ''' testing that the vertices are infact added to the vertices set'''
        
        self.graph_obj.add_vertex('DUB')
        self.graph_obj.add_vertex('JFK')
        self.assertTrue(len(self.graph_obj.vertices) == 2, "Vertices not correctly added")
    
    def test_addEdge(self):
        
        ''' testing that edges are successfully created between nodes '''
        
        self.graph_obj.add_edge('DUB', 'JFK', 100)
        self.graph_obj.add_edge('JFK', 'DUB', 100)
        self.assertTrue(len(self.graph_obj.edges['DUB']) == 1, "edge between nodes not successfully created ")
        self.assertTrue(self.graph_obj.edges['DUB'] == ['JFK'], "edge between nodes not successfully created ")
        self.assertTrue(len(self.graph_obj.edges['JFK']) == 1, "edge between nodes not successfully created ")
        self.assertTrue(self.graph_obj.edges['JFK'] == ['DUB'], "edge between nodes not successfully created ")
             
    def test_addWeights(self):
        
        '''Testing that the correct weights are added '''
        
        self.assertEqual(self.graph_obj.weights[('DUB','JFK')], 100, "Weights not successfully implemented on graph")
        self.graph_obj.add_edge('JFK', 'DUB', 500)
        self.assertEqual(self.graph_obj.weights[('JFK','DUB')], 500, "Weights not successfully implemented on graph")



class Test_Queue(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        ''' Setting up an empty graph'''
        
        self.queue_obj = data_structures.Queue()
    
    def test_enqueue(self):
        
        ''' This method cheecks that elements are sucesfully being added to the queue '''
        
        self.queue_obj.enqueue("Hello World")
        self.assertTrue(self.queue_obj.size() == 1, "Item not queued correctly")
        self.queue_obj.dequeue()
    
    def test_dequeue(self):
        
        ''' This method cheecks that elements are sucecsfully dequeued '''
        
        self.queue_obj.enqueue("Hello World")
        self.queue_obj.dequeue()
        self.queue_obj.enqueue("Hello World")
        self.queue_obj.dequeue()
        self.queue_obj.enqueue("Hello World")
        self.assertTrue(self.queue_obj.size() == 1, "Item not queued correctly")
        self.queue_obj.dequeue()
        self.assertTrue(self.queue_obj.size() == 0, "Item not queued correctly")
    
    def test_size(self):
        
        ''' This method tests the is empty function'''

        self.assertTrue(self.queue_obj.size() == 0,"Method returning that queue is not empty")
        self.queue_obj.enqueue("Well Boi")
        self.assertFalse(self.queue_obj.size() == 0,"Method returning that queue is not empty")
        self.queue_obj.dequeue()
        self.assertTrue(self.queue_obj.size() == 0,"Method returning that queue is not empty")


class Test_UnorderedList(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        ''' Setting up an empty graph'''
        
        self.linked_list_obj = data_structures.UnorderedList()
    
    def test_add_remove(self):
        
        ''' This method adds elements to the linked list '''
        
        self.linked_list_obj.add("Hello World")
        self.assertFalse(self.linked_list_obj.isEmpty(), "Error in isEmpty Method")
        self.assertTrue(self.linked_list_obj.size() ==1, "Error in size method" )
        self.linked_list_obj.remove("Hello World")
        self.assertTrue(self.linked_list_obj.isEmpty(), "Error in isEmpty Method")

    def test_isEmpty(self):
        
        ''' This method checks that elements are sucesfully being added to the queue '''
        
        self.assertTrue(self.linked_list_obj.isEmpty(), "Item not queued correctly")
        
    
    def test_return_last(self):
        
        ''' This method checks that the last element (first added) is returned '''
        
        self.linked_list_obj.add("Hello")
        self.linked_list_obj.add("World")
        self.linked_list_obj.add("Hello World")
        self.assertEquals(self.linked_list_obj.returnLast(), "Hello", "Item not queued correctly")
        self.linked_list_obj.remove("Hello")
        self.assertEquals(self.linked_list_obj.returnLast(), "World", "Item not queued correctly")
        
    def test_search(self):
        
        ''' this method checks that the search method can successfully find and locate and element in the Linked List  '''
        
        self.linked_list_obj.add(10)
        self.linked_list_obj.add("DundalkFC")
        self.linked_list_obj.add(20)
        self.assertTrue(self.linked_list_obj.search("DundalkFC"),"couldnt find element in the linked list")
        
        
if __name__ == '__main__':
    unittest.main()