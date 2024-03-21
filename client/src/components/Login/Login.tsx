import GoogleButton from 'react-google-button'
import css from './Login.module.css'
import { FC } from "react"
import {tminingUrl, urls} from "../../api/routers/tminingRouters";


const Login: FC = () => {
    
    const handleLoginClick = async () => {
        window.location.href = `${tminingUrl}${urls.login}`;
    }
    

    return (
        <div className={css.login_wrapper}>
            <div className={css.login_container}>
                <div className={css.login_title_container}>
                    <h1 className={css.login_title}>
                        Text Mining
                    </h1>
                </div>
                <div className={css.sigin_container}>
                    <GoogleButton onClick={handleLoginClick}/>
                </div>
            </div>
        </div>
    )

}

export { Login }
