from typing import Tuple, TypeVar, Generic
import random
import numpy as np

T = TypeVar('T')

class Heap(Generic[T]):
    def __init__(self, type="min"):
        self.order = type if type in ["min", "max"] else "min"

        self.arr: list[T] = []
        self.index: dict[T, int] = dict()

        self.keys: dict[T, int] = dict()
        self.tie_breaks: dict[T, int] = dict()

        return
    
    def __contains__(self, item: T):
        return item in self.index
    
    @property
    def size(self):
        return len(self.arr)
    
    @property
    def lead(self):
        if self.size == 0:
            return None
        return self.arr[0]
    
    def build_heap(self, items: list[T], keys: dict[T, int]=None, tie_breaks: dict[T, int]=None):
        self.arr = items

        if keys == None:
            self.keys = {k: k for k in items}
        else:
            self.keys = keys.copy()

        if tie_breaks == None:
            self.tie_breaks = keys.copy()
        else:
            self.tie_breaks = tie_breaks.copy()
        
        self.index = {k: v for v, k in enumerate(items)}
        
        for r in range((len(items) // 2), -1, -1):
            self.heapify_down(r)
        return
    
    def compare_items(self, item_1: T, item_2: T):
        if self.order == "max":
            if self.keys[item_1] == self.keys[item_2]:
                return self.tie_breaks[item_1] > self.tie_breaks[item_2]
            return self.keys[item_1] > self.keys[item_2]
        else:
            if self.keys[item_1] == self.keys[item_2]:
                    return self.tie_breaks[item_1] < self.tie_breaks[item_2]
            return self.keys[item_1] < self.keys[item_2]

    def heapify_up(self, start_idx: int):
        if start_idx == 0:
            return
        
        parent_idx = (start_idx -1) // 2

        parent_node = self.arr[parent_idx]
        start_node = self.arr[start_idx]

        if self.compare_items(parent_node, start_node):
            return

        self.arr[parent_idx], self.arr[start_idx] = self.arr[start_idx], self.arr[parent_idx]
        self.index[parent_node], self.index[start_node] = self.index[start_node], self.index[parent_node]

        self.heapify_up(parent_idx)
        
        return

    def heapify_down(self, start_idx: int):
        arr_size = len(self.arr)

        left_idx = 2 * start_idx + 1
        right_idx = 2 * start_idx + 2

        start_node = self.arr[start_idx]
        
        if left_idx > arr_size-1:
            return
        
        left_node = self.arr[left_idx]

        compare_idx, compare_node = left_idx, left_node
        
        if right_idx < arr_size:

            right_node = self.arr[right_idx]

            if not self.compare_items(left_node, right_node):
                compare_idx, compare_node = right_idx, right_node

        if self.compare_items(start_node, compare_node):
            return
        
        self.arr[compare_idx], self.arr[start_idx] = self.arr[start_idx], self.arr[compare_idx]
        self.index[compare_node], self.index[start_node] = self.index[start_node], self.index[compare_node]

        self.heapify_down(compare_idx)

        return

    def extract_lead(self) -> Tuple[T, int]:
        '''
        Return Item, Key
        '''
        arr_size = len(self.arr)

        if arr_size == 0:
            return None
        
        if arr_size == 1:
            min_element = self.arr.pop()

            self.tie_breaks.pop(min_element)
            self.index.pop(min_element)

            return min_element, self.keys.pop(min_element)
        
        last_element = self.arr[-1]
        
        self.arr[0], self.arr[-1] = self.arr[-1], self.arr[0]
        self.index[last_element] = 0
        
        min_element = self.arr.pop()
        key = self.keys.pop(min_element)
        self.index.pop(min_element)
        self.tie_breaks.pop(min_element)

        self.heapify_down(0)
        
        return min_element, key
        
    def insert(self, item: T, key: int=None, tie_break: int=None):
        size = len(self.arr)

        self.arr.append(item)
        self.index[item] = size
        
        if key == None:
            key = item

        if tie_break == None:
            tie_break = key

        self.keys[item] = key
        self.tie_breaks[item] = tie_break
        
        if size > 0:
            self.heapify_up(size)
        return
    
    def delete(self, item: T):
        idx = self.index[item]

        if idx == len(self.arr) -1:
            self.arr.pop()
            self.index.pop(item)
            self.keys.pop(item)
            self.tie_breaks.pop(item)
            
            return

        last = self.arr[-1]

        self.arr[idx], self.arr[-1] = self.arr[-1], self.arr[idx]
        self.index[last] = idx
        
        deleted = self.arr.pop()
        
        if self.compare_items(deleted, last):
            self.heapify_down(idx)
        else:
            self.heapify_up(idx)
        
        self.index.pop(item)
        self.keys.pop(item)
        self.tie_breaks.pop(item)

        return
    
    def validate(self):

        def report():
            print(self.arr)
            print(self.index)
            print(self.keys)
            return
        
        if len(self.arr) == 0:
            print("heap empty")
            return False
        
        if len(self.arr) != len(self.keys.keys()) and len(self.arr) != len(self.index.keys()):
            report()
            return False

        for idx, item in enumerate(self.arr):
            if self.index[item] != idx:
                report()
                return False
        
        nodeStack = [0]
        while len(nodeStack) != 0:
            parent_idx = nodeStack.pop()

            lchild_idx = 2 * parent_idx + 1
            rchild_idx = 2 * parent_idx + 2

            arr_size = len(self.arr)
            
            parent_node = self.arr[parent_idx]
            
            if lchild_idx > arr_size -1:
                continue
            
            left_node = self.arr[lchild_idx]
            
            if rchild_idx > arr_size -1:
                if self.compare_items(parent_node, left_node):
                    continue
                
                report()
                return False

            right_node = self.arr[rchild_idx]
            
            if self.compare_items(parent_node, left_node) and self.compare_items(parent_node, right_node):
                nodeStack.append(lchild_idx)
                nodeStack.append(rchild_idx)
            else:
                report()
                return False

        return True
    
    def test_heap(self, num_items: int = 500):
        self.__init__()

        random_inserts = random.sample(range(1, num_items*3), num_items)
        random_keys = {k: random.random() for k in random_inserts}

        self.build_heap(
            random_inserts,
            random_keys
        )
        
        print(f'Insert: {"PASSED" if self.validate() else "FAILED"}')
        
        for i in random.sample(random_inserts, num_items // 2):
            self.delete(i)

        print(f'Delete: {"PASSED" if self.validate() else "FAILED"}')
        
        self.extract_lead()
        print(f'Extract Lead: {"PASSED" if self.validate() else "FAILED"}')

def dijkstra(g: dict[int, list[Tuple[int, int]]], startNode: int):
    '''
    Runs Dijkstras on a graph g from a given start node

    g = { tail: (head, cost) }

    Returns (closest node, edge), { node: score }
    '''
    nodeHeap = Heap[int](type="min")
    processedNodes = {1: 0}
    closest_node = None

    for tail, edges in g.items():
        if tail == startNode:
            for edge in edges:
                head, weight = edge
                nodeHeap.insert(head, weight)
        elif tail not in nodeHeap:
            nodeHeap.insert(tail, np.Inf)

    while len(processedNodes.keys()) < len(g.keys()):
        
        greedy_node, greedy_score = nodeHeap.extract_lead()
        processedNodes[greedy_node] = greedy_score

        if closest_node is None or greedy_score < closest_node[1]:
            closest_node = (greedy_node, greedy_score)
        
        for edge in g[greedy_node]:
            head, weight = edge
            
            if head in nodeHeap:
                old_key = nodeHeap.keys[head]
                nodeHeap.delete(head)
                
                new_key = min(old_key, greedy_score + weight)
                nodeHeap.insert(head, new_key)
    
    return closest_node, processedNodes