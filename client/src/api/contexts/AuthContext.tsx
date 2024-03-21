// AuthContext.tsx
import React, { useContext, useEffect, useState } from 'react';
import { fetchUserData } from '../services/apiService';
import {AuthContext, AuthProviderProps, UserData} from '../../interfaces/auth.context.interface'
import {useNavigate} from "react-router-dom";

export const useAuth = () => useContext(AuthContext);
export { AuthContext } from '../../interfaces/auth.context.interface';

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
    const [userData, setUserData] = useState<UserData | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const navigate = useNavigate();

    useEffect(() => {
        setLoading(true);
        fetchUserData()
            .then(data => {
                setIsLoggedIn(true);
                setUserData(data);
                setLoading(false);
            })
            .catch(error => {
                setIsLoggedIn(false);
                console.error(error);
                setLoading(false);
                navigate('/login');
            });
    }, [navigate, loading]);
    return (
        <AuthContext.Provider value={{ isLoggedIn, userData, loading }}>
            {children}
        </AuthContext.Provider>
    );
};