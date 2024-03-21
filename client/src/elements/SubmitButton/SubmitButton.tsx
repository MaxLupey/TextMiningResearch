import { FC } from 'react'
import css from './SubmitButton.module.css'

interface IProps {
    isLoading: boolean
    isValid: boolean
    name?: string
}


const SubmitButton: FC<IProps> = ({isLoading, isValid , name = 'Sumbit'}) => {

    return (
        <div className={css.submit_button_container}>
            <button disabled={isLoading || !isValid}  className={css.submit_button}>{name}</button>
        </div>
    )
}

export { SubmitButton }