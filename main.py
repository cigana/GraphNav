#Hilfsfunktionen
#erzeugt Liste der Tags
from igraph._igraph import OUT


def createTags(numberTags):
    tags = string.ascii_uppercase[0:numberTags]
    tagList = []

    for i in range(len(tags)):
        tagList.append(tags[i])

    return tagList

#default Graph-Erzeugung - Kanten werden zufällig zwischen Tags und Items verteilt
def createGraph(numberTags, numberItems, numberEdges):
    g = igraph.Graph()
    g.add_vertices(numberTags)

    #Knoten hinzufügen
    tags = createTags(numberTags)
    g.vs["name"] = tags
    for i in range(numberItems):
        g.add_vertices(str(i + 1))

    #Liste für Type erstellen
    type=[]
    for i in range(numberTags):
        type.append("t")
    for i in range(numberItems):
        type.append("i")

    g.vs["type"]=type

    edges = []
    for e in range(numberEdges):
        t = random.randint(0, numberTags-1)
        i = random.randint(numberTags, numberTags + numberItems-1)
        edges.append((t, i))
    t1 = set(edges)
    g.add_edges(t1)
    return g

#KnoWorks-Graph-Erzeugung - Einige Tags werden bevorzugt, andere Tags werden selten vergeben
def createKWGraph(numberTags, numberItems, numberEdges):
    g = igraph.Graph()
    g.add_vertices(numberTags)

    #Knoten hinzufügen
    tags = createTags(numberTags)
    g.vs["name"] = tags
    for i in range(numberItems):
        g.add_vertices(str(i + 1))

    #Liste für Type erstellen
    type=[]
    for i in range(numberTags):
        type.append("t")
    for i in range(numberItems):
        type.append("i")

    g.vs["type"]=type

    edges = []
    for e in range(numberEdges):
        t = random.randint(0, numberTags-1)
        #falls t in erster Drittel der tags, dann bilde neue Zufallszahl
        #sorgt für seltenere Kanten ausgehend von der erste Drittel der Tags
        if t < numberTags/2:
            t = random.randint(0, numberTags - 1)
            if t < numberTags / 3:
                t = random.randint(0, numberTags - 1)
        i = random.randint(numberTags, numberTags + numberItems-1)
        edges.append((t, i))
    t1 = set(edges)
    g.add_edges(t1)
    return g

#erzeugt Dictionary mit key=tagName, value=degree
def tagDegree(g, numberTags):
    tagDegree = g.vs.degree()[0:numberTags]
    tags = createTags(numberTags)
    tDeg =dict(zip(tags, tagDegree))
    return tDeg

#sortiert tags in Kategorien nach Knotengrad
def rankTags(dictTDeg):
    high = []
    medium = []
    low = []

    for tag, deg in dictTDeg.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
        if deg > 10:
            high.append(tag)
        if  deg > 3 and deg < 11:
            medium.append(tag)
        if deg < 4:
            low.append(tag)

    sortTags = [high, medium, low]

    return sortTags

def findPath(tag1, tag2):


    path = g.get_shortest_paths(tag1, to=tag2, mode=OUT, output='vpath')

    for n in path[0]:
        if n < numberTags:
            print("{}".format(g.vs[n]['name']))

    return path

#Findet kürzesten Pfad, wirft Fehler bei falscher Eingabe
def path_Input():
    tagList = createTags(numberTags)
    while 1:
        cmd = input('Geben Sie 2 Tags ein, mit Leerzeichen: ')
        if cmd == 'q':
            break;
        else:
            tags = cmd.split()
            if tags[0] not in tagList:
                print("Erste Eingabe", tags[0] ,"fehlerhaft.")
                return
            if tags[1] not in tagList:
                print("Zweite Eingabe", tags[1] ,"fehlerhaft.")
                return
            else:
                path = findPath(tags[0], tags[1])
                print("Dies ist der kürzeste Pfad. Items wurden nicht aufgelistet.")

# Interaction with graph
def input_loop():

    tagDeg = tagDegree(g, numberTags)
    tagRank = rankTags(tagDeg)
    while 1:
        cmd = input('--> ')
        if cmd == 'c':
            print("hier anzahl cluster auflisten")
        if cmd == 'e':
            print("Alle Kanten (egdes):",g.get_edgelist())
        if cmd == 'g':
            #plot des Graphen
            igraph.plot(g, layout=layout, bbox=(800, 600), margin=20)
        if cmd == 'i':
            print("Es gibt folgende Items: ", g.vs.select(type="i")["name"])
        if cmd == 'o':
            print("Der vorliegende Graph enthält insgesamt",numberItems,"Items und",numberTags,"Tags. Es sind",len(tagRank[0]),"Tags mit hohem Knotengrad,",len(tagRank[1]),
            "Tags mit mittlerem Knotengrad, und",len(tagRank[2]), "Tags mit niedrigem Knotengrad.")
        if cmd == 'p':
            path_Input()
        if cmd == 'q':
            break;
        if cmd == 't':
            print("Es gibt folgende Tags: ", g.vs.select(type="t")["name"])  # alpabethische Sortierung fehlt noch
        if cmd == 'v':
            print("Die Tag-Knoten mit Knotengrad: ", tagDeg)
        if cmd == '1':
            print("Es gibt", len(tagRank[0]), "Tags mit hohem Knotengrad. Es sind: ", tagRank[0])
        if cmd == '2':
            print("Es gibt", len(tagRank[1]), "Tags mit mittlerem Knotengrad. Es sind: ", tagRank[1])
        if cmd == '3':
            print("Es gibt", len(tagRank[2]), "Tags mit niedrigem Knotengrad. Es sind: ", tagRank[2])


if __name__ == '__main__':
    import igraph
    import cairo
    import matplotlib.pyplot as plt
    import pandas as pd
    import string
    import random

    print(igraph.__version__)

    numberTags = 9
    numberItems = 90
    numberEdges = 180
    #hier wird der Graph erzeugt
    g = createKWGraph(numberTags,numberItems, numberEdges)

    #Darstellung Graph
    layout = g.layout("fr")
    g.vs["label"] = g.vs["name"]
    color_dict = {"t": "red", "i": "white"}
    shape_dict = {"t": "circle", "i": "rectangle"}
    g.vs["color"] = [color_dict[type] for type in g.vs["type"]]
    g.vs["shape"] = [shape_dict[type] for type in g.vs["type"]]
    igraph.plot(g, layout=layout, bbox=(800, 600), margin=20)

    input_loop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
