import pytholog as pl
from time import time
import psycopg2
import pandas as pd


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

    # Clearing cache to prevent memoization, just to test computing times with and without
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


# --- || SAVING TO PROLOG FILE DEMO || ---

def outupt_kb_to_file(kb):
    with open("test_prolog_output.pl", "w") as f:
        for i in kb.db.keys():
            for d in kb.db[i]["facts"]:
                f.write(d.to_string() + "." + "\n")

    f.close()


# --- || CREATING KB FROM FILE DEMO || ---

can_print = False

outupt_kb_to_file(friends_kb)
test_kb = pl.KnowledgeBase("test_kb")
test_kb.from_file("test_prolog_output.pl")

if can_print:
    print(test_kb.query(pl.Expr("to_have_asthma(Who, P)")))


# --- || GRAPH TRAVERSAL DEMO || ---

can_print = False

graph_kb = pl.KnowledgeBase("MSA_graph")
graph_kb([## routes between adjacent cities
    "route(seattle, chicago, 1737)",
    "route(seattle, san_francisco, 678)",
    "route(san_francisco, riverside, 386)",
    "route(san_francisco, los_angeles, 348)",
    "route(los_angeles, riverside, 50)",
    "route(los_angeles, phoenix, 357)",
    "route(riverside, phoenix, 307)",
    "route(riverside, chicago, 1704)",
    "route(phoenix, dallas, 887)",
    "route(phoenix, houston, 1015)",
    "route(dallas, chicago, 805)",
    "route(dallas, atlanta, 721)",
    "route(dallas, houston, 225)",
    "route(houston, atlanta, 702)",
    "route(houston, miami, 968)",
    "route(atlanta, chicago, 588)",
    "route(atlanta, washington, 543)",
    "route(atlanta, miami, 604)",
    "route(miami, washington, 923)",
    "route(chicago, detroit, 238)",
    "route(detroit, boston, 613)",
    "route(detroit, washington, 396)",
    "route(detroit, new_york, 482)",
    "route(boston, new_york, 190)",
    "route(new_york, philadelphia, 81)",
    "route(philadelphia, washington, 123)",
    
    "path(X, Y, P) :- route(X, Y, P)",
    "path(X, Y, P) :- route(X, Z, P2), path(Z, Y, P3), P is P2 + P3",
    "path(X, Y, P) :- route(Y, Z, P2), path(Z, X, P3), P is P2 + P3"
    ])

# Cut argument is used to to stop searching when the first path is found, which should be the most optimal one.
answer, path = graph_kb.query(pl.Expr("path(boston, miami, Weight)"), cut = True, show_path = True) 

if can_print:
    print(answer)

    # The path given isn't sorted.
    print([answer for answer in path if str(answer) > "Z"])
