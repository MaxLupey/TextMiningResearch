import React, {FC, useContext, useState} from "react"
import {SubmitHandler, useForm} from "react-hook-form"
import { AxiosError } from "axios"
import { joiResolver } from "@hookform/resolvers/joi"
import { AutoComplete } from "../../../elements/AutoСomplete/AutoComplete";
import css from './ValidateForm.module.css'
import { IValidateData } from "../../../interfaces/validate.interface"
import { validateValidator } from "../../../validators/validateValidator"
import { tminginRequest } from "../../../api/requests/tminingRequests"
import { TextField } from "@mui/material"
import { UploadFileInput } from "../../../elements/UplodaFileInput/UploadFileInput"
import { ErrorResponse } from "../../../elements/ErrorResponse/ErrorResponse"
import { SubmitButton } from "../../../elements/SubmitButton/SubmitButton"
import { CSRFTokenContext } from '../../../api/contexts/CSRFTokenContext';

interface IProps {
    setValidateData: React.Dispatch<React.SetStateAction<IValidateData | null>>
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>
    isLoading: boolean
}
const ValidateForm: FC<IProps> = ({setValidateData, setIsLoading, isLoading}) => {
    const {register, control, handleSubmit, formState:{errors, isValid}} = useForm({mode: 'all', resolver: joiResolver(validateValidator)});
    const csrfToken = useContext(CSRFTokenContext);
    const [error, setError] = useState<null | AxiosError>(null)

    const onSubmit: SubmitHandler<any> = async (data) => {
        setIsLoading(true)
        setError(null)
        setValidateData(null)
        const formData = new FormData()
        formData.append("dataset", data.dataset[0])

        let queries = {
            x: data?.x,
            y: data?.y,
            test_size: data?.test_size,
            model: data?.model
        }

        try {
            await tminginRequest.validateModel(queries, formData, csrfToken).then(({data}) => {
                setIsLoading(false)
                setValidateData(data)
            })
        } catch (error: any) {
            setIsLoading(false)
            setError(error)
        }
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className={css.validate_form}>
            <AutoComplete
                name={"model"}
                control={control}
                error={errors.model}
                label={"Model"}
                helperText={errors.model ? String(errors.model.message) : "Select a trained model to validate."}
             />
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.x)}
                helperText={errors.x ? String(errors.x.message) : "Name of the column containing the input text. Default, if the field is empty: text"}
                className={css.input}
                label="X"
                {...register('x')}/>
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.y)}
                helperText={errors.y ? String(errors.y.message) : "Name of the column containing the output labels. Default, if the field is empty: target"}
                className={css.input}
                label="Y"
                {...register('y')}/>
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.test_size)}
                helperText={errors.test_size ? String(errors.test_size.message) : "Size of the test set. The test size must be at least 0.0 and less than 1.0. Default, if the field is empty: 0.2"}
                className={css.input}
                label="Test size"
                {...register('test_size')}/>
            <UploadFileInput fileName={"dataset"} register={register} registerAs={"dataset"} fileError={errors.dataset}/>
            <ErrorResponse error={error}/>
            <SubmitButton isValid={isValid} isLoading={isLoading}/>
        </form>
    )
}

export { ValidateForm }