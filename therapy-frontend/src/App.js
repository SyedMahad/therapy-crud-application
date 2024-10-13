import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './styles.css';  // Importing the global CSS file
import Login from './components/Login';
import SignUp from './components/SignUp'; // Import SignUp component
import Patients from './components/Patients';
import Appointments from './components/Appointments';
import Landing from './components/Landing';

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/patients" element={<Patients />} />
                <Route path="/appointments" element={<Appointments />} />
            </Routes>
        </Router>
    );
};

export default App;
