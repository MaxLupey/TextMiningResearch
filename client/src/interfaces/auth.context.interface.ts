import {createContext, ReactNode} from "react";

export interface AuthContextProps {
    isLoggedIn: boolean;
    userData: UserData | null;
    loading: boolean;
}

export interface UserData {
    firstName: string;
    lastName: string;
    avatarUrl: string;
}

export const AuthContext = createContext<AuthContextProps>({
    isLoggedIn: false,
    userData: null,
    loading: false,
});

export interface AuthProviderProps {
    children: ReactNode;
}