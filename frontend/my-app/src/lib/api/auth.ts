import { UserRead, UserCreate } from "@/types/user";
import { mockUsersRead } from "../mock/userMockData";

export const getUsers = async (): Promise<UserRead[]> => {
    return mockUsersRead
}

export const registerUser = async (data: UserCreate): Promise<UserRead> => {
    return 
}