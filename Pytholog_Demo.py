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




# -- MEMOIZATION DEMO --

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