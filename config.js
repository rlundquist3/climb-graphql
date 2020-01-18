import { withData } from 'next-apollo';
import { HttpLink } from 'apollo-link-http';

const config = {
  link: new HttpLink({
    uri: 'https://riley-hasura-test.herokuapp.com/v1/graphql',
  }),
};

export default withData(config);
