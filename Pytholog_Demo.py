from pyswip import*

# Demo imports
import pytholog as pl
from time import time

import psycopg2
import pandas as pd

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

can_print = False

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


# --- || SQL DEMO || ---

can_print = False

# Connecting to sql database
psql = psycopg2.connect(host = "localhost", database = "dvdrental", user = "postgres", password = "postgres")
cursor = psql.cursor()

# Extracting info from some of the tables
def query_defn(table):
    return f"SELECT * FROM {table};"

actor = pd.read_sql(query_defn("actor"), psql)
language = pd.read_sql(query_defn("language"), psql)
film = pd.read_sql(query_defn("film"), psql)
category = pd.read_sql(query_defn("category"), psql)

actor["Actor"] = (actor["first_name"] + "_" + actor["last_name"]).str.lower()
language["name"] = language["name"].str.lower()
film["title"] = film["title"].str.replace(" ", "_").str.lower()
category["name"] = category["name"].str.lower()

# Setting pytholog knowledge base with extracted data
dvd_kb = pl.KnowledgeBase("dvd_rental")

for i in range(film.shape[0]):
    dvd_kb([f"film({film.film_id[i]}, {film.title[i]}, {film.language_id[i]})"])

for i in range(language.shape[0]):
    dvd_kb([f"language({language.language_id[i]}, {language.name[i]})"])

dvd_kb(["film_language(F, L) :- film(_, F, LID), language(LID, L)"])

# Simple knowledge base query
if can_print:
    print(dvd_kb.query(pl.Expr("film_language(young_language, L)")))


print(dvd_kb.db.keys())
""" 
with open("dvd_rental.pl", "w") as f:
    for i in dvd_kb.db.keys():
        
        for d in dvd_kb.db[i]["facts"]:
            f.write(d.to_string() + "." + "\n")

f.close()
 """