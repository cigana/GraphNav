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
    #for n in path[0]:
    #    if n < numberTags:
    #        print("{}".format(g.vs[n]['name']))
    return path

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
    color_dict = {"t": "red", "i": "white"}
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
        [sg.Text("Beschreibung")],
        [sg.Text("o: Überblick (overview)")],
        [sg.Text("i/t: Auflistung aller Items/Tags")],
        [sg.Text("1/2/3: Auflistung der Tags mit hohem/mittlerem/niedrigem Knotengrad")],
        [sg.Text("v: Auflistung aller Tags mit Knotengrad")],
        [sg.Text("c: Auflistung der Item-Cluster")],
        [sg.Text("Navigation")],
        [sg.Text("p: Findet kürzesten Pfad von Tag zu Tag")],
        [sg.Text('Auswahl:', size=(15, 1)), sg.InputText()],
        [sg.Text('Pfad von:', size=(15, 1)), sg.InputText()],
        [sg.Text('Pfad bis:', size=(15, 1)), sg.InputText()],
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
            g = createKWGraph(numberTags,numberItems, numberEdges)
            layout = g.layout("fr")
            g.vs["label"] = g.vs["name"]
            color_dict = {"t": "red", "i": "white"}
            shape_dict = {"t": "circle", "i": "rectangle"}
            g.vs["color"] = [color_dict[type] for type in g.vs["type"]]
            g.vs["shape"] = [shape_dict[type] for type in g.vs["type"]]
            igraph.plot(g, "testgraph2.png")
            window["-DEFAULT-"].update(filename="testgraph2.png")
            #window["-IMAGE-"].update(filename="testgraph2.png")
        if event == "Execute":
            ausgabe=""
            cmd = values[3]
            tagDeg = tagDegree(g, numberTags)
            tagRank = rankTags(tagDeg)
            if cmd == 'c':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("hier anzahl cluster auflisten")
            if cmd == 'e':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Alle Kanten (egdes):", g.get_edgelist())
            if cmd == 'i':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt folgende Items: ", g.vs.select(type="i")["name"])
            if cmd == 'o':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Der vorliegende Graph enthält insgesamt", numberItems, "Items und", numberTags, "Tags. Es sind", len(tagRank[0]), "Tags mit hohem Knotengrad,", len(tagRank[1]), "Tags mit mittlerem Knotengrad, und", len(tagRank[2]), "Tags mit niedrigem Knotengrad.", end='')
            if cmd == 'p':
                tagList = createTags(numberTags)
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
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Die Tag-Knoten mit Knotengrad: ", tagDeg)
            if cmd == '1':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt", len(tagRank[0]), "Tags mit hohem Knotengrad. Es sind: ", tagRank[0])
            if cmd == '2':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt", len(tagRank[1]), "Tags mit mittlerem Knotengrad. Es sind: ", tagRank[1])
            if cmd == '3':
                window['-ML1-' + sg.WRITE_ONLY_KEY].print("Es gibt", len(tagRank[2]), "Tags mit niedrigem Knotengrad. Es sind: ", tagRank[2])

            window['-ML1-' + sg.WRITE_ONLY_KEY].print('\n', end='')

    window.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
