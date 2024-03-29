import { AxiosError } from "axios"
import { FC } from "react"

import css from './ErrorResponse.module.css'

interface IProps {
    error: AxiosError | null
}

const ErrorResponse: FC<IProps> = ({error}) => {    
    let existError = ""

    if(error?.response?.data) {
        existError = Object.values(error.response.data)[0]
    } else if(error?.message) {
        existError = error.message
    }
    
    
    return (
        <div className={css.error}>
           {existError || ""}
        </div>
    )
}

export { ErrorResponse }