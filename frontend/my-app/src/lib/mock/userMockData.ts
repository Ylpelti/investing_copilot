import { UserRead, UserCreate } from "../../types/user"


export const mockUsersRead: UserRead[] = [
  {
    id: 4,
    username: "alice_investor",
    email: "new_user_1@example.com"
  },
  {
    id: 2,
    username: "bob_portfolio",
    email: "new_user_2@example.com"
  },
  {
    id: 3,
    username: "charlie_quant",
    email: "new_user_3@example.com"
  }
]

export const currentUser: UserRead = {
  id: 42,
  username: "Ylpelti",
  email: "yl.pelti@example.com"
}


export const mockUsersCreate: UserCreate[] = [
  {
    username: "new_user_1",
    password: "plain_password_1",
    email: "new_user_1@example.com"
  },
  {
    username: "new_user_2",
    password: "plain_password_2",
    email: "new_user_2@example.com"
  }
]

export const getCurrentUser = () => {
  return currentUser
}