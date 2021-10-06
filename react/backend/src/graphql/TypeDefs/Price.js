import { gql } from 'apollo-server-express';

export default gql`
    type Price {
        id: String
        departure: String
        appointment: String
        AK: String
        cost: String
    }
    type Query {
        getPriceAerodar(limit: Int): [Price]
        getPriceAerosib(limit: Int): [Price]
        getPriceArtis(limit: Int): [Price]
        getPriceMdcargo(limit: Int): [Price]
        getPriceTranscom(limit: Int): [Price]
    }
`