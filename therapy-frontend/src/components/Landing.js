import React from 'react';
import { Link } from 'react-router-dom';

const Landing = () => {
    return (
        <div className="container">
            <h1>Welcome to the Therapy App</h1>
            <p>This is a platform for managing appointments between patients and counselors.</p>
            <nav className="nav-links">
                <Link to="/login">Login</Link>
                <Link to="/signup">Sign Up</Link>
            </nav>
        </div>
    );
};

export default Landing;
