import prisma from '../pclient'

export default {
    Query: {
        getPriceAerodar: async (_, {limit}) => {
            return await prisma.aerodar.findMany({
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