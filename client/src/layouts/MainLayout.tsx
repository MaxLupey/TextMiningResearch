import { Outlet } from "react-router-dom"
import { FC } from "react"

import { Header } from "../components/Header/Header"
import css from './MainLayout.module.css'

const MainLayout: FC = () => {

    return (
        <>
            <Header/>
            <div className={css.outlet_container}>
                <Outlet/>
            </div>
        </>
    )

}

export { MainLayout }
