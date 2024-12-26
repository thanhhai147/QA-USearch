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
    static querySearch(query) {
        return fetch(
            `http://localhost:8000/query_search`, 
            {
                method: "POST",
                mode: "cors",
                headers: { 
                    "Content-type": "application/json; charset=UTF-8"
                },
                body: JSON.stringify({
                    query: query
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

}

export default RAGAPI