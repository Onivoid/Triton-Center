/*
import dotenv from 'dotenv';
import { client } from '@/pages/_app';
import { gql } from '@apollo/client';
import { LoginResponse } from '@/services/types/LoginResponse';
import { RegisterResponse } from '@/services/types/RegisterResponse';

dotenv.config();

const login = async (username: string, password: string) => {
    const LOGIN = await gql`
      mutation {
        login(password: "${password}", username: "${username}") {
          ... on AuthenticatedUser {
            __typename
            email
            token
            username
            discordId
          }
          ... on Error {
            __typename
            message
          }
        }
      }
    `;
    const {data} = await client.mutate({ mutation: LOGIN });
    const result = new LoginResponse(data);

    return result;
};

const register = async (email: string, username: string, password: string) => {
  const REGISTER = await gql`
    mutation {
      register(
        email: "${email}"
        password: "${password}"
        username: "${username}"
      ) {
        ... on PublicUser {
          __typename
          username
        }
        ... on Error {
          __typename
          message
        }
      }
    }
  `;
  const {data} = await client.mutate({ mutation: REGISTER });
  const result = new RegisterResponse(data);

  return result;
};

export { login };
*/