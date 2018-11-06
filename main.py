from collections import deque
import syslog
import math


class Node:
    nextNodes = {}
    is_final = False
    dist_from_root = -1

    # unites 2 nodes
    def UniteNodes(self, other):
        if other.is_final:
            self.is_final = True
        self.nextNodes.update(other.nextNodes)


class Automata:
    alpha = []
    root = Node()
    automat_cur_size = 0

    # @check_type_of_alpha
    def __init__(self, a):
        self.alpha = a;

    def add_new_node(self, cur, char_):
        new_node = Node()
        cur.nextNodes[char_] = new_node
        return new_node

    def alpha_to_automat(self):
        stack = deque()
        stack.append('$')
        first = deque()
        first.append(self.root)
        last = deque()
        last.append(self.root)
        for i in self.alpha:
            if i.isalpha() or i == '1':
                stack.append(i)
            else:
                if i == '.':
                    second_el = stack.pop()
                    first_el = stack.pop()
                    if first_el != '$':
                        cur_left = Node()
                        cur_right = self.add_new_node(cur_left, first_el)
                        cur_right = self.add_new_node(cur_left, second_el)
                        first.append(cur_left)
                        last.append(cur_right)
                    else:
                        stack.append('$')
                        cur_left = first.pop()
                        cur_right = last.pop()
                        cur_right = self.add_new_node(cur_left, second_el)
                        first.append(cur_left)
                        last.append(cur_right)

                if i == '*':
                    cur_left = first.pop()
                    cur_right = last.pop()
                    cur_right.nextNodes['1'] = cur_left
                    cur_left.nextNodes['1'] = cur_right
                    first.append(cur_left)
                    last.append(cur_right)

                if i == '+':
                    first_el = stack.pop()
                    if first_el != '$':
                        f_left = first.pop()
                        f_right = self.add_new_node(f_left, first_el)
                        last.append(f_right)
                        first.append(f_left)
                        second_el = stack.pop()
                        if second_el != '$':
                            f_right = self.add_new_node(f_left, second_el)
                            last.append(f_right)
                            first.append(f_left)
                    else:
                        stack.append('$')
                    f_left = first.pop()
                    f_right = last.pop()
                    s_left = first.pop()
                    s_right = last.pop()
                    f_left.UniteNodes(s_left)
                    first.append(f_left)
                    f_right.UniteNodes(s_right)
                    last.append(f_right)

                if i == '#':
                    f_right = last.pop()
                    f_right.is_final = True
                    return 'Automat is finished'

        return 'Something went wrong'


def bfs(cur_node, word_len, num_of_x, x, k):
    if (cur_node.is_final):
        if (num_of_x == k):
            return word_len  # found it
        else:
            return math.inf  # +infinity
    cur_min = math.inf
    for key in cur_node.nextNodes:
        if (key == x):
            cur_min = min(cur_min, bfs(cur_node.nextNodes[key], word_len + 1, num_of_x + 1, x, k))
        else:
            cur_min = min(cur_min, bfs(cur_node.nextNodes[key], word_len + 1, num_of_x, x, k))
    return cur_min


def input_function():
    alpha = input()
    alpha = list(alpha)
    alpha.append('#')
    x = input()
    k = int(input())
    find_shortest_string(alpha, x, k)


# decorator
def check_types(func):
    def wrapper(*args, **kwargs):
        if kwargs.__len__() != 0 or args.__len__() != 3:
            raise ValueError('Incorrect number of parameters')
        if not (isinstance(args[0], list) or
                isinstance(args[1], str) or
                args[1].__len__() != 1 or isinstance(args[2], int)):
            raise ValueError('Incorrect input type')
        func(*args, **kwargs)

    return wrapper


@check_types
def find_shortest_string(alpha, x, k):
    my_automat = Automata(alpha)
    syslog.syslog(my_automat.alpha_to_automat())
    root = my_automat.root
    bfs(root, 0, 0, x, k)


input_function()
