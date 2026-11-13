"""
Auto-Assignment Generator for Personalised Learning.
Generates MCQ assignments with questions based on topic content.
Matches the actual database schema:
  - assignments: id, module_id, title, difficulty_mix
  - assignment_questions: id, assignment_id, question_text, option_a/b/c/d, correct_option, difficulty, concept
"""

from utils import database as db


def query_db(sql, args=(), one=False):
    if isinstance(args, list):
        args = tuple(args)
    sql_upper = sql.strip().upper()
    if sql_upper.startswith('SELECT') or sql_upper.startswith('SHOW'):
        if one:
            return db.fetch_one(sql, args)
        return db.fetch_all(sql, args)
    else:
        return db.execute(sql, args)


# Comprehensive question bank organized by subject/topic
QUESTION_BANK = {
    'Data Structures': {
        'Arrays': [
            {'q': 'What is the time complexity of accessing an element in an array by index?', 'a': 'O(1)', 'b': 'O(n)', 'c': 'O(log n)', 'd': 'O(n²)', 'ans': 'A', 'diff': 'Easy', 'exp': 'Array access by index is O(1) because elements are stored at contiguous memory locations.'},
            {'q': 'Which is NOT a valid array operation?', 'a': 'Traversal', 'b': 'Insertion', 'c': 'Enqueue', 'd': 'Searching', 'ans': 'C', 'diff': 'Easy', 'exp': 'Enqueue is a queue operation, not an array operation.'},
            {'q': 'What is the worst-case time complexity for searching in an unsorted array?', 'a': 'O(1)', 'b': 'O(log n)', 'c': 'O(n)', 'd': 'O(n²)', 'ans': 'C', 'diff': 'Easy', 'exp': 'Linear search in unsorted array requires checking each element.'},
            {'q': 'In which memory layout are arrays stored?', 'a': 'Contiguous', 'b': 'Non-contiguous', 'c': 'Random', 'd': 'Linked', 'ans': 'A', 'diff': 'Easy', 'exp': 'Arrays are stored in contiguous memory locations.'},
            {'q': 'What happens when you insert an element in the middle of an array?', 'a': 'Nothing changes', 'b': 'Elements shift right', 'c': 'Array resizes', 'd': 'Error occurs', 'ans': 'B', 'diff': 'Medium', 'exp': 'Elements after insertion point must shift right.'},
            {'q': 'What is a 2D array commonly called?', 'a': 'Matrix', 'b': 'Stack', 'c': 'Queue', 'd': 'Heap', 'ans': 'A', 'diff': 'Easy', 'exp': 'A 2D array is commonly called a matrix.'},
            {'q': 'What is the main disadvantage of arrays?', 'a': 'Slow access', 'b': 'Fixed size', 'c': 'No indexing', 'd': 'High memory', 'ans': 'B', 'diff': 'Easy', 'exp': 'Arrays have fixed size and cannot grow dynamically.'},
            {'q': 'What index does the first element have in most languages?', 'a': '1', 'b': '0', 'c': '-1', 'd': 'Depends', 'ans': 'B', 'diff': 'Easy', 'exp': 'Most languages use 0-based indexing.'},
            {'q': 'Time complexity to delete last element from array?', 'a': 'O(1)', 'b': 'O(n)', 'c': 'O(log n)', 'd': 'O(n²)', 'ans': 'A', 'diff': 'Easy', 'exp': 'Deleting last element requires no shifting.'},
            {'q': 'What is the space complexity of an array with n elements?', 'a': 'O(1)', 'b': 'O(n)', 'c': 'O(n²)', 'd': 'O(log n)', 'ans': 'B', 'diff': 'Easy', 'exp': 'Space complexity is O(n) as it stores n elements.'},
        ],
        'Linked Lists': [
            {'q': 'What does each node in a linked list contain?', 'a': 'Only data', 'b': 'Data and a pointer', 'c': 'Only pointer', 'd': 'Index and data', 'ans': 'B', 'diff': 'Easy', 'exp': 'Each node contains data and a pointer to the next node.'},
            {'q': 'What is the time complexity of searching in a linked list?', 'a': 'O(1)', 'b': 'O(log n)', 'c': 'O(n)', 'd': 'O(n²)', 'ans': 'C', 'diff': 'Easy', 'exp': 'Searching requires traversing the list sequentially.'},
            {'q': 'In a doubly linked list, each node has:', 'a': 'One pointer', 'b': 'Two pointers', 'c': 'Three pointers', 'd': 'No pointers', 'ans': 'B', 'diff': 'Easy', 'exp': 'Doubly linked lists have pointers to next and previous nodes.'},
            {'q': 'What points to NULL in a singly linked list?', 'a': 'Head node', 'b': 'Middle node', 'c': 'Last node', 'd': 'Every node', 'ans': 'C', 'diff': 'Easy', 'exp': 'The last node points to NULL.'},
            {'q': 'Main advantage of linked lists over arrays?', 'a': 'Faster access', 'b': 'Dynamic size', 'c': 'Less memory', 'd': 'Sorted data', 'ans': 'B', 'diff': 'Easy', 'exp': 'Linked lists can grow and shrink dynamically.'},
            {'q': 'What is the time complexity to insert at the beginning of a linked list?', 'a': 'O(1)', 'b': 'O(n)', 'c': 'O(log n)', 'd': 'O(n²)', 'ans': 'A', 'diff': 'Medium', 'exp': 'Inserting at head is O(1) as we just update the head pointer.'},
            {'q': 'What is a circular linked list?', 'a': 'List with loops', 'b': 'Last node points to head', 'c': 'Sorted list', 'd': 'Doubly linked', 'ans': 'B', 'diff': 'Medium', 'exp': 'In circular linked list, the last node points back to the head.'},
            {'q': 'How do you find the middle of a linked list efficiently?', 'a': 'Two pointer technique', 'b': 'Binary search', 'c': 'Hash map', 'd': 'Recursion', 'ans': 'A', 'diff': 'Medium', 'exp': 'Slow and fast pointers find the middle in one pass.'},
            {'q': 'What is the space complexity of a linked list with n nodes?', 'a': 'O(1)', 'b': 'O(n)', 'c': 'O(log n)', 'd': 'O(n²)', 'ans': 'B', 'diff': 'Easy', 'exp': 'Space is O(n) for n nodes, each with data and pointer.'},
            {'q': 'Which linked list allows traversal in both directions?', 'a': 'Singly linked', 'b': 'Doubly linked', 'c': 'Circular', 'd': 'None', 'ans': 'B', 'diff': 'Easy', 'exp': 'Doubly linked lists support bidirectional traversal.'},
        ],
        'Stacks': [
            {'q': 'Which data structure follows LIFO principle?', 'a': 'Queue', 'b': 'Stack', 'c': 'Array', 'd': 'Linked List', 'ans': 'B', 'diff': 'Easy', 'exp': 'Stack follows Last In First Out (LIFO) principle.'},
            {'q': 'What operation removes an element from a stack?', 'a': 'Push', 'b': 'Pop', 'c': 'Enqueue', 'd': 'Insert', 'ans': 'B', 'diff': 'Easy', 'exp': 'Pop removes the top element from a stack.'},
            {'q': 'What is stack overflow?', 'a': 'Stack is empty', 'b': 'Stack is full', 'c': 'Stack is corrupted', 'd': 'Stack underflow', 'ans': 'B', 'diff': 'Easy', 'exp': 'Stack overflow occurs when trying to push to a full stack.'},
            {'q': 'What is the time complexity of push operation?', 'a': 'O(1)', 'b': 'O(n)', 'c': 'O(log n)', 'd': 'O(n²)', 'ans': 'A', 'diff': 'Easy', 'exp': 'Push is O(1) as it only modifies the top.'},
            {'q': 'Which is a common application of stacks?', 'a': 'Print queue', 'b': 'Function call management', 'c': 'CPU scheduling', 'd': 'Memory allocation', 'ans': 'B', 'diff': 'Medium', 'exp': 'Stacks are used for managing function calls (call stack).'},
            {'q': 'What does peek operation do?', 'a': 'Removes top element', 'b': 'Returns top element without removing', 'c': 'Adds element', 'd': 'Searches element', 'ans': 'B', 'diff': 'Easy', 'exp': 'Peek returns the top element without removing it.'},
            {'q': 'Which data structure is used for undo functionality?', 'a': 'Queue', 'b': 'Stack', 'c': 'Tree', 'd': 'Graph', 'ans': 'B', 'diff': 'Easy', 'exp': 'Stacks are used for undo operations (LIFO).'},
            {'q': 'What is the minimum number of stacks needed to implement a queue?', 'a': '1', 'b': '2', 'c': '3', 'd': '4', 'ans': 'B', 'diff': 'Medium', 'exp': 'Two stacks are needed to implement a queue.'},
            {'q': 'Infix to postfix conversion uses which data structure?', 'a': 'Queue', 'b': 'Stack', 'c': 'Array', 'd': 'Tree', 'ans': 'B', 'diff': 'Medium', 'exp': 'Stacks are used for operator precedence in conversion.'},
            {'q': 'What is the time complexity of pop operation?', 'a': 'O(1)', 'b': 'O(n)', 'c': 'O(log n)', 'd': 'Depends on implementation', 'ans': 'A', 'diff': 'Easy', 'exp': 'Pop is O(1) as it only modifies the top pointer.'},
        ],
        'Trees': [
            {'q': 'What is a binary tree?', 'a': 'Tree with 2 nodes', 'b': 'Tree where each node has at most 2 children', 'c': 'Tree with 2 levels', 'd': 'Sorted tree', 'ans': 'B', 'diff': 'Easy', 'exp': 'Binary tree nodes have at most 2 children.'},
            {'q': 'What is the height of a tree with one node?', 'a': '0', 'b': '1', 'c': '2', 'd': 'Undefined', 'ans': 'A', 'diff': 'Easy', 'exp': 'Height of a single node tree is 0.'},
            {'q': 'What is a BST?', 'a': 'Binary Search Tree', 'b': 'Best Search Tree', 'c': 'Balanced Search Tree', 'd': 'Basic Search Tree', 'ans': 'A', 'diff': 'Easy', 'exp': 'BST stands for Binary Search Tree.'},
            {'q': 'In a BST, left child is always:', 'a': 'Greater than parent', 'b': 'Less than parent', 'c': 'Equal to parent', 'd': 'Any value', 'ans': 'B', 'diff': 'Easy', 'exp': 'Left child is always less than parent in BST.'},
            {'q': 'What traversal visits root first?', 'a': 'In-order', 'b': 'Pre-order', 'c': 'Post-order', 'd': 'Level-order', 'ans': 'B', 'diff': 'Easy', 'exp': 'Pre-order visits root before children.'},
            {'q': 'What is the time complexity of search in a balanced BST?', 'a': 'O(1)', 'b': 'O(n)', 'c': 'O(log n)', 'd': 'O(n²)', 'ans': 'C', 'diff': 'Medium', 'exp': 'Balanced BST search is O(log n).'},
            {'q': 'What is an AVL tree?', 'a': 'Sorted array', 'b': 'Self-balancing BST', 'c': 'Complete binary tree', 'd': 'Heap', 'ans': 'B', 'diff': 'Medium', 'exp': 'AVL tree is a self-balancing binary search tree.'},
            {'q': 'Which traversal gives sorted order in BST?', 'a': 'Pre-order', 'b': 'Post-order', 'c': 'In-order', 'd': 'Level-order', 'ans': 'C', 'diff': 'Medium', 'exp': 'In-order traversal of BST gives sorted sequence.'},
            {'q': 'What is a leaf node?', 'a': 'Root node', 'b': 'Node with no children', 'c': 'Node with one child', 'd': 'Internal node', 'ans': 'B', 'diff': 'Easy', 'exp': 'A leaf node has no children.'},
            {'q': 'What is the maximum number of nodes at level l?', 'a': 'l', 'b': '2^l', 'c': '2l', 'd': 'l²', 'ans': 'B', 'diff': 'Medium', 'exp': 'Maximum nodes at level l is 2^l.'},
        ],
        'Graphs': [
            {'q': 'What data structure is used for BFS?', 'a': 'Stack', 'b': 'Queue', 'c': 'Array', 'd': 'Tree', 'ans': 'B', 'diff': 'Easy', 'exp': 'BFS uses a queue for level-by-level traversal.'},
            {'q': 'What data structure is used for DFS?', 'a': 'Queue', 'b': 'Stack (or recursion)', 'c': 'Array', 'd': 'Heap', 'ans': 'B', 'diff': 'Easy', 'exp': 'DFS uses a stack (or recursive call stack).'},
            {'q': 'What is a directed graph?', 'a': 'Edges have no direction', 'b': 'Edges have direction', 'c': 'No cycles', 'd': 'Connected graph', 'ans': 'B', 'diff': 'Easy', 'exp': 'Directed graphs have edges with direction.'},
            {'q': 'What is the time complexity of BFS?', 'a': 'O(1)', 'b': 'O(V + E)', 'c': 'O(V * E)', 'd': 'O(V²)', 'ans': 'B', 'diff': 'Medium', 'exp': 'BFS is O(V + E) where V is vertices and E is edges.'},
            {'q': 'What is a weighted graph?', 'a': 'Graph with weights on edges', 'b': 'Heavy graph', 'c': 'Graph with many nodes', 'd': 'Directed graph', 'ans': 'A', 'diff': 'Easy', 'exp': 'Weighted graphs have values on edges.'},
            {'q': 'What algorithm finds shortest path in weighted graph?', 'a': 'BFS', 'b': 'DFS', 'c': 'Dijkstra', 'd': 'Kruskal', 'ans': 'C', 'diff': 'Medium', 'exp': "Dijkstra's algorithm finds shortest path in weighted graphs."},
            {'q': 'What is an adjacency matrix?', 'a': 'List of edges', 'b': '2D array representing connections', 'c': 'Tree representation', 'd': 'Heap structure', 'ans': 'B', 'diff': 'Easy', 'exp': 'Adjacency matrix is a 2D array showing node connections.'},
            {'q': 'What is a cycle in a graph?', 'a': 'Disconnected nodes', 'b': 'Path that starts and ends at same node', 'c': 'All nodes connected', 'd': 'No edges', 'ans': 'B', 'diff': 'Easy', 'exp': 'A cycle is a path that returns to the starting node.'},
            {'q': 'What is the space complexity of adjacency list?', 'a': 'O(V²)', 'b': 'O(V + E)', 'c': 'O(E)', 'd': 'O(V)', 'ans': 'B', 'diff': 'Medium', 'exp': 'Adjacency list space is O(V + E).'},
            {'q': 'What is topological sort used for?', 'a': 'Finding cycles', 'b': 'Ordering tasks with dependencies', 'c': 'Finding shortest path', 'd': 'Finding MST', 'ans': 'B', 'diff': 'Medium', 'exp': 'Topological sort orders tasks respecting dependencies.'},
        ],
        'Sorting Algorithms': [
            {'q': 'What is the best case time complexity of Bubble Sort?', 'a': 'O(n)', 'b': 'O(n²)', 'c': 'O(log n)', 'd': 'O(n log n)', 'ans': 'A', 'diff': 'Easy', 'exp': 'Bubble sort best case is O(n) with optimization.'},
            {'q': 'Which sorting algorithm has O(n log n) average case?', 'a': 'Bubble Sort', 'b': 'Selection Sort', 'c': 'Merge Sort', 'd': 'Insertion Sort', 'ans': 'C', 'diff': 'Easy', 'exp': 'Merge Sort has O(n log n) in all cases.'},
            {'q': 'What is the space complexity of Merge Sort?', 'a': 'O(1)', 'b': 'O(log n)', 'c': 'O(n)', 'd': 'O(n²)', 'ans': 'C', 'diff': 'Medium', 'exp': 'Merge Sort requires O(n) extra space.'},
            {'q': 'Which sorting is stable?', 'a': 'Quick Sort', 'b': 'Heap Sort', 'c': 'Merge Sort', 'd': 'Selection Sort', 'ans': 'C', 'diff': 'Medium', 'exp': 'Merge Sort preserves relative order of equal elements.'},
            {'q': 'What is the worst case of Quick Sort?', 'a': 'O(n)', 'b': 'O(n log n)', 'c': 'O(n²)', 'd': 'O(log n)', 'ans': 'C', 'diff': 'Medium', 'exp': 'Quick Sort worst case is O(n²) with poor pivot selection.'},
            {'q': 'Which sorting uses divide and conquer?', 'a': 'Bubble Sort', 'b': 'Insertion Sort', 'c': 'Merge Sort', 'd': 'Selection Sort', 'ans': 'C', 'diff': 'Easy', 'exp': 'Merge Sort uses divide and conquer strategy.'},
            {'q': 'What is the space complexity of Quick Sort?', 'a': 'O(n)', 'b': 'O(log n)', 'c': 'O(1)', 'd': 'O(n²)', 'ans': 'B', 'diff': 'Medium', 'exp': 'Quick Sort uses O(log n) stack space.'},
            {'q': 'Which is the fastest sorting algorithm in practice?', 'a': 'Bubble Sort', 'b': 'Quick Sort', 'c': 'Selection Sort', 'd': 'Insertion Sort', 'ans': 'B', 'diff': 'Easy', 'exp': 'Quick Sort is generally fastest in practice.'},
            {'q': 'What is the time complexity of Insertion Sort?', 'a': 'O(n)', 'b': 'O(n log n)', 'c': 'O(n²)', 'd': 'O(log n)', 'ans': 'C', 'diff': 'Easy', 'exp': 'Insertion Sort is O(n²) in worst and average case.'},
            {'q': 'Which sorting is best for nearly sorted arrays?', 'a': 'Merge Sort', 'b': 'Quick Sort', 'c': 'Insertion Sort', 'd': 'Heap Sort', 'ans': 'C', 'diff': 'Medium', 'exp': 'Insertion Sort is efficient for nearly sorted data.'},
        ],
    },
    'Database Management Systems': {
        'SQL Basics': [
            {'q': 'Which SQL statement retrieves data?', 'a': 'GET', 'b': 'SELECT', 'c': 'FETCH', 'd': 'RETRIEVE', 'ans': 'B', 'diff': 'Easy', 'exp': 'SELECT is the standard SQL query statement.'},
            {'q': 'What does WHERE clause do?', 'a': 'Groups data', 'b': 'Filters rows', 'c': 'Sorts data', 'd': 'Joins tables', 'ans': 'B', 'diff': 'Easy', 'exp': 'WHERE filters rows based on conditions.'},
            {'q': 'Which function counts rows?', 'a': 'SUM', 'b': 'COUNT', 'c': 'AVG', 'd': 'TOTAL', 'ans': 'B', 'diff': 'Easy', 'exp': 'COUNT() returns the number of rows.'},
            {'q': 'What is the default sorting in ORDER BY?', 'a': 'Descending', 'b': 'Ascending', 'c': 'Random', 'd': 'None', 'ans': 'B', 'diff': 'Easy', 'exp': 'ORDER BY defaults to ascending order.'},
            {'q': 'Which clause is used with aggregate functions?', 'a': 'WHERE', 'b': 'GROUP BY', 'c': 'ORDER BY', 'd': 'LIMIT', 'ans': 'B', 'diff': 'Easy', 'exp': 'GROUP BY is used with aggregate functions.'},
            {'q': 'What does HAVING clause do?', 'a': 'Filters rows', 'b': 'Filters groups', 'c': 'Sorts results', 'd': 'Joins tables', 'ans': 'B', 'diff': 'Medium', 'exp': 'HAVING filters groups after aggregation.'},
            {'q': 'Which join returns all rows from both tables?', 'a': 'INNER JOIN', 'b': 'LEFT JOIN', 'c': 'RIGHT JOIN', 'd': 'FULL OUTER JOIN', 'ans': 'D', 'diff': 'Medium', 'exp': 'FULL OUTER JOIN returns all rows from both tables.'},
            {'q': 'What is a primary key?', 'a': 'Any column', 'b': 'Unique identifier for each row', 'c': 'Foreign reference', 'd': 'Index', 'ans': 'B', 'diff': 'Easy', 'exp': 'Primary key uniquely identifies each row.'},
            {'q': 'What does UPDATE statement do?', 'a': 'Deletes data', 'b': 'Modifies existing data', 'c': 'Creates table', 'd': 'Adds columns', 'ans': 'B', 'diff': 'Easy', 'exp': 'UPDATE modifies existing records.'},
            {'q': 'Which keyword removes duplicates?', 'a': 'DISTINCT', 'b': 'UNIQUE', 'c': 'REMOVE', 'd': 'FILTER', 'ans': 'A', 'diff': 'Easy', 'exp': 'DISTINCT removes duplicate rows from results.'},
        ],
        'Normalization': [
            {'q': 'What is 1NF?', 'a': 'No duplicate rows', 'b': 'Atomic values only', 'c': 'No partial dependencies', 'd': 'No transitive dependencies', 'ans': 'B', 'diff': 'Medium', 'exp': '1NF requires atomic (indivisible) values.'},
            {'q': 'What is 2NF?', 'a': 'No duplicate rows', 'b': 'Atomic values', 'c': 'No partial dependencies', 'd': 'No transitive dependencies', 'ans': 'C', 'diff': 'Medium', 'exp': '2NF eliminates partial dependencies.'},
            {'q': 'What does BCNF stand for?', 'a': 'Basic Normal Form', 'b': 'Boyce-Codd Normal Form', 'c': 'Best Complex Normal Form', 'd': 'Base Column Normal Form', 'ans': 'B', 'diff': 'Easy', 'exp': 'BCNF stands for Boyce-Codd Normal Form.'},
            {'q': 'What is the purpose of normalization?', 'a': 'Speed up queries', 'b': 'Reduce data redundancy', 'c': 'Increase storage', 'd': 'Add constraints', 'ans': 'B', 'diff': 'Easy', 'exp': 'Normalization reduces data redundancy.'},
            {'q': 'What is a functional dependency?', 'a': 'Table relationship', 'b': 'Column determines another column', 'c': 'Foreign key', 'd': 'Index', 'ans': 'B', 'diff': 'Medium', 'exp': 'Functional dependency means one column determines another.'},
        ],
        'Transactions': [
            {'q': 'What does ACID stand for?', 'a': 'Atomicity, Consistency, Isolation, Durability', 'b': 'Automatic, Consistent, Independent, Distributed', 'c': 'Asynchronous, Concurrent, Integrated, Direct', 'd': 'Atomic, Computed, Indexed, Durable', 'ans': 'A', 'diff': 'Easy', 'exp': 'ACID: Atomicity, Consistency, Isolation, Durability.'},
            {'q': 'Which isolation level allows dirty reads?', 'a': 'Serializable', 'b': 'Repeatable Read', 'c': 'Read Committed', 'd': 'Read Uncommitted', 'ans': 'D', 'diff': 'Medium', 'exp': 'Read Uncommitted allows dirty reads.'},
            {'q': 'What is a deadlock?', 'a': 'Transaction failure', 'b': 'Two transactions waiting for each other', 'c': 'Database crash', 'd': 'Lock timeout', 'ans': 'B', 'diff': 'Medium', 'exp': 'Deadlock is when two transactions each wait for the other.'},
            {'q': 'What does COMMIT do?', 'a': 'Cancels transaction', 'b': 'Saves all changes', 'c': 'Locks table', 'd': 'Creates backup', 'ans': 'B', 'diff': 'Easy', 'exp': 'COMMIT saves all changes made by the transaction.'},
            {'q': 'What is atomicity?', 'a': 'All or nothing', 'b': 'Data consistency', 'c': 'Isolation level', 'd': 'Data durability', 'ans': 'A', 'diff': 'Easy', 'exp': 'Atomicity means all operations complete or none do.'},
        ],
    },
    'Machine Learning': {
        'Introduction to ML': [
            {'q': 'What is Machine Learning?', 'a': 'Explicit programming', 'b': 'Learning from data', 'c': 'Database management', 'd': 'Web development', 'ans': 'B', 'diff': 'Easy', 'exp': 'ML enables systems to learn from data.'},
            {'q': 'Which is a type of ML?', 'a': 'Supervised Learning', 'b': 'Structured Query', 'c': 'HTML Parsing', 'd': 'File Processing', 'ans': 'A', 'diff': 'Easy', 'exp': 'Supervised Learning is a major type of ML.'},
            {'q': 'What is training data?', 'a': 'Test data', 'b': 'Data used to teach the model', 'c': 'Final results', 'd': 'Database backup', 'ans': 'B', 'diff': 'Easy', 'exp': 'Training data is used to teach the ML model.'},
            {'q': 'What is a feature in ML?', 'a': 'Movie feature', 'b': 'Input variable', 'c': 'Output label', 'd': 'Model parameter', 'ans': 'B', 'diff': 'Easy', 'exp': 'Features are input variables used by the model.'},
            {'q': 'What is overfitting?', 'a': 'Model too simple', 'b': 'Model learns noise in training data', 'c': 'Model is perfect', 'd': 'Model is slow', 'ans': 'B', 'diff': 'Medium', 'exp': 'Overfitting means the model memorizes training data including noise.'},
            {'q': 'What is the purpose of a test set?', 'a': 'Train the model', 'b': 'Evaluate model performance', 'c': 'Clean data', 'd': 'Store results', 'ans': 'B', 'diff': 'Easy', 'exp': 'Test set evaluates how well the model generalizes.'},
            {'q': 'Which is NOT a type of ML?', 'a': 'Supervised', 'b': 'Unsupervised', 'c': 'Reinforcement', 'd': 'Deterministic', 'ans': 'D', 'diff': 'Easy', 'exp': 'Deterministic is not a type of machine learning.'},
            {'q': 'What is a label in supervised learning?', 'a': 'Input feature', 'b': 'Expected output', 'c': 'Model weight', 'd': 'Data point', 'ans': 'B', 'diff': 'Easy', 'exp': 'Labels are the expected outputs the model learns to predict.'},
            {'q': 'What is underfitting?', 'a': 'Model too complex', 'b': 'Model too simple to capture patterns', 'c': 'Perfect model', 'd': 'Model memorizes data', 'ans': 'B', 'diff': 'Medium', 'exp': 'Underfitting means the model is too simple.'},
            {'q': 'What is a hyperparameter?', 'a': 'Data parameter', 'b': 'Setting configured before training', 'c': 'Learned weight', 'd': 'Output label', 'ans': 'B', 'diff': 'Medium', 'exp': 'Hyperparameters are settings set before model training.'},
        ],
        'Linear Regression': [
            {'q': 'What type of problem does linear regression solve?', 'a': 'Classification', 'b': 'Regression', 'c': 'Clustering', 'd': 'Dimensionality Reduction', 'ans': 'B', 'diff': 'Easy', 'exp': 'Linear regression is for regression (continuous values).'},
            {'q': 'What is the equation of simple linear regression?', 'a': 'y = mx + c', 'b': 'y = mx² + c', 'c': 'y = e^x', 'd': 'y = log(x)', 'ans': 'A', 'diff': 'Easy', 'exp': 'Simple linear regression: y = mx + c.'},
            {'q': 'What cost function is commonly used?', 'a': 'Cross Entropy', 'b': 'Mean Squared Error', 'c': 'Accuracy', 'd': 'F1 Score', 'ans': 'B', 'diff': 'Medium', 'exp': 'MSE is the common cost function for linear regression.'},
            {'q': 'What does the slope (m) represent?', 'a': 'Y-intercept', 'b': 'Rate of change', 'c': 'Error', 'd': 'Prediction', 'ans': 'B', 'diff': 'Easy', 'exp': 'The slope represents the rate of change.'},
            {'q': 'What is the y-intercept?', 'a': 'Slope', 'b': 'Value of y when x=0', 'c': 'Maximum value', 'd': 'Error', 'ans': 'B', 'diff': 'Easy', 'exp': 'Y-intercept is the value of y when x is 0.'},
        ],
        'Decision Trees': [
            {'q': 'What criterion splits nodes in decision trees?', 'a': 'MSE', 'b': 'Gini Impurity / Entropy', 'c': 'Accuracy', 'd': 'Precision', 'ans': 'B', 'diff': 'Easy', 'exp': 'Gini or Entropy determines the best split.'},
            {'q': 'What is pruning in decision trees?', 'a': 'Adding nodes', 'b': 'Removing branches to reduce overfitting', 'c': 'Training faster', 'd': 'Increasing depth', 'ans': 'B', 'diff': 'Medium', 'exp': 'Pruning removes branches to prevent overfitting.'},
            {'q': 'What is information gain?', 'a': 'Data amount', 'b': 'Reduction in entropy after split', 'c': 'Model accuracy', 'd': 'Training time', 'ans': 'B', 'diff': 'Medium', 'exp': 'Information gain measures entropy reduction.'},
            {'q': 'What type of learning are decision trees?', 'a': 'Unsupervised', 'b': 'Supervised', 'c': 'Reinforcement', 'd': 'Semi-supervised', 'ans': 'B', 'diff': 'Easy', 'exp': 'Decision trees are supervised learning algorithms.'},
            {'q': 'What is the leaf node of a decision tree?', 'a': 'Root node', 'b': 'Decision point', 'c': 'Final prediction', 'd': 'Split node', 'ans': 'C', 'diff': 'Easy', 'exp': 'Leaf nodes contain the final prediction/class.'},
        ],
        'Random Forests': [
            {'q': 'What is a Random Forest?', 'a': 'Single tree', 'b': 'Ensemble of decision trees', 'c': 'Neural network', 'd': 'Linear model', 'ans': 'B', 'diff': 'Easy', 'exp': 'Random Forest is an ensemble of multiple decision trees.'},
            {'q': 'What technique does Random Forest use?', 'a': 'Boosting', 'b': 'Bagging', 'c': 'Stacking', 'd': 'Blending', 'ans': 'B', 'diff': 'Medium', 'exp': 'Random Forest uses Bootstrap Aggregating (Bagging).'},
            {'q': 'What is the advantage of Random Forest over a single tree?', 'a': 'Faster training', 'b': 'Reduces overfitting', 'c': 'Uses less memory', 'd': 'Simpler model', 'ans': 'B', 'diff': 'Medium', 'exp': 'Ensemble approach reduces overfitting.'},
            {'q': 'How are trees in Random Forest different?', 'a': 'Different algorithms', 'b': 'Different random subsets of data and features', 'c': 'Different predictions', 'd': 'Same data', 'ans': 'B', 'diff': 'Medium', 'exp': 'Each tree gets a random subset of data and features.'},
            {'q': 'What is feature importance in Random Forest?', 'a': 'Most used feature', 'b': 'Measure of each feature contribution', 'c': 'First feature', 'd': 'Random feature', 'ans': 'B', 'diff': 'Medium', 'exp': 'Feature importance measures each feature contribution to predictions.'},
        ],
        'Neural Networks': [
            {'q': 'What is a perceptron?', 'a': 'Database', 'b': 'Simple neural unit', 'c': 'Sorting algorithm', 'd': 'Search method', 'ans': 'B', 'diff': 'Easy', 'exp': 'A perceptron is the simplest neural network unit.'},
            {'q': 'What is backpropagation?', 'a': 'Forward pass', 'b': 'Algorithm to update weights', 'c': 'Data loading', 'd': 'Model saving', 'ans': 'B', 'diff': 'Medium', 'exp': 'Backpropagation calculates gradients to update weights.'},
            {'q': 'What is an activation function?', 'a': 'Data activation', 'b': 'Non-linear function introducing complexity', 'c': 'Weight initialization', 'd': 'Loss function', 'ans': 'B', 'diff': 'Medium', 'exp': 'Activation functions add non-linearity to the network.'},
            {'q': 'What is a hidden layer?', 'a': 'Input layer', 'b': 'Layer between input and output', 'c': 'Output layer', 'd': 'Last layer', 'ans': 'B', 'diff': 'Easy', 'exp': 'Hidden layers are between input and output layers.'},
            {'q': 'What is the purpose of the loss function?', 'a': 'Make predictions', 'b': 'Measure prediction error', 'c': 'Train faster', 'd': 'Store data', 'ans': 'B', 'diff': 'Easy', 'exp': 'Loss function measures how wrong the predictions are.'},
        ],
        'Clustering': [
            {'q': 'What type of learning is clustering?', 'a': 'Supervised', 'b': 'Unsupervised', 'c': 'Reinforcement', 'd': 'Semi-supervised', 'ans': 'B', 'diff': 'Easy', 'exp': 'Clustering is unsupervised learning.'},
            {'q': 'What does K-Means require as input?', 'a': 'Labels', 'b': 'Number of clusters (K)', 'c': 'Decision boundaries', 'd': 'Test data', 'ans': 'B', 'diff': 'Medium', 'exp': 'K-Means requires the number of clusters K.'},
            {'q': 'What is the elbow method?', 'a': 'Data cleaning', 'b': 'Finding optimal K value', 'c': 'Feature selection', 'd': 'Model evaluation', 'ans': 'B', 'diff': 'Medium', 'exp': 'Elbow method finds optimal number of clusters.'},
            {'q': 'What does DBSCAN stand for?', 'a': 'Database Scan', 'b': 'Density-Based Spatial Clustering', 'c': 'Data Balanced Scan', 'd': 'Dynamic Best Scan', 'ans': 'B', 'diff': 'Medium', 'exp': 'DBSCAN: Density-Based Spatial Clustering of Applications with Noise.'},
            {'q': 'Which clustering uses hierarchical approach?', 'a': 'K-Means', 'b': 'DBSCAN', 'c': 'Hierarchical Clustering', 'd': 'KNN', 'ans': 'C', 'diff': 'Easy', 'exp': 'Hierarchical clustering builds a tree of clusters.'},
        ],
    },
    'Artificial Intelligence': {
        'Search Algorithms': [
            {'q': 'Which search uses a queue?', 'a': 'DFS', 'b': 'BFS', 'c': 'Binary Search', 'd': 'Linear Search', 'ans': 'B', 'diff': 'Easy', 'exp': 'BFS uses a queue (FIFO) for level-by-level search.'},
            {'q': 'What is A* search?', 'a': 'Uninformed search', 'b': 'Optimal informed search using heuristic', 'c': 'Random search', 'd': 'Greedy search only', 'ans': 'B', 'diff': 'Medium', 'exp': 'A* combines cost so far with heuristic estimate.'},
            {'q': 'What is a heuristic?', 'a': 'Exact solution', 'b': 'Estimated cost to goal', 'c': 'Random guess', 'd': 'Database query', 'ans': 'B', 'diff': 'Easy', 'exp': 'Heuristic estimates the cost from current state to goal.'},
            {'q': 'What does BFS guarantee?', 'a': 'Least memory', 'b': 'Shortest path in unweighted graph', 'c': 'Fastest search', 'd': 'Optimal path always', 'ans': 'B', 'diff': 'Medium', 'exp': 'BFS finds shortest path in unweighted graphs.'},
            {'q': 'What is the space complexity of BFS?', 'a': 'O(1)', 'b': 'O(b^d)', 'c': 'O(n)', 'd': 'O(log n)', 'ans': 'B', 'diff': 'Medium', 'exp': 'BFS space is O(b^d) where b is branching factor, d is depth.'},
        ],
        'Knowledge Representation': [
            {'q': 'What is a semantic network?', 'a': 'Computer network', 'b': 'Graph representing knowledge', 'c': 'Database schema', 'd': 'Web graph', 'ans': 'B', 'diff': 'Easy', 'exp': 'Semantic networks use graphs to represent relationships.'},
            {'q': 'What is a production rule?', 'a': 'If-then rule', 'b': 'Database rule', 'c': 'Sort rule', 'd': 'Search rule', 'ans': 'A', 'diff': 'Easy', 'exp': 'Production rules are IF condition THEN action.'},
            {'q': 'What is propositional logic?', 'a': 'First-order logic', 'b': 'Logic with propositions', 'c': 'Fuzzy logic', 'd': 'Probabilistic logic', 'ans': 'B', 'diff': 'Easy', 'exp': 'Propositional logic deals with true/false propositions.'},
            {'q': 'What is an inference engine?', 'a': 'Database engine', 'b': 'Component that applies rules', 'c': 'Search engine', 'd': 'Storage engine', 'ans': 'B', 'diff': 'Medium', 'exp': 'Inference engine applies rules to derive new knowledge.'},
            {'q': 'What is forward chaining?', 'a': 'Working backward from goal', 'b': 'Applying rules from known facts', 'c': 'Random reasoning', 'd': 'Database lookup', 'ans': 'B', 'diff': 'Medium', 'exp': 'Forward chaining applies rules starting from known facts.'},
        ],
    },
    'Design and Analysis of Algorithms': {
        'Dynamic Programming': [
            {'q': 'What are the two key properties of DP?', 'a': 'Recursion and iteration', 'b': 'Overlapping subproblems and optimal substructure', 'c': 'Linear and nonlinear', 'd': 'Sequential and parallel', 'ans': 'B', 'diff': 'Easy', 'exp': 'DP requires overlapping subproblems and optimal substructure.'},
            {'q': 'What is top-down DP?', 'a': 'Tabulation', 'b': 'Memoization', 'c': 'Iteration', 'd': 'Brute force', 'ans': 'B', 'diff': 'Medium', 'exp': 'Top-down DP uses memoization (recursive + caching).'},
            {'q': 'What is bottom-up DP?', 'a': 'Memoization', 'b': 'Tabulation', 'c': 'Recursion', 'd': 'Backtracking', 'ans': 'B', 'diff': 'Medium', 'exp': 'Bottom-up DP uses tabulation (iterative table building).'},
            {'q': 'What is optimal substructure?', 'a': 'Optimal solution from sub-solutions', 'b': 'Recursive solution', 'c': 'Random solution', 'd': 'Greedy solution', 'ans': 'A', 'diff': 'Medium', 'exp': 'Optimal substructure means optimal solution is built from optimal sub-solutions.'},
            {'q': 'Which problem is classic DP?', 'a': 'Linear Search', 'b': 'Fibonacci Sequence', 'c': 'Bubble Sort', 'd': 'Binary Search', 'ans': 'B', 'diff': 'Easy', 'exp': 'Fibonacci is a classic DP problem with overlapping subproblems.'},
        ],
        'Greedy Algorithms': [
            {'q': 'What is the greedy approach?', 'a': 'Try all solutions', 'b': 'Make locally optimal choices', 'c': 'Random choices', 'd': 'Backtrack', 'ans': 'B', 'diff': 'Easy', 'exp': 'Greedy algorithms make locally optimal choices at each step.'},
            {'q': 'Which algorithm is greedy?', 'a': 'Quick Sort', 'b': 'Dijkstra Algorithm', 'c': 'Merge Sort', 'd': 'Binary Search', 'ans': 'B', 'diff': 'Medium', 'exp': "Dijkstra's algorithm uses greedy approach for shortest path."},
            {'q': 'What is a greedy choice property?', 'a': 'Global optimal', 'b': 'Local optimal leads to global optimal', 'c': 'Random choice', 'd': 'All choices', 'ans': 'B', 'diff': 'Medium', 'exp': 'Greedy choice property: local optimum leads to global optimum.'},
            {'q': 'Which is NOT a greedy algorithm?', 'a': "Kruskal's", 'b': "Prim's", 'c': 'Huffman Coding', 'd': 'Dynamic Programming', 'ans': 'D', 'diff': 'Easy', 'exp': 'DP is not greedy; it considers all subproblems.'},
            {'q': "What does Kruskal's algorithm find?", 'a': 'Shortest path', 'b': 'Minimum Spanning Tree', 'c': 'Maximum flow', 'd': 'Sorting', 'ans': 'B', 'diff': 'Medium', 'exp': "Kruskal's algorithm finds the Minimum Spanning Tree."},
        ],
    },
}


