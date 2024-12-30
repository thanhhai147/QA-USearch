import React, { useState, useEffect } from "react"
import { Button, Input, Menu, Dropdown, Popconfirm, Modal, Spin, Upload, Tag } from "antd"
import { MenuOutlined, UserOutlined, DownOutlined, MinusCircleOutlined, EditOutlined, FormOutlined, UploadOutlined } from "@ant-design/icons"
import { useNavigate } from "react-router-dom"
import { useAuth } from '../context/authentication.context'
import UserAPI from "../API/user"
import ChatAPI from "../API/chat"
import RAGAPI from "../API/rag"
import SessionAPI from "../API/session"
import "../assets/css/ChatPage.css"

let flag = false

export default function ChatPage() {
    const [isSidebarVisible, setSidebarVisible] = useState(true)
    const [sessionHistory, setSessionHistory] = useState([])
    const [chatHistory, setChatHistory] = useState([])
    const [currentSessionId, setCurrentSessionId] = useState(null)
    const [currentChat, setCurrentChat] = useState("")
    const [isFirstMessageSent, setIsFirstMessageSent] = useState(false)
    const [editingSessionId, setEditingSessionId] = useState(null)
    const [sessionName, setSessionName] = useState("Trò chuyện mới")
    // const [context, setContext] = useState("")
    const [message, setMessage] = useState(null) // State để lưu thông báo
    const [isSuccess, setIsSuccess] = useState(false) // State để xác định loại thông báo
    // const [isContextModalOpen, setIsContextModalOpen] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isAddModalOpen, setIsAddModalOpen] = useState(false)
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [metadata, setMetadata] = useState([]);
    const { username, logout , userId } = useAuth()
    const navigate = useNavigate()
    // const { TextArea } = Input

    useEffect(() => {
        handleLoadSessionHistory()
    }, [])

    useEffect(() => {
        setCurrentSessionId(sessionHistory[0]?.sessionId)
    }, [sessionHistory])

    useEffect(() => {
        handleLoadChatHistory()
    }, [currentSessionId])

    useEffect(() => {
        if (message) {
            const messageTimeout = setTimeout(() => {
                setMessage(null)
            }, 2000)
    
            return () => clearTimeout(messageTimeout)
        }
    }, [message])

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth < 768 && isFirstMessageSent) {
                document.querySelector(".chat-area").classList.add("with-first-message")
            } else {
                document.querySelector(".chat-area").classList.remove("with-first-message")
            }
        }

        window.addEventListener("resize", handleResize)

        handleResize()

        return () => window.removeEventListener("resize", handleResize)
    }, [isFirstMessageSent])

    const handleLoadSessionHistory = () => {
        setIsLoading(true)
        SessionAPI.getSession(userId)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const sessions = data?.data?.sessions
                if (sessions) {
                    setSessionHistory(() => {
                        let updatedSessionHistory = []
                        sessions.forEach(session => {
                            updatedSessionHistory.push({
                                sessionId: session?.session_id,
                                sessionName: session?.session_name,
                                context: session?.context,
                                updatedAt: session?.updated_at
                            })
                        })
                        return updatedSessionHistory
                    })
                }
                if (sessions.length === 0 && !flag) {
                    handleCreateSession()
                    // setIsContextModalOpen(true)
                }
            } else {
                setMessage("Lỗi khi truy xuất phiên: " + data.message)
                setIsSuccess(false)
            }
        })
        .catch(error => {
            setMessage("Lỗi khi truy xuất phiên: " + error.message)
            setIsSuccess(false)
        })
        .finally(() => {
            setIsLoading(false)
            flag = true
        })
    }

    const handleLoadChatHistory = () => {
        if (!currentSessionId) return
        setIsLoading(true)
        ChatAPI.getChat(currentSessionId)
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                const chats = data?.data?.chats
                if (chats) {
                    setChatHistory(chats.map(chat => ({
                        sessionId: chat.session_id,
                        chatId: chat.chat_id,
                        chatPosition: chat.chat_position,
                        userAsk: chat.user_ask,
                        botAnswer: chat.bot_answer
                    })))
                } else {
                    setMessage("Lỗi khi truy xuất trò chuyện: " + data.message)
                    setIsSuccess(false)
                }
            }
        })
        .catch(error => {
            setMessage("Lỗi khi truy xuất trò chuyện: " + error.message)
            setIsSuccess(false)
        })
        .finally(() => {
            setIsLoading(false)
        })
    }

    const handleCreateSession = () => {
        setIsLoading(true)
        SessionAPI.createSession(userId, sessionName) 
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                handleLoadSessionHistory()
                setIsFirstMessageSent(false)
            } else {
                setMessage("Lỗi khi tạo phiên: " + data.message)
                setIsSuccess(false)
            }
        })
        .catch(error => {
            setMessage("Lỗi khi tạo phiên: " + error.message)
            setIsSuccess(false)
        })
        .finally(() => {
            // setIsContextModalOpen(false)
            setIsLoading(false)
        })
    }

    
    const deleteSession = (sessionId) => {
        setIsLoading(true)
        SessionAPI.deleteSession(sessionId)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                handleLoadSessionHistory()
                setMessage("Xóa phiên trò chuyện thành công")
                setIsSuccess(true)
            } else {
                setMessage("Lỗi khi xóa phiên: " + data.message)
                setIsSuccess(false)
            }
        })
        .catch(error => {
            setMessage("Lỗi khi xóa phiên: " + error.message)
            setIsSuccess(false)
        })
        .finally(() => {
            setIsLoading(false)
        })
    }


    const handleCreateChat = () => {
               
        if (currentChat.trim()) {   
            setIsLoading(true)
            RAGAPI.querySearch(currentChat.trim()) 
            .then(response => response.json())
            .then(data => {
                console.log(data)
                if (data.success) {
                    handleLoadChatHistory()
                    setCurrentChat("")
                    setIsFirstMessageSent(true)
                } else {
                    setMessage("Lỗi khi tạo trò chuyện: " + data.message)
                    setIsSuccess(false)
                }
            })
            .catch(error => {
                setMessage("Lỗi khi tạo trò chyện: " + error.message)
                setIsSuccess(false)
            })
            .finally(() => {
                setIsLoading(false)
            })
        }
    }
    

    const handleKeyDown = (e) => {
        if (e.key === "Enter") {
            handleCreateChat()
        }
    }

    const selectSession = (sessionId) => {
        setCurrentSessionId(sessionId)
    }
    
    const handleEditSessionName = (sessionId) => {
        setEditingSessionId(sessionId)
    }

    const handleSaveSessionName = (sessionId) => {
        if (!sessionName) return
        setIsLoading(true)
        SessionAPI.updateSessionName(sessionId, sessionName)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                setMessage(data.message)
                setIsSuccess(true)
                handleLoadSessionHistory()
            } else {
                setMessage("Lỗi khi cập nhật tên phiên: " + data.message)
                setIsSuccess(false)
            }
        })
        .catch(error => {
            setMessage("Lỗi khi cập nhật tên phiên: " + error.message)
            setIsSuccess(false)
        })
        .finally(() => {
            setEditingSessionId(null)
            setSessionName("")
            setIsLoading(false)
        })
    }

    const handleLogout = () => {
        setIsLoading(true)
        UserAPI.logout(userId) 
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                setMessage(data.message) // Hiển thị thông báo thành công
                setIsSuccess(true)
                setTimeout(() => {
                    setMessage(data.message) 
                    logout() // ================
                    navigate("/login") 
                }, 1500)
            } else {
                setMessage(data.message)
                setIsSuccess(false)
            }
        })
        .catch((e) => {
            setMessage("Lỗi: " + e.message)
            setIsSuccess(false)
        })
        .finally(() => {
            setIsLoading(false)
        })
    }

    const handleOpenAddModal = () => {
        setIsModalOpen(false)
        setIsAddModalOpen(true)
    }

    const handleCloseAddModal = () => {
        setIsAddModalOpen(false)
    }

    const accountMenu = (
        <Menu>
            <Menu.Item key="1">
                Tài khoản: <strong>{username}</strong>
            </Menu.Item>
            <Menu.Item
                key="2"
                danger
                onClick={handleLogout} 
            >
                Đăng xuất
            </Menu.Item>
        </Menu>
    )
    

    const handleOpenModal = () => {
        RAGAPI.getUploadedFiles(uploadedFiles) 
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            setMetadata(data.data);
            console.log(data.data);
        })
        setIsModalOpen(true);
    };

    const handleCloseModal = () => {
        setIsModalOpen(false);
    };

    const handleFiles = (file) => {
        const isPDF = file.type === 'application/pdf';
        if (!isPDF) {
            console.log('You can only upload PDF files!');
            return Upload.LIST_IGNORE; // Ngăn file không hợp lệ vào danh sách
        }

        const isDuplicate = uploadedFiles.some((uploadedFile) => uploadedFile.name === file.name);
        if (isDuplicate) {
            console.log('This file has already been uploaded!');
            return Upload.LIST_IGNORE; // Ngăn file trùng lặp vào danh sách
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const fileData = {
                name: file.name,
                content: e.target.result, // Lưu Base64 hoặc URL tạm
            };
            setUploadedFiles((prevFiles) => [...prevFiles, fileData]);
        };
        reader.readAsDataURL(file);
        return false; // Ngăn không tải lên server
    };
    const handleAddFiles = () => {
        RAGAPI.addFilesToUSearch(uploadedFiles) 
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                setMessage(data.message) // Hiển thị thông báo thành công
                setIsSuccess(true)
            } else {
                setMessage(data.message)
                setIsSuccess(false)
            }
        })
        .catch((e) => {
            setMessage("Lỗi: " + e.message)
            setIsSuccess(false)
        })
        .finally(() => {
            setIsLoading(false)
        })
    }
    return (
        <div className="chat-page">
           
            {isSidebarVisible && (
                <div className="sidebar">
                    <div key={'his-chat'} className="his-chat">Lịch sử trò chuyện</div>
                    <div className="chat-history">
                        {
                            sessionHistory.map(session => (
                                <div key={session?.sessionId} className={`chat-title ${currentSessionId === session?.sessionId ? "selected" : ""}`}>
                                    {
                                        editingSessionId === session?.sessionId ? (
                                            <Input
                                                value={sessionName}
                                                onChange={(e) => setSessionName(e.target.value)}
                                                onBlur={() => handleSaveSessionName(session?.sessionId)}
                                                autoFocus
                                                disabled={isLoading}
                                            />
                                        ) : (
                                            <span className="chat-title-text" onClick={() => selectSession(session?.sessionId)}>
                                                {session?.sessionName}
                                            </span>
                                        )
                                    }
                                    <div className="chat-actions">
                                        <Popconfirm
                                            title="Bạn có chắc muốn xóa trò chuyện này?"
                                            onConfirm={() => deleteSession(session?.sessionId)}
                                            okText="Xóa"
                                            cancelText="Hủy"
                                            disabled={isLoading}
                                        >
                                            <Button type="link" danger><MinusCircleOutlined /></Button>
                                        </Popconfirm>
                                        <Button type="link" disabled={isLoading} onClick={() => handleEditSessionName(session?.sessionId)}><EditOutlined /></Button>
                                    </div>
                                </div>
                            ))
                        }
                    </div>
                </div>
            )}

            <div className={`main-content ${isSidebarVisible ? "" : "no-sidebar"}`}>
                <div className="header">
                    <div className="header-buttons">
                        <Button
                            className="toggle-sidebar"
                            icon={<MenuOutlined />}
                            onClick={() => setSidebarVisible(!isSidebarVisible)}
                            disabled={isLoading}
                        />
                        <Button
                            className="new-chat"
                            icon={<FormOutlined />}
                            // onClick={() => setIsContextModalOpen(true)}
                            onClick={() => handleCreateSession()}
                            disabled={isLoading}
                        >
                        </Button>
                        <Button icon={<UploadOutlined />} onClick={handleOpenModal}>
                        </Button>

                        <Modal
                            title="Upload PDF Files"
                            open={isModalOpen}
                            onCancel={handleCloseModal}
                            footer={[
                                <Button key="close" onClick={handleCloseModal}>
                                    Close
                                </Button>,
                            ]}
                        >
                            <Upload
                                accept=".pdf"
                                multiple
                                beforeUpload={handleFiles}
                                onRemove={(file) => {
                                    setUploadedFiles((prevFiles) => prevFiles.filter((f) => f.name !== file.name));
                                }}
                                showUploadList={true}
                            >
                                <Button icon={<UploadOutlined />}>
                                    Select Files
                                </Button>
                            </Upload>
                            
                            <div style={{ marginTop: 20 }}>
                                <Button onClick={handleAddFiles}>
                                    Add to DB
                                </Button>
                                <h4>Uploaded Files:</h4>
                                <ul>
                                    {metadata.map((file, index) => (
                                        <li key={index}>{file?.file_name} {file?.created_at}</li>
                                    ))}
                                </ul>
                            </div>
                        </Modal>
                        
                    </div>

                        <Dropdown 
                            overlay={accountMenu}
                            disabled={isLoading}
                        >
                            <Button className="account-info" icon={<UserOutlined />}>
                                {username} <DownOutlined />
                            </Button>
                        </Dropdown>
                    
                </div>

                {message && (
                    <div className={`message-box ${isSuccess ? "success" : "error"}`}>
                        {message}
                    </div>
                )}

                <div className="chat-area">
                    {/* {
                        currentSessionId &&
                        <div className="session-context">
                            {
                                sessionHistory.filter(session => session?.sessionId === currentSessionId)[0]?.context
                            }
                        </div>
                    } */}
                    {
                        currentSessionId &&
                        chatHistory.filter(chat => chat?.sessionId === currentSessionId).map(chat => {
                            return (
                                <>
                                    <div className="chat-message user-ask" key={"user-ask: " + chat.chatId}>
                                        {chat.userAsk}
                                    </div>
                                    <div className="chat-message bot-answer" key={"bot-answer: " + chat.chatId}>
                                        {chat.botAnswer}
                                    </div>
                                </>
                            )
                        })
                    }
                </div>

                <div className="chat-input-area">
                    <Input
                        value={currentChat}
                        onChange={(e) => setCurrentChat(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Nhập tin nhắn"
                        rows={1}
                        disabled={isLoading}
                    />
                    <Button type="primary" disabled={isLoading} onClick={handleCreateChat}>
                        Gửi
                    </Button>
                </div>
            </div>

            {/* <Modal
                className="context-modal"
                open={isContextModalOpen}
                title="Tạo cuộc trò chuyện mới"
                onCancel={() => {
                    setSessionName(null)
                    setIsContextModalOpen(false)
                }}
                footer={() => (
                <>
                    <Button type="primary" disabled={isLoading} onClick={handleCreateSession}>
                        Tạo
                    </Button>
                </>
                )}
            >
                <Input 
                    className="input-session-name"
                    value={sessionName}
                    onChange={(e) => setSessionName(e.target.value)}
                    placeholder="Nhập tên cuộc trò chuyện"
                    disabled={isLoading}
                />
                <TextArea 
                    className="input-session-context"
                    value={context}
                    onChange={(e) => setContext(e.target.value)}
                    placeholder="Nhập đoạn thông tin bạn muốn đặt câu hỏi. Đoạn thông tin dài tối đa 4000 ký tự"
                    rows={20}
                    disabled={isLoading}
                />
            </Modal> */}

            <Modal
                title="Tải File PDF"
                open={isAddModalOpen}
                onCancel={handleCloseAddModal}
                footer={[
                    <Button key="close" onClick={handleCloseAddModal}>
                        Hủy
                    </Button>,
                    <Button type="primary" onClick={handleAddFiles}>
                        Thêm vào kho lưu trữ
                    </Button>
                ]}
            >
                <Upload
                    accept=".pdf"
                    multiple
                    beforeUpload={handleFiles}
                    onRemove={(file) => {
                        setUploadedFiles((prevFiles) => prevFiles.filter((f) => f.name !== file.name));
                    }}
                    showUploadList={true}
                >
                    <Button icon={<UploadOutlined />}>
                        Chọn File
                    </Button>
                </Upload>
            </Modal>

            <Modal
                title="Kho Lưu Trữ"
                open={isModalOpen}
                onCancel={handleCloseModal}
                footer={[
                    <Button key="close" onClick={handleCloseModal}>
                        Hủy
                    </Button>,
                    <Button type="primary" key="add" onClick={handleOpenAddModal}>
                        Thêm
                    </Button>
                ]}
            >
                {
                    metadata.map((file, index) => (
                        <Tag className="mb-2 pdf-tag" key={index}>{file?.file_name}</Tag>
                    ))
                }
            </Modal>

            {
                isLoading ?
                <div className="spin-container"> 
                    <Spin size="large" />
                </div> 
                : null
            }
        </div>
    )
}
