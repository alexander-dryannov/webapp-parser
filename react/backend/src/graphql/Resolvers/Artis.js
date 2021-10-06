import prisma from '../pclient'

export default {
    Query: {
        getPriceArtis: async (_, {limit}) => {
            return await prisma.artis.findMany({
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