import { FC } from "react"
import { useNavigate, useLocation } from "react-router-dom";
import { FiArrowLeft } from "react-icons/fi";
import css from './Header.module.css'
import { Logo } from "../../elements/Logo/Logo"
import { AvatarComponent } from "../../elements/Avatar/Avatar"

const Header: FC = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const BackButton: FC = () => {
        return (
            location.pathname !== '/' ?
            <FiArrowLeft className={css.backButton} onClick={() => navigate('/')} size={30} /> : null
        )
    }

    return (
        <div className={css.header_wrapper}>
            <div className={css.limit_container}>
                <div className={css.navigation}><BackButton /> <Logo/></div>
                <AvatarComponent/>
            </div>
        </div>
    )
}

export { Header }