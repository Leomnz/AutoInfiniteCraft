import graph_visualization


class Element:
    def __init__(self, name, emoji, first_discovery=False, parent1=None, parent2=None):
        self.name = name
        self.emoji = emoji
        self.first_discovery = first_discovery
        self.parent1 = parent1
        self.parent2 = parent2

    def set_parents(self, parent1, parent2):
        self.parent1 = parent1
        self.parent2 = parent2

    def add_to_graph(self):
        graph_visualization.add_element(self)

    def __str__(self, verbose=False):
        if verbose:
            return f"Name: {self.name}, Emoji: {self.emoji}, First Discovery: {self.first_discovery}, Parent1: {self.parent1}, Parent2: {self.parent2}"
        else:
            return f"{self.emoji} {self.name}"

    def __repr__(self):
        return self.__str__()
