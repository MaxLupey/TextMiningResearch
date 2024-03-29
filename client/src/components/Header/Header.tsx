import { FC } from "react"
import { useNavigate, useLocation } from "react-router-dom";
import { FiArrowLeft } from "react-icons/fi";
import css from './Header.module.css'
import { Logo } from "../../elements/Logo/Logo"
import { AvatarComponent } from "../../elements/Avatar/Avatar"

interface BackButtonProps {
  navigate: (path: string) => void;
  pathname: string;
}

const BackButton: FC<BackButtonProps> = ({ navigate, pathname }) => {
  return (
    pathname !== '/' ?
    <FiArrowLeft className={css.backButton} onClick={() => navigate('/')} size={30} /> : null
  )
}

const Header: FC = () => {
    const navigate = useNavigate();
    const location = useLocation();

    return (
        <div className={css.header_wrapper}>
            <div className={css.limit_container}>
                <div className={css.navigation}><BackButton navigate={navigate} pathname={location.pathname}/> <Logo/>
                </div>
                <AvatarComponent/>
            </div>
        </div>
    )
}

export {Header}