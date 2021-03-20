#Hilfsfunktionen
#erzeugt Liste der Tags
from igraph._igraph import OUT

def createTags(numberTags):
    tags_up = string.ascii_uppercase[0:26]
    tags_low = string.ascii_lowercase[0:26]
    tags= tags_up+tags_low
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

#entferne isolierte Knoten
def dropIsolates(g) -> object:
    g.delete_vertices(g.vs.select(_degree=0))
    return g

#Alle Items zu einem Tag
def findItems(tagName):
    neis = g.neighbors(tagName, mode="out")
    return g.vs[neis]["name"]

#Alle Items zu 2 Tags
def findCommonItems(tagName1, tagName2):
    path = findPath(tagName1, tagName2)
    if len(path[0]) > 3:
        result = "haben keine Items/Tags gemeinsam"
    else:
        neiT1 =findItems(tagName1)
        neiT2 = findItems(tagName2)
        result = set(neiT1) & set(neiT2)
    return result

#erzeugt Dictionary mit key=Vertex-Name, value=degree, Absteigende Reihenfolge
def listDegree(g, strType) -> object:
    names = (g.vs.select(type=strType)["name"])
    deg = (g.vs.select(type=strType).degree())
    lDeg =dict(zip(names, deg))
    sort_Deg = dict(sorted(lDeg.items(), key=lambda x: x[1], reverse=True))
    return sort_Deg

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
    #for n in path[0]:
    #    if n < numberTags:
    #        print("{}".format(g.vs[n]['name']))
    return path

# Hilfsfunktion zur Cluster Funktion
def defineGroups(itemList):
    dict = {}
    for item in itemList:
        group = findItems(item)
        groupWord = ' '.join(group)
        if groupWord  in dict:
            dict[groupWord].append(item)
        else:
            dict[groupWord ] = [item]
    return dict

# Finde Cluster im Graphen, einfacher Ansatz
def findCluster(g):
    itemDeg = listDegree(g, "i")
    deg_dict = {}
    cluster = {}
    for key in itemDeg:
        deg_dict.setdefault(itemDeg[key], []).append(key)

    for key in deg_dict.keys():
        val = defineGroups(deg_dict[key])
        cluster[key] = [val]

    return cluster

