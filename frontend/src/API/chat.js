class ChatAPI {
    static createChat(sessionId, userAsk) {
        return fetch(
            `http://localhost:8000/create-chat`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    user_ask: userAsk
                })
            }
        )
    }

    static getChat(sessionId) {
        return fetch(
            `http://localhost:8000/get-chat?session_id=${sessionId}`, 
            {
                method: "GET",
                mode: "cors"
            }
        )
    }

    static deleteChat(sessionId) {
        return fetch(
            `http://localhost:8000/delete-chat`, 
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
}

export default ChatAPI