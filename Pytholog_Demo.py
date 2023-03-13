from pyswip import*
import pytholog as pl
from time import time

""" 
prolog = Prolog()
prolog.assertz("father(michael,john)")
prolog.assertz("father(michael,gina)")
#list(prolog.query("father(michael,X)")) == [{'X': 'john'}, {'X': 'gina'}]
for soln in prolog.query("father(X,Y)"):
    print(soln["X"], "is the father of", soln["Y"])
# michael is the father of john
# michael is the father of gina



def hello(t):
    print("Hello,", t)
hello.arity = 1

registerForeign(hello)
print(list(prolog.query("father(michael,X), hello(X)")))
"""




# --- || MEMOIZATION DEMO || ---

can_print = True

new_kb = pl.KnowledgeBase("flavor")
new_kb([
        "food_type(gouda, cheese)",
        "food_type(ritz, cracker)",
        "food_type(steak, meat)",
        "food_type(sausage, meat)",
        "food_type(limonade, juice)",
        "food_type(cookie, dessert)",

        "flavor(sweet, dessert)",
        "flavor(savory, meat)",
        "flavor(savory, cheese)",
        "flavor(sweet, juice)",

        "food_flavor(X, Y) :- food_type(X, Z), flavor(Y, Z)",

        "dish_to_like(X, Y) :- likes(X, L), food_type(L, T), flavor(F, T), food_flavor(Y, F), neq(L, Y)"
    ])

if can_print:
    start = time()
    print(new_kb.query(pl.Expr("food_flavor(What, sweet)")))
    print(time() - start)

    new_kb.clear_cache()

    start = time()
    print(new_kb.query(pl.Expr("food_flavor(What, sweet)")))
    print(time() - start)

    start = time()
    print(new_kb.query(pl.Expr("food_flavor(What, sweet)")))
    print(time() - start)


# --- || PROBABILITIES DEMO || ---

can_print = False

friends_kb = pl.KnowledgeBase("friends")
friends_kb([
    "stress(X, P) :- has_lot_work(X, P2), P is P2 * 0.2",

    "to_smoke(X, Prob) :- stress(X, P1), friends(Y, X), influences(Y, X, P2), smokes(Y), Prob is P1 * P2",

    "to_have_asthma(X, 0.4) :- smokes(X)",
    "to_have_asthma(X, Prob) :- to_smoke(X, P2), Prob is P2 * 0.25",

    "friends(X, Y) :- friend(X, Y)",
    "friends(X, Y) :- friend(Y, X)",

    "influences(X, Y, 0.6) :- friends(X, Y)",

    "friend(peter, david)",
    "friend(peter, rebecca)",
    "friend(daniel, rebecca)",

    "smokes(peter)",
    "smokes(rebecca)",

    "has_lot_work(daniel, 0.8)",
    "has_lot_work(david, 0.3)"
])

if can_print:
    print(friends_kb.query(pl.Expr("influences(X, rebecca, P)")))
    print(friends_kb.query(pl.Expr("smokes(Who)")))
    print(friends_kb.query(pl.Expr("to_smoke(Who, P)")))
    print(friends_kb.query(pl.Expr("to_have_asthma(Who, P)")))