import prisma from '../pclient'

export default {
    Query: {
        getPriceMdcargo: async (_, {limit}) => {
            return await prisma.mdcargo.findMany({
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