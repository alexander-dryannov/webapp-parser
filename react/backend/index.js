import { ApolloServer } from 'apollo-server-express'
import express from 'express'
import http from 'http'
import typeDefs from './src/graphql/TypeDefs'
import resolvers from './src/graphql/Resolvers'
import dotenv from 'dotenv'

dotenv.config()

async function startApolloServer(typeDefs, resolvers) {
    const app = express();
    const httpServer = http.createServer(app);
    const server = new ApolloServer({
      typeDefs,
      resolvers
    });
    await server.start();
    server.applyMiddleware({ app });
    await new Promise(resolve => httpServer.listen({ port: process.env.SERVER_PORT }, resolve));
    console.log(`🚀 Server ready at http://localhost:${process.env.SERVER_PORT}${server.graphqlPath}`);
  }
  
  startApolloServer(typeDefs, resolvers) 
