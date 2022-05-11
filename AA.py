def aa_search_tree(v1, v2):
    if v1 == v2:
        return 0
    else:
        return -1 if v1 < v2 else 1


def make_cmp_fn_by_key(key):
    return lambda v1, v2: aa_search_tree(key(v1), key(v2))


class AastNode():
    def __init__(self, val, parent, direction=None):
        self.level = self.len = 1
        self.left = self.right = None
        self.val = val
        self.is_array = False
        self.parent = parent
        self.direction = direction

    def getval(self):
        return self.val if not self.is_array else self.val[0]

    def addval(self, val):
        if self.is_array:
            self.val.append(val)
        else:
            self.val = [self.val, val]
            self.is_array = True
        self.len += 1

    def dropval(self, val, allcopies):
        if self.is_array:
            i = 0
            while i < self.len:
                if val == self.val[i]:
                    self.len -= 1
                    self.val = self.val[0: i] + self.val[i + 1:]
                    if not allcopies:
                        break
        else:
            if val == self.val:
                self.len = 0


class sbst():
    """
    Класс, в котором создаётся само-балансирующего дерево поиска
    """
    def __init__(self, comparison_func=aa_search_tree, source=None):
        self.root = None
        self.comp_f = comparison_func
        self._len = 0
        if source != None:
            self.addfrom(source)

    def __len__(self):
        return self._len
    def add(self, val):
        """
        Добавление значения в дерево
        :param val: значение
        :return: val
        """
        self.root = self._insert_into_node(self.root, val, None)

    def addfrom(self, source):
        """
        Добавление из других источников/ через функцию
        :param source: источник
        :return:
        """
        for val in source:
            self.root = self._insert_into_node(self.root, val, None)
    def _skew(self, node):
        """
         Устранение левого горизонтального ребра. Делаем правое вращение, чтобы заменить поддерево, содержащее левую
         горизонтальную связь, на поддерево, содержащее разрешенную правую горизонтальную связь.
        :param node: Узел
        :return: Node
        """
        if node == None or node.left == None:
            return node
        elif node.left.level == node.level:
            L = node.left
            node.left = L.right
            if L.right:
                L.right.parent = node
                L.right.direction = 'L'
            L.right = node
            L.parent = node.parent
            L.direction = node.direction
            node.parent = L
            node.direction = 'R'
            return L
        else:
            return node
    def _split(self, node):
        """
       Устранение двух последовательных правых горизонтальных ребер. Делаем левое вращение и увеличиваем уровень,
       чтобы заменить поддерево, содержащее две или более последовательных правильных горизонтальных связи, на вершину,
       содержащую два поддерева с меньшим уровнем.
        :param node: узел
        :return: node
        """
        if node == None or node.right == None or node.right.right == None:
            return node
        elif node.level == node.right.right.level:
            R = node.right
            node.right = R.left
            if R.left:
                R.left.parent = node
                R.left.direction = 'R'
            R.left = node
            R.parent = node.parent
            R.direction = node.direction
            node.parent = R
            node.direction = 'L'
            R.level += 1
            return R
        else:
            return node

    def _insert_into_node(self, node, val, parent, direction=None):
        """
        Вставка в узел
        :param node: Узел
        :param val: Значение
        :param parent: Родитель
        :param direction: Путь
        :return:
        """

        if node == None:
            self._len += 1
            return AastNode(val, parent, direction)
        else:
            cmp = self.comp_f(val, node.getval())
            if cmp < 0:
                node.left = self._insert_into_node(node.left, val, node, 'L')
            elif cmp > 0:
                node.right = self._insert_into_node(node.right, val, node, 'R')
            else:
                self._len += 1
                node.addval(val)
                return node
            node = self._skew(node)
            node = self._split(node)
            return node

    def forward_from(self, start=None, inclusive=True,
                     stop=None, stop_incl=False):
        node = self.root
        curr = None
        while node:
            cmp = -1 if start == None else self.comp_f(start, node.getval())
            if cmp == 0:
                if inclusive:
                    curr = node
                    node = None
                else:
                    node = node.right
            elif cmp < 0:
                curr = node
                node = node.left
            else:
                node = node.right
        while curr:
            if curr.len > 0:
                if stop != None:
                    cmp = self.comp_f(curr.getval(), stop)
                    if cmp > 0 or cmp == 0 and not stop_incl:
                        return
                if curr.is_array:
                    i = 0
                    while i < curr.len:
                        yield curr.val[i]
                        i += 1
                else:
                    yield curr.val
            # step forward
            if curr.right:
                curr = curr.right
                while curr.left:
                    curr = curr.left
            else:
                new_curr = curr.parent
                while new_curr and curr.direction == 'R':
                    curr = new_curr
                    new_curr = curr.parent
                curr = new_curr

    def min(self, limit=None, inclusive=True):
        """
        Возвращает минимальное значение
        :param limit: окончательное значение
        :param inclusive: От какого значенимя высчитывать min()
        :return: val
        """
        for val in self.forward_from(limit, inclusive):
            return val
        return None

    def nodes_list(self):
        return self.nodes_list(self.root)

    def nodes_list(self, node):
        """
        Функция: Список узлов
        :param node: узел
        :return: self.nodes_list(node.left) + [node] \
                   + self.nodes_list(node.right)
        """
        if not node:
            return []
        else:
            return self.nodes_list(node.left) + [node] \
                   + self.nodes_list(node.right)

    def remove(self, val, allcopies=False):

        if val != None:
            self.root = self._delete(val, self.root, allcopies)

    def _delete(self, val, node, allcopies):
        """

        :param val: Значение
        :param node: Узел
        :param allcopies: Все подобные значиения
        :return:
        """
        if node == None:
            return None
        cmp = self.comp_f(val, node.getval())
        if cmp > 0:
            node.right = self._delete(val, node.right, allcopies)
        elif cmp < 0:
            node.left = self._delete(val, node.left, allcopies)
        else:
            node_len_before_deletion = node.len
            node.dropval(val, allcopies)
            self._len -= node_len_before_deletion - node.len
            if node.len == 0:
                if node.left == None and node.right == None:
                    return None
                elif node.left == None:
                    NN = node.right
                    while NN.left:
                        NN = NN.left
                    if NN != node.right:
                        if NN.right:
                            NN.right.parent = NN.parent
                            NN.right.direction = 'L'
                        NN.parent.left = NN.right
                        RN = NN.parent
                        while RN != node:
                            self.decrease_level(RN)
                            RN = RN.parent
                        NN.right = node.right
                        NN.right.parent = NN
                    NN.parent = node.parent
                    NN.direction = node.direction
                    NN.level = node.level
                    node.right = NN
                    node = NN
                else:
                    PN = node.left
                    while PN.right:
                        PN = PN.right
                    if PN != node.left:
                        if PN.left:
                            PN.left.parent = PN.parent
                            PN.left.direction = 'R'
                        PN.parent.right = PN.left
                        RN = PN.parent
                        while RN != node:
                            self.decrease_level(RN)
                            RN = RN.parent
                        PN.left = node.left
                        PN.left.parent = PN
                    PN.parent = node.parent
                    PN.direction = node.direction
                    PN.level = node.level
                    PN.right = node.right
                    if PN.right:
                        PN.right.parent = PN
                    node.left = PN
                    node = PN
        self.decrease_level(node)
        return node

    def decrease_level(self, node):
        """
        Данная функция понижает уровень узла
        :param node: узел дерева
        :return: None
        """
        should_be = max(node.left.level if node.left else 0, \
                        node.right.level if node.right else 0) + 1
        if should_be < node.level:
            node.level = should_be
            if should_be < (node.right.level if node.right else 0):
                node.right.level = should_be

    def calc_depth(self, root, current_length):
        """

        :param root: Корень дерева
        :param current_length: Текущая длинна
        :return: max(left, right)
        """
        left = 0
        right = 0
        if root is None:
            return current_length
        if not root.left is None:
            left = self.calc_depth(root.left, current_length + 1)
        if not root.right is None:
            right = self.calc_depth(root.right, current_length + 1)
        return max(left, right)

    def bp(self):
        """
        Обход дерева
        :return: val
        """
        return self.bypass(self.root, path=[self.calc_depth(self.root, 0)])

    def bypass(self, elem, long=0, path=[]):
        """
        Обходит дерево и записывает путь обхода в path.
        Данная функция нужна для отрисовки дерева.
        :param long: глубина дерева (изначально равно нулю)
        :param path: путь обхода, а на первом месте максимальная глубина дерева
        :return: path
        """

        if elem is None:
            return path
        else:
            a = [elem.val, elem.val]
            path.append(a)
            if elem.left is not None:
                path = self.bypass(elem.left, long+1, path)
                path.append([elem.val, None])

            if elem.right is not None:
                path = self.bypass(elem.right, long+1, path)
                path.append([elem.val, None])

            if long > path[0]:
                path[0] = long

            return path