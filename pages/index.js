import gql from 'graphql-tag';
import { useQuery } from '@apollo/react-hooks';
import withData from '../config';

import RouteList from './route-list';

const routeQuery = gql`
  query {
    route {
      name
      grade
      area {
        name
        parent_area {
          name
        }
      }
      location
    }
  }
`;

const Index = ({ authors }) => {
  const { data, loading, error } = useQuery(routeQuery, {
    fetchPolicy: 'cache-and-network',
  });

  return (
    <React.Fragment>
      {error && <div>Error..</div>}
      {
        <React.Fragment>
          <h1>Routes</h1>
          {loading && <div>Loading...</div>}
          <RouteList routes={data ? data.route : []} />
        </React.Fragment>
      }
    </React.Fragment>
  );
};

export default withData(Index);
