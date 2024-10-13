import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';

const Appointments = () => {
    const [appointments, setAppointments] = useState([]);

    useEffect(() => {
        const fetchAppointments = async () => {
            const response = await axiosInstance.get('appointments/');
            setAppointments(response.data);
        };
        fetchAppointments();
    }, []);

    return (
        <div className="container">
            <h1>Appointments</h1>
            <ul>
                {appointments.map((appointment) => (
                    <li key={appointment.id}>
                        {appointment.patient.username} with {appointment.counselor.username} on {appointment.appointment_date}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Appointments;
