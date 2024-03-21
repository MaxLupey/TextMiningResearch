import { FC } from 'react';
import "@fontsource/inter";
import { Route, Routes } from 'react-router-dom';
import { MainLayout } from './layouts/MainLayout';
import { AuthProvider } from './api/contexts/AuthContext';
import { LoginPage } from './pages/LoginPage/LoginPage/LoginPage';
import css from './App.module.css'
import { MainSectionPage } from './pages/LoginPage/MainSectionPage/MainSectionPage';
import {ModelsPage} from "./pages/ModelsPage/ModelsPage";


const App:FC = () => {
  return (
    <div className={css.general_container}>
        <AuthProvider>
            <Routes>
            <Route path={'/'} element={<MainLayout/>}>
                <Route path={'/models'} element={<ModelsPage/>}/>
                <Route index element={<MainSectionPage/>}/>
            </Route>
            <Route path={'/login'} element={<LoginPage/>}/>
            </Routes>
        </AuthProvider>
    </div>
  )
}

export { App }