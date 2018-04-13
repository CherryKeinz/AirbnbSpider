# -*-coding:utf-8-*-
import csv
import json
import codecs
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getReviewDate(load_dict):
    model = []
    for item in load_dict['reviews']:
        model.append(item['localized_date'])
    return  model

def getPrice(load_dict):
    return load_dict['pdp_listing_booking_details'][0]['rate_with_service_fee']['amount']
def select(load_dict):
    model = []
    for i, item in enumerate(load_dict):
        per = {}
        host_dict = {}
        home_dict = {}
        location_dict = {}
        # jsonItem = dict([(k,item[k]) for k in item if k== "json"])
        for k in item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing']:
            # hosts data
            if k == 'primary_host':
                host = item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]
                for hostKey in host:
                    if hostKey == 'host_name':
                        host_dict['hostname'] = host[hostKey]
                    if hostKey == 'member_since_full_str':
                        host_dict['jointime'] = host[hostKey]
            per['host'] = host_dict
            # locations data
            if k == 'location_title':
                location = item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]
                per['locaiton'] = splitLocation(location_dict, location)
            # homes data
            if k == 'guest_label':
                home_dict['guest'] = item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]
            if k == 'bed_label':
                home_dict['bed'] = \
                    item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]
            if k == 'bedroom_label':
                home_dict['bedroom'] = \
                    item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]
            if k == 'bathroom_label':
                home_dict['bathroom'] = \
                    item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]
            if k == 'room_and_property_type':
                home_dict['hometype'] = \
                    item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]
            if k == 'review_details_interface':
                home_dict['review'] = \
                    item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]['review_count']
            if k == 'localized_city':
                home_dict['city'] = \
                    item['json']['bootstrapData']['reduxData']['homePDP']['listingInfo']['listing'][k]
            per['home'] = home_dict
        # per['website'] = dict([(k, item[k]) for k in item if k == 'website'])
        model.append(per)
    return model

# filePath 绝对路径
# fileName 无后缀名
def trans(filePath, fileName):
    model = []
    with codecs.open(filePath + '/' + fileName + '.json', 'r', 'utf-8') as jsonData:
        load_dict = json.loads(jsonData.read())
        model  = getReviewDate(load_dict)
    with codecs.open(filePath + '/' + fileName + 'datanew.json', 'wb','utf-8') as newJSONfile:
        json.dump(model, newJSONfile)

def splitLocation(location_dict,location):
    locationList = location.split(', ')
    if len(locationList)==3:
        location_dict['city'] = locationList[0]
        location_dict['state'] = locationList[1]
        location_dict['country'] = locationList[2]
    elif len(locationList)==2:
        location_dict['city'] = locationList[0]
        location_dict['country'] = locationList[1]
    return location_dict
if __name__ == '__main__':
    ##    # path=str(sys.argv[1]) # 获取path参数
    path = 'D:\MyCode\Python\sihuo\JSON2CSV'
    trans (path ,'reviewdate')

