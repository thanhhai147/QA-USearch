class RAGAPI {
    static addFilesToUSearch(files) {
        return fetch(
            `http://localhost:8000/add-files-to-usearch`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    files: files,
                })
            }
        )
    }
    static querySearch(query, sessionId) {
        return fetch(
            `http://localhost:8000/query-search`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    query: query,
                    session_id: sessionId
                })
            }
        )
    }

    static getUploadedFiles() {
        return fetch(
            `http://localhost:8000/get-uploaded-files`, 
            {
                method: "GET",
                mode: "cors"
            }
        )
    }

    static getSource(chatId) {
        return fetch(
            `http://localhost:8000/get-source?chat_id=${chatId}`, 
            {
                method: "GET",
                mode: "cors"
            }
        )
    }
}

export default RAGAPI