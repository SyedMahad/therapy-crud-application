import React, { useState } from 'react';
import axiosInstanceWithoutAuth from '../axiosInstance';
import { useNavigate } from 'react-router-dom';

const SignUp = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        password2: '',
        user_type: 'patient', // default user type
    });

    const [errors, setErrors] = useState({});
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axiosInstanceWithoutAuth.post('register/', formData);
            console.log('Registration successful:', response.data);
            // Optionally, you can log the user in automatically or redirect to login
            navigate('/login');
        } catch (error) {
            console.error('Registration error:', error.response.data);
            setErrors(error.response.data);
        }
    };

    return (
        <div className="container">
            <h1>Sign Up</h1>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                />
                {errors.username && <p className="error">{errors.username}</p>}
                
                <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                />
                {errors.email && <p className="error">{errors.email}</p>}
                
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                />
                {errors.password && <p className="error">{errors.password}</p>}
                
                <input
                    type="password"
                    name="password2"
                    placeholder="Confirm Password"
                    value={formData.password2}
                    onChange={handleChange}
                    required
                />
                {errors.password2 && <p className="error">{errors.password2}</p>}
                
                <select name="user_type" value={formData.user_type} onChange={handleChange} required>
                    <option value="patient">Patient</option>
                    <option value="counselor">Counselor</option>
                </select>
                {errors.user_type && <p className="error">{errors.user_type}</p>}
                
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default SignUp;
