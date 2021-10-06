import prisma from '../pclient'

export default {
    Query: {
        getPriceAerosib: async (_, {limit}) => {
            return await prisma.aerosib.findMany({
                take: limit
            })
            .catch((e) => {
                throw e
            })
            .finally(() => {
                prisma.$disconnect
            })
        }
    }
}