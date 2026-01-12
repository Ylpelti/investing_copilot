type UserBase = {
    username: string
    email:string
}

export type UserRead = UserBase & {
    id:number
}

export type UserCreate = UserBase & {
    password: string
}

export type UserLogin = {
    username: string
    password: string
}