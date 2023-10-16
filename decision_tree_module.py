### Made by Haris Rasul
### Oct 15th 2023
### Purpose: Create Descision tee with features and structure etc.
# decision_tree_module.py

# Features
class Feature:
    def __init__(self, name, possible_values):
        self.name = name
        self.possible_values = possible_values
        
    def validate_value(self, value):
        return value in self.possible_values


# Tree Structure
class TreeNode:
    def __init__(self, parent=None):
        self.parent = parent
        self.left = None
        self.right = None
        
    def depth(self):
        if self.parent:
            return 1 + self.parent.depth()
        return 0

class Tree:
    def __init__(self):
        self.root = TreeNode()
        
    def is_complete(self):
        # Check if all leaf nodes have the same depth
        leaf_depths = [leaf.depth() for leaf in self.get_leaves()]
        return all(depth == leaf_depths[0] for depth in leaf_depths)
        
    def get_leaves(self):
        # A method to retrieve all leaf nodes. This will be a recursive traversal.
        pass


# Decision Tree Structure
class DecisionTreeNode(TreeNode):
    def __init__(self, feature=None, threshold=None, label=None, parent=None):
        super().__init__(parent)
        self.feature = feature
        self.threshold = threshold
        self.label = label

class DecisionTree(Tree):
    def __init__(self):
        super().__init__()
        self.root = DecisionTreeNode()

    # Alpha predict function .
    def predict(self, data_point):
        """
        Predict the label based on the provided data_point.
        
        Parameters:
        - data_point (dict): Dictionary with feature names as keys and feature values as items.
        
        Returns:
        - label (str): Predicted label for the given data_point.
        """
        node = self.root
        while node.label is None:  #  until we reach a leaf node
            threshold = node.threshold
            feature_value = data_point[node.feature.name]
            
            if isinstance(feature_value, (int, float)):
                if feature_value <= threshold:
                    node = node.left
                else:
                    node = node.right
            else:
                if feature_value == threshold:
                    node = node.left
                else:
                    node = node.right
                    
        return node.label
    
    def accuracy(self, dataset, labels):
        """
        Calculate the accuracy of the decision tree on a labeled dataset.
        
        Parameters:
        - dataset (list of dict): List of data points with each data point being a dictionary 
          of feature values.
        - labels (list): List of actual labels corresponding to the data points in the dataset.
        
        Returns:
        - accuracy (float): The accuracy of the decision tree on the given dataset.
        """
        correct_predictions = 0
        
        for data_point, label in zip(dataset, labels):
            if self.predict(data_point) == label:
                correct_predictions += 1
                
        return correct_predictions / len(dataset)

    # Need to rework this with proper visualization - keep as is for now; 
    def visualize(self, node=None, indent=""):
        """
        Visualize the decision tree using a simple text-based representation.
        """
        if node is None:
            node = self.root
            
        if node.label:
            print(indent + "Label: " + node.label)
            return
        
        print(indent + f"If {node.feature.name} <= {node.threshold} :")
        self.visualize(node=node.left, indent=indent + "  ")
        
        print(indent + f"If {node.feature.name} > {node.threshold} :")
        self.visualize(node=node.right, indent=indent + "  ")