def _get_module_id(topic_id):
    """Look up the module_id for a given topic_id."""
    row = db.fetch_one('SELECT module_id FROM topics WHERE id=%s', (topic_id,))
    return row['module_id'] if row else None


def auto_generate_assignment(topic_id, topic_name, subject_name):
    """
    Auto-generate an assignment for a topic if one doesn't exist.
    The assignments table uses module_id (not topic_id).
    Returns the assignment_id.
    """
    module_id = _get_module_id(topic_id)
    if not module_id:
        return None

    # Check if assignment already exists for this module
    existing = query_db(
        'SELECT id FROM assignments WHERE module_id = %s',
        [module_id], one=True
    )
    if existing:
        return existing['id']

    # Find questions from question bank
    questions = _find_questions(subject_name, topic_name)

    if not questions:
        questions = _generate_generic_questions(topic_name)

    # Determine difficulty_mix from the question distribution
    easy_count = len([q for q in questions if q['diff'] == 'Easy'])
    hard_count = len([q for q in questions if q['diff'] == 'Hard'])
    if easy_count > len(questions) // 2:
        difficulty_mix = 'Easy'
    elif hard_count > len(questions) // 2:
        difficulty_mix = 'Hard'
    else:
        difficulty_mix = 'Mixed'

    # Create assignment - only columns that exist in the actual schema:
    # id, module_id, title, difficulty_mix, created_at
    assignment_id = query_db(
        'INSERT INTO assignments (module_id, title, difficulty_mix) VALUES (%s, %s, %s)',
        [module_id, f'{topic_name} Assessment', difficulty_mix]
    )

    # Insert questions - columns: assignment_id, question_text, option_a/b/c/d, correct_option, difficulty, concept
    for q in questions:
        query_db(
            """INSERT INTO assignment_questions
               (assignment_id, question_text, option_a, option_b, option_c, option_d, correct_option, difficulty, concept)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            [
                assignment_id,
                q['q'], q['a'], q['b'], q['c'], q['d'],
                q['ans'], q['diff'], q['exp']
            ]
        )

    return assignment_id


def _find_questions(subject_name, topic_name):
    """Find questions from the question bank matching the subject and topic."""
    questions = []

    for subj_key, topics in QUESTION_BANK.items():
        if subj_key.lower() in subject_name.lower() or subject_name.lower() in subj_key.lower():
            for topic_key, q_list in topics.items():
                if topic_key.lower() in topic_name.lower() or topic_name.lower() in topic_key.lower():
                    questions.extend(q_list)
                    break
        elif any(word in subject_name.lower() for word in subj_key.lower().split()):
            for topic_key, q_list in topics.items():
                if any(word in topic_name.lower() for word in topic_key.lower().split()):
                    questions.extend(q_list)
                    break

    return questions[:10]


def _generate_generic_questions(topic_name):
    """Generate generic questions when no specific questions are available."""
    return [
        {'q': f'What is the primary purpose of {topic_name}?', 'a': 'Data storage', 'b': 'Problem solving with specific techniques', 'c': 'Web design', 'd': 'Database management', 'ans': 'B', 'diff': 'Easy', 'exp': f'{topic_name} provides specific techniques for problem solving.'},
        {'q': f'Which of the following is related to {topic_name}?', 'a': 'HTML', 'b': 'Core computer science concepts', 'c': 'CSS styling', 'd': 'SQL queries', 'ans': 'B', 'diff': 'Easy', 'exp': f'{topic_name} is a core computer science concept.'},
        {'q': f'What is a key characteristic of {topic_name}?', 'a': 'Random behavior', 'b': 'Well-defined operations and properties', 'c': 'No structure', 'd': 'Only theoretical', 'ans': 'B', 'diff': 'Easy', 'exp': f'{topic_name} has well-defined operations and properties.'},
        {'q': f'In {topic_name}, what is typically analyzed?', 'a': 'Time and space complexity', 'b': 'Color schemes', 'c': 'Font sizes', 'd': 'File formats', 'ans': 'A', 'diff': 'Easy', 'exp': f'Complexity analysis is fundamental to understanding {topic_name}.'},
        {'q': f'What skill is important for mastering {topic_name}?', 'a': 'Only memorization', 'b': 'Understanding concepts and practicing problems', 'c': 'Speed typing', 'd': 'Graphic design', 'ans': 'B', 'diff': 'Easy', 'exp': 'Conceptual understanding and practice are key to mastery.'},
        {'q': f'How is {topic_name} typically evaluated?', 'a': 'By appearance', 'b': 'Through problem-solving and analysis', 'c': 'By file size', 'd': 'By color', 'ans': 'B', 'diff': 'Easy', 'exp': 'Problem-solving ability demonstrates understanding.'},
        {'q': f'Which approach helps learn {topic_name} effectively?', 'a': 'Skip fundamentals', 'b': 'Start with basics and build progressively', 'c': 'Only read theory', 'd': 'Memorize without understanding', 'ans': 'B', 'diff': 'Easy', 'exp': 'Progressive learning from fundamentals is most effective.'},
        {'q': f'What is a common application of {topic_name}?', 'a': 'Only academic use', 'b': 'Solving real-world computational problems', 'c': 'Drawing pictures', 'd': 'Playing games only', 'ans': 'B', 'diff': 'Easy', 'exp': f'{topic_name} is applied to solve real-world problems.'},
        {'q': f'What makes {topic_name} important in CS?', 'a': 'It is easy', 'b': 'It provides efficient solutions to problems', 'c': 'It uses less code', 'd': 'It is new', 'ans': 'B', 'diff': 'Medium', 'exp': f'{topic_name} provides efficient and effective problem-solving approaches.'},
        {'q': f'How do experts approach {topic_name} problems?', 'a': 'Trial and error only', 'b': 'Systematic analysis and methodical solution', 'c': 'Skip reading the problem', 'd': "Copy others' work", 'ans': 'B', 'diff': 'Medium', 'exp': 'Expert approach involves systematic analysis and methodical solving.'},
    ]


def setup_assignments_for_topic(topic_id, topic_name, subject_name):
    """Setup assignment for a topic. Returns assignment_id."""
    return auto_generate_assignment(topic_id, topic_name, subject_name)
