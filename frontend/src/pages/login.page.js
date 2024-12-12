import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../assets/css/LoginPage.css";
import { useAuth } from "../context/authentication.context";
import UserAPI from "../API/user";
import { useLocation } from "react-router-dom";

const LoginPage = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [username, setUsername] = useState(null);
  const [password, setPassword] = useState(null);
  const [message, setMessage] = useState(""); // State để lưu thông báo
  const [isSuccess, setIsSuccess] = useState(false); // State để xác định loại thông báo

  const location = useLocation();
  const { message2 } = location.state || {}; // Lấy thông báo từ state

  useEffect(() => {
    if (message2) {
      const timeout = setTimeout(() => {
        navigate("/login", { replace: true }); // Reset message2 sau 2 giây
      }, 2000);
      return () => clearTimeout(timeout); // Dọn dẹp timeout
    }
  }, [message2, navigate]);

  const handleLogin = () => {
    console.log("Username:", username);
    console.log("Password:", password);

    UserAPI.login(username, password)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          login(data.data.user_id, data.data.user_name);
          setMessage(data.message); // Hiển thị thông báo thành công
          setIsSuccess(true);

          // Sau 1,5 giây chuyển hướng đến /chat
          setTimeout(() => {
            setMessage(""); // Ẩn thông báo
            navigate("/chat");
          }, 1500);
        } else {
          setMessage(data.message); 
          setTimeout(() => {
            setMessage(""); 
          }, 3000);
          setIsSuccess(false);
        }
      })
      .catch((e) => {
        setMessage("Lỗi đăng nhập: " + e.message);
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
          <button className="btn white-btn" id="loginBtn">
            Đăng nhập
          </button>
          <button
            className="btn"
            id="registerBtn"
            onClick={() => navigate("/signup")}
          >
            Đăng ký
          </button>
        </div>
      </nav>

      <div className="form-box">
        <div className="login-container" id="login">
          <div className="top">
            <span>
              Bạn chưa có tài khoản?{" "}
              <a href="#" onClick={() => navigate("/signup")}>
                Đăng ký
              </a>
            </span>
            <header>ĐĂNG NHẬP</header>
          </div>
          <div className="input-box">
            <input
              type="text"
              className="input-field"
              placeholder="Tên đăng nhập"
              onChange={(e) => setUsername(e.target.value)}
            />
            <i className="bx bx-user"></i>
          </div>
          <div className="input-box">
            <input
              type="password"
              className="input-field"
              placeholder="Mật khẩu"
              onChange={(e) => setPassword(e.target.value)}
            />
            <i className="bx bx-lock-alt"></i>
          </div>
          <div className="input-box">
            <input
              type="submit"
              className="submit"
              value="Đăng nhập"
              onClick={handleLogin}
            />
          </div>
          {/* <div className="two-col">
            <div className="one">
              <input type="checkbox" id="login-check" />
              <label htmlFor="login-check"> Ghi nhớ đăng nhập</label>
            </div>
          </div> */}
        </div>
      </div>

      {message && (
        <div className={`message-box ${isSuccess ? "success" : "error"}`}>
          {message}
        </div>
      )}

      {message2 && (
        <div className={`message-box2 ${isSuccess ? "success" : "error"}`}>
          {message2} {/* Hiển thị thông báo đăng nhập */}
        </div>
      )}


    </div>
  );
};

export default LoginPage;
