import { FC } from "react"

import css from './DownloadModel.module.css'

interface IProps {
    url: string
}


const DownloadModel: FC<IProps> = ({url}) => {

    return (
        <a href={url}>
            <button className={css.download_button}>click on</button>
        </a>
    )

    
}

export { DownloadModel }