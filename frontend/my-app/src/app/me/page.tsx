import { getCurrentUser } from "@/lib/api/auth/auth"

const MePage = async () => {
    const user = await getCurrentUser()
    return (
        <p>{user.username}</p>
    )
}

export default MePage