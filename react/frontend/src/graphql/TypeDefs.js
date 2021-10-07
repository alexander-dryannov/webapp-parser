import { gql } from '@apollo/client'

export const GET_PRICE_AEROSIB = gql`
    query getPriceAerosib($limit: Int) {
        getPriceAerosib(limit: $limit) {
            id
            departure
            appointment
            AK
            cost
        }
    }
`
export const GET_PRICE_AERODAR = gql`
    query getPriceAerodar($limit: Int) {
        getPriceAerodar(limit: $limit) {
            id
            departure
            appointment
            AK
            cost
        }
    }
`
export const GET_PRICE_TRANSCOM = gql`
    query getPriceTranscom($limit: Int) {
        getPriceTranscom(limit: $limit) {
            id
            departure
            appointment
            AK
            cost
        }
    }
`
export const GET_PRICE_ARTIS = gql`
    query getPriceArtis($limit: Int) {
        getPriceArtis(limit: $limit) {
            id
            departure
            appointment
            AK
            cost
        }
    }
`
export const GET_PRICE_MDCARGO = gql`
    query getPriceMdcargo($limit: Int) {
        getPriceMdcargo(limit: $limit) {
            id
            departure
            appointment
            AK
            cost
        }
    }
`