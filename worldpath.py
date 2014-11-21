import heapq
res = []
letters = 'abcdefghijklmnopqrstuvwxyz'
def search(words, word, path):
    path.append(word)
    if word in words:
        res.append(word)
    yield tuple(path)
    for i in xrange(len(word)+1):
        before, after = word[:i], word[i:]
        for c in letters:
            new_word = '%s%s%s' % (before, c, after)
            if new_word  in words:
                for new_path in search(words, new_word, path):
                    res.append(new_word)
                    yield new_path
    path.pop()

def load(path):
    result = set()
    with open(path, 'r') as f:
        for line in f:
            word = line.lower().strip()
            result.add(word)
    return result

def find_top(paths, n):
    gen = ((len(x), x) for x in paths)
    return heapq.nlargest(n, gen)

if __name__ == '__main__':
    words = load('dictionary.txt')
    gen = search(words, 'a', [])
    top = find_top(gen, 10)
    print "Expect Result is :  %s"  % set(res)
    for path in top:
        print path
