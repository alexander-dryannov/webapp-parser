import prisma from '../pclient'

export default {
    Query: {
        getPriceTranscom: async (_, {limit}) => {
            return await prisma.transcomavia.findMany({
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