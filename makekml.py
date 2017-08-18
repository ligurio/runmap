#!/usr/bin/python
# -*- coding: utf-8

import json
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def main():

    with open("data.json") as f:
        data = json.load(f)

    map = KML.kml(
        KML.Document(
          GX.Tour(
            KML.name("Play me!"),
            GX.Playlist(),
          ),
          KML.Folder(
            KML.name(u'Беговые дорожки Москвы'),
            id='features',
          ),
        )
    )

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

        map.Document.Folder.append(
             KML.Placemark(
               KML.name(object.get("ObjectName")),
               #KML.description(make_desc(object).encode('utf8')),
               KML.description(make_desc(object)),
               KML.Point(
                 KML.coordinates("{lon},{lat},{alt}".format(
                         lon=object["geoData"]["coordinates"][0],
                         lat=object["geoData"]["coordinates"][1],
                         alt=50,
                     )
                 )
               ),
               # KML.ExtendedData(
               # KML.Data(KML.value('someValueGadzilion'),name='Your value name here')
               # ),
               id=str(object["global_id"])
             )
           )

        print make_desc(object)

    filename = "map.kml"
    with open(filename, 'w') as outfile:
        outfile.write(etree.tostring(map, pretty_print=True))


def make_desc(object):

    # Using the CDATA Element
    # https://developers.google.com/kml/documentation/kml_tut#descriptive_html
    desc = ""
    if "SurfaceTypeSummer" in object.keys():
        desc = desc + u'<b>Покрытие дорожек:</b> '
        desc = desc + object.get("SurfaceTypeSummer", "").encode('utf8') + '.'
    if "TracksInfo" in object.keys():
        desc = desc + " "
        desc = desc + object.get("TracksInfo", "").encode('utf8')
    if "FoursquareTips" in object.keys():
        url = object.get("FoursquareTips", "").encode('utf8')
        href = "<a href=\"%s\">Подсказки</a>" % url
        desc = desc + " " + href
    if "Lighting" in object.keys():
        light = object.get("Lighting", "").encode('utf8')
        desc = desc + " " + upperfirst(light) + "."
    if "Paid" in object.keys():
        desc = desc + " " + "Посещение "
        desc = desc + object.get("Paid", "").encode('utf8') + "."

    desc = desc + " " + make_props(object)
    desc = desc + " " + make_contacts(object)

    return desc


def make_props(object):

    desc = ""
    if "HasToilet" in object.keys() or \
       "HasEatery" in object.keys() or \
       "HasDressingRoom" in object.keys() or \
       "HasCashMachine" in object.keys():

        desc = "Там есть "
        if "HasToilet" in object.keys() and \
            object.get("HasToilet", "").encode('utf8') == "да":
            desc = desc + "туалет"
        if "HasEatery" in object.keys() and \
            object.get("HasEatery", "").encode('utf8') == "да":
            if desc == 'Там есть':
                desc = desc + "кафе"
            else:
                desc = desc + ", кафе"
        if "HasDressingRoom" in object.keys() and \
            object.get("HasDressingRoom", "").encode('utf8') == "да":
            if desc == 'Там есть':
                desc = desc + "раздевалки"
            else:
                desc = desc + ", раздевалки"
        if "HasCashMachine" in object.keys() and \
            object.get("HasCashMachine", "").encode('utf8') == "да":
            if desc == 'Там есть':
                desc = desc + "банкомат"
            else:
                desc = desc + ", банкомат"
        else:
            desc = desc + "."

    return desc


def make_contacts(object):

    desc = "<br><b>Контакты:</b> "
    if "Address" in object.keys():
        desc = desc + object.get("Address", "").encode('utf8')
    if "HelpPhone" in object.keys():
        desc = desc + ", " + object.get("HelpPhone", "").encode('utf8')
    if "WebSite" in object.keys():
        url = object.get("WebSite", "").encode('utf8')
        href = "<a href=\"http://%s\">%s</a>" % (url, url)
        desc = desc + ", " + href

    return desc


def upperfirst(x):
    return x[0].upper() + x[1:]


main()
