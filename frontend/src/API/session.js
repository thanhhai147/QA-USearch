class SessionAPI {
    static createSession(userId, sessionName, context) {
        return fetch(
            `http://localhost:8000/create-session`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    user_id: userId,
                    session_name: sessionName,
                    context: context
                })
            }
        )
    }

    static getSession(userId) {
        return fetch(
            `http://localhost:8000/get-session?user_id=${userId}`, 
            {
                method: "GET",
                mode: "cors"
            }
        )
    }

    static deleteSession(sessionId) {
        return fetch(
            `http://localhost:8000/delete-session`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    session_id: sessionId
                })
            }
        )
    }

    static updateSessionName(sessionId, sessionName) {
        return fetch(
            `http://localhost:8000/update-session-name`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    session_name: sessionName
                })
            }
        )
    }
}

export default SessionAPI