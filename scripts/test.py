from graphqlclient import GraphQLClient

client = GraphQLClient('https://riley-hasura-test.herokuapp.com/v1/graphql')

def insert_area(name, location):
    result = client.execute('''
    mutation InsertArea {
      insert_area(objects: {name: "%s", location: "%s"}) {
        returning {
          id
        }
      }
    }
    ''' % (name, location))
    result_json = json.loads(result)
    return not not result_json['data']
