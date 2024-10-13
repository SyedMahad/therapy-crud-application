import React, { useState } from 'react';
import axiosInstanceWithoutAuth from '../axiosInstance';

const Login = () => {
    const [errors, setErrors] = useState({});
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axiosInstanceWithoutAuth.post('login/', {
                email,
                password,
            });
            localStorage.setItem('access_token', response.data.access);
        } catch (error) {
            console.error("Error:", error);
            setErrors(error.response.data);
        }
    };

    return (
        <div className="container">
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                {/* Display general errors like non_field_errors */}
                {errors.non_field_errors && (
                    <p className="error">{errors.non_field_errors[0]}</p>
                )}
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
