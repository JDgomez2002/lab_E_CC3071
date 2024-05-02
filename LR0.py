import pydotplus

class LR0:
    def __init__(self, grammar):
        self.grammar = grammar
        self.states = []
        self.transitions = {}
        self.generateLR0()

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

    def generateLR0(self):

        grammar = self.grammar

        states = []
        transitions = {}

        # Aumentamos la gramtica, con S' -> S
        S = grammar["P"][0][0]
        augmented_production = [S + "'", [S]]
        grammar["P"].insert(0, augmented_production)
        grammar["NT"].insert(0, S + "'")

        # the init state is closure({S' -> .S})
        first = [grammar["P"][0][0], grammar["P"][0][1].copy()]
        first[1].insert(0, ".")
        initial_state = self.closure([first])
        states.append(initial_state)

        state_queue = [initial_state]
        while state_queue:
            current_state = state_queue.pop(0)
            kernel_items = [
                item
                for item in current_state
                if item[1][0] != "." or item == current_state[0]
            ]
            accept_item = None

            # The state is an accept state if it contains a production of the form S' -> S. (with the dot at the end)
            for item in kernel_items:
                if item[0] == grammar["P"][0][0] and "." == item[1][-1]:
                    accept_item = item

            print("---------------")
            print(f"----- I{states.index(current_state)} -----")
            print("---------------")
            print("Kernel items")
            for item in current_state:
                if item in kernel_items:
                    print(f"\t{item[0]} -> {item[1]}")

            print("\nClosure items")
            for item in current_state:
                if item not in kernel_items:
                    print(f"\t{item[0]} -> {item[1]}")

            print()

            current_state_index = states.index(current_state)
            if accept_item is not None:
                if current_state_index not in transitions:
                    transitions[current_state_index] = {}
                transitions[current_state_index]["$"] = "Accept"

            for symbol in grammar["items"]:
                next_state = self.goto(
                    current_state, symbol
                )  # Calculamos el siguiente estado, dado el simbolo
                if next_state and next_state not in states:
                    states.append(next_state)
                    state_queue.append(next_state)
                if next_state:
                    next_state_index = states.index(next_state)
                    if current_state_index not in transitions:
                        transitions[current_state_index] = {}
                    transitions[current_state_index][symbol] = next_state_index

        self.states = states
        self.transitions = transitions
        self.grammar = grammar

        return states, transitions, grammar
