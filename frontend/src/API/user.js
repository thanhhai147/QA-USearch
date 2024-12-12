class UserAPI {
    static login(username, password) {
        return fetch(
            `http://localhost:8000/login`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    user_name: username || "", // Tránh null
                    password: password || ""  // Tránh null
                })
            }
        )
    }

    static signup(username, password) {
        return fetch(
            `http://localhost:8000/signup`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    user_name: username,
                    password: password
                })
            }
        )
    }

    static logout(userId) {
        return fetch(
            `http://localhost:8000/logout`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    user_id: userId
                })
            }
        )
    }
}

export default UserAPI