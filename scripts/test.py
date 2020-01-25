import requests
import re
import json
from graphqlclient import GraphQLClient

client = GraphQLClient('https://riley-hasura-test.herokuapp.com/v1/graphql')

response = requests.get('https://www.mountainproject.com/data/get-routes-for-lat-lon?lat=44.366803&lon=%20-121.140765&maxDistance=10&minDiff=5.10&maxDiff=5.12&key=111896882-73c802f3b0ee5993f90fbf10bb77d49f')

def get_areas():
    result = client.execute('''
    query Areas {
      area {
        id
        name
      }
    }
    ''')
    return json.loads(result)['data']['area']

def insert_route(name, lat, lng, grade, type, area_id):
    if area_id:
        result = client.execute('''
        mutation InsertRoute {
          insert_route(objects: {name: "%s", location: "(%s, %s)", grade: "%s", type: %s, area_id: "%s"}) {
            returning {
              id
            }
          }
        }
        ''' % (name, lat, lng, grade, type, area_id))
    else:
        result = client.execute('''
        mutation InsertRoute {
          insert_route(objects: {name: "%s", location: "(%s, %s)", grade: "%s", type: %s}) {
            returning {
              id
            }
          }
        }
        ''' % (name, lat, lng, grade, type))
    return json.loads(result)

def insert_area(name, lat, lng, parent_area_id = None):
    if parent_area_id:
        result = client.execute('''
        mutation InsertArea {
          insert_area(objects: {name: "%s", location: "(%s, %s)", parent_area_id: "%s"}) {
            returning {
              id
            }
          }
        }
        ''' % (name, lat, lng, parent_area_id))
    else:
        result = client.execute('''
        mutation InsertArea {
          insert_area(objects: {name: "%s", location: "(%s, %s)"}) {
            returning {
              id
            }
          }
        }
        ''' % (name, lat, lng))
        result_json = json.loads(result)
        print('area inserted', result_json)
        return result_json['data']['insert_area']['returning'][0]

if response.status_code == 200:
    routes = response.json()['routes']

    for route in routes:
        areas = get_areas()
        parent_area_id = None
        for area in route['location']:
            existing_area = next((a for a in areas if a['name'] == area), None)

            if existing_area:
                parent_area_id = existing_area['id']
            else:
                result = insert_area(re.sub(r'\(.*\) ', '', area), route['latitude'], route['longitude'], parent_area_id)
                print('area', result)
                if result:
                    parent_area_id = result['id']

        result = insert_route(route['name'], route['latitude'], route['longitude'], route['rating'], route['type'], parent_area_id)
        print('route inserted', result)
