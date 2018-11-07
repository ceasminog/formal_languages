from collections import deque
import syslog
import math
import copy


class Node:
    nextNodes = {}
    is_final = False
    is_root = False

    def __init__(self):
        self.is_final = False
        self.nextNodes = {}
        is_root = False

    def unite_nodes(self, other):
        if other.is_final:
            self.is_final = True
        if other.is_root:
            self.is_root = True
        self.nextNodes.update(other.nextNodes)
        syslog.syslog('nodes united')


class Automata:
    alpha = []
    root = Node()
    fin = Node()
    automat_cur_size = 0

    # @check_type_of_alpha
    def __init__(self, a):
        self.alpha = a
        self.root.is_root = True
        self.fin.is_final = True

    def add_new_node(self, cur, char_):
        new_node = Node()
        cur.nextNodes[char_] = new_node
        syslog.syslog('new node ' + char_)
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
                        cur = Node()
                        cur_right = Node()
                        cur_left.nextNodes[first_el] = cur
                        cur.nextNodes[second_el] = cur_right
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
                        if f_left.is_root:
                            self.root = f_left
                    else:
                        stack.append('$')
                    f_left = first.pop()
                    f_right = last.pop()
                    s_left = first.pop()
                    s_right = last.pop()
                    f_left.unite_nodes(s_left)
                    first.append(f_left)
                    f_right.unite_nodes(s_right)
                    last.append(f_right)
                    if f_left.is_root:
                        self.root = f_left

                if i == '#':
                    self.fin = last.pop()
                    return 'Automat is finished'

        return 'Something went wrong'


def bfs(cur_node, word_len, num_of_x, x, k):
    if (cur_node.nextNodes.__len__() == 0):
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


# decorator
def check_types(func):
    def wrapper(*args, **kwargs):
        if kwargs.__len__() != 0 or args.__len__() != 3:
            raise ValueError('Incorrect number of parameters')
        if not (isinstance(args[0], list) and
                isinstance(args[1], str) and
                isinstance(args[2], int)):
            raise ValueError('Incorrect input type')
        func(*args, **kwargs)

    return wrapper


@check_types
def find_shortest_string(alpha, x, k):
    my_automat = Automata(alpha)
    syslog.syslog(my_automat.alpha_to_automat())  # log
    root = my_automat.root
    print(bfs(root, 0, 0, x, k))
