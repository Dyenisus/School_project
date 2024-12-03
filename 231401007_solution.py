import zeep
import json

def announcements(line_code):
    announcement_messages = []
    number_of_announcements = 0
    
    url = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl"
    client = zeep.Client(wsdl = url)
    all_announcement_messages = client.service.GetDuyurular_json()
    all_announcement_messages = json.loads(all_announcement_messages)
    
    for item in all_announcement_messages:
        
        if  item["HATKODU"] == line_code and item["MESAJ"] != []:
            
            announcement_messages.append(item["MESAJ"])
            number_of_announcements = len(announcement_messages) 
        
        elif item["HATKODU"] == line_code and item["MESAJ"] == []:
            
            announcement_messages = []
            number_of_announcements = 0
        
        elif item["HATKODU"] != line_code:
            announcement_messages = []
            number_of_announcements = 0

    return number_of_announcements,announcement_messages


def stopping_buses():
    stopping_bus_list = []
    
    url = "https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl"
    client = zeep.Client(wsdl = url)
    all_buses = client.service.GetFiloAracKonum_json()
    all_buses = json.loads(all_buses)
    for item in all_buses:
        if item["Hiz"] == "0":
            stopping_bus_list.append(item["KapiNo"])
    
    
    return stopping_bus_list


def max_speeds():
    max3_speed = []

    url = "https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl"
    client = zeep.Client(wsdl = url)
    all_buses = client.service.GetFiloAracKonum_json()
    all_buses = json.loads(all_buses)
    
    all_buses_sorted = sorted(all_buses, key=lambda x: int(x["Hiz"]), reverse=True)
    max3_speed = all_buses_sorted[0:3]

    return max3_speed


def show_line_stops(line_code, direction):
    
    stop_list = []
    url = "https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl"
    client = zeep.Client(wsdl = url)  
    all_stops = client.service.DurakDetay_GYY(hat_kodu = line_code)
    
    for child in all_stops:
        if child.find("YON").text == direction:
            stop_list.append(child.find("DURAKADI").text)

    return stop_list

    
def live_tracking(line_code, direction):

    file_name = "where.js"
    stops = []
    buses = []
    
    url ="https://api.ibb.gov.tr/iett/ibb/ibb.asmx?wsdl"#ibb web service
    client = zeep.Client(wsdl = url)  
    all_stops = client.service.DurakDetay_GYY(hat_kodu = line_code)

    for child in all_stops:
        if child.find("YON").text == direction:
            stops.append([child.find("DURAKADI").text,child.find("YKOORDINATI").text,child.find("XKOORDINATI").text])
        
    url ="https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx?wsdl"#fleet
    client = zeep.Client(wsdl = url)
    all_buses = client.service.GetHatOtoKonum_json(HatKodu = line_code)
    all_buses = json.loads(all_buses)

    for item in all_buses:
        buses.append([item["kapino"],item["enlem"],item["boylam"]])
    
    with open(file_name,"a") as file:
        file.write("stops ="+json.dumps(stops)+"\n")
        file.write("buses ="+json.dumps(buses))

    return stops , buses