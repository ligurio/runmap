#!/usr/bin/python

import json
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

def main():

    with open("data.json") as f:
        data = json.load(f)

    pm_list = []
    for object in data:
        print object["ObjectName"]

        try:
            print object["Address"]
            print object["HelpPhone"]
            print object["WebSite"]
            print object["Paid"]
            print object["Lighting"]
            print object["HasToilet"]
            print object["HasEatery"]
            print object["HasDressingRoom"]
            print object["HasCashMachine"]
            print object["SurfaceTypeSummer"]
        except KeyError:
            pass

        coordinates = "%s, %s" % (object["geoData"]["coordinates"][0], object["geoData"]["coordinates"][1])

        pm = KML.Placemark(
            KML.name(object["ObjectName"]),
            KML.Point(KML.coordinates(coordinates))
        )
        pm_list.append(pm)

    doc = KML.Folder(pm_list)
    print etree.tostring(doc, pretty_print=True)

    filename = "map1.kml"
    with open(filename, 'w') as outfile:
        outfile.write(etree.tostring(doc, pretty_print=True))

main()
