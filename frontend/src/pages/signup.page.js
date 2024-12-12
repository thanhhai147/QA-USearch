import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../assets/css/SignupPage.css";
import UserAPI from "../API/user";

const SignupPage = () => {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState(""); // State để lưu thông báo
  const [isSuccess, setIsSuccess] = useState(false); // State để xác định loại thông báo


  const handleSignup = () => {
    UserAPI.signup(username, password)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          setMessage(data.message1); // Hiển thị thông báo thành công
          setIsSuccess(true);
          setTimeout(() => {
            setMessage("");
            navigate("/login", { state: { message2: data.message2 } }); // Chuyển hướng đến trang đăng nhập
          }, 1000);

        } else {
          setMessage(data.message); 
          setIsSuccess(false);
          setTimeout(() => {
            setMessage(""); 
          }, 3000);
        }
      })
      .catch((e) => {
        setMessage("Lỗi: " + e.message);
        setIsSuccess(false);
      });
  };

  return (
    <div className="wrapper">
      <nav className="nav">
        <div className="nav-logo">
          <p>QA-LLM</p>
        </div>
        <div className="nav-button">
          <button
            className="btn"
            id="loginBtn"
            onClick={() => navigate("/login")}
          >
            Đăng nhập
          </button>
          <button className="btn white-btn" id="registerBtn">
            Đăng ký
          </button>
        </div>
      </nav>

      
      {message && (
        <div className={`message-box ${isSuccess ? "success" : "error"}`}>
          {message}
        </div>
      )}

      <div className="form-box">
        <div className="register-container" id="register">
          <div className="top">
            <span>
              Đã có tài khoản?{" "}
              <a href="#" onClick={() => navigate("/login")}>
                Đăng nhập
              </a>
            </span>
            <header>ĐĂNG KÝ</header>
          </div>
          <div className="input-box">
            <input type="text" 
            className="input-field" 
            placeholder="Tên đăng nhập" 
            value={username}
            onChange={(e) => setUsername(e.target.value)} /////
            />
            <i className="bx bx-envelope"></i>
          </div>
          <div className="input-box">
            <input
              type="password"
              className="input-field"
              placeholder="Mật khẩu"
              value={password}
              onChange={(e) => setPassword(e.target.value)} /////
            />
            <i className="bx bx-lock-alt"></i>
          </div>
          <div className="input-box">
            <input type="submit" 
            className="submit" 
            value="Đăng ký" 
            onClick={handleSignup} /////
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;
