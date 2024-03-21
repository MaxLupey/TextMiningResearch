import { ChangeEvent, FC, useState } from 'react'

import css from './UploadFileInput.module.css'
import { FieldError, FieldErrorsImpl, FieldValues, Merge, UseFormRegister } from 'react-hook-form'

interface IProps {
    fileName: string
    register: UseFormRegister<FieldValues>
    registerAs: string
    fileError: FieldError | Merge<FieldError, FieldErrorsImpl<any>> | undefined
}


const UploadFileInput: FC<IProps> = (props) => {
    const {fileError, fileName, register, registerAs} = props

    const [selectedFile, setSelectedFile] = useState<File | null>(null)

    const handleFileSelect = (event: ChangeEvent<HTMLInputElement>) => {
        const file =  event.target.files?.[0] || null;

        if (file) {
          setSelectedFile(file);
        }
    };
    
    return (
        <div className={css.file_input_container}>
            <div className={`${css.file_area} ${fileError ? css.file_area_error : ""}`}>
                <input className={css.file_input} onInput={handleFileSelect} type="file" {...register(registerAs)}/>
                <div className={css.file_dummy}>
                    {!fileError && selectedFile && <div className={css.success}>Great, {fileName} is selected</div>}
                    {(fileError || !selectedFile) && <div className={css.default}>Please select {fileName}</div>}
                </div>
            </div>
            { fileError && <div className={css.error_container}>{String(fileError.message)}</div> }
        </div>
    )
}

export { UploadFileInput }