from typing import Any
from queue import Queue
import math


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.

        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add(
                            (value1, value2))
                        self.binary_constraints[(variable1, variable2)].add(
                            (value2, value1))

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.

        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
        # YOUR CODE HERE (and remove the assertion below)
        # add all arcs to the queue
        arc_queue = Queue()
        for arc in self.binary_constraints.items():
            arc_queue.put(arc[0])
        while not arc_queue.empty():
            item = arc_queue.get()
            if self.revise(item[0],item[1]):
                if len(self.domains.get(item[0])) == 0:
                    return False
                # add neighbors to queue
                for edge in self.binary_constraints.items():
                    if edge[0][0] == item[0] and edge[0][1] != item[1]:
                        arc_queue.put((item[0],edge[0][1]))



        return True

    def revise(self, variable1, variable2):
        revised = False
        domain1 = self.domains.get(variable1)
        domain2 = self.domains.get(variable2)
        
        values_to_remove = set()
        for value1 in domain1.copy():  # Iterate over a copy
            violation = True
            for value2 in domain2:
                if not (
                    (variable1, variable2) in self.binary_constraints and
                    (value1, value2) not in self.binary_constraints[(variable1, variable2)]
                ) and not (
                    (variable2, variable1) in self.binary_constraints and
                    (value2, value1) not in self.binary_constraints[(variable2, variable1)]
                ):
                    violation = False
                    break
            if violation:
                values_to_remove.add(value1)
                revised = True
        
        domain1.difference_update(values_to_remove)  # Remove values after iteration
        return revised

                


    def backtracking_search(self, print_backtrack_called=False) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.

        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        # Use lists to keep track of backtrack calls and False returns
        backtrackCalled = [0]  # To count backtrack calls
        falseReturns = [0]     # To count the number of times False is returned
        
        def backtrack(assignment: dict[str, Any], backtrackCalled: list[int], falseReturns: list[int], counting=False):
            if counting:
                backtrackCalled[0] += 1
            # IF assignment complete, return assignment
            if len(assignment.keys()) == len(self.variables):
                return assignment
            # select an unassigned variable
            variable = self.select_unassigned_variable(assignment)[1]
            if variable is None or variable == 'none':
                falseReturns[0] += 1  # Increment the False counter when returning False
                return False
            for value in self.order_domain_value(variable, assignment):
                assignment[variable] = value
                result = backtrack(assignment, backtrackCalled, falseReturns, counting)
                if result:
                    return result
                del assignment[variable]
            falseReturns[0] += 1  # Increment the False counter when returning False after trying all values
            return False
        
        if print_backtrack_called:
            backtrackCalled[0] = 0  # Reset the counter before the search
            falseReturns[0] = 0     # Reset the false return counter before the search
            result = backtrack({}, backtrackCalled, falseReturns, True)
            return result, backtrackCalled[0], falseReturns[0]
        else:
            return backtrack({}, backtrackCalled, falseReturns)


    def select_unassigned_variable(self, assignment: dict[str, Any]) -> str:
        # find the variable with the fewest legal moves and return it
        upperBound = float('inf'), ""
        minVariable = [upperBound[0], "none"]
        for variable in self.variables:
            legalMoves = len(self.legal_moves(variable, assignment))
            if variable not in assignment and legalMoves < minVariable[0] and legalMoves > 0:
                minVariable = [legalMoves, variable]

        if minVariable[0] == upperBound:
            #If no legal moves then return None to indicate that there is no solution for this branch
            return None
        else:
            return minVariable

    def legal_moves(self, variable: str, assignment: dict[str, Any]) -> list:
        legal_moves = []
        for value1 in self.domains.get(variable):
            # check validity of value
            valid = True
            for variable2, value2 in assignment.items():
                # iterate over assignment
                #  To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
                if (
                    (variable, variable2) in self.binary_constraints and
                    (value1, value2) not in self.binary_constraints[(
                        variable, variable2)]
                ) or (
                    (variable2, variable) in self.binary_constraints and
                    (value1, value2) not in self.binary_constraints[(
                        variable2, variable)]
                ):
                    valid = False
                    break
            if valid:
                legal_moves.append(value1)
        return legal_moves

    def order_domain_value(self, variable: str, assignment: dict[str, Any]):
        # not really optimal but it should be ideal variable and only legal moves, so that is something
        # probably there is a heuristic to find ideal first assignment but I dont know it
        return self.legal_moves(variable, assignment)


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables

    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]
