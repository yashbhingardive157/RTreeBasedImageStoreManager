# rtree_node.py
class RTreeNode:
    def __init__(self, is_leaf=True, max_entries=4):
        self.is_leaf = is_leaf
        self.max_entries = max_entries
        self.entries = []  #list of (rectangle,child_node)pairs
    
    def is_full(self):
        #Check if the node is full
        return len(self.entries) >= self.max_entries
    
    def get_mbr(self):
        #Get the minimum bounding rectangle for all entries
        if not self.entries:
            return None
        
        mbr = self.entries[0][0]
        for i in range(1, len(self.entries)):
            mbr = mbr.enlarge(self.entries[i][0])
        return mbr
    
    def choose_subtree(self, rectangle):
        #Choose the best subtree to insert a new rectangle
        min_increase = float('inf')
        best_idx = 0
        
        for i, (mbr, _) in enumerate(self.entries):
            increase = mbr.enlarge(rectangle).area() - mbr.area()
            if increase < min_increase:
                min_increase = increase
                best_idx = i
                
        return best_idx
    
    def split(self):
        #Split an overflowing node into two nodes
        # Use the quadratic split algorithm
        # First, find the two entries that waste the most area if put together
        max_waste = -1
        seeds = (0, 0)
        
        for i in range(len(self.entries)):
            for j in range(i + 1, len(self.entries)):
                mbr_i = self.entries[i][0]
                mbr_j = self.entries[j][0]
                waste = mbr_i.enlarge(mbr_j).area() - mbr_i.area() - mbr_j.area()
                if waste > max_waste:
                    max_waste = waste
                    seeds = (i, j)
        
        # Create two groups with the seeds
        group1 = [self.entries[seeds[0]]]
        group2 = [self.entries[seeds[1]]]
        remaining = [e for i, e in enumerate(self.entries) if i != seeds[0] and i != seeds[1]]
        
        # Assign remaining entries to groups
        while remaining:
            # If one group is getting too small, assign all remaining entries to it
            if len(group1) + len(remaining) <= 1:
                group1.extend(remaining)
                break
            elif len(group2) + len(remaining) <= 1:
                group2.extend(remaining)
                break
                
            # Find entry that has maximum difference in area enlargement
            # between the two groups
            max_diff = -1
            best_idx = 0
            best_group = 1
            
            for i, entry in enumerate(remaining):
                mbr1 = group1[0][0]
                for e in group1[1:]:
                    mbr1 = mbr1.enlarge(e[0])
                
                mbr2 = group2[0][0]
                for e in group2[1:]:
                    mbr2 = mbr2.enlarge(e[0])
                
                d1 = mbr1.enlarge(entry[0]).area() - mbr1.area()
                d2 = mbr2.enlarge(entry[0]).area() - mbr2.area()
                diff = abs(d1 - d2)
                
                if diff > max_diff:
                    max_diff = diff
                    best_idx = i
                    best_group = 1 if d1 < d2 else 2
            
            # Add the entry to the chosen group
            if best_group == 1:
                group1.append(remaining[best_idx])
            else:
                group2.append(remaining[best_idx])
            
            remaining.pop(best_idx)
        
        # Create two new nodes
        node1 = RTreeNode(is_leaf=self.is_leaf, max_entries=self.max_entries)
        node1.entries = group1
        
        node2 = RTreeNode(is_leaf=self.is_leaf, max_entries=self.max_entries)
        node2.entries = group2
        
        return node1, node2
