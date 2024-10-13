import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';

const Patients = () => {
    const [patients, setPatients] = useState([]);

    useEffect(() => {
        const fetchPatients = async () => {
            const response = await axiosInstance.get('patients/');
            setPatients(response.data);
        };
        fetchPatients();
    }, []);

    return (
        <div className="container">
            <h1>Patients</h1>
            <ul>
                {patients.map((patient) => (
                    <li key={patient.id}>
                        {patient.username} - {patient.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Patients;
