import { FC, useContext, useEffect } from "react"
import { AuthContext } from '../../api/contexts/AuthContext';
import { Alert, Backdrop, CircularProgress } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { Menu } from "../Menu/Menu"
import css from './MainSection.module.css'
import { Train } from "../Train/Train"
import { Validate } from "../Validate/Validate"
import { Predict } from "../Predict/Predict"
import { Visualize } from "../Visualize/Visualize"


const MainSection: FC = () => {
    const { isLoggedIn, loading } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (!isLoggedIn && !loading) {
            navigate('/login');
        }
        // else {
        //     navigate('/')
        // }
    }, [isLoggedIn, navigate, loading]);

    return (
        <div className={css.main_section_wrapper}>
            <Menu/>
            <div className={css.main_section_items}>
                {isLoggedIn ? (
                    <>
                        <Train/>
                        <Validate/>
                        <Predict/>
                        <Visualize/>
                    </>
                ) : (
                    <Alert severity="error">Please log in first</Alert>
                )}
            </div>
            <Backdrop
                sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1, backgroundColor: 'rgba(0, 0, 0, 1)' }}
                open={loading}
            >
                <CircularProgress color="inherit" />
            </Backdrop>
        </div>
    )
}

export { MainSection }