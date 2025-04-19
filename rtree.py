from rtree_node import RTreeNode

class RTree:
    #r-tree implementation for spatial indexing
    def __init__(self, max_entries=4):
        self.max_entries = max_entries
        self.root = RTreeNode(is_leaf=True, max_entries=max_entries)
    
    def insert(self, rectangle, data_id):
        #insert a new rectangle with associated data ID
        # handle case when the root splits
        new_node = self._insert(self.root, rectangle, data_id)
        if new_node:
            # create a new root
            old_root = self.root
            self.root = RTreeNode(is_leaf=False, max_entries=self.max_entries)
            self.root.entries = [
                (old_root.get_mbr(), old_root),
                (new_node.get_mbr(), new_node)
            ]
    
    def _insert(self, node, rectangle, data_id):
        """recursive insert helper"""
        if node.is_leaf:
            # insert into leaf node
            node.entries.append((rectangle, data_id))
            if node.is_full():
                return self._split_node(node)
            return None
        else:
            #choose subtree and insert recursively
            idx = node.choose_subtree(rectangle)
            child_node = node.entries[idx][1]
            new_node = self._insert(child_node, rectangle, data_id)
            
            if new_node:
                #update MBR of the child node
                node.entries[idx] = (child_node.get_mbr(), child_node)
                #insert the new node
                node.entries.append((new_node.get_mbr(), new_node))
                if node.is_full():
                    return self._split_node(node)
            else:
                #update MBR of the child node
                node.entries[idx] = (child_node.get_mbr(), child_node)
            
            return None
    
    def _split_node(self, node):
        #split a node and return the new node
        node1, node2 = node.split()
        # copy data from node1 back to original node (node)
        node.entries = node1.entries
        return node2
    
    def search(self, query_rect):
        #search for data ids that intersect with query_rect
        result = []
        self._search(self.root, query_rect, result)
        return result
    
    def _search(self, node, query_rect, result):
        #recursive search helper"""
        for mbr, data in node.entries:
            if mbr.intersects(query_rect):
                if node.is_leaf:
                    result.append(data)
                else:
                    self._search(data, query_rect, result)
    
    # Add to the RTree class in rtree.py
    def print_structure(self):
        #Print the structure of the tree for debugging
        print(f"R-tree with max_entries={self.max_entries}")
        self._print_node(self.root)
        
    def _print_node(self, node, level=0, prefix="Root"):
        indent = "  " * level
        node_type = "Leaf" if node.is_leaf else "Internal"
        print(f"{indent}{prefix} ({node_type}): {len(node.entries)} entries")
        
        for i, (mbr, data) in enumerate(node.entries):
            if node.is_leaf:
                print(f"{indent}  Entry {i}: MBR={mbr}, Data={data[0] if isinstance(data, tuple) else data}")
            else:
                print(f"{indent}  Entry {i}: MBR={mbr}")
                self._print_node(data, level+1, f"Child {i}")
