# From https://nlp.stanford.edu/IR-book/html/htmledition/positional-indexes-1.html

# "An algorithm for proximity intersection of postings lists p1 and p2.
# The algorithm finds places where the two terms appear within k words of each other
# and returns a list of triples giving docID and the term position in p1 and p2."

# p1 = term1, p2 = term2, k = number of words within which the two terms appear

def docId(term):
    return -1

def positional_intersect(p1, p2, k):
    results = []
    while len(p1) != 0 and len(p2) != 0:
        if docId(p1) == docId(p2): # find out doc id
            # postings lists





    return results # list of triples e.g. [[1, 18, 17], [4, 16, 17]...]