if __name__ == '__main__':
    import igraph
    import cairo
    import matplotlib.pyplot as plt
    import pandas as pd
    import string
    import random

    print(igraph.__version__)

    numberTags = 6
    numberItems = 90
    numberEdges = 160
    #hier wird der Graph erzeugt
    g = createKWGraph(numberTags,numberItems, numberEdges)

    #Darstellung Graph
    layout = g.layout("kk")
    g.vs["label"] = g.vs["name"]
    color_dict = {"t": "green", "i": "white"}
    shape_dict = {"t": "circle", "i": "rectangle"}
    g.vs["color"] = [color_dict[type] for type in g.vs["type"]]
    g.vs["shape"] = [shape_dict[type] for type in g.vs["type"]]
    #igraph.plot(g, layout=layout, bbox=(800, 600), margin=20)

    #speichert Graphen in Projektverzeichnis
    igraph.plot(g,  "testgraph.png")

    #Starte Beautification
    import PySimpleGUI as sg

    graph_column = [
        [sg.Text("Graph-Visualisierung:")],
        [sg.Text(size=(40, 1))],
        [sg.Text(size=(40, 1), key="-TOUT-")],
        [sg.Image(key="-DEFAULT-", filename="testgraph.png")],
    ]

    command_column = [
        [sg.Text("Kreire den Graphen neu (Eingabe+Submit):")],
        [sg.Text('Anzahl Tags:', size=(15, 1)), sg.InputText("6")],
        [sg.Text('Anzahl Items:', size=(15, 1)), sg.InputText("90")],
        [sg.Text('Anzahl Kanten:', size=(15, 1)), sg.InputText("160")],
        [sg.Submit(bind_return_key=False)],

        [sg.Text("Erhalte Informationen durch Tastenbefehle (Befehl+Enter/Execute),")],
        [sg.Text("Folgende Befehle stehen zur Verfügung:")],
        [sg.Text("Beschreibung", text_color='black')],
        [sg.Text("o: Überblick (overview)                       z: Zusammenhängender Graph")],
        [sg.Text("i/t: Auflistung aller Items/Tags              d: Details zu Tags oder Items")],
        [sg.Text("1/2/3: Auflistung der Tags mit hohem/mittlerem/niedrigem Knotengrad")],
        [sg.Text("v: Auflistung aller Tags mit Knotengrad")],
        [sg.Text("c: Auflistung der Item-Cluster")],
        [sg.Text("Navigation", text_color='black')],
        [sg.Text("p: Findet kürzesten Pfad von Tag zu Tag")],
        [sg.Text('Auswahl:', size=(16, 1)), sg.InputText()],
        [sg.Text('Details 1/Pfad von:', size=(16, 1)), sg.InputText()],
        [sg.Text('Details 2/Pfad bis:', size=(16, 1)), sg.InputText()],
        [sg.Text(size=(20, 1), key="-TIN-")],
        [sg.Button('Execute', bind_return_key=True) ],
        [sg.MLine(key='-ML1-' + sg.WRITE_ONLY_KEY, size=(60, 10))],

    ]

    # Full Layout
    layout = [
        [
            sg.Column(command_column),
            sg.VSeperator(),
            sg.Column(graph_column),
        ],[sg.Text("GraphNav Prototyp (c) Melanie Forker 2021")], [sg.Button("Quit")]]

    # Create the window
    window = sg.Window("GraphNav", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "Quit" or event == sg.WIN_CLOSED:
            break
        if event == "Submit":
            numberTags = int(values[0])
            numberItems = int(values[1])
            numberEdges = int(values[2])
            g = createKWGraph(numberTags, numberItems, numberEdges)
            layout = g.layout("fr")
            g.vs["label"] = g.vs["name"]
            color_dict = {"t": "green", "i": "white"}
            shape_dict = {"t": "circle", "i": "rectangle"}
            g.vs["color"] = [color_dict[type] for type in g.vs["type"]]
            g.vs["shape"] = [shape_dict[type] for type in g.vs["type"]]
            igraph.plot(g, "testgraph2.png")
            window["-DEFAULT-"].update(filename="testgraph2.png")
            #window["-IMAGE-"].update(filename="testgraph2.png")
        if event == "Execute":
            ausgabe=""
            cmd = values[3]
            tagDeg = listDegree(g, "t")
            tagRank = rankTags(tagDeg)
            if cmd == 'c':
                cluster = findCluster(g)
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Folgende Cluster wurden gefunden, sortiert nach Größe absteigend ->Anzahl Tags -> Namen Tags, Dazugehörige Items<-  ", cluster)
            if cmd == 'e':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Alle Kanten (egdes):", g.get_edgelist())
            # Ausgabe Details ****NEU**********:
            if cmd == 'd':
                VertexList = g.vs["name"]
                tagList = (g.vs.select(type='t')["name"])
                # prüfe ob eine Eingabe leer ist
                if (values[4] == '') or (values[5] == ''):
                    # beide leer
                    if (values[4] == '') and (values[5] == ''):
                        window['-ML1-' + sg.WRITE_ONLY_KEY].print("Zur Abfrage der Details mindestens ein Tag oder Item auswählen. Bei zwei Einträgen gleichartige Knoten wählen")
                    else:
                        vertex = values[4] + values[5]
                        if (vertex not in VertexList):
                            window['-ML1-' + sg.WRITE_ONLY_KEY].print("Die Eingabe ist fehlerhaft.")
                        else:
                            neighbors = findItems(vertex)
                            if vertex in tagList:
                                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt", len(neighbors), "Items die zu Tag", vertex, "gehören:", neighbors)
                            else:
                                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt", len(neighbors), "Tags die zu Item", vertex, "gehören:", neighbors)
                # in beiden Fenstern ist was eingetragen -> Prüfung ob gleicher Typ fehlt noch
                else:
                    if (values[4] not in VertexList) or (values[5] not in VertexList):
                        window['-ML1-' + sg.WRITE_ONLY_KEY].print("Die Eingabe ist fehlerhaft.")
                    else:
                        commonNodes = findCommonItems(values[4], values[5])
                        if commonNodes == "haben keine Items/Tags gemeinsam":
                            window['-ML1-' + sg.WRITE_ONLY_KEY].print("Die Tags oder Items", values[4], "und", values[5], commonNodes)
                        else:
                            if values[4] in tagList:
                                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Die", len(commonNodes), "gemeinsamen Items von", values[4], "und", values[5], "sind:", commonNodes)
                            else:
                                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Die", len(commonNodes), "gemeinsamen Tags von", values[4], "und", values[5], "sind:", commonNodes)

            if cmd == 'i':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt folgende Items: ", g.vs.select(type="i")["name"])
            if cmd == 'o':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Der vorliegende Graph enthält insgesamt", numberItems, "Items und", numberTags, "Tags. Es sind", len(tagRank[0]), "Tags mit hohem Knotengrad,", len(tagRank[1]), "Tags mit mittlerem Knotengrad, und", len(tagRank[2]), "Tags mit niedrigem Knotengrad.", end='')
            if cmd == 'p':
                tagList = (g.vs.select(type='t')["name"])
                if values[4] not in tagList:
                    window['-ML1-' + sg.WRITE_ONLY_KEY].print("Erste Eingabe fehlerhaft.")
                if values[5] not in tagList:
                    window['-ML1-' + sg.WRITE_ONLY_KEY].print("Zweite Eingabe fehlerhaft.")
                else:
                    weg = ""
                    path = findPath(values[4], values[5])
                    for n in path[0]:
                        if n < numberTags:
                            weg += (g.vs[n]['name'])
                    window['-ML1-' + sg.WRITE_ONLY_KEY].print("Kürzester Pfad von",values[4], "nach", values[5], "ist", weg)
            if cmd == 't':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt folgende Tags: ", g.vs.select(type="t")["name"]) # alpabethische Sortierung fehlt noch
            if cmd == 'v':
                tagDeg = listDegree(g, "t")
                itemDeg = listDegree(g, "i")
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Die Tag-Knoten mit Knotengrad in absteigender Reihenfolge: ", tagDeg)
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Die Items mit Knotengrad in absteigender Reihenfolge:", itemDeg)

            if cmd == '1':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt", len(tagRank[0]), "Tags mit hohem Knotengrad. Es sind: ", tagRank[0])
            if cmd == '2':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt", len(tagRank[1]), "Tags mit mittlerem Knotengrad. Es sind: ", tagRank[1])
            if cmd == '3':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt", len(tagRank[2]), "Tags mit niedrigem Knotengrad. Es sind: ", tagRank[2])
            if cmd == 'z':
                g = dropIsolates(g)
                tagList = (g.vs.select(type='t')["name"])
                numberTags = len(tagList)
                numberItems = len(g.vs.select(type='i')["name"])
                igraph.plot(g, "testgraph2.png")
                window["-DEFAULT-"].update(filename="testgraph2.png")
            window['-ML1-' + sg.WRITE_ONLY_KEY].print('\n', end='')

    window.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
