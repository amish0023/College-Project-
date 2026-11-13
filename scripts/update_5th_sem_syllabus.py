"""
Script to populate complete 5th Semester syllabus modules, topics, curated YouTube lectures,
AI notes, and adaptive assignments for:
- Compiler Design (CSE16503)
- Artificial Intelligence (CSE16501)
- Big Data Analysis (CSE16504.1)
- NLP for Health Related Text (CSD14505.3/CSE16505.2)
- Introduction to Virtual Reality and 3D Interaction (CSE16511A.3)
"""
import pymysql
import pymysql.cursors

def connect_db():
    return pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='',
        database='personalised_learning',
        cursorclass=pymysql.cursors.DictCursor,
        charset='utf8mb4',
        autocommit=False
    )

SYLLABUS_DATA = [
    # -------------------------------------------------------------------------------------------------
    # SUBJECT 1: COMPILER DESIGN (CSE - 16503)
    # -------------------------------------------------------------------------------------------------
    {
        'subject_code': 'CSE16503',
        'subject_name': 'Compiler Design',
        'modules': [
            {
                'seq': 1,
                'name': 'Introduction to Compilers & Lexical Analysis',
                'desc': 'Compiler vs Interpreter, phases of a compiler, lexical analyzer role, regular expressions, finite automata, bootstrapping, LEX tool, context-free grammars, derivations, parse trees, ambiguity, left recursion, left factoring, dangling-else, top-down predictive LL(1) parsing.',
                'video_id': 'Qkwj65l_96I',
                'video_title': 'Compiler Design: Introduction, Phases of a Compiler & Lexical Analysis',
                'duration': 1200,
                'transcript': 'Welcome to this in-depth lecture on Compiler Design. In this module, we examine how high-level programming language code transforms into executable machine binaries. A compiler translates the entire source program into target code prior to execution, whereas an interpreter translates and executes line-by-line. The compilation pipeline is partitioned into analysis (front end) and synthesis (back end). In lexical analysis, source text is scanned into tokens using regular expressions and deterministic finite automata (DFA). We address grammar ambiguities such as left recursion and left factoring to construct deterministic top-down predictive LL(1) parsers.',
                'summary': 'This module introduces compiler architecture, translation phases, regular language tokenization, and deterministic top-down grammar parsing.',
                'key_concepts': '• Compiler vs Interpreter Differences\n• Six Major Compilation Phases (Lexical, Syntax, Semantic, Intermediate Code, Optimization, Code Generation)\n• Regular Expressions to Finite Automata (Thompson Construction & Subset Construction)\n• Context-Free Grammars (CFG) and Parse Trees\n• Elimination of Left Recursion and Left Factoring for LL(1) Parsing',
                'important_points': '• Lexical analysis produces a stream of tokens and constructs the initial symbol table entries.\n• Top-down predictive parsers cannot process left-recursive grammars without infinite recursion.\n• Bootstrapping allows a compiler to be written in its own source language once a base core exists.',
                'revision_notes': '1. Convert CFG to LL(1) by removing left recursion: A -> Aa | b becomes A -> bA\', A\' -> aA\' | epsilon.\n2. Left factoring eliminates common prefixes: A -> ab1 | ab2 becomes A -> aA\', A\' -> b1 | b2.\n3. Verify LL(1) condition: FIRST and FOLLOW sets for disjoint alternative productions.',
                'possible_questions': 'Q1: Explain the six phases of a compiler with a neat translation diagram for position = initial + rate * 60.\nQ2: How do you eliminate immediate left recursion from a context-free grammar?\nQ3: Construct the predictive parsing table for an LL(1) arithmetic grammar and verify parse steps.\nQ4: Differentiate between a compiler pass and a compiler phase.',
                'questions': [
                    {
                        'q': 'What is the primary function of the Lexical Analysis phase in a compiler?',
                        'a': 'To convert the raw stream of source characters into meaningful grammatical tokens',
                        'b': 'To allocate memory registers for target machine instructions',
                        'c': 'To link external dynamic library files at runtime',
                        'd': 'To execute intermediate code statements line-by-line',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'Why is it mandatory to eliminate left recursion from a context-free grammar before building a predictive top-down parser?',
                        'a': 'Because left recursion increases intermediate file sizes unnecessarily',
                        'b': 'Because a top-down parser will enter an infinite recursion loop attempting to expand the same non-terminal',
                        'c': 'Because hardware ALUs do not support left-handed arithmetic registers',
                        'd': 'Because lexical tokens cannot be scanned backwards',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In programming language syntax, how does a standard compiler resolve the classic "dangling-else" ambiguity?',
                        'a': 'By throwing a fatal compile-time syntax error on every nested if-statement',
                        'b': 'By systematically associating each "else" clause with the closest preceding unmatched "if"',
                        'c': 'By ignoring all else branches unless explicitly flagged by the operating system',
                        'd': 'By converting all conditional statements into while loops',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 2,
                'name': 'Bottom-Up Parsing & LR Parsers',
                'desc': 'Bottom-up parsing principles, handles, handle pruning, shift-reduce parsing on stack, shift/reduce and reduce/reduce conflicts, LR grammars, Simple LR (SLR), Canonical LR (CLR), Look-Ahead LR (LALR), error recovery, YACC generator.',
                'video_id': 'n3_t7k3K0mU',
                'video_title': 'Bottom-Up Parsing: Shift-Reduce, Operator Precedence & LR Parsing Algorithms',
                'duration': 1350,
                'transcript': 'In this session, we investigate Bottom-Up Parsing, which constructs parse trees starting from leaves up to the root non-terminal. We implement shift-reduce parsing using an explicit parser stack. A "handle" is a substring matching the right-hand side of a production whose reduction represents one step along the reverse of a rightmost derivation. We evaluate LR parsers: SLR(1) uses FOLLOW sets for reduce decisions; CLR(1) embeds explicit lookahead tokens into LR items; LALR(1) merges states with identical item cores to reduce memory footprint. Finally, we explore YACC for automatic parser generation.',
                'summary': 'Detailed exploration of shift-reduce parsing, handles, handle pruning, and the mathematical construction of SLR, CLR, and LALR parsing tables.',
                'key_concepts': '• Handles and Handle Pruning in Rightmost Derivations in Reverse\n• Shift-Reduce Stack Operations (Shift, Reduce, Accept, Error)\n• Parsing Conflicts: Shift-Reduce (S/R) and Reduce-Reduce (R/R)\n• LR(0), SLR(1), CLR(1), and LALR(1) Parsing Table Construction\n• Automatic Parser Generation using YACC',
                'important_points': '• CLR(1) is the most powerful deterministic LR parser but requires an enormous number of states.\n• LALR(1) merges states with the same LR(0) core, preventing shift-reduce conflicts while occasionally introducing reduce-reduce conflicts.\n• Shift-reduce conflicts occur when the parser cannot decide whether to shift the next token or reduce the current handle.',
                'revision_notes': '1. Handle: substring that matches RHS of production and whose reduction corresponds to a step in reverse rightmost derivation.\n2. SLR(1) reduce condition: Place r_j in state i for column a if A -> alpha. is in state i and a is in FOLLOW(A).\n3. LALR(1) table size equals SLR(1) table size, with the parsing power of CLR(1).',
                'possible_questions': 'Q1: Trace the shift-reduce parsing actions on stack for the input id + id * id.\nQ2: What is a handle? Explain handle pruning with a concrete grammar derivation.\nQ3: Construct the Canonical Collection of LR(0) items and build the SLR(1) parsing table.\nQ4: Differentiate between CLR(1) and LALR(1) parsing algorithms regarding state count and conflict possibilities.',
                'questions': [
                    {
                        'q': 'During shift-reduce parsing, what exact operation is performed during a "Reduce" step?',
                        'a': 'The right-hand side handle on the top of the stack is popped and replaced with its corresponding LHS non-terminal',
                        'b': 'The next input token is pushed onto the stack without evaluation',
                        'c': 'The compiler terminates execution and outputs an error log',
                        'd': 'The stack is completely cleared to restart compilation from the beginning',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'Which class of LR parsers merges states with identical LR(0) item cores, producing a compact table equal in size to SLR while providing superior parsing power?',
                        'a': 'Operator Precedence Parser',
                        'b': 'Recursive Descent Parser',
                        'c': 'LALR(1) Parser (Look-Ahead LR)',
                        'd': 'Non-deterministic Finite Automaton',
                        'correct': 'C',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'Under what precise structural condition does an LR parsing table experience a Reduce-Reduce (R/R) conflict in state I?',
                        'a': 'When two distinct complete production items A -> alpha. and B -> beta. both propose reductions on the same lookahead symbol',
                        'b': 'When the input string contains two consecutive addition operators',
                        'c': 'When a non-terminal has more than three production alternatives',
                        'd': 'When the lexical analyzer returns an unrecognized variable name',
                        'correct': 'A',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 3,
                'name': 'Syntax Directed Translation & Intermediate Code',
                'desc': 'Syntax-directed definitions (SDD), syntax trees, S-attributed and L-attributed definitions, translation schemes (SDT), intermediate representations, Abstract Syntax Trees (AST), Polish notation, Three-Address Code (TAC), quadruples, triples, translation of Boolean & control flow.',
                'video_id': 'WvW6i-yYx4A',
                'video_title': 'Syntax Directed Translation (SDT) & Three Address Code Generation',
                'duration': 1260,
                'transcript': 'This lecture covers Syntax Directed Translation (SDT) and Intermediate Code Generation (ICG). Syntax Directed Definitions associate grammar productions with semantic rules. We classify attributes as synthesized (computed from children) or inherited (computed from parent or siblings). In S-attributed SDDs, all attributes are synthesized and can be evaluated during bottom-up parsing. In L-attributed definitions, dependency arrows flow left-to-right. We then generate machine-independent intermediate code: Abstract Syntax Trees, Postfix notation, and Three-Address Code (TAC) represented via quadruples, triples, and indirect triples.',
                'summary': 'Covers semantic rules, attribute grammars (S-attributed vs L-attributed), and converting language statements into Three-Address Code representations.',
                'key_concepts': '• Synthesized vs Inherited Attributes in SDDs\n• S-Attributed Definitions and Bottom-Up Evaluation on Parser Stacks\n• L-Attributed Definitions and Top-Down Depth-First Traversal\n• Three-Address Code (TAC) Structure (Quadruples, Triples, Indirect Triples)\n• Backpatching and Boolean Control-Flow Expression Translation',
                'important_points': '• Intermediate code separates front-end language parsing from back-end machine-specific hardware generation.\n• Quadruples contain 4 fields: op, arg1, arg2, result.\n• Triples eliminate temporary variables by referring to instructions by position index.',
                'revision_notes': '1. S-attributed: synthesized only; evaluated bottom-up with Postfix SDT.\n2. L-attributed: synthesized or inherited from left siblings/parent; evaluated via depth-first traversal.\n3. TAC Quadruple representation: (op, arg1, arg2, result).',
                'possible_questions': 'Q1: Differentiate between synthesized and inherited attributes with examples.\nQ2: Generate three-address code, quadruples, and triples for: x = a + b * c - d / e.\nQ3: Explain backpatching in Boolean flow-of-control translation with a code snippet.\nQ4: Construct a syntax tree and DAG for the arithmetic statement a = b * -c + b * -c.',
                'questions': [
                    {
                        'q': 'What characterizes an S-attributed Syntax-Directed Definition (SDD)?',
                        'a': 'Every attribute is synthesized and computed exclusively from the attribute values of child nodes in the parse tree',
                        'b': 'Attributes can only be evaluated from right to left across sister nodes',
                        'c': 'It only applies to source code written in assembly language',
                        'd': 'Inherited attributes are passed down without mathematical operations',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'How many address fields are explicitly stored in each record of a "Quadruple" representation of Three-Address Code?',
                        'a': '2 fields (operator and operand)',
                        'b': '3 fields (operator, operand1, operand2)',
                        'c': '4 fields (operator, argument1, argument2, and result)',
                        'd': '8 fields for 64-bit CPU registers',
                        'correct': 'C',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In Three-Address Code generation for Boolean expressions, what does the technique of "Backpatching" accomplish?',
                        'a': 'It translates all while loops into unconditional goto statements before parsing',
                        'b': 'It passes lists of unresolved jump instructions as synthesized attributes and fills in target labels as soon as they become known',
                        'c': 'It reverses the order of arithmetic operands to support little-endian processors',
                        'd': 'It recalculates register allocation tables after syntax errors',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 4,
                'name': 'Type Checking & Runtime Environments',
                'desc': 'Type systems, static vs dynamic type checking, type expressions, equivalence of type expressions, type conversions, overloading, runtime storage organization, activation records, stack and heap allocation, access to non-local names, symbol tables.',
                'video_id': '0k_5u8mI9Gk',
                'video_title': 'Runtime Environments, Storage Allocation & Symbol Table Organization',
                'duration': 1100,
                'transcript': 'In this lecture, we examine Type Checking and Runtime Storage Environments. A type system enforces language semantics and guarantees memory safety. Type checkers verify that operations receive valid operand types, performing implicit coercions where valid. In Runtime Environments, the operating system allocates memory into code, static data, call stack, and heap. Each function invocation creates an activation record (stack frame) containing return address, parameters, local variables, and saved registers. We explore access links and displays for accessing non-local variables in lexically scoped languages.',
                'summary': 'Explores static and dynamic type systems, runtime memory partitions, activation records, parameter passing, and non-local variable access.',
                'key_concepts': '• Static vs Dynamic Type Checking\n• Type Expressions and Structural vs Name Type Equivalence\n• Runtime Memory Organization: Code Segment, Static Area, Stack, Heap\n• Anatomy of an Activation Record (Frame Pointer, Return Address, Locals, Temporaries)\n• Access Links and Displays for Non-Local Variable References',
                'important_points': '• Stack allocation supports recursion because each invocation receives its own dedicated activation record.\n• Dynamic memory allocation requires heap management with garbage collection or manual deallocation.\n• Symbol tables persist variable types, memory offsets, and scoping scopes across compiler phases.',
                'revision_notes': '1. Activation record fields: Temporary values, local variables, saved machine status, access link, control link, return value, actual parameters.\n2. Access link (static link): points to activation record of immediate lexical enclosing procedure.\n3. Control link (dynamic link): points to activation record of calling procedure.',
                'possible_questions': 'Q1: Draw and explain the complete structure of a function activation record.\nQ2: Differentiate between static and dynamic scoping with execution traces.\nQ3: How do access links and displays resolve non-local variable lookups in nested procedures?\nQ4: Explain parameter passing mechanisms: Call by Value, Call by Reference, and Call by Name.',
                'questions': [
                    {
                        'q': 'Which runtime memory segment dynamically manages activation records for recursive function calls and local variables?',
                        'a': 'Call Stack',
                        'b': 'Static Read-Only Code Segment',
                        'c': 'Hardware BIOS Firmware',
                        'd': 'Persistent Disk Partition',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'What is the core difference between "Name Equivalence" and "Structural Equivalence" of type expressions?',
                        'a': 'Name equivalence requires identical type names, whereas structural equivalence requires identical internal structure regardless of names',
                        'b': 'Structural equivalence applies only to floating point variables',
                        'c': 'Name equivalence is checked at runtime while structural equivalence is checked by the linker',
                        'd': 'There is no difference in modern programming languages',
                        'correct': 'A',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In languages supporting lexically nested procedure declarations, what purpose does the "Access Link" (Static Link) in an activation record serve?',
                        'a': 'It points to the activation record of the function caller to restore stack pointers',
                        'b': 'It points to the activation record of the statically enclosing lexical scope to allow access to non-local variables',
                        'c': 'It links external C dynamic libraries into the program space',
                        'd': 'It provides an index into the kernel interrupt vector table',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 5,
                'name': 'Code Optimization & Data Flow Analysis',
                'desc': 'Code optimizer structure, basic blocks and Control Flow Graphs (CFG), local optimizations, principal sources of optimization (common subexpressions, copy propagation, dead code, loop invariants), DAG representation of basic blocks, global data flow analysis.',
                'video_id': 'kQ_FmR_3a_o',
                'video_title': 'Code Optimization Techniques, Directed Acyclic Graphs (DAG) & Data Flow',
                'duration': 1300,
                'transcript': 'In our final module on Compiler Design, we explore Code Optimization. The optimizer transforms intermediate code into equivalent representations that consume fewer CPU cycles and less memory. A Basic Block is a sequence of three-address statements entered only at the first statement and exited only at the last. By linking basic blocks with directed edges, we construct the Control Flow Graph (CFG). We construct Directed Acyclic Graphs (DAGs) to identify local common subexpressions, dead code, and temporary variable reuse. Finally, we formulate Global Data Flow Equations (Reaching Definitions, Live Variable Analysis) using iterative data flow frameworks.',
                'summary': 'Covers basic block partitioning, Control Flow Graphs, DAG-based local optimization, loop optimizations, and global data flow analysis.',
                'key_concepts': '• Basic Block Partitioning (Leaders: first statement, target of jump, statement following jump)\n• Control Flow Graph (CFG) Construction\n• Local Optimization via DAG Representation\n• Principal Sources of Optimization: Common Subexpression Elimination, Copy Propagation, Dead Code Elimination, Loop Invariant Motion, Strength Reduction\n• Global Data Flow Frameworks (IN/OUT equations, Gen and Kill sets)',
                'important_points': '• Optimization must preserve program semantics; it must never alter the observable output of the program.\n• Loop optimization yields the highest execution performance gains since programs spend most time in loops.\n• DAG interior nodes represent operators; leaf nodes represent initial values of variables.',
                'revision_notes': '1. Finding leaders: (a) Statement 1 is a leader, (b) Target of conditional/unconditional jump is a leader, (c) Statement immediately following jump is a leader.\n2. Strength reduction: replacing expensive operations (x * 8) with cheaper ones (x << 3).\n3. Reaching definitions: IN[B] = Union(OUT[P]), OUT[B] = Gen[B] U (IN[B] - Kill[B]).',
                'possible_questions': 'Q1: Write the algorithm to partition three-address code into basic blocks and identify leaders.\nQ2: Construct the DAG for the basic block: d = b * c; e = a + b; b = b * c; a = e - d.\nQ3: Explain Loop Invariant Computation and Strength Reduction with code examples.\nQ4: Formulate the data flow equations for Live Variable Analysis.',
                'questions': [
                    {
                        'q': 'What defines a "Basic Block" in intermediate code optimization?',
                        'a': 'A straight-line sequence of code instructions with a single entry point and single exit point, with no branch jumps in between',
                        'b': 'A block of memory reserved on the SSD for file buffering',
                        'c': 'A collection of global variables initialized to zero',
                        'd': 'An encrypted password hash generated by the compiler',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'Which optimization technique replaces an expensive mathematical instruction like multiplication by a constant power of two with a fast bitwise shift left?',
                        'a': 'Loop unrolling',
                        'b': 'Strength Reduction',
                        'c': 'Dead Code Elimination',
                        'd': 'Code Hoisting',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In a Directed Acyclic Graph (DAG) built for basic block optimization, what do interior nodes with multiple parent edges directly signify?',
                        'a': 'A fatal syntax error in the source expression',
                        'b': 'A common subexpression whose computed value is reused without redundant recalculation',
                        'c': 'An infinite loop that will cause hardware lockup',
                        'd': 'A pointer referencing unallocated heap memory',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            }
        ]
    },

    # -------------------------------------------------------------------------------------------------
    # SUBJECT 2: ARTIFICIAL INTELLIGENCE (CSE16501)
    # -------------------------------------------------------------------------------------------------
    {
        'subject_code': 'CSE16501',
        'subject_name': 'Artificial Intelligence',
        'modules': [
            {
                'seq': 1,
                'name': 'Introduction to AI & Intelligent Agents',
                'desc': 'Introduction, definition, future of AI, characteristics of intelligent agents, PEAS description, typical agent architectures (simple reflex, model-based, goal-based, utility-based), problem-solving approach to typical AI problems.',
                'video_id': 'JMUxmLgw-GA',
                'video_title': 'Artificial Intelligence: Intelligent Agents & Problem Solving Formulations',
                'duration': 1150,
                'transcript': 'Welcome to Artificial Intelligence. In this opening module, we define artificial intelligence and investigate what constitutes an intelligent agent. An agent perceives its environment through sensors and acts upon it via actuators. We formalize task environments using the PEAS model: Performance measure, Environment, Actuators, and Sensors. We contrast simple reflex agents, model-based agents with internal memory, goal-driven agents, and utility-maximizing agents. Finally, we formulate AI search problems with initial states, actions, transition models, goal tests, and path cost functions.',
                'summary': 'Introduces artificial intelligence paradigms, intelligent agent models, PEAS environment specifications, and state-space problem formulation.',
                'key_concepts': '• Definition and Rationality in AI\n• PEAS Specification (Performance, Environment, Actuators, Sensors)\n• Environment Properties: Fully vs Partially Observable, Deterministic vs Stochastic, Episodic vs Sequential, Static vs Dynamic, Discrete vs Continuous\n• Four Intelligent Agent Architectures: Simple Reflex, Model-Based, Goal-Based, Utility-Based\n• Problem Formulation: State Space, Initial State, Actions, Transition Model, Goal Test, Path Cost',
                'important_points': '• Rationality depends on the performance measure, prior knowledge, available actions, and percept sequence—not on omniscience.\n• A utility-based agent provides a continuous measure of performance to trade off competing goals under risk.\n• Formulating problems in state space is the prerequisite for all heuristic search algorithms.',
                'revision_notes': '1. PEAS framework: specify P, E, A, S for automated taxi driver, medical diagnosis system, vacuum cleaner.\n2. Agent Function maps percept sequences to actions: f: P* -> A.\n3. State space abstraction eliminates irrelevant real-world details.',
                'possible_questions': 'Q1: Define an intelligent agent. Specify PEAS for an automated vacuum cleaner and an automated taxi.\nQ2: Explain the four primary agent architectures with block diagrams.\nQ3: What makes an environment dynamic and partially observable? Give two examples.\nQ4: Formulate the 8-puzzle problem and the Vacuum World problem as state-space search problems.',
                'questions': [
                    {
                        'q': 'In the PEAS specification of an intelligent agent environment, what does the letter "E" denote?',
                        'a': 'Environment',
                        'b': 'Efficiency',
                        'c': 'Error Rate',
                        'd': 'Episodic Function',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'Which agent architecture maintains an internal state to track aspects of the environment that cannot be viewed in the current percept alone?',
                        'a': 'Simple Reflex Agent',
                        'b': 'Model-Based Reflex Agent',
                        'c': 'Random Walk Agent',
                        'd': 'Stateless Logic Gate',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'Why is an automated chess-playing engine classified as operating in a "Static" environment during its decision turn?',
                        'a': 'Because the rules of chess were established centuries ago',
                        'b': 'Because the state of the chessboard does not change while the agent is deliberating its next move',
                        'c': 'Because the pieces are physically stationary on the table',
                        'd': 'Because both players possess equal numbers of pieces at the start',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 2,
                'name': 'Problem Solving Methods & Heuristic Search',
                'desc': 'Uninformed search (BFS, DFS, Uniform Cost), Heuristic search (Greedy Best-First, A* search, admissibility, consistency), Local search (Hill Climbing, Simulated Annealing), Constraint Satisfaction Problems (CSP), Constraint Propagation, Backtracking, Game Playing (Minimax, Alpha-Beta Pruning).',
                'video_id': 'b8f444cGYfs',
                'video_title': 'A* Heuristic Search Algorithm, Constraint Satisfaction & Minimax with Alpha-Beta',
                'duration': 1400,
                'transcript': 'This lecture examines search algorithms that solve complex AI problems. We contrast uninformed search with heuristic search. A* search evaluates f(n) = g(n) + h(n), balancing path cost g(n) with estimated distance h(n). When h(n) is admissible (never overestimating true cost) and consistent (satisfying triangle inequality), A* is complete and optimal. We address local optimization using Hill Climbing and Simulated Annealing. In Constraint Satisfaction Problems (CSP), we explore backtracking with Arc Consistency (AC-3). Finally, we analyze Adversarial Game Playing using Minimax and Alpha-Beta Pruning.',
                'summary': 'Covers uninformed and informed search, A* admissibility, CSP constraint propagation, and two-player zero-sum Minimax with Alpha-Beta pruning.',
                'key_concepts': '• Uninformed Search: BFS (optimal for unit cost), DFS, Uniform-Cost Search (Dijkstra variant)\n• A* Search: f(n) = g(n) + h(n), Admissibility condition: h(n) <= h*(n), Consistency: h(n) <= c(n,a,n\') + h(n\')\n• Local Search: Hill Climbing, Local Maxima, Simulated Annealing with Boltzmann probability\n• Constraint Satisfaction Problems: Variables, Domains, Constraints, Arc Consistency (AC-3)\n• Adversarial Search: Minimax Value, Alpha-Beta Pruning conditions (alpha >= beta)',
                'important_points': '• A* tree search requires admissibility for optimality; A* graph search requires consistency to prevent revisiting closed states.\n• Alpha-Beta pruning does not change the minimax value of the root; it only skips exploration of subtrees that cannot influence the decision.\n• AC-3 enforces that every value in variable Xi has an allowed partner in variable Xj.',
                'revision_notes': '1. A* evaluation function: f(n) = g(n) + h(n).\n2. Admissible heuristic: h(n) never overestimates actual cost to goal.\n3. Alpha cut-off: when beta <= alpha at a MIN node, prune remaining children.',
                'possible_questions': 'Q1: Prove that A* graph search is optimal when the heuristic function h(n) is consistent.\nQ2: Apply Alpha-Beta pruning on a given game tree of depth 3 and identify pruned nodes.\nQ3: Solve the 4-Queens problem using Backtracking Search combined with Forward Checking.\nQ4: Explain the working of Simulated Annealing and how it escapes local extrema.',
                'questions': [
                    {
                        'q': 'What does it mean for a heuristic function h(n) in A* search to be "admissible"?',
                        'a': 'It never overestimates the true minimal cost to reach the goal from state n',
                        'b': 'It always evaluates to zero for every node in the graph',
                        'c': 'It executes in polynomial time on parallel processors',
                        'd': 'It requires no domain-specific knowledge',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In Minimax game tree search, under what mathematical condition is an Alpha-Beta branch pruned?',
                        'a': 'Whenever alpha becomes equal to zero',
                        'b': 'Whenever alpha >= beta at a node',
                        'c': 'Whenever the search depth reaches an odd number',
                        'd': 'Whenever both players have an equal score',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In Constraint Satisfaction Problems (CSP), what does the Arc Consistency algorithm AC-3 verify for an arc (Xi, Xj)?',
                        'a': 'That variables Xi and Xj have identical alphabetical domain sizes',
                        'b': 'That for every valid value x in the domain of Xi, there exists at least one value y in the domain of Xj satisfying the constraint between them',
                        'c': 'That Xi and Xj can be merged into a single variable',
                        'd': 'That the graph is planar and contains no cycles',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 3,
                'name': 'Knowledge Representation & Logic',
                'desc': 'First Order Predicate Logic (FOPL), syntax and semantics, Prolog programming, Unification, Forward Chaining, Backward Chaining, Resolution refutation, Ontological Engineering, categories and objects, events, mental objects, reasoning with default information.',
                'video_id': 'O88U_9gO2fA',
                'video_title': 'Knowledge Representation: First Order Predicate Logic, Unification & Resolution Refutation',
                'duration': 1320,
                'transcript': 'In this session, we investigate Knowledge Representation and Automated Reasoning. Propositional logic lacks expressiveness for quantified objects and relations; hence we adopt First Order Predicate Logic (FOPL) with quantifiers, constants, predicates, and functions. We study inference engines using Generalized Modus Ponens, Forward Chaining (data-driven), and Backward Chaining (goal-driven, used in Prolog). We examine the Unification algorithm and Robinson\'s Resolution Refutation method in Conjunctive Normal Form (CNF). Finally, we review Ontological Engineering, category hierarchies, semantic networks, and default reasoning.',
                'summary': 'Covers First Order Logic, Unification, resolution refutation proofs in CNF, forward/backward chaining, and ontological categories.',
                'key_concepts': '• First Order Predicate Logic: Syntax, Semantics, Quantifiers (Universal, Existential)\n• Unification Algorithm and Most General Unifier (MGU)\n• Conversion to Conjunctive Normal Form (CNF): Skolemization, Prenex form, Elimination of implications\n• Resolution Refutation Proofs (Deriving the Empty Clause / Contradiction)\n• Forward Chaining vs Backward Chaining in Rule-Based Expert Systems',
                'important_points': '• Skolemization replaces existentially quantified variables with Skolem constants or Skolem functions of universally quantified outer variables.\n• Resolution is refutation-complete: if a set of sentences is unsatisfiable, resolution will always derive a contradiction.\n• Prolog evaluates Horn clauses via depth-first backward chaining with backtracking.',
                'revision_notes': '1. CNF conversion steps: Eliminate <=>, Eliminate =>, Move ~ inwards, Standardize variables, Skolemize, Drop universals, Distribute OR over AND.\n2. Resolution rule: (A v B) and (~B v C) yields resolvent (A v C).\n3. Most General Unifier: unifies two literals with the minimal variable substitution.',
                'possible_questions': 'Q1: Convert the following English sentences into First Order Predicate Logic: "Every student who studies passes".\nQ2: Explain Skolemization with examples involving universal and existential quantifiers.\nQ3: Prove by Resolution Refutation in CNF that: "Marcus is dead" given a set of premise axioms.\nQ4: Differentiate between Forward Chaining and Backward Chaining inference mechanisms.',
                'questions': [
                    {
                        'q': 'What is the purpose of the Unification algorithm in First Order Predicate Logic inference?',
                        'a': 'To find a set of variable substitutions that makes two distinct logical expressions syntactically identical',
                        'b': 'To encrypt knowledge bases before transmission over networks',
                        'c': 'To calculate probabilities for random variables',
                        'd': 'To compile Python scripts into C executable code',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In converting First Order Logic formulas to Conjunctive Normal Form (CNF), what is "Skolemization"?',
                        'a': 'Converting all logical AND operators into logical OR operators',
                        'b': 'Eliminating existential quantifiers by replacing them with Skolem constants or functions of outer universal variables',
                        'c': 'Deleting all negative clauses from the knowledge base',
                        'd': 'Sorting clauses in alphabetical order',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In Resolution Refutation theorem proving, what specific outcome formally verifies that the original query sentence is logically entailed by the knowledge base?',
                        'a': 'Deriving an infinite loop in the search space',
                        'b': 'Deriving the empty clause (Box / False / Contradiction) from the negated query and axiom clauses',
                        'c': 'Showing that the knowledge base contains an equal count of positive and negative literals',
                        'd': 'Proving that all variables evaluate to true under every possible interpretation',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 4,
                'name': 'Software Agents & Multi-Agent Systems',
                'desc': 'Architecture for Intelligent Software Agents, agent communication languages (ACL, FIPA-ACL, KQML), negotiation and bargaining protocols, argumentation among agents, trust and reputation mechanisms in distributed multi-agent systems.',
                'video_id': '7vKqNqPjX_A',
                'video_title': 'Multi-Agent Systems: Distributed AI, Communication Protocols, Negotiation & Trust',
                'duration': 1050,
                'transcript': 'This lecture focuses on Multi-Agent Systems (MAS) and Distributed AI. When problems are distributed geographically, computationally, or administratively, multiple autonomous software agents must coordinate. We study agent communication architectures including speech act theory, KQML, and FIPA-ACL. We examine negotiation protocols such as Contract Net for task allocation, Rubinstein alternating offers bargaining, and argumentation frameworks. Finally, we formulate mathematical trust and reputation models (Beta reputation, EigenTrust) to secure multi-agent systems against malicious or deceptive agents.',
                'summary': 'Explores multi-agent coordination, agent communication languages (FIPA-ACL), negotiation bargaining protocols, and reputation models.',
                'key_concepts': '• Autonomous Agent Characteristics: Autonomy, Reactivity, Proactiveness, Social Ability\n• Agent Communication: Speech Act Theory, KQML (Performatives), FIPA-ACL Standard\n• Coordination and Task Allocation: Contract Net Protocol (Manager Call for Proposals, Bids, Award)\n• Negotiation and Bargaining: Alternating Offers, Pareto Efficiency, Argumentation Frameworks\n• Trust and Reputation Models (Direct observation vs peer recommendations)',
                'important_points': '• In FIPA-ACL, performatives like inform, request, propose, and accept convey intentional meaning.\n• Contract Net Protocol allocates tasks dynamically without requiring centralized global knowledge.\n• Reputation models aggregate historical interaction ratings to establish probabilistic reliability scores.',
                'revision_notes': '1. Contract Net Protocol steps: Announcement -> Bidding -> Awarding -> Execution -> Result.\n2. Performative: message verb specifying illocutionary force (e.g. REQUEST, INFORM).\n3. Trust: subjective expectation of another agent\'s future cooperative performance.',
                'possible_questions': 'Q1: Explain the architectural phases of the Contract Net Protocol for distributed task sharing.\nQ2: Describe the anatomy of a FIPA-ACL message with its mandatory header parameters.\nQ3: How does game-theoretic negotiation differ from argumentation-based negotiation among agents?\nQ4: Describe how trust and reputation systems isolate Byzantine agents in peer-to-peer multi-agent networks.',
                'questions': [
                    {
                        'q': 'What core characteristic distinguishes an autonomous "Agent" from an ordinary software object or subroutine?',
                        'a': 'Agents possess autonomy to decide whether and how to execute actions in pursuit of their own goals without external invocation',
                        'b': 'Agents can only be executed on supercomputers with thousands of cores',
                        'c': 'Agents cannot communicate over internet protocols',
                        'd': 'Objects contain databases while agents do not',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In the Contract Net Protocol for multi-agent task distribution, what is the initial message broadcast by a Manager agent called?',
                        'a': 'Task Completion Acknowledgment',
                        'b': 'Call for Proposals (CFP) / Task Announcement',
                        'c': 'Contract Cancellation Notice',
                        'd': 'Hostile Takeover Declaration',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In decentralized multi-agent trust models such as Beta Reputation, how is the trust score of an agent mathematically calculated?',
                        'a': 'By counting total lines of code submitted by the agent',
                        'b': 'By computing the expected value of a Beta probability distribution based on the counts of observed successful and failed historical interactions',
                        'c': 'By randomly picking a number between 0 and 100 on every transaction',
                        'd': 'By measuring the CPU clock speed of the agent host machine',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 5,
                'name': 'Learning Processes & Probabilistic Reasoning',
                'desc': 'Supervised, unsupervised, and reinforcement learning paradigms, uncertainty quantification, Bayes Theorem, probabilistic inference, Linear Regression, Support Vector Machines (SVM), Decision Trees, and Random Forests.',
                'video_id': '7VeUPuFG374',
                'video_title': 'Machine Learning Processes: Probability, Supervised Learning, SVM & Decision Trees',
                'duration': 1250,
                'transcript': 'In this lecture, we study learning processes and probabilistic reasoning. In real environments, agents possess incomplete and uncertain knowledge. We apply probability axioms, joint probability distributions, and Bayes Theorem to perform probabilistic inference. We classify machine learning into supervised learning (labeled targets), unsupervised learning (clustering patterns), and reinforcement learning (reward signals). We examine foundational supervised models: Linear Regression via gradient descent, Support Vector Machines maximizing functional margins with kernel tricks, and tree-based models using Information Gain and Gini Impurity.',
                'summary': 'Covers probabilistic reasoning under uncertainty, Bayes theorem, Supervised vs Unsupervised vs RL, SVMs, and Decision Tree ensembles.',
                'key_concepts': '• Reasoning Under Uncertainty: Prior and Conditional Probability, Bayes Rule, Independence\n• Machine Learning Taxonomy: Supervised, Unsupervised, Reinforcement Learning\n• Linear Regression and Mean Squared Error Loss Function\n• Support Vector Machines (SVM): Maximum Margin Hyperplane, Support Vectors, Kernel Trick\n• Decision Trees (Entropy, Information Gain, ID3/C4.5) and Random Forest Bagging',
                'important_points': '• Bayes Rule: P(A|B) = [P(B|A) * P(A)] / P(B) enables updating prior beliefs with diagnostic evidence.\n• SVM finds the optimal hyperplane that maximizes the geometric margin between data classes.\n• Random Forests ensemble multiple de-correlated decision trees to reduce variance and mitigate overfitting.',
                'revision_notes': '1. Entropy H(S) = - sum(p_i * log2(p_i)).\n2. Information Gain = H(S) - sum(|Sv|/|S| * H(Sv)).\n3. SVM margin = 2 / ||w||, minimized subject to yi(w.xi + b) >= 1.',
                'possible_questions': 'Q1: State Bayes Rule and explain how a medical diagnosis agent updates disease probability given test results.\nQ2: Explain the mathematics of Information Gain and Entropy in constructing an ID3 decision tree.\nQ3: Formulate the optimization problem for a Soft-Margin Support Vector Machine.\nQ4: Differentiate between Supervised, Unsupervised, and Reinforcement Learning with real-world examples.',
                'questions': [
                    {
                        'q': 'Which learning paradigm relies on an agent interacting with an environment through trial-and-error, receiving scalar reward or penalty signals?',
                        'a': 'Reinforcement Learning',
                        'b': 'Supervised Classification',
                        'c': 'Unsupervised Clustering',
                        'd': 'Rule-Based Parsing',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In Decision Tree learning algorithms like ID3, what statistical metric measures the reduction in dataset entropy achieved by splitting on an attribute?',
                        'a': 'Mean Squared Error',
                        'b': 'Information Gain',
                        'c': 'Euclidean Distance',
                        'd': 'Confusion Matrix',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In a Support Vector Machine (SVM), what is the primary role of the "Kernel Trick"?',
                        'a': 'It reduces the total number of training data points by 50%',
                        'b': 'It implicitly maps non-linearly separable input data into a higher-dimensional feature space where a linear separating hyperplane exists, without computing coordinates directly',
                        'c': 'It accelerates matrix multiplication using floating point approximations',
                        'd': 'It compresses the weight vector into integer values for low-power hardware',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 6,
                'name': 'AI Applications & Perception',
                'desc': 'Language Models, Information Retrieval (IR), Information Extraction (IE), Natural Language Processing, Machine Translation, Speech Recognition architectures, Robotics hardware, perception, localization, mapping (SLAM), and motion planning.',
                'video_id': 'tp0m1y8_1k8',
                'video_title': 'Applied AI: Language Models, NLP, Machine Translation, Robotics & Perception',
                'duration': 1100,
                'transcript': 'Our concluding module explores applied AI systems across perception, language, and physical robotics. In language systems, we study the evolution from statistical n-gram language models to modern Transformer architectures. We examine Information Retrieval engines using inverted indices and TF-IDF/BM25 scoring, alongside Information Extraction for entity and relation extraction. In physical agents, we investigate robotic hardware, perception using LiDAR and stereo vision, probabilistic localization using particle filters, Simultaneous Localization and Mapping (SLAM), and configuration space motion planning.',
                'summary': 'Explores modern applications of AI: NLP, Machine Translation, Information Retrieval, and Autonomous Robotic Perception and Navigation.',
                'key_concepts': '• Natural Language Processing & Language Models (Tokenization, Embeddings, Attention)\n• Information Retrieval (Inverted Index, TF-IDF, Vector Space Model, BM25)\n• Information Extraction vs Information Retrieval\n• Speech Recognition Pipeline (Acoustic and Language Models)\n• Robotics: Sensors (LiDAR, Sonar, Vision), SLAM (Simultaneous Localization and Mapping), Configuration Space (C-space) Motion Planning',
                'important_points': '• Information Retrieval returns ranked relevant documents; Information Extraction populates structured databases from unstructured text.\n• SLAM solves the chicken-and-egg problem: building a map of an unknown environment while simultaneously tracking the robot\'s location within it.\n• Configuration space represents a robot as a single point, facilitating collision-free path planning.',
                'revision_notes': '1. TF-IDF = Term Frequency * Inverse Document Frequency: log(N / df).\n2. SLAM: Simultaneous Localization and Mapping using Extended Kalman Filters or Particle Filters.\n3. Motion planning algorithms: A*, Rapidly-exploring Random Trees (RRT), Visibility Graphs.',
                'possible_questions': 'Q1: Explain the architecture of an Information Retrieval system using an inverted index and vector space model.\nQ2: What is SLAM? Why is it fundamental for autonomous mobile robots?\nQ3: Differentiate between Information Extraction (IE) and Information Retrieval (IR).\nQ4: Describe how Transformer self-attention mechanisms revolutionized machine translation.',
                'questions': [
                    {
                        'q': 'What does the acronym "SLAM" stand for in autonomous robotic navigation and perception?',
                        'a': 'Simultaneous Localization and Mapping',
                        'b': 'Standard Linear Algebra Machine',
                        'c': 'Synchronous Low-latency Audio Multiplexer',
                        'd': 'Systematic Learning Algorithm Module',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In Information Retrieval search engines, what core data structure maps every distinct vocabulary word to a list of documents in which it appears?',
                        'a': 'Hash Table of Binary Trees',
                        'b': 'Inverted Index',
                        'c': 'Circular Queue',
                        'd': 'Relational Schema Matrix',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In robotics path planning, why do engineers transform the robot and physical obstacles into "Configuration Space" (C-Space)?',
                        'a': 'Because C-Space compresses 3D geometry into 2D bitmaps to save disk space',
                        'b': 'Because shrinking the physical robot to a single point while expanding obstacles by the robot radius simplifies collision detection to basic point-in-polygon tests',
                        'c': 'Because hardware motors only accept coordinates expressed in polar angles',
                        'd': 'Because obstacle coordinates change on every CPU clock cycle',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            }
        ]
    },

    # -------------------------------------------------------------------------------------------------
    # SUBJECT 3: BIG DATA ANALYSIS (CSE16504.1)
    # -------------------------------------------------------------------------------------------------
    {
        'subject_code': 'CSE16504.1',
        'subject_name': 'Big Data Analysis',
        'modules': [
            {
                'seq': 1,
                'name': 'Introduction to Big Data & Hadoop Ecosystem',
                'desc': 'Types of digital data (Structured, Semi-Structured, Unstructured), Big Data definition and analytics, History of Hadoop, Apache Hadoop architecture, analysing data with Unix tools vs Hadoop, Hadoop streaming, Hadoop Ecosystem, IBM Big Data strategy, Infosphere BigInsights & BigSheets.',
                'video_id': 'gB9n2Ghs3eQ',
                'video_title': 'Introduction to Big Data, The 5 Vs & The Apache Hadoop Ecosystem Overview',
                'duration': 1250,
                'transcript': 'Welcome to Big Data Analysis. In this foundational module, we analyze the characteristics of Big Data. Data is classified as structured (relational tables), semi-structured (XML, JSON, server logs), or unstructured (audio, video, raw text). We examine the 5 Vs: Volume, Velocity, Variety, Veracity, and Value. We trace the history of Apache Hadoop from Google GFS and MapReduce whitepapers. We contrast data analysis using classic Unix shell pipes against Hadoop distributed clusters. Finally, we survey the Hadoop ecosystem: HDFS, YARN, MapReduce, Pig, Hive, HBase, Spark, and enterprise platforms like IBM BigInsights.',
                'summary': 'Covers Big Data characteristics (5 Vs), data types, distributed computing motivations, Hadoop architecture history, and ecosystem tools.',
                'key_concepts': '• Classification of Digital Data: Structured, Semi-Structured, Unstructured\n• The 5 Vs of Big Data: Volume, Velocity, Variety, Veracity, Value\n• Limitations of Traditional RDBMS at Terabyte/Petabyte Scale\n• Apache Hadoop Core Architecture: Storage (HDFS), Resource Management (YARN), Compute (MapReduce)\n• Hadoop Ecosystem Components (Sqoop, Flume, Hive, Pig, HBase, Spark)',
                'important_points': '• Hadoop brings computation to where data resides rather than moving massive datasets across networks.\n• Hadoop is designed to run on clusters of commodity hardware with built-in software-level fault tolerance.\n• Hadoop Streaming permits writing MapReduce jobs using any language supporting standard input/output.',
                'revision_notes': '1. Structured: RDBMS tables, CSV with strict schema.\n2. Semi-structured: JSON, XML, NoSQL documents with self-describing tags.\n3. Unstructured: Images, video streams, medical sensor waveforms.\n4. Core principle: Data Locality (moving computation is cheaper than moving data).',
                'possible_questions': 'Q1: Describe the 5 Vs of Big Data with practical industrial examples.\nQ2: Differentiate between structured, semi-structured, and unstructured digital data.\nQ3: Explain the core architectural components of the Apache Hadoop Ecosystem.\nQ4: Why do traditional relational databases fail when processing high-velocity, unstructured big data?',
                'questions': [
                    {
                        'q': 'Which of the following data formats is classified as "Semi-Structured" data?',
                        'a': 'Relational MySQL database table',
                        'b': 'JSON (JavaScript Object Notation) file with nested key-value tags',
                        'c': 'Raw uncompressed WAV audio recording',
                        'd': 'Printed hardcover book page',
                        'correct': 'B',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'What core philosophy enables Apache Hadoop to efficiently process petabytes of distributed data without network bandwidth saturation?',
                        'a': 'Data Locality: scheduling computation tasks directly on the cluster nodes where the required data blocks physically reside',
                        'b': 'Compressing all data onto a single high-speed solid state drive',
                        'c': 'Converting all text into 8-bit integer codes before saving',
                        'd': 'Requiring dedicated gigabit satellite uplinks between all servers',
                        'correct': 'A',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In Big Data analytics, what does the "Veracity" dimension specifically assess regarding incoming data streams?',
                        'a': 'The maximum network throughput in gigabits per second',
                        'b': 'The trustworthiness, accuracy, noise level, and reliability of the data source',
                        'c': 'The monetary market price of the raw data on commercial exchanges',
                        'd': 'The physical weight of the storage server racks',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 2,
                'name': 'HDFS (Hadoop Distributed File System)',
                'desc': 'Design principles of HDFS, HDFS concepts, block size and replication, Command Line Interface (CLI), Hadoop file system interfaces, read and write data flow, data ingestion with Apache Flume and Apache Sqoop, Hadoop archives, Hadoop I/O, compression, serialization, Apache Avro.',
                'video_id': '4ZylXhB63-E',
                'video_title': 'HDFS Architecture: NameNode, DataNodes, Read/Write Data Flow & Ingestion Tools',
                'duration': 1350,
                'transcript': 'This lecture investigates HDFS (Hadoop Distributed File System). HDFS is designed for storing very large files with streaming data access patterns on commodity clusters. Files are split into large blocks (default 128MB) replicated across distinct racks (default replication factor 3). We examine the master-worker topology: NameNode manages namespace and block locations in RAM; DataNodes store and serve actual blocks. We trace the complete read and write pipeline, rack awareness, and checkpointing by the Secondary NameNode. We explore ingestion tools: Apache Sqoop for RDBMS transfer and Apache Flume for streaming web logs.',
                'summary': 'Deep dive into HDFS architecture, block allocation, read/write pipelines, replication strategies, and ingestion using Sqoop and Flume.',
                'key_concepts': '• HDFS Architecture: Master NameNode, Worker DataNodes, Secondary NameNode\n• Block Size (128 MB default) and Rack-Aware Replication Factor (3x default)\n• Anatomy of File Read and File Write in HDFS\n• Fault Tolerance: Heartbeats, Block Reports, Automatic Re-replication\n• Data Ingest Tools: Apache Sqoop (RDBMS <-> HDFS) and Apache Flume (Streaming logs <-> HDFS)\n• Hadoop I/O: SequenceFiles, Apache Avro serialization, compression codecs (Snappy, Gzip)',
                'important_points': '• NameNode stores all metadata in memory (fsimage + edits log); losing the NameNode renders the entire HDFS cluster inaccessible.\n• HDFS follows a "Write Once, Read Many" (WORM) access model; random in-place updates are not supported.\n• Rack awareness places replica 1 on local rack, replica 2 on same rack, and replica 3 on a separate remote rack.',
                'revision_notes': '1. CLI commands: hdfs dfs -ls /, hdfs dfs -put file.txt /user/data, hdfs dfs -cat /user/data/file.txt.\n2. Sqoop: import from MySQL to HDFS; export from HDFS to MySQL.\n3. Flume: Source -> Channel -> Sink architecture for continuous streaming data.',
                'possible_questions': 'Q1: Explain the master-slave architecture of HDFS with a diagram showing NameNode, DataNodes, and Secondary NameNode.\nQ2: Trace the step-by-step data flow when an HDFS client writes a 256MB file.\nQ3: How does HDFS rack awareness optimize network bandwidth and fault tolerance?\nQ4: Differentiate between Apache Sqoop and Apache Flume regarding target data sources and architectures.',
                'questions': [
                    {
                        'q': 'What is the default block size for files stored in modern Apache Hadoop HDFS clusters?',
                        'a': '4 KB',
                        'b': '64 KB',
                        'c': '128 MB',
                        'd': '10 GB',
                        'correct': 'C',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'Which tool in the Hadoop ecosystem is specialized for bidirectional bulk data transfer between relational databases (like MySQL/Oracle) and HDFS?',
                        'a': 'Apache Sqoop',
                        'b': 'Apache Flume',
                        'c': 'Apache Spark Streaming',
                        'd': 'Apache Oozie',
                        'correct': 'A',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'What critical role does the Secondary NameNode perform in an HDFS cluster topology?',
                        'a': 'It acts as an instantaneous active-standby hot failover if the primary NameNode hardware crashes',
                        'b': 'It periodically merges the NameNode fsimage snapshot with the edit log to prevent the edit log from growing uncontrollably in RAM',
                        'c': 'It encrypts data blocks before writing to worker DataNode hard drives',
                        'd': 'It compresses network packets passing between cluster switches',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 3,
                'name': 'MapReduce Architecture & Execution',
                'desc': 'Anatomy of a MapReduce job run, job submission, failure modes, job scheduling (FIFO, Fair, Capacity), shuffle and sort phase, task execution, MapReduce data types, InputFormats, OutputFormats, partitioners, combiners, distributed cache.',
                'video_id': 'S99B9X3q0i8',
                'video_title': 'MapReduce Framework: Programming Model, Shuffle & Sort Mechanics, and Task Execution',
                'duration': 1400,
                'transcript': 'In this lecture, we examine MapReduce, Hadoop\'s original distributed parallel compute engine. The MapReduce model processes data as key-value pairs: Map: (k1, v1) -> list(k2, v2), and Reduce: (k2, list(v2)) -> list(k3, v3). We analyze the anatomy of a job execution under YARN: ResourceManager allocates container resources, while NodeManagers launch tasks. We examine the Shuffle and Sort phase where intermediate map outputs are partitioned by key, sorted, and transferred over the network to reducers. We explore performance optimizations: in-mapper combining, custom partitioners, and the distributed cache.',
                'summary': 'Comprehensive guide to the MapReduce programming paradigm, YARN execution pipeline, Shuffle & Sort phase, and combiner/partitioner optimization.',
                'key_concepts': '• MapReduce Mathematical Transformation: Map and Reduce Signatures\n• YARN Architecture: ResourceManager, NodeManager, ApplicationMaster, Containers\n• Shuffle and Sort Phase: Spill to disk, In-memory buffer, Merging, Network fetch\n• Combiner Function: Mini-reducer applied locally to reduce network shuffle traffic\n• Partitioner: HashPartitioner determining target reducer for intermediate keys\n• InputFormats (TextInputFormat, KeyValueTextInputFormat) and RecordReaders',
                'important_points': '• Combiner functions must be commutative and associative (like Sum or Max, but not simple Average).\n• The Shuffle phase is the most network-intensive phase of a MapReduce job.\n• Speculative execution launches duplicate tasks on alternative nodes when a node runs unusually slow.',
                'revision_notes': '1. Map output is buffered in RAM (default 100MB); spills to disk when 80% full.\n2. HashPartitioner formula: (key.hashCode() & Integer.MAX_VALUE) % numReduceTasks.\n3. ApplicationMaster manages lifecycle of a specific application within YARN.',
                'possible_questions': 'Q1: Trace the lifecycle of a MapReduce job execution from submission to completion under YARN.\nQ2: Explain the Shuffle and Sort phase in detail with a diagram.\nQ3: Why can a Combiner be used for counting words but cannot be directly used for calculating average temperatures?\nQ4: Write the Map and Reduce logic in pseudocode for calculating Word Count on big datasets.',
                'questions': [
                    {
                        'q': 'In Hadoop MapReduce, what are the formal input and output signatures of the Map function?',
                        'a': 'Input: (k1, v1) -> Output: list of intermediate key-value pairs (k2, v2)',
                        'b': 'Input: SQL query string -> Output: HTML web page table',
                        'c': 'Input: Array of integers -> Output: Single floating point average',
                        'd': 'Input: Binary executable -> Output: Compiler assembly listing',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'What is the primary optimization benefit of implementing a "Combiner" in a MapReduce application pipeline?',
                        'a': 'It bypasses the need for the HDFS file system',
                        'b': 'It performs local pre-aggregation on map task outputs, significantly reducing the volume of data transmitted across the network during Shuffle',
                        'c': 'It converts Java source code into compiled GPU machine instructions',
                        'd': 'It automatically corrects typographical errors in text datasets',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'During the Shuffle and Sort phase, how does the default Hadoop "HashPartitioner" determine which specific Reducer task receives an intermediate key-value pair?',
                        'a': 'By randomly picking an idle Reducer from the cluster pool',
                        'b': 'By evaluating: (key.hashCode() & Integer.MAX_VALUE) % numReduceTasks',
                        'c': 'By checking alphabetical order of the worker node IP addresses',
                        'd': 'By measuring which Reducer has the lowest CPU temperature',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 4,
                'name': 'Hadoop Eco System: Pig, Hive, HBase & Big SQL',
                'desc': 'Apache Pig (Grunt shell, Pig Latin, UDFs, data operations vs databases), Apache Hive (Hive shell, services, metastore, HiveQL, managed vs external tables, querying data, UDFs), Apache HBase (concepts, column-oriented storage, clients, HBase vs RDBMS), Big SQL introduction.',
                'video_id': 'N67p9_nN2kI',
                'video_title': 'Hadoop Ecosystem: Apache Pig, Apache Hive, HBase Columnar Store & Big SQL',
                'duration': 1300,
                'transcript': 'In this session, we investigate higher-level Hadoop ecosystem tools: Pig, Hive, HBase, and Big SQL. Writing raw Java MapReduce code is verbose and complex; Apache Pig introduces Pig Latin, an imperative dataflow language compiled into MapReduce DAGs. Apache Hive provides HiveQL, a declarative SQL dialect that allows data analysts to query petabytes stored on HDFS without writing code. We contrast Hive Managed Tables with External Tables. We then examine Apache HBase, a distributed, versioned, column-oriented NoSQL database modeled after Google Bigtable, delivering sub-millisecond random read/write lookups on billions of rows.',
                'summary': 'Covers higher-level query engines: Apache Pig dataflows, Apache Hive SQL data warehousing, and Apache HBase real-time columnar storage.',
                'key_concepts': '• Apache Pig: Execution Modes (Local, MapReduce/Tez), Grunt Shell, Pig Latin (LOAD, FILTER, GROUP, FOREACH)\n• Apache Hive: Hive Architecture (Driver, Compiler, Metastore, Execution Engine)\n• Hive Tables: Managed (Internal) vs External Tables, Partitioning, Bucketing\n• Apache HBase: Architecture (HMaster, RegionServer, HLog/WAL, MemStore, HFile)\n• Row-Oriented (RDBMS) vs Column-Family Oriented (HBase) Data Storage\n• Big SQL: Enterprise SQL on Hadoop with cost-based query optimization',
                'important_points': '• Dropping a Managed Hive table deletes both metadata and actual HDFS data; dropping an External table preserves HDFS files.\n• Hive partitioning creates physical subdirectories on HDFS, radically accelerating query filtering.\n• HBase uses row keys for fast lookups; data is stored sorted lexicographically by row key.',
                'revision_notes': '1. Pig Latin: A = LOAD \'data.txt\' AS (id:int, name:chararray); B = FILTER A BY id > 10; DUMP B;\n2. Hive partitioning: PARTITIONED BY (year INT, month INT) avoids full table scans.\n3. HBase write path: Client -> Write-Ahead Log (WAL) -> MemStore -> Flush to HFile on HDFS.',
                'possible_questions': 'Q1: Compare and contrast Apache Pig, Apache Hive, and traditional RDBMS on language, execution model, and latency.\nQ2: Explain Hive Managed Tables vs External Tables with DDL commands.\nQ3: Describe the architecture and write path of Apache HBase from client to HFile.\nQ4: What is the purpose of Partitioning and Bucketing in Apache Hive performance optimization?',
                'questions': [
                    {
                        'q': 'What high-level declarative language is used in Apache Hive to query large datasets stored on HDFS?',
                        'a': 'HiveQL (HQL)',
                        'b': 'Pig Latin',
                        'c': 'C++ Assembly',
                        'd': 'Prolog Predicate Calculus',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'When dropping an "External Table" in Apache Hive using the command DROP TABLE my_external_table, what happens to the underlying data files on HDFS?',
                        'a': 'The underlying HDFS data files are permanently deleted along with the metadata',
                        'b': 'Only the schema metadata in the Hive Metastore is deleted; the actual data files remain safe and intact on HDFS',
                        'c': 'The entire Hadoop cluster restarts in emergency recovery mode',
                        'd': 'The data files are moved to the MySQL recycle bin',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In Apache HBase, how does the architecture guarantee high write throughput while maintaining durable persistence on HDFS?',
                        'a': 'By writing exclusively to optical discs',
                        'b': 'By writing incoming mutations simultaneously to an in-memory MemStore and an append-only Write-Ahead Log (WAL), flushing to HFiles asynchronously',
                        'c': 'By bypassing network protocols and writing directly to RAM chips on the master server',
                        'd': 'By converting table columns into CSV text files every millisecond',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 5,
                'name': 'Predictive Analytics & Visual Data Analysis',
                'desc': 'Simple linear regression, multiple linear regression, Ordinary Least Squares (OLS), interpretation of regression coefficients, model evaluation, visual data analysis techniques, interactive visualizations, systems, dashboards and big data applications.',
                'video_id': 'zITIFTsivN8',
                'video_title': 'Predictive Analytics: Simple & Multiple Linear Regression, Residual Analysis and Big Data Visualization',
                'duration': 1200,
                'transcript': 'This lecture covers Predictive Analytics and Visual Data Analysis for Big Data. Predictive analytics uncovers patterns in historical data to forecast future events. We examine Linear Regression, modeling relationships between dependent target variables and independent predictors. We formulate Ordinary Least Squares (OLS) to minimize the sum of squared residuals. In Multiple Linear Regression, we interpret coefficients, test for multicollinearity (VIF), and evaluate goodness of fit with R-squared and Adjusted R-squared. Finally, we explore visual interaction techniques (brushing, zooming, linked views) for analyzing high-dimensional big data.',
                'summary': 'Covers predictive modeling using simple and multiple linear regression, residual analysis, statistical significance, and big data visualization systems.',
                'key_concepts': '• Linear Regression Model Formulation: y = beta_0 + beta_1*x_1 + ... + epsilon\n• Ordinary Least Squares (OLS) Parameter Estimation\n• Interpretation of Regression Coefficients and p-values\n• Model Evaluation: R-Squared, Adjusted R-Squared, RMSE, Residual Diagnostics\n• Big Data Visualization Techniques: Density Heatmaps, Hexagonal Binning, Parallel Coordinates, Interactive Dashboards',
                'important_points': '• Correlation does not imply causation; regression identifies association patterns.\n• Multicollinearity inflates standard errors of regression coefficients, making estimates unstable.\n• Visualizing big data directly as raw scatter points causes overplotting; binning aggregation reveals underlying density.',
                'revision_notes': '1. Simple linear regression slope: beta_1 = Cov(x, y) / Var(x).\n2. R-squared = 1 - (SS_res / SS_tot): proportion of variance explained by the model.\n3. Residual assumptions: Normality, Homoscedasticity, Independence.',
                'possible_questions': 'Q1: Derive the Ordinary Least Squares (OLS) estimates for the slope and intercept in simple linear regression.\nQ2: Explain the difference between R-squared and Adjusted R-squared in multiple linear regression.\nQ3: What is multicollinearity? How do you detect and resolve it in regression modeling?\nQ4: Describe three interactive visualization techniques used for analyzing high-dimensional big datasets.',
                'questions': [
                    {
                        'q': 'In simple linear regression (y = beta_0 + beta_1 * x), what does the coefficient beta_1 mathematically represent?',
                        'a': 'The predicted value of y when x equals zero',
                        'b': 'The estimated change in the target variable y for every one-unit increase in predictor variable x',
                        'c': 'The total number of samples in the dataset',
                        'd': 'The percentage of errors made by the CPU',
                        'correct': 'B',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'Why is "Adjusted R-Squared" preferred over standard R-Squared when evaluating a multiple linear regression model with numerous predictor variables?',
                        'a': 'Standard R-Squared can only be computed for integer numbers',
                        'b': 'Standard R-Squared never decreases when adding new predictors, whereas Adjusted R-Squared penalizes the addition of non-informative variables',
                        'c': 'Adjusted R-Squared executes faster on GPU hardware',
                        'd': 'Standard R-Squared requires non-linear activation functions',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'When visualizing multi-million-row big datasets in interactive analytics dashboards, what visual artifact occurs if all raw data points are rendered simultaneously, and how is it resolved?',
                        'a': 'Under-fitting resolved by adding more monitor screens',
                        'b': 'Severe Overplotting (occlusion) resolved by 2D spatial binning (hexagonal binning or density heatmaps)',
                        'c': 'Data corruption resolved by restarting the MySQL server',
                        'd': 'Pixel inverted colors resolved by gamma calibration',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 6,
                'name': 'NoSQL Databases & Distributed Data Modeling',
                'desc': 'Introduction to NoSQL, aggregate data models, key-value, document, column-family, graph databases, relationships, schemaless databases, materialized views, distribution models, sharding, master-slave replication, peer-to-peer replication, CAP Theorem, BASE consistency, version stamps, MapReduce on NoSQL.',
                'video_id': '0buKQHokLK8',
                'video_title': 'NoSQL Database Architectures, CAP Theorem, Sharding, Replication & Consistency Models',
                'duration': 1100,
                'transcript': 'In our final module on Big Data, we explore NoSQL Databases and Distributed Data Modeling. Traditional relational databases enforce ACID transactions with rigid schemas, creating bottlenecks for horizontal scaling. NoSQL architectures embrace Aggregate Data Models: Key-Value stores (Redis), Document databases (MongoDB), Column-Family stores (Cassandra), and Graph databases (Neo4j). We explore distributed data distribution: Sharding for horizontal partitioning, and Replication (Master-Slave vs Peer-to-Peer). We study Brewer\'s CAP Theorem and BASE properties (Basically Available, Soft state, Eventual consistency), alongside vector clocks for version reconciliation.',
                'summary': 'Covers the four NoSQL database categories, horizontal sharding, replication models, the CAP Theorem, and BASE eventual consistency.',
                'key_concepts': '• Four NoSQL Data Models: Key-Value, Document, Wide-Column, Graph\n• Schema-less Data Design and Denormalization\n• Distribution Strategies: Sharding (Hash vs Range Partitioning), Master-Slave vs Peer-to-Peer Replication\n• The CAP Theorem: Consistency, Availability, Partition Tolerance (Why CA is impossible distributed)\n• ACID vs BASE: Basically Available, Soft State, Eventual Consistency\n• Vector Clocks and Version Stamps for Conflict Resolution',
                'important_points': '• Under a network partition (P), a distributed system must choose between Consistency (CP) and Availability (AP).\n• Graph databases use index-free adjacency to traverse connections in O(1) time per edge.\n• Document stores represent hierarchical relationships via embedded documents instead of expensive joins.',
                'revision_notes': '1. Key-Value: high throughput caching (Redis, DynamoDB).\n2. Document: flexible JSON-like documents (MongoDB, CouchDB).\n3. Wide-column: massive sparse write throughput (Cassandra, ScyllaDB).\n4. Graph: connected nodes and edges (Neo4j, Amazon Neptune).\n5. CAP Theorem: In distributed systems, network partitions are inevitable; you must choose CP or AP.',
                'possible_questions': 'Q1: Explain the four categories of NoSQL databases with examples and ideal use cases for each.\nQ2: State and prove the CAP Theorem. Give examples of CP, AP, and CA systems.\nQ3: Compare ACID transaction guarantees in RDBMS with BASE properties in NoSQL systems.\nQ4: Describe how Vector Clocks resolve concurrent write conflicts in peer-to-peer distributed databases.',
                'questions': [
                    {
                        'q': 'Which category of NoSQL database represents data as nodes, edges, and properties to efficiently traverse highly interconnected relationships?',
                        'a': 'Graph Database (e.g. Neo4j)',
                        'b': 'Key-Value Cache',
                        'c': 'Flat CSV File',
                        'd': 'Columnar HDFS Archive',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'According to Brewer\'s CAP Theorem, when an unavoidable network partition occurs in a distributed database cluster, what trade-off must the system make?',
                        'a': 'The system must choose between encrypting data or compressing data',
                        'b': 'The system must choose between returning consistent latest data (Consistency) or guaranteeing a response to every query (Availability)',
                        'c': 'The system must reboot all servers and format storage arrays',
                        'd': 'The system must switch from 64-bit to 32-bit integer arithmetic',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In distributed NoSQL databases with Master-Slave replication, what is a primary drawback compared to Peer-to-Peer (Masterless) replication topologies?',
                        'a': 'Master-Slave systems cannot store text strings',
                        'b': 'The Master node represents a single point of failure for write operations until an election promotes a new master',
                        'c': 'Slave nodes consume double the memory bandwidth of master nodes',
                        'd': 'Data can only be replicated across computers on the same physical table',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            }
        ]
    },

    # -------------------------------------------------------------------------------------------------
    # SUBJECT 4: NLP FOR HEALTH RELATED TEXT (CSD14505.3/CSE16505.2)
    # -------------------------------------------------------------------------------------------------
    {
        'subject_code': 'CSE16505.2',
        'subject_name': 'NLP for Health Related Text',
        'modules': [
            {
                'seq': 1,
                'name': 'Introduction to Healthcare NLP & Preprocessing',
                'desc': 'Overview of Natural Language Processing in medicine, clinical linguistic characteristics, text representation and preprocessing for clinical notes, medical tokenization, clinical stop words, lemmatization, applications of NLP in healthcare, challenges and HIPAA compliance.',
                'video_id': 'd_ERyP0yQfU',
                'video_title': 'Natural Language Processing for Healthcare: Clinical NLP, Text Preprocessing & Challenges',
                'duration': 1200,
                'transcript': 'Welcome to NLP for Health-Related Text. In healthcare, over 80% of critical patient information resides in unstructured clinical narratives—physician progress notes, radiology reports, and pathology summaries. In this opening module, we analyze the challenges of biomedical NLP: non-standard abbreviations, ambiguous clinical shorthand, telegraphic sentence fragments, and typographical errors. We establish clinical text preprocessing pipelines including specialized sentence splitting, medical tokenization, and negation detection (e.g. NegEx). Finally, we explore HIPAA regulations and de-identification algorithms that remove Protected Health Information (PHI).',
                'summary': 'Introduces clinical NLP applications, unique characteristics of unstructured EHR narratives, medical preprocessing, negation detection, and patient privacy.',
                'key_concepts': '• Unstructured vs Structured Healthcare Data in Electronic Health Records (EHR)\n• Challenges in Clinical Text: Acronyms, Jargon, Misspellings, Negated Concepts\n• Medical Preprocessing Pipeline: Tokenization, Lemmatization, Section Segmentation\n• Negation and Uncertainty Detection (NegEx algorithm, ConText)\n• De-identification of Protected Health Information (PHI) under HIPAA Safe Harbor',
                'important_points': '• A medical symptom mentioned in a clinical note is frequently negated (e.g. "patient denies chest pain"); standard NLP models fail if they miss negation.\n• HIPAA specifies 18 types of Protected Health Information (PHI) that must be removed before sharing.\n• Clinical tokenizers must avoid splitting medical compounds like "mg/kg" or numerical dosages like "0.5mg".',
                'revision_notes': '1. NegEx algorithm: detects pre-negation and post-negation trigger phrases within a window of words.\n2. PHI: names, geographic subdivisions, dates directly related to an individual, phone numbers, medical record numbers.\n3. Clinical text representation: bag of medical words vs contextual biomedical transformer embeddings.',
                'possible_questions': 'Q1: Why is negation detection critical when extracting symptoms from physician notes? Explain the NegEx algorithm.\nQ2: List and describe six categories of Protected Health Information (PHI) under HIPAA Safe Harbor rules.\nQ3: Explain the challenges of clinical text processing compared to general domain NLP on newspaper articles.\nQ4: Describe how clinical section segmentation helps interpret ambiguous medical findings.',
                'questions': [
                    {
                        'q': 'Why is "Negation Detection" (such as via the NegEx algorithm) indispensable when analyzing patient clinical notes?',
                        'a': 'Because physicians frequently document symptoms that the patient does NOT have (e.g. "denies fever, no shortness of breath")',
                        'b': 'Because computers cannot process negative numbers in medical billing',
                        'c': 'Because medical software only accepts affirmative statements',
                        'd': 'Because hospital networks invert electrical polarity at night',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'Under United States HIPAA Safe Harbor regulations, how many distinct categories of Protected Health Information (PHI) must be stripped during de-identification?',
                        'a': '2 categories',
                        'b': '5 categories',
                        'c': '18 categories',
                        'd': '100 categories',
                        'correct': 'C',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'Why do standard general-purpose tokenizers (like NLTK word_tokenize) frequently corrupt clinical text during preprocessing?',
                        'a': 'They split critical numerical drug dosages (e.g. "0.25mg" into "0", ".", "25mg") and split slash-separated clinical shorthand (e.g. "w/o", "s/p")',
                        'b': 'They translate Latin anatomical names into Greek',
                        'c': 'They cannot process documents longer than 10 lines',
                        'd': 'They only recognize capital letters',
                        'correct': 'A',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 2,
                'name': 'Clinical Corpus Creation & Medical Annotation',
                'desc': 'Introduction to corpus creation for healthcare NLP, data sources (MIMIC-III, PubMed, clinical trials, EHRs), biomedical ontologies (UMLS, SNOMED CT, ICD-10, MeSH, RxNorm), annotation tools and techniques (brat, Prodigy), annotation guidelines, inter-annotator agreement (Cohen\'s Kappa), quality assurance.',
                'video_id': 'e62uE2rY3nQ',
                'video_title': 'Clinical Corpus Curation: Medical Ontologies, Annotation Guidelines & Quality Evaluation',
                'duration': 1150,
                'transcript': 'In this lecture, we study the methodology of building high-quality clinical corpora. Supervised medical machine learning requires rigorously annotated datasets. We explore open-access clinical data repositories like MIMIC-III and MIMIC-IV from MIT, alongside biomedical literature from PubMed Central. We examine standard medical vocabularies: SNOMED CT for clinical findings, ICD-10 for diagnostic billing, RxNorm for medications, and MeSH for indexing. We examine the UMLS Metathesaurus that unifies these ontologies. We detail manual annotation workflows using tools like brat, formulation of annotation guidelines, and inter-rater agreement measurement via Cohen\'s Kappa and Fleiss\' Kappa.',
                'summary': 'Covers medical dataset curation, clinical ontologies (UMLS, SNOMED CT, ICD-10), annotation workflows, and inter-annotator agreement evaluation.',
                'key_concepts': '• Benchmark Medical Corpora: MIMIC-III/IV, i2b2/n2c2 Clinical Challenges\n• Controlled Medical Vocabularies: SNOMED CT, ICD-10-CM, RxNorm, LOINC, MeSH\n• Unified Medical Language System (UMLS) and Concept Unique Identifiers (CUIs)\n• Medical Annotation Tools: brat, Prodigy, INCEpTION\n• Quality Assurance: Inter-Annotator Agreement (Cohen\'s Kappa k, Fleiss\' Kappa)',
                'important_points': '• Medical annotation requires certified clinical domain experts (doctors, nurses, medical coders).\n• Cohen\'s Kappa accounts for agreement occurring purely by chance: k = (Po - Pe) / (1 - Pe).\n• UMLS maps synonymous clinical terms across 100+ vocabularies to a single CUI.',
                'revision_notes': '1. SNOMED CT: comprehensive clinical healthcare terminology with poly-hierarchical relationships.\n2. ICD-10: international classification of diseases primarily used for epidemiological tracking and hospital reimbursement.\n3. Cohen\'s Kappa: k > 0.8 represents near-perfect agreement; k < 0.4 represents poor agreement.',
                'possible_questions': 'Q1: What is the Unified Medical Language System (UMLS)? Explain how Concept Unique Identifiers (CUIs) resolve medical synonymy.\nQ2: Describe the formula and significance of Cohen\'s Kappa in evaluating medical corpus annotation quality.\nQ3: Differentiate between SNOMED CT, ICD-10, and RxNorm regarding scope and healthcare usage.\nQ4: Detail the steps required to curate an annotated clinical corpus from raw EHR progress notes.',
                'questions': [
                    {
                        'q': 'Which standardized pharmaceutical vocabulary is specifically designed to normalize clinical medication names, active ingredients, and dosage forms?',
                        'a': 'RxNorm',
                        'b': 'ICD-10',
                        'c': 'HTML5',
                        'd': 'TCP/IP',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'What statistical metric is standardly computed to assess whether two clinical annotators agree consistently above random chance when labeling medical spans?',
                        'a': 'Cohen\'s Kappa coefficient',
                        'b': 'Euclidean Norm',
                        'c': 'Shannon Entropy',
                        'd': 'P-value of Linear Regression',
                        'correct': 'A',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In the Unified Medical Language System (UMLS), how does the system represent that "Myocardial Infarction", "Heart Attack", and "Cardiac Arrest" share conceptual equivalence?',
                        'a': 'By deleting all three terms and replacing them with a random number',
                        'b': 'By mapping all synonymous expressions to a single unified Concept Unique Identifier (CUI)',
                        'c': 'By appending exclamation points to the end of each word',
                        'd': 'By converting them into SQL join tables',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 3,
                'name': 'Clinical Information Extraction & NER',
                'desc': 'Named Entity Recognition (NER) for healthcare entities (diseases, drugs, dosages, routes, frequencies, symptoms, lab tests), Relation Extraction (RE) for biomedical events (drug-disease interactions, adverse drug reactions, treatment relations), Entity linking and concept normalization to ontologies, Knowledge Graph creation.',
                'video_id': 'JqY6Yt9u6E4',
                'video_title': 'Clinical Named Entity Recognition (NER), Relation Extraction & Medical Knowledge Graphs',
                'duration': 1300,
                'transcript': 'In this lecture, we study Clinical Information Extraction (IE). Information extraction converts unstructured clinical text into structured relational records. We formulate Named Entity Recognition (NER) as sequence labeling (IOB/BIO schemes) to detect medical entities: diseases, anatomical sites, pharmaceuticals, dosages, routes, and temporal markers. We explore neural architectures: BiLSTM-CRF and fine-tuned BioBERT. We then investigate Biomedical Relation Extraction (RE) to identify interactions such as Drug-Cause-Adverse Event or Treatment-Treats-Condition. Finally, we link entities to ontology concepts and construct clinical Knowledge Graphs.',
                'summary': 'Covers sequence tagging for clinical NER, relation extraction for drug-event interactions, ontology entity linking, and knowledge graph construction.',
                'key_concepts': '• Clinical Named Entity Recognition (NER) and BIO Tagging Schemes\n• Deep Learning Sequence Tagging Architectures: BiLSTM-CRF, BioBERT, ClinicalBERT\n• Biomedical Relation Extraction (RE): Pairwise sentence-level classification of clinical relationships\n• Medical Entity Linking / Concept Normalization (String matching, TF-IDF cosine similarity, dense embedding retrieval)\n• Constructing Clinical Knowledge Graphs from extracted entities and relations',
                'important_points': '• Clinical NER must identify both entity span boundaries and fine-grained semantic categories.\n• A CRF layer on top of BiLSTM/BERT enforces valid label transition constraints (e.g. I-Disease cannot follow O without B-Disease).\n• Relation extraction determines whether a medication mentioned in a note caused an adverse reaction or was prescribed to treat it.',
                'revision_notes': '1. BIO tagging: B = Begin entity, I = Inside entity, O = Outside entity.\n2. Clinical relations: Treats(Drug, Disease), Causes(Drug, Adverse_Effect), Diagnosed_With(Patient, Condition).\n3. Entity normalization: maps extracted string "aspirin 81mg" to RxNorm code.',
                'possible_questions': 'Q1: Illustrate BIO sequence tagging on a sample sentence: "Patient was administered 500mg Metformin oral for Type 2 Diabetes".\nQ2: Explain why adding a Conditional Random Field (CRF) layer enhances BiLSTM and BERT performance on clinical NER.\nQ3: Detail the pipeline for extracting Adverse Drug Events (ADEs) from clinical progress notes.\nQ4: Describe how clinical Knowledge Graphs support diagnostic reasoning in healthcare AI.',
                'questions': [
                    {
                        'q': 'In Named Entity Recognition (NER) using the standard BIO tagging scheme, what does the tag "B-Drug" indicate for a word token?',
                        'a': 'The token represents the beginning word of a drug name entity',
                        'b': 'The token represents a broken database connection',
                        'c': 'The token represents an ordinary non-medical English word',
                        'd': 'The token is ignored by the compiler',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'What is the architectural purpose of placing a Conditional Random Field (CRF) output layer after a bidirectional LSTM in a clinical NER model?',
                        'a': 'To compress weights so the model fits onto a smartphone',
                        'b': 'To model transition dependencies between sequential output labels, preventing illegal tag sequences (like I-Disease directly following O)',
                        'c': 'To perform optical character recognition on scanned PDF notes',
                        'd': 'To execute SQL select queries on clinical databases',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In healthcare NLP, what task does "Entity Normalization" (or Concept Resolution) specifically accomplish after an entity mention is extracted by an NER model?',
                        'a': 'It translates the entity text into multiple European languages',
                        'b': 'It maps the unstructured entity string mention (e.g. "sugar problem") to its standardized concept identifier in a clinical ontology (e.g. SNOMED CT: Diabetes Mellitus)',
                        'c': 'It rounds all numerical lab values to the nearest whole integer',
                        'd': 'It calculates the patient\'s hospital billing invoice',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 4,
                'name': 'Clinical Text Classification & BioBERT',
                'desc': 'Binary and multi-class classification for medical documents, automated clinical diagnostic coding (ICD-10 prediction), feature selection and medical extraction, sentiment analysis for patient experience reviews, deep learning models (CNN, BiLSTM-CRF, Transformer encoders: BioBERT, ClinicalBERT, PubMedBERT).',
                'video_id': '4Bdc55j80l8',
                'video_title': 'Clinical Text Classification: Transformers, BioBERT, ClinicalBERT & Automated ICD Coding',
                'duration': 1350,
                'transcript': 'This session explores Clinical Text Classification. Medical institutions generate millions of documents requiring categorization: triaging emergency admissions, assigning ICD-10 diagnostic billing codes, and analyzing patient satisfaction surveys. We contrast traditional bag-of-words and TF-IDF classifiers with deep Transformer representations. General BERT models trained on Wikipedia fail on clinical jargon; hence we examine domain-specific pre-trained models: BioBERT (trained on PubMed abstracts) and ClinicalBERT (trained on MIMIC clinical notes). We analyze multi-label classification architectures designed to predict hundreds of co-occurring ICD codes from lengthy hospital discharge summaries.',
                'summary': 'Covers medical document classification, automated ICD-10 coding, clinical sentiment analysis, and domain-adapted Transformer models (BioBERT, ClinicalBERT).',
                'key_concepts': '• Clinical Text Classification Applications: Diagnostic Triage, Readmission Risk, Automated ICD-10 Billing\n• Domain-Adapted Pre-trained Transformers: BioBERT, ClinicalBERT, PubMedBERT\n• Multi-Label Classification Challenges in Long Medical Narratives\n• Attention Visualization: Explaining model predictions by highlighting salient clinical keywords\n• Evaluating Medical Classifiers: Micro/Macro F1-Score, Area Under Precision-Recall Curve (AUPRC)',
                'important_points': '• Medical datasets suffer from extreme class imbalance: rare diseases have very few training examples, while hypertension has tens of thousands.\n• Standard BERT has a 512-token limit; clinical discharge summaries often span 3,000+ words, requiring chunking or long-context Transformers (Longformer, BigBird).\n• Domain-specific pre-training on clinical text aligns token embeddings with biomedical vocabulary.',
                'revision_notes': '1. BioBERT: BERT architecture pre-trained on biomedical literature from PubMed and PMC.\n2. ClinicalBERT: BERT pre-trained on ICU clinical notes from MIMIC-III.\n3. Multi-label loss: Binary Cross-Entropy with Sigmoid activations on each output node.',
                'possible_questions': 'Q1: Why does ClinicalBERT significantly outperform standard BERT-base on hospital readmission prediction tasks?\nQ2: Explain the challenge of extreme class imbalance in automated ICD-10 medical coding and how to mitigate it.\nQ3: How do you handle clinical documents that exceed the 512-token limit of Transformer encoders?\nQ4: Describe how attention weight visualization provides explainability in clinical decision support.',
                'questions': [
                    {
                        'q': 'Why does a domain-specific model like ClinicalBERT achieve superior performance on clinical notes compared to general BERT-Base?',
                        'a': 'Because it has 100 times fewer parameters',
                        'b': 'Because it was pre-trained on millions of actual clinical inpatient notes from hospitals, capturing medical acronyms and jargon',
                        'c': 'Because it only runs on medical-grade computer hardware',
                        'd': 'Because it does not utilize attention mechanisms',
                        'correct': 'B',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In automated hospital medical billing, why is ICD-10 coding formulated as a "Multi-Label" classification task rather than a "Multi-Class" classification task?',
                        'a': 'Because a single patient discharge summary can be assigned multiple co-occurring diagnosis and procedure codes simultaneously',
                        'b': 'Because multi-label tasks require no labeled training data',
                        'c': 'Because doctors only write notes on weekends',
                        'd': 'Because ICD-10 codes cannot be represented by numerical matrices',
                        'correct': 'A',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'When evaluating a clinical document classifier predicting a rare life-threatening condition (present in only 0.5% of cases), why is Accuracy a misleading metric, and what metric should be reported instead?',
                        'a': 'Accuracy is misleading because a trivial classifier predicting "negative" every time achieves 99.5% accuracy; PR-AUC and F1-Score must be used',
                        'b': 'Accuracy can only evaluate integer values',
                        'c': 'Accuracy increases training time on GPU clusters',
                        'd': 'There is no issue; Accuracy is always the gold standard metric',
                        'correct': 'A',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 5,
                'name': 'Medical Text Summarization & Generation',
                'desc': 'Automatic summarization of healthcare documents, extractive vs abstractive summarization, text generation for healthcare use cases (patient discharge summaries, clinical consultation notes, radiology impressions), evaluation metrics (ROUGE, BLEU, BERTScore, factual consistency checking in healthcare).',
                'video_id': 'K7_7eG7_b3Y',
                'video_title': 'Clinical Text Summarization & Generative AI: Discharge Summaries, Radiology Reports & Factual Evaluation',
                'duration': 1250,
                'transcript': 'In this lecture, we examine Clinical Text Summarization and Medical Text Generation. Clinicians spend over two hours documenting notes for every hour spent with patients. We examine Extractive Summarization, which scores and selects salient sentences from medical histories, and Abstractive Summarization using sequence-to-sequence Transformers (BART, T5, LLMs) that generate coherent narrative summaries. We examine key clinical generation use cases: synthesizing multi-day hospital stays into discharge summaries, and generating radiology report impressions from findings sections. Finally, we address the critical challenge of factual hallucinations and explore specialized medical evaluation metrics.',
                'summary': 'Covers extractive and abstractive clinical summarization, clinical document generation, and evaluating medical factual consistency.',
                'key_concepts': '• Extractive Summarization (Graph-based TextRank, BERT sentence classification) vs Abstractive Summarization (Seq2Seq, LLMs)\n• Clinical Applications: Discharge Summary Synthesis, Radiology Impression Generation, Doctor-Patient Dialogue to SOAP Note\n• The Clinical Hallucination Dilemma: Fabricated medications, altered lab values, or inverted findings\n• Evaluation Metrics: ROUGE-1/2/L, BLEU, BERTScore, Fact-checking via Natural Language Inference (NLI)\n• Human-in-the-Loop Clinical Verification Workflows',
                'important_points': '• In clinical summarization, a factual hallucination can be fatal; factual correctness is vastly more important than syntactic fluency.\n• Extractive summaries are guaranteed to contain authentic physician text but can be disjointed; abstractive summaries are fluid but carry hallucination risks.\n• NLI-based factual consistency models verify that every generated sentence is strictly entailed by the original source record.',
                'revision_notes': '1. Extractive: selects existing sentences from source text without modification.\n2. Abstractive: generates novel sentences expressing the core concepts.\n3. ROUGE metric: measures n-gram overlap between generated summary and gold reference summary.\n4. SOAP note format: Subjective, Objective, Assessment, Plan.',
                'possible_questions': 'Q1: Differentiate between extractive and abstractive summarization in the context of clinical patient records.\nQ2: What are factual hallucinations in generative clinical AI, and what mechanisms prevent them in medical deployments?\nQ3: Explain how the ROUGE and BERTScore metrics evaluate the quality of an automated radiology impression summary.\nQ4: Describe how speech-to-text combined with LLMs generates structured SOAP notes from doctor-patient consultations.',
                'questions': [
                    {
                        'q': 'What is the format of a standard clinical SOAP progress note generated from patient consultations?',
                        'a': 'Subjective, Objective, Assessment, Plan',
                        'b': 'Summary, Operations, Analysis, Pricing',
                        'c': 'Surgery, Outcome, Antibiotics, Pathology',
                        'd': 'System, Optimization, Algorithm, Protocol',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'What is the critical clinical danger of deploying unconstrained generative abstractive language models to write patient discharge summaries?',
                        'a': 'The summary might use overly complex Latin vocabulary',
                        'b': 'The model might hallucinate fabricated drug dosages, invent non-existent allergies, or reverse clinical findings',
                        'c': 'The summary text might take up too much storage on hard drives',
                        'd': 'The model might print the text in capital letters',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'Why is standard n-gram overlap (ROUGE-1 / ROUGE-2) insufficient on its own for evaluating clinical text summarization?',
                        'a': 'ROUGE measures only lexical token match; it awards high scores to fluent text even if a single critical negated word (e.g. "no" in "no tumor") is omitted, completely inverting clinical truth',
                        'b': 'ROUGE requires millions of GPU hours to compute on text',
                        'c': 'ROUGE cannot evaluate English sentences',
                        'd': 'ROUGE is owned by private pharmaceutical companies',
                        'correct': 'A',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 6,
                'name': 'Clinical Decision Support Systems & Healthcare Chatbots',
                'desc': 'Clinical Decision Support Systems (CDSS), longitudinal Electronic Health Record (EHR) analysis, healthcare chatbots and virtual assistants, symptom triage conversational agents, NLP-based drug discovery, pharmacovigilance, and post-market safety surveillance.',
                'video_id': 'pM3V7k8X1hM',
                'video_title': 'Clinical Decision Support Systems, Healthcare Conversational Agents & Pharmacovigilance NLP',
                'duration': 1100,
                'transcript': 'In our concluding module, we study integrated NLP applications in healthcare: Clinical Decision Support Systems (CDSS), conversational virtual assistants, and pharmacovigilance. CDSS systems analyze real-time patient charts to alert physicians about drug-drug interactions, sepsis onset, or missed clinical guidelines. We examine patient-facing healthcare chatbots: symptom triage protocols, intent classification, entity extraction, and clinical safety guardrails that escalate urgent symptoms to emergency services. Finally, we explore NLP in pharmacovigilance: mining PubMed, clinical trial registries, and patient forums to detect Adverse Drug Reactions (ADRs) long before formal recalls.',
                'summary': 'Covers AI Clinical Decision Support Systems, conversational symptom triage agents, safety guardrails, and NLP for drug discovery and pharmacovigilance.',
                'key_concepts': '• Clinical Decision Support Systems (CDSS): Rule-Based vs Machine Learning-Driven Alerting\n• Longitudinal Patient Trajectory Modeling from Unstructured EHR Data\n• Healthcare Conversational Agents: Intent Classification, Entity Slot Filling, Dialogue State Tracking\n• Clinical Safety Architectures: Medical triage guardrails, handling high-risk red-flag symptoms\n• Pharmacovigilance: Mining literature, spontaneous reporting databases (FAERS), and social media for Adverse Drug Events',
                'important_points': '• CDSS alerts must avoid "alert fatigue" where doctors dismiss notifications due to high false-alarm rates.\n• Patient-facing medical conversational systems must NEVER provide definitive diagnostic prescriptions without human clinical review.\n• Pharmacovigilance NLP uncovers rare post-market drug side effects across diverse demographic populations.',
                'revision_notes': '1. CDSS: right information to the right person in the right format at the right time.\n2. Dialogue State Tracking: maintaining patient symptom history across multiple conversational turns.\n3. FAERS: FDA Adverse Event Reporting System mined using NLP relation extraction.',
                'possible_questions': 'Q1: Explain how an NLP-powered Clinical Decision Support System flags adverse drug interactions from physician orders.\nQ2: What is "alert fatigue" in hospital decision support systems and how do machine learning models reduce it?\nQ3: Detail the architecture and safety guardrails required for a patient symptom triage chatbot.\nQ4: Describe the role of NLP text mining in pharmacovigilance and drug repurposing.',
                'questions': [
                    {
                        'q': 'What is the primary operational objective of an NLP-driven Clinical Decision Support System (CDSS)?',
                        'a': 'To assist healthcare providers with evidence-based diagnostic suggestions, clinical guideline reminders, and drug interaction alerts at point of care',
                        'b': 'To replace doctors and perform autonomous surgeries without human presence',
                        'c': 'To calculate insurance company stock market valuations',
                        'd': 'To format hospital accounting spreadsheets',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In healthcare conversational agents designed for patient symptom checking, what architectural safety mechanism is mandatory when a patient inputs "severe crushing chest pain radiating to left arm"?',
                        'a': 'The chatbot should schedule an appointment for next month',
                        'b': 'The chatbot must trigger an immediate Emergency Red-Flag protocol, instructing the patient to dial 911/emergency services immediately without attempting further automated diagnosis',
                        'c': 'The chatbot should recommend drinking cold water and closing the browser',
                        'd': 'The chatbot should reboot the server',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'How does NLP contribute to "Pharmacovigilance" in post-market pharmaceutical safety surveillance?',
                        'a': 'By manufacturing synthetic chemical drug molecules in automated laboratories',
                        'b': 'By scanning thousands of biomedical research papers, EHR notes, and patient forums to detect emerging signals of rare adverse drug side effects before official recalls',
                        'c': 'By printing barcode labels on prescription medication bottles',
                        'd': 'By auditing the tax returns of pharmaceutical corporations',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            }
        ]
    },

    # -------------------------------------------------------------------------------------------------
    # SUBJECT 5: INTRODUCTION TO VIRTUAL REALITY (VR) AND 3D INTERACTION (CSE16511A.3)
    # -------------------------------------------------------------------------------------------------
    {
        'subject_code': 'CSE16511A.3',
        'subject_name': 'Introduction to Virtual Reality and 3D Interaction',
        'modules': [
            {
                'seq': 1,
                'name': 'Introduction to Virtual Reality & Immersion',
                'desc': 'Definition and history of Virtual Reality (Sensorama, Sutherland\'s Sword of Damocles, modern HMDs), components of VR: hardware (headsets, motion tracking, controllers), software (platforms, tools, frameworks), types of VR (immersive, non-immersive, AR, MR), applications in gaming, medicine, architecture, education, challenges and simulator sickness.',
                'video_id': 'k_91T6b7X4o',
                'video_title': 'Introduction to Virtual Reality: History, Hardware, Immersion & Human Factors',
                'duration': 1150,
                'transcript': 'Welcome to Introduction to Virtual Reality and 3D Interaction. Virtual Reality is an artificial, computer-generated simulation of a 3D environment with which a person can interact using specialized electronic devices. We trace the history of VR: Morton Heilig\'s 1956 Sensorama, Ivan Sutherland\'s 1968 Sword of Damocles, up to modern standalone headsets. We distinguish between non-immersive VR (desktop), semi-immersive (flight simulators, CAVE systems), and fully immersive VR (HMDs with 6DoF tracking). We analyze the Milgram Reality-Virtuality Continuum connecting Real World, Augmented Reality (AR), Augmented Virtuality (AV), and Pure Virtual Reality. Finally, we explore human perceptual factors, latency, and simulator sickness.',
                'summary': 'Covers the history of VR, the Milgram Continuum (VR, AR, MR), hardware/software components, and human factors like simulator sickness.',
                'key_concepts': '• Definition and Milestones: Sensorama, Sword of Damocles, VPL Research, Oculus Rift, Meta Quest, Apple Vision Pro\n• Milgram Reality-Virtuality Continuum: Real Environment <-> AR <-> MR <-> VR\n• Degrees of Immersion: Non-Immersive, Semi-Immersive (CAVE), Fully Immersive (HMD)\n• Components of a VR System: Display, Head Tracking, Spatial Input, Game Engine, Audio\n• Human Factors & Cybersickness: Vestibular-Visual Conflict, Latency, Vergence-Accommodation Conflict',
                'important_points': '• Immersion is an objective technological property of the VR system; Presence is the subjective psychological sensation of "being there".\n• Simulator sickness is triggered when visual motion perceived by the eyes is not accompanied by matching vestibular inner-ear acceleration.\n• Augmented Reality overlays digital graphics on the real world; Virtual Reality completely replaces the real world with a virtual environment.',
                'revision_notes': '1. CAVE: Cave Automatic Virtual Environment (projection-based cube room).\n2. 3DoF: Pitch, Yaw, Roll (rotational only).\n3. 6DoF: Pitch, Yaw, Roll + X, Y, Z translation (surge, sway, heave).\n4. Motion-to-photon latency must remain below 20ms to prevent nausea.',
                'possible_questions': 'Q1: Trace the historical evolution of Virtual Reality from early mechanical simulators to modern consumer HMDs.\nQ2: Explain the Milgram Reality-Virtuality Continuum with clear diagrams and examples of AR, MR, and VR.\nQ3: What causes cybersickness/simulator sickness in virtual reality? Describe technical methods to mitigate it.\nQ4: Differentiate between Immersion and Presence in virtual environments.',
                'questions': [
                    {
                        'q': 'What is the defining characteristic that separates "Fully Immersive Virtual Reality" from "Augmented Reality (AR)"?',
                        'a': 'Fully immersive VR completely replaces the user\'s perception of the physical real world with a simulated 3D environment',
                        'b': 'VR only works when connected to home electrical outlets',
                        'c': 'AR requires wearing heavy soundproof headphones',
                        'd': 'VR can only display monochrome black and white graphics',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In Virtual Reality system ergonomics, what physiological phenomenon is the primary catalyst for "Simulator Sickness"?',
                        'a': 'The weight of the plastic plastic head strap on the skull',
                        'b': 'Sensory conflict between visual motion cues perceived by the ocular system and the physical lack of motion reported by the inner-ear vestibular system',
                        'c': 'Listening to spatial audio at high volume',
                        'd': 'Low Wi-Fi download bandwidth',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'What historical invention built by Ivan Sutherland in 1968 is widely recognized as the world\'s first computer-driven Head-Mounted Display system?',
                        'a': 'The Google Cardboard',
                        'b': 'The Sword of Damocles',
                        'c': 'The Nintendo Virtual Boy',
                        'd': 'The Oculus Rift DK1',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 2,
                'name': 'VR Hardware, Sensors & Rendering Pipelines',
                'desc': 'VR devices: Headsets (Meta Quest, HTC Vive, Apple Vision Pro), Motion tracking (inside-out vs outside-in, 3DoF vs 6DoF), Controllers, Haptic feedback, Display technologies: stereoscopic displays, optics, 3D rendering pipeline, software platforms: Unity, Unreal Engine, Vuforia, sensors, latency and frame rate considerations (<20ms, 90fps).',
                'video_id': 'Wc1W5X9g4P8',
                'video_title': 'VR Hardware Architecture: Displays, Inside-Out Optical Tracking, Optics & 90FPS Rendering',
                'duration': 1280,
                'transcript': 'In this lecture, we examine VR Hardware Architecture and 3D Rendering Systems. A high-performance VR headset integrates ultra-fast displays, custom lenses, and high-frequency tracking sensors. We explore display technologies: dual OLED and fast-switch LCD panels with high pixel density to eliminate the "screen-door effect". We analyze lens physics: Fresnel lenses vs pancake optical assemblies. We contrast tracking mechanisms: outside-in lighthouse tracking using infrared lasers versus inside-out computer vision tracking using optical cameras and SLAM on the headset. Finally, we trace the stereoscopic rendering pipeline, time-warp / reprojection, and strict latency budgets.',
                'summary': 'Covers VR hardware, optical lenses, inside-out vs outside-in 6DoF tracking, stereoscopic rendering, and latency optimization.',
                'key_concepts': '• Tracking Architectures: 3DoF (rotational) vs 6DoF (positional), Inside-Out (SLAM) vs Outside-In (Lighthouse)\n• Display Technologies: Refresh Rate (90Hz-120Hz), Low Persistence Displays, Resolution per Eye, Screen Door Effect\n• VR Optics: Interpupillary Distance (IPD), Field of View (FOV), Fresnel vs Pancake Lenses, Chromatic Aberration Correction\n• Stereoscopic Rendering Pipeline: Two virtual cameras separated by interpupillary distance, asymmetric frustums\n• Asynchronous Timewarp (ATW) and Asynchronous Spacewarp (ASW) to maintain smooth frame rates',
                'important_points': '• Motion-to-photon latency is the time delay between physical head movement and the updated display photons reaching the eye; must be <20ms.\n• Inside-out tracking uses on-headset cameras to map environmental feature points and estimate pose via visual-inertial odometry.\n• Asynchronous Timewarp re-projects the rendered frame based on the latest head orientation just before display refresh, preventing dropped frames.',
                'revision_notes': '1. 6DoF: Pitch, Yaw, Roll, X, Y, Z.\n2. IMU: Accelerometer (measures gravity/acceleration) + Gyroscope (angular velocity) + Magnetometer (compass heading).\n3. Target frame rate: strictly 90 FPS or higher to prevent visual stutter.',
                'possible_questions': 'Q1: Explain the difference between Inside-Out and Outside-In tracking architectures with diagrams.\nQ2: What is the Screen Door Effect in VR displays, and how do modern high-PPD panels eliminate it?\nQ3: Explain the concept and significance of Interpupillary Distance (IPD) adjustment in VR headsets.\nQ4: Describe how Asynchronous Timewarp (ATW) safeguards user comfort when an application drops frames.',
                'questions': [
                    {
                        'q': 'What minimum frame rate (refresh rate) is standardly required in commercial VR headsets to ensure visual smoothness and prevent motion sickness?',
                        'a': '24 frames per second',
                        'b': '30 frames per second',
                        'c': '90 frames per second (or higher)',
                        'd': '5 frames per second',
                        'correct': 'C',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'How does modern "Inside-Out Tracking" on standalone headsets (like Meta Quest) track the user\'s 6DoF position without external room sensors?',
                        'a': 'By bouncing sound waves off the ceiling',
                        'b': 'By using on-board computer vision cameras and Visual-Inertial Odometry (VIO) to continuously track real-world environmental landmarks',
                        'c': 'By pinging cell phone cellular towers',
                        'd': 'By requiring the user to remain completely stationary',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In Virtual Reality graphics optimization, what is the role of "Asynchronous Timewarp (ATW)"?',
                        'a': 'It automatically lowers the resolution of 3D models when enemies appear',
                        'b': 'It warps and re-projects the previously rendered image using the latest rotational head tracking data immediately before scanout if the game engine misses a 90 FPS frame deadline',
                        'c': 'It converts 3D games into 2D videos for recording',
                        'd': 'It shuts down background audio processes to save battery',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 3,
                'name': '3D Interaction in Virtual Reality',
                'desc': 'Basics of 3D Interaction, input devices (controllers, gloves, eye-tracking), navigation in virtual spaces: walking, flying, teleportation, gesture recognition, body movement tracking, interaction techniques: pointing, ray-casting, direct grabbing, manipulating objects in 3D, feedback mechanisms (visual, auditory, haptic), designing 3D UI and interaction models.',
                'video_id': '5x7Q3X_9uP0',
                'video_title': '3D Spatial Interaction: Locomotion, Teleportation, Physics Grabbing & 3D User Interfaces',
                'duration': 1350,
                'transcript': 'In this lecture, we explore 3D Interaction Techniques in Virtual Reality. Interaction in 3D space departs radically from 2D desktop mouse-and-keyboard metaphors. We analyze the three fundamental tasks of 3D interaction: Navigation, Selection, and Manipulation. In navigation, we contrast continuous locomotion with discrete Teleportation paradigms (parabolic ray arc) and dynamic vignetting to prevent cybersickness. In selection and manipulation, we analyze Direct Virtual Hand Grabbing versus Ray-Casting for distant objects. Finally, we investigate multi-modal sensory feedback—visual highlights, spatial audio clicks, and vibrotactile haptic pulses—and examine spatial 3D UI architectures.',
                'summary': 'Covers the three core 3D interaction tasks: Navigation (locomotion/teleportation), Selection, and Manipulation, alongside haptics and 3D UI design.',
                'key_concepts': '• The Three Core Tasks of 3D Interaction: Navigation (Travel & Wayfinding), Selection, Manipulation\n• Locomotion Paradigms: Discrete Teleportation (Parabolic Arc), Continuous Smooth Locomotion, Room-Scale Walking\n• Manipulation Techniques: Direct Touch/Virtual Hand, Ray-Casting with Snap-to-Target, Virtual Hand Extensions (Go-Go technique)\n• Sensory Feedback in VR: Visual Feedback (Highlights, Reticles), Audio (Spatial feedback), Haptic (Vibrotactile waveforms)\n• 3D User Interfaces: Diegetic UI (integrated in-world), Non-Diegetic, Spatial Menus, Hand-Attached Wrist Palettes',
                'important_points': '• Teleportation with instant fading avoids optical flow acceleration, keeping the vestibular system undisturbed.\n• Ray-casting is fast for distant selections; direct grabbing is intuitive for near-field precision work.\n• Diegetic UI elements (like a watch display or physical cockpit switches) enhance presence and immersion.',
                'revision_notes': '1. Travel: physical motor movement through virtual space; Wayfinding: cognitive navigation and mental mapping.\n2. Teleportation arc: physics trajectory projecting where the user will land.\n3. Degrees of manipulation: 6DoF translation (X,Y,Z) + rotation (Pitch,Yaw,Roll).',
                'possible_questions': 'Q1: Explain the difference between continuous locomotion and teleportation in VR, highlighting pros and cons of each.\nQ2: Compare Direct Grabbing vs Ray-Casting for 3D object manipulation with interaction diagrams.\nQ3: What are Diegetic, Non-Diegetic, and Spatial user interfaces in VR? Provide an example of each.\nQ4: Describe how multi-modal haptic and auditory feedback reinforces virtual object manipulation.',
                'questions': [
                    {
                        'q': 'Which interaction technique is most commonly used in VR to select and activate distant virtual objects beyond the user\'s physical arm reach?',
                        'a': 'Ray-Casting (Virtual Laser Pointer)',
                        'b': 'Direct touch with fingers',
                        'c': 'Pressing Alt+Tab on a keyboard',
                        'd': 'Tapping the side of the headset',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In VR user interface design, what is a "Diegetic" UI element?',
                        'a': 'An interface element that exists physically within the virtual 3D environment and narrative world (e.g. ammo counter on the physical gun barrel or a wristwatch display)',
                        'b': 'A floating 2D billboard menu glued to the camera view that blocks the user\'s vision',
                        'c': 'A command-line terminal running in the background',
                        'd': 'A printed paper instruction manual outside the VR headset',
                        'correct': 'A',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'During continuous smooth joystick locomotion in VR games, what visual comfort technique temporarily restricts the user\'s field of view to reduce optical flow and prevent motion sickness?',
                        'a': 'Dynamic Vignetting (Tunnel Vision Effect)',
                        'b': 'Inverting all screen colors',
                        'c': 'Displaying an error dialogue box',
                        'd': 'Lowering headset volume to zero',
                        'correct': 'A',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 4,
                'name': 'VR Environment Design & Spatial Audio',
                'desc': 'Principles of VR environment design: immersion, presence, interaction, designing virtual worlds: spatial layout, lighting, PBR texture mapping, sound design for VR: spatial audio, HRTF, binaural sound, environmental sounds, creating realistic and engaging experiences, user-centered design, usability and UX heuristics in VR.',
                'video_id': '9X_jP4wQ2s0',
                'video_title': 'VR Environment Design: Spatial Acoustics, Lighting, Presence & Virtual World UX',
                'duration': 1220,
                'transcript': 'In this lecture, we examine VR Environment Design and Spatial Audio. Creating compelling virtual environments requires a mastery of architectural spatial design, real-time lighting, and psychoacoustics. We analyze Mel Slater\'s theory of Presence: the Place Illusion (PI - the illusion of being there) and the Plausibility Illusion (Psi - the illusion that events occurring in the virtual world are really happening). We study real-time lighting: baked global illumination lightmaps, Physically Based Rendering (PBR) materials, and realistic scale. We dive deep into Spatial Audio: Head-Related Transfer Functions (HRTF), binaural audio, sound reflection, and Doppler shift.',
                'summary': 'Explores virtual world construction, PBR rendering, Mel Slater presence illusions, binaural audio acoustics, and VR usability heuristics.',
                'key_concepts': '• The Duality of Presence: Place Illusion (PI) and Plausibility Illusion (Psi)\n• Architectural Ergonomics: Human scale (1 unit = 1 meter), eye-level calibration, comfortable reach zones\n• Physically Based Rendering (PBR): Albedo, Normal maps, Roughness, Metallic channels\n• Spatial Sound Engineering: HRTF (Head-Related Transfer Function), Interaural Time Difference (ITD), Interaural Level Difference (ILD)\n• Acoustics: Sound Occlusion, Obstruction, Reverberation, Early Reflections\n• VR Usability Heuristics: Preventing fatigue, clear affordances, avoiding neck strain (>30 degree gaze angles)',
                'important_points': '• In VR, scale is critical: if a table is 5% too tall, the user immediately feels disoriented like a child.\n• Spatial audio is 50% of the immersion equation; believable 3D sound anchors visual objects in physical space.\n• Baked static lighting delivers photorealistic ambient occlusion without burning mobile GPU cycles at runtime.',
                'revision_notes': '1. ITD: sound arrives at the closer ear microseconds before the further ear.\n2. ILD: the head creates an acoustic shadow, making sound louder in the closer ear.\n3. Ergonomic comfort: interactables should be placed between chest and waist height within 0.5m of user.',
                'possible_questions': 'Q1: Explain Mel Slater\'s Place Illusion (PI) and Plausibility Illusion (Psi) and how each is achieved in VR design.\nQ2: Describe how Head-Related Transfer Functions (HRTFs) synthesize realistic 3D spatial audio for stereo headphones.\nQ3: What are the best practices for lighting and material optimization in standalone VR environments?\nQ4: List five critical VR User Experience (UX) design heuristics that prevent user fatigue and disorientation.',
                'questions': [
                    {
                        'q': 'In 3D sound design for VR headsets, what mathematical filter models the anatomical acoustic filtering of human ears, head, and torso to position sound anywhere in 3D space?',
                        'a': 'Head-Related Transfer Function (HRTF)',
                        'b': 'Fast Fourier Transform (FFT) exclusively for bass',
                        'c': 'MP3 Audio Compression Codec',
                        'd': 'Graphic Equalizer Slider',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'According to Virtual Reality presence theory by Mel Slater, what is the "Plausibility Illusion" (Psi)?',
                        'a': 'The belief that the VR headset was manufactured in an ISO-certified facility',
                        'b': 'The subjective sensation that the events occurring in the virtual world are really happening and respond credibly to user actions',
                        'c': 'The physical illusion that the computer screen is made of glass',
                        'd': 'The ability to run multiple programs simultaneously',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'When designing 3D user interfaces in VR, why do UX guidelines mandate that interactive menus should not force users to maintain an upward neck tilt greater than 15-20 degrees for extended periods?',
                        'a': 'Because it causes severe cervical spine fatigue and muscular neck strain (commonly referred to as "Gorilla Neck")',
                        'b': 'Because the headset optical lenses will fall out of the chassis',
                        'c': 'Because Bluetooth signals from controllers get blocked by the chin',
                        'd': 'Because the display refresh rate drops at high angles',
                        'correct': 'A',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 5,
                'name': 'Applications of Virtual Reality',
                'desc': 'VR in gaming: full-body immersion and interactive physics, VR in healthcare: surgery simulation, pain management, therapy (phobia and PTSD exposure), VR in education and training: flight simulators, hazardous industry training, virtual tours, social VR and metaverse platforms, future trends with AR/MR and AI.',
                'video_id': '7c_X2y8b9v4',
                'video_title': 'Industrial & Medical VR Applications: Surgical Simulation, Therapy, Training & Social Metaverses',
                'duration': 1180,
                'transcript': 'This lecture surveys the transformative real-world applications of Virtual Reality. In medicine, VR powers high-fidelity surgical simulators with haptic feedback, allowing surgeons to practice rare procedures without patient risk. In clinical psychiatry, Virtual Reality Exposure Therapy (VRET) treats PTSD, phobias, and anxiety through controlled stimulus exposure. In industrial training, aviation and heavy equipment operators train in hazardous scenarios—emergency fire evacuations, chemical plant failures—safely and cost-effectively. In enterprise and education, Social VR platforms enable global collaborative design reviews and virtual classrooms. Finally, we analyze convergence with Artificial Intelligence and spatial computing.',
                'summary': 'Surveys real-world applications of VR in surgical simulation, psychiatry, aviation training, architecture, and social collaboration.',
                'key_concepts': '• Medical VR: Pre-Operative Planning, Surgical Simulation with Force Feedback, Burn Patient Pain Distraction (SnowWorld)\n• Psychiatric Applications: Virtual Reality Exposure Therapy (VRET) for Phobias (Arachnophobia, Acrophobia, PTSD)\n• Industrial & Military Training: Flight Simulators, Hazardous Waste Handling, Nuclear Plant Safety Drills\n• Architectural & Engineering CAD Visualization and Digital Twin Walkthroughs\n• Social VR & Telepresence: Spatial Audio, Non-Verbal Eye/Face Tracking, Photorealistic Digital Avatars',
                'important_points': '• VR surgical simulation allows trainees to commit critical mistakes without risk to human life.\n• Immersion in interactive snowy VR worlds acts as non-pharmacological analgesic pain relief by flooding cognitive attention bandwidth.\n• Virtual industrial training reduces corporate training costs by 70% while improving memory retention.',
                'revision_notes': '1. VRET: graded exposure to fearful stimuli in an immersive, clinician-controlled virtual environment.\n2. Telepresence: feeling present with remote colleagues in a shared digital workspace.\n3. Digital Twins: real-time 3D VR simulation mirroring a physical factory or jet engine.',
                'possible_questions': 'Q1: Explain how Virtual Reality Exposure Therapy (VRET) treats anxiety disorders and phobias.\nQ2: Describe how haptic feedback surgical simulators evaluate surgeon skill metrics.\nQ3: What are the economic and safety advantages of VR simulation in aviation and heavy industrial training?\nQ4: Discuss the architectural requirements of a Social VR platform supporting multi-user collaboration.',
                'questions': [
                    {
                        'q': 'How does Virtual Reality Exposure Therapy (VRET) assist clinical psychologists in treating patients with severe phobias (such as acrophobia or fear of flying)?',
                        'a': 'By exposing patients to computer-generated phobic stimuli in a gradual, controlled, and safe immersive environment under therapist guidance',
                        'b': 'By hypnotizing patients through flashing colored lights on screen',
                        'c': 'By teaching patients how to code software in C++',
                        'd': 'By permanently erasing memory registers in the patient\'s brain',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In medical simulation training, why is the inclusion of "Haptic Feedback" essential in virtual laparoscopic surgical simulators?',
                        'a': 'It vibrates when the surgeon\'s smartphone receives a text message',
                        'b': 'It physically reproduces realistic tactile resistance and tissue compliance, allowing surgeons to feel the delicate mechanical boundaries of virtual human organs',
                        'c': 'It reduces electricity bills for hospital training rooms',
                        'd': 'It generates background music during operations',
                        'correct': 'B',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'In psychological pain management during burn wound debridement treatments, how does an immersive VR experience (such as "SnowWorld") act as an effective non-pharmacological analgesic?',
                        'a': 'By cooling down the patient\'s body temperature by 10 degrees Celsius',
                        'b': 'By flooding conscious cognitive attention capacity with intense multi-sensory immersion, leaving significantly fewer attentional resources available to process incoming pain signals',
                        'c': 'By shutting down the patient\'s auditory nerves',
                        'd': 'By administering chemical anesthesia through the headset foam padding',
                        'correct': 'B',
                        'diff': 'Hard'
                    }
                ]
            },
            {
                'seq': 6,
                'name': 'VR Application Development with Unity / Unreal Engine',
                'desc': 'Introduction to VR development tools: Unity3D, Unreal Engine, OpenXR standard, setting up a VR development environment, creating basic VR scenes and interactions, integrating 3D models, textures, and spatial audio, implementing core interaction techniques (teleportation, grabbing, socket interactors), debugging and performance optimization.',
                'video_id': 'd1P_3K6x2G0',
                'video_title': 'VR Development Masterclass: Unity OpenXR, XR Interaction Toolkit & Performance Profiling',
                'duration': 1450,
                'transcript': 'In our final module, we learn how to build and optimize Virtual Reality applications using industry-standard game engines. We focus on Unity3D and the OpenXR cross-platform standard. We configure the XR Interaction Toolkit: establishing the XR Origin rig, mapping head and hand controllers, and setting up interaction managers. We implement Core VR Interactors: XR Direct Interactor for grabbing near objects, XR Ray Interactor for teleportation locomotion and UI clicks, and Socket Interactors for snap-in inventory mechanics. Finally, we deep dive into performance profiling: reducing draw calls via static and dynamic batching, occlusion culling, and shader optimization for mobile headsets.',
                'summary': 'Hands-on VR development guide covering OpenXR, Unity XR Interaction Toolkit, locomotion, grabbing mechanics, and mobile VR performance optimization.',
                'key_concepts': '• VR Development Frameworks: Unity3D, Unreal Engine, OpenXR Industry Standard API\n• The XR Rig (XR Origin): Tracking space, Main Camera (HMD), Left/Right Controller Hand Anchors\n• Unity XR Interaction Toolkit (XRI): XR Interaction Manager, XR Direct Interactor, XR Ray Interactor\n• Grabbable Objects: XR Grab Interactable, Colliders, Rigidbodies, Throw Physics (Velocity Tracking)\n• Locomotion System: Teleportation Provider, Snap Turn / Continuous Turn, Continuous Move Provider\n• Performance Optimization: Draw Call Batching (Static/Dynamic/GPU Instancing), Occlusion Culling, Single-Pass Stereo Instanced Rendering',
                'important_points': '• OpenXR eliminates fragmentation: develop one codebase that deploys to Meta Quest, HTC Vive, Pico, Valve Index, and Windows Mixed Reality.\n• Single-Pass Stereo Instancing renders both left and right eye views in a single GPU draw call, doubling rendering efficiency.\n• Physics updates in VR must run on FixedUpdate at identical frequency to display refresh (e.g. 90Hz) to prevent controller tracking jitter.',
                'revision_notes': '1. OpenXR: royalty-free open standard from Khronos Group for AR/VR runtime interoperability.\n2. XR Grab Interactable: attach to any GameObject with Collider + Rigidbody to enable pickup.\n3. Teleportation Area: surface where user can teleport anywhere; Teleportation Anchor: specific landing point with locked orientation.',
                'possible_questions': 'Q1: Detail the step-by-step setup of a modern VR application in Unity3D using OpenXR and XR Interaction Toolkit.\nQ2: Explain the difference between an XR Direct Interactor, an XR Ray Interactor, and an XR Socket Interactor.\nQ3: What is Single-Pass Instanced Stereo Rendering, and how does it optimize GPU rendering performance in VR?\nQ4: Describe four techniques to reduce draw calls when building a complex VR scene for a standalone mobile headset.',
                'questions': [
                    {
                        'q': 'What open, royalty-free industry standard developed by the Khronos Group enables developers to write cross-platform VR/AR code that runs across multiple headset manufacturers without rebuilding code?',
                        'a': 'OpenXR',
                        'b': 'DirectX 9',
                        'c': 'Adobe Flash',
                        'd': 'Apple QuickTime',
                        'correct': 'A',
                        'diff': 'Easy'
                    },
                    {
                        'q': 'In the Unity XR Interaction Toolkit, which component must be added to a 3D prop (like a cup or sword) so that a VR user can pick it up with their motion controller and throw it?',
                        'a': 'XR Grab Interactable',
                        'b': 'Audio Source',
                        'c': 'Canvas Scaler',
                        'd': 'Mesh Renderer exclusively',
                        'correct': 'A',
                        'diff': 'Medium'
                    },
                    {
                        'q': 'When developing VR applications for standalone mobile headsets with limited GPU fill-rate, what does "Single-Pass Stereo Instanced Rendering" accomplish?',
                        'a': 'It renders the left and right eye views in a single GPU draw call, dramatically reducing CPU overhead and driver state changes',
                        'b': 'It deletes all shadows and textures from the scene',
                        'c': 'It renders only the left eye, duplicating it onto the right eye without parallax offset',
                        'd': 'It executes all shader code on the battery microcontroller',
                        'correct': 'A',
                        'diff': 'Hard'
                    }
                ]
            }
        ]
    }
]

def update_syllabus():
    conn = connect_db()
    cursor = conn.cursor()
    
    print("Beginning 5th Semester Syllabus Update...")
    
    SUBJECT_MAP = {
        'Compiler Design': 47,
        'Artificial Intelligence': 25,
        'Big Data Analysis': 31,
        'NLP for Health Related Text': 49,
        'Introduction to Virtual Reality and 3D Interaction': 48,
    }

    for subj_data in SYLLABUS_DATA:
        code = subj_data['subject_code']
        name = subj_data['subject_name']
        subject_id = SUBJECT_MAP.get(name)
        
        if not subject_id:
            cursor.execute("SELECT id FROM subjects WHERE name=%s", (name,))
            row = cursor.fetchone()
            if row:
                subject_id = row['id']
            else:
                cursor.execute("INSERT INTO subjects (name, code, description) VALUES (%s, %s, %s)",
                               (name, code, f"Semester 5 core course: {name}"))
                subject_id = cursor.lastrowid
        else:
            cursor.execute("UPDATE subjects SET code=%s, name=%s WHERE id=%s", (code, name, subject_id))
            
        print(f"\nProcessing Subject: {name} (ID: {subject_id}, Code: {code})")
        
        # 2. Clean up any existing modules for this subject to prevent duplicates
        cursor.execute("SELECT id FROM modules WHERE subject_id=%s", (subject_id,))
        old_mods = cursor.fetchall()
        for om in old_mods:
            mod_id = om['id']
            # Delete assignments, topics, lectures cascading
            cursor.execute("DELETE FROM assignments WHERE module_id=%s", (mod_id,))
            cursor.execute("DELETE FROM lectures WHERE module_id=%s", (mod_id,))
            cursor.execute("DELETE FROM topics WHERE module_id=%s", (mod_id,))
            cursor.execute("DELETE FROM modules WHERE id=%s", (mod_id,))
            
        # 3. Insert new modules, topics, lectures, transcripts, notes, assignments, questions
        for mod in subj_data['modules']:
            # Insert module
            cursor.execute(
                """INSERT INTO modules (subject_id, name, sequence_no, description)
                   VALUES (%s, %s, %s, %s)""",
                (subject_id, mod['name'], mod['seq'], mod['desc'])
            )
            module_id = cursor.lastrowid
            
            # Insert topic
            cursor.execute(
                """INSERT INTO topics (module_id, name, difficulty, description)
                   VALUES (%s, %s, 'Medium', %s)""",
                (module_id, mod['name'], mod['desc'])
            )
            topic_id = cursor.lastrowid
            
            # Insert lecture
            cursor.execute(
                """INSERT INTO lectures (module_id, title, youtube_video_id, duration_seconds)
                   VALUES (%s, %s, %s, %s)""",
                (module_id, mod['video_title'], mod['video_id'], mod['duration'])
            )
            lecture_id = cursor.lastrowid
            
            # Insert transcript
            cursor.execute(
                """INSERT INTO transcripts (lecture_id, transcript_text)
                   VALUES (%s, %s)""",
                (lecture_id, mod['transcript'])
            )
            
            # Insert lecture notes
            cursor.execute(
                """INSERT INTO lecture_notes (lecture_id, summary, key_concepts, important_points, revision_notes, possible_questions)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (lecture_id, mod['summary'], mod['key_concepts'], mod['important_points'], mod['revision_notes'], mod['possible_questions'])
            )
            
            # Insert assignment
            cursor.execute(
                """INSERT INTO assignments (module_id, title, difficulty_mix)
                   VALUES (%s, %s, 'Adaptive (Easy, Medium, Hard)')""",
                (module_id, f"{mod['name']} Adaptive Mastery Assessment")
            )
            assignment_id = cursor.lastrowid
            
            # Insert questions
            for q in mod['questions']:
                # Provide reasonable dummy options matching correct letter
                if q['correct'] == 'A':
                    opt_a = q['a']
                    opt_b = q.get('b', 'Unrelated auxiliary system process')
                    opt_c = q.get('c', 'Static hardware firmware allocation')
                    opt_d = q.get('d', 'None of the above')
                elif q['correct'] == 'B':
                    opt_a = q.get('a', 'Arbitrary system transformation without evaluation')
                    opt_b = q['b']
                    opt_c = q.get('c', 'Deleting temporary local cache registers')
                    opt_d = q.get('d', 'None of the above')
                elif q['correct'] == 'C':
                    opt_a = q.get('a', 'First-in first-out sequential buffer')
                    opt_b = q.get('b', 'Static hardware clock synchronization')
                    opt_c = q['c']
                    opt_d = q.get('d', 'None of the above')
                else:
                    opt_a = q.get('a', 'Option A')
                    opt_b = q.get('b', 'Option B')
                    opt_c = q.get('c', 'Option C')
                    opt_d = q.get('d', 'Correct D')

                cursor.execute(
                    """INSERT INTO assignment_questions 
                       (assignment_id, question_text, option_a, option_b, option_c, option_d, correct_option, difficulty, concept)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (assignment_id, q['q'], opt_a, opt_b, opt_c, opt_d, q['correct'], q['diff'], mod['name'])
                )
                
            print(f"  -> Added Module {mod['seq']}: {mod['name']} (Lecture: {mod['video_id']})")

    # 4. Initialize performance and regenerate adaptive plan for active students
    cursor.execute("SELECT id FROM students WHERE current_semester=5")
    sem5_students = cursor.fetchall()
    
    for st in sem5_students:
        sid = st['id']
        # Initialize topics for student
        cursor.execute("SELECT subject_id, priority FROM student_subjects WHERE student_id=%s AND is_active=1", (sid,))
        enrolled = cursor.fetchall()
        for e in enrolled:
            cursor.execute(
                """SELECT t.id FROM topics t JOIN modules m ON m.id = t.module_id WHERE m.subject_id=%s""",
                (e['subject_id'],)
            )
            top_ids = cursor.fetchall()
            for tid in top_ids:
                cursor.execute(
                    """INSERT IGNORE INTO student_topic_performance 
                       (student_id, topic_id, quiz_score, accuracy, attempts, time_spent, previous_score, assignment_score, study_hours, difficulty, lecture_completion, improvement, mastery, priority_score, priority)
                       VALUES (%s, %s, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 'MODERATE', 50.0, %s)""",
                    (sid, tid['id'], e['priority'])
                )
        print(f"Initialized topic performance for student ID {sid}")

    conn.commit()
    conn.close()
    print("\nSUCCESS! All 5 subjects, 29 modules, YouTube lectures, transcripts, notes, and questions have been updated.")

if __name__ == '__main__':
    update_syllabus()
