from nltk.corpus import words as words_corpus

# to run:
"""
from stack_solution import *
from functions import get_board
board, *_ = get_board()
grid = list(zip(*[iter([l.lower() for l in board])]*5))  # "reshape" str list
# grid = ['fxie', 'amlo', 'ewbx', 'astu']
g, c = make_graph(grid)
w, p = make_lookups(grid)
# res = set()
# res = []
# paths = []
res = {}
paths = {}
find_words(g, c, None, [], res, w, p)
print(res) # alphabetical
print(sorted(res, key=len, reverse=True)) # descending length
"""

# searching only works with lowercase letters
# need to figure out how to deal with Qu:
# - maybe use a number until searching dict, then replace with qu?
# save word paths so the board can get highlighted(!)


def get_word_list(board=None, min_length=0):
    """
    Find all words in board.

    Returns a dict where keys are words and values are (x,y) paths
    """
    grid = list(zip(*[iter([l.lower() for l in board])] * 5))  # "reshape" str list
    graph, chardict = make_graph(grid)
    words, prefixes = make_lookups(grid)
    results = {}
    find_words(graph, chardict, None, [], results, words, prefixes, min_length)

    return results


def make_lookups(grid, fn="dict.txt"):
    # Make set of valid characters.
    chars = set()

    for row in grid:
        for word in row:
            chars.update(word.lower())

    valid_words = set()
    for w in words_corpus.words():
        if set(w.strip()) <= chars:
            valid_words.add(w)

    prefixes = set()
    for w in valid_words:
        for i in range(len(w) + 1):
            prefixes.add(w[:i])

    return valid_words, prefixes


def make_graph(grid):
    root = None
    graph = {root: set()}
    chardict = {root: ""}

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            chardict[(i, j)] = char.lower()
            node = (i, j)
            children = set()
            graph[node] = children
            graph[root].add(node)
            add_children(node, children, grid)

    return graph, chardict


def add_children(node, children, grid):
    x0, y0 = node
    for i in [-1, 0, 1]:
        x = x0 + i
        if not (0 <= x < len(grid)):
            continue
        for j in [-1, 0, 1]:
            y = y0 + j
            if not (0 <= y < len(grid[0])) or (i == j == 0):
                continue

            children.add((x, y))


def to_word(chardict, pos_list):
    return "".join(chardict[x] for x in pos_list)


def find_words(graph, chardict, position, prefix, results, words, prefixes, min_length):
    """ Arguments:
      graph :: mapping (x,y) to set of reachable positions
      chardict :: mapping (x,y) to character
      position :: current position (x,y) -- equals prefix[-1]
      prefix :: list of positions in current string
      results :: set of words found
      words :: set of valid words in the dictionary
      prefixes :: set of valid words or prefixes thereof
    """

    word = to_word(chardict, prefix)

    if word not in prefixes:
        return

    if word in words:
        if word not in results.keys() and len(word) >= min_length:
            results[word] = prefix

    for child in graph[position]:
        if child not in prefix:
            find_words(
                graph,
                chardict,
                child,
                prefix + [child],
                results,
                words,
                prefixes,
                min_length,
            )
