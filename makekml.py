#!/usr/bin/python
# -*- coding: utf-8

import json
from pykml.factory import KML_ElementMaker as KML
from lxml import etree

def main():

    with open("data.json") as f:
        data = json.load(f)

    pm_list = []
    for object in data:
        print object.get("ObjectName", "")
        print "\tАдрес:", object.get("Address", "")
        print "\tТелефон:", object.get("HelpPhone", "")
        print "\tСайт:", object.get("WebSite", "")
        print "\tПлата:", object.get("Paid", "")
        print "\tОсвещение:", object.get("Lighting", "")
        print "\tТуалет:", object.get("HasToilet", "")
        print "\tКафе:", object.get("HasEatery", "")
        print "\tРаздевалки:", object.get("HasDressingRoom", "")
        print "\tБанкомат:", object.get("HasCashMachine", "")
        print "\tПокрытие:", object.get("SurfaceTypeSummer", "")

        coordinates = "%s, %s" % (object["geoData"]["coordinates"][0], object["geoData"]["coordinates"][1])

        pm = KML.Placemark(
            KML.name(object["ObjectName"]),
            KML.Point(KML.coordinates(coordinates))
        )
        pm_list.append(pm)

    doc = KML.Folder(pm_list)
    #print etree.tostring(doc, pretty_print=True)

    filename = "map1.kml"
    with open(filename, 'w') as outfile:
        outfile.write(etree.tostring(doc, pretty_print=True))

# <Placemark>
# <description>
#   <![CDATA[
#     <a href="http://yourserver.com/your.kml#Location1;Flyto">Click Me</a>
#   ]]>
# </description>
# </Placemark>

main()
