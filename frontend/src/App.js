import './App.css';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import PrivateRoute from './utils/privateRoute.util.js'
import { AuthProvider } from './context/authentication.context.js';

import ChatPage from './pages/chat.page.js'
import LoginPage from './pages/login.page.js'
import SignupPage from './pages/signup.page.js'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path='/login' element={ <LoginPage/> } />
          <Route path='/signup' element={ <SignupPage/> } />
          <Route 
            path='/chat'
            element={
              <PrivateRoute>
                <ChatPage />
              </PrivateRoute>
            }
          />
          <Route 
            path='/'
            element={
              <PrivateRoute>
                <ChatPage />
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
