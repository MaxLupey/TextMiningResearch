import React, {useEffect, useState} from 'react';
import { Avatar, Menu, MenuItem } from '@mui/material';
import { useAuth } from '../../api/contexts/AuthContext';
import {Link} from "react-router-dom";
import { tminginRequest } from '../../api/requests/tminingRequests';

const AvatarComponent = () => {
    const [avatarEl, setAvatarEl] = useState<HTMLElement | null>(null);
    const { isLoggedIn, userData } = useAuth();
    const [avatarStatus, setAvatarStatus] = useState<string>('Not authorized');
    const [avatarSrc, setAvatarSrc] = useState<string>('/static/images/default_avatar.png');

    useEffect(() => {
        if (userData) {
            setAvatarSrc(userData?.avatarUrl);
            setAvatarStatus(`${userData?.firstName} ${userData?.lastName}`);
        }
    }, [userData]);

    const handleClick = (event: React.MouseEvent<HTMLElement>) => {
        setAvatarEl(event.currentTarget as HTMLElement);
    };
    const handleClose = () => {
        setAvatarEl(null);
    };

    const handleLogout = async () => {
    document.cookie = 'user_id=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';

    // Send a request to the server to logout
    try {
        const response = await tminginRequest.logout();
        if (response.status !== 200) {
            throw new Error('Logout request failed');
        }
    } catch (error) {
        console.error('Failed to logout:', error);
    }

    window.location.href = window.location.origin;
};

    return (
    <div>
        <Avatar
            alt={avatarStatus}
            src={avatarSrc}
            onClick={handleClick}
        />
        <Menu
            id="simple-menu"
            anchorEl={avatarEl}
            keepMounted
            open={Boolean(avatarEl)}
            onClose={handleClose}
        >
            {isLoggedIn ? [
            <MenuItem key="models" component={Link} to="/models">My models</MenuItem>,
            <MenuItem key="logout" onClick={handleLogout}>Logout</MenuItem>
        ] : (
                <MenuItem key="login" component={Link} to="/login">Login</MenuItem>
                // <MenuItem onClick={handleLogin}>Login</MenuItem>
            )}
        </Menu>
    </div>
)};

export { AvatarComponent };