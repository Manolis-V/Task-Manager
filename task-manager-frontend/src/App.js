// import logo from './logo.svg';
import './App.css';
import TaskManagement from './pages/TaskManagement';
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignUpPage from "./pages/SignUpPage";


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignUpPage />} />
        <Route path="/manage-tasks" element={<TaskManagement />} />
      </Routes>
    </Router>
  );
}

export default App;