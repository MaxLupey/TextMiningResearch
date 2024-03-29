// AuthContext.tsx
import React, {useContext, useEffect, useMemo, useState} from 'react';
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
    const providerValue = useMemo(() => ({ isLoggedIn, userData, loading }), [isLoggedIn, userData, loading]);

    useEffect(() => {
        fetchUserData()
            .then(data => {
                if(data) {
                    setIsLoggedIn(true);
                    setUserData(data);
                    setLoading(false);
                }
            })
            .catch(error => {
                if (error.message === 'Request failed with status code 401') {
                    setIsLoggedIn(false);
                    setLoading(false);
                    navigate('/login');
                    return;
                }
                console.error('Failed to fetch user data:', error.message);
            });
    }, [navigate, loading]);
    return (
        <AuthContext.Provider value={providerValue}>
            {children}
        </AuthContext.Provider>
    );
};