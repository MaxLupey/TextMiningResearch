import { FC } from "react";

import css from './Logo.module.css'

const Logo: FC = () => {

   return (
    <div className={css.logo_container}>
        <h1 className={css.logo_title}>Text Mining</h1>
    </div>
   ) 
}

export { Logo }