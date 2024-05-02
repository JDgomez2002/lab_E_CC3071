
class LR0:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []
        self.transitions = {}

    def closure(self, I):
        J = []
        J.extend(I)
        added = True
        while added:
            added = False
            for item in J:
                if "." in item[1] and item[1].index(".") != len(item[1]) - 1:
                    next = item[1][item[1].index(".") + 1]
                    if next in self.grammar["NT"]:
                        for prod in self.grammar["P"]:
                            if prod[0] == next:
                                newItem = [prod[0], prod[1].copy()]
                                newItem[1].insert(0, ".")
                                if newItem not in J:
                                    J.append(newItem)
                                    added = True
        return J


    def goto(self, items, symbol):
        goToItems = []
        for item in items:
            if "." in item[1]:
                dotPosition = item[1].index(".")
                if dotPosition < len(item[1]) - 1:
                    nextItem = item[1][dotPosition + 1]
                    if nextItem == symbol:
                        newItem = [
                            item[0],
                            item[1][:dotPosition]
                            + [item[1][dotPosition + 1], "."]
                            + item[1][dotPosition + 2 :],
                        ]
                        goToItems.append(newItem)
        return self.closure(goToItems)
