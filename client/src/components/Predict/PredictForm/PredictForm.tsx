import {FC, useEffect, useState} from "react";
import {FieldError, SubmitHandler, useForm} from "react-hook-form";
import { joiResolver } from "@hookform/resolvers/joi";
import { TextField} from "@mui/material";

import css from './PredictForm.module.css'
import { predictValidator } from "../../../validators/predictValidator";
import { tminginRequest } from "../../../api/requests/tminingRequests";
import { ErrorResponse } from "../../../elements/ErrorResponse/ErrorResponse";
import { AxiosError } from "axios";
import { SubmitButton } from "../../../elements/SubmitButton/SubmitButton";
import { IPredictData } from "../../../interfaces/predict.interface";
import { AutoComplete } from "../../../elements/AutoСomplete/AutoComplete";

interface IProps {
    setPredictData: React.Dispatch<React.SetStateAction<IPredictData | null>>
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>
    isLoading: boolean
}

const PredictForm: FC<IProps> = ({setPredictData, setIsLoading, isLoading}) => {
    const {register, control, handleSubmit, formState:{errors, isValid}} = useForm({mode: 'all', resolver: joiResolver(predictValidator)});

    const [error, setError] = useState<null | AxiosError>(null)
    const onSubmit: SubmitHandler<any> = async (data) => {
        setIsLoading(true)
        setError(null)
        setPredictData(null)
        let queries = {
            model : data.model, // pass the uuid instead of the name
            text : data.text,
        }
        try {
            await tminginRequest.predictModel(queries).then(({data}) => {
                setIsLoading(false)
                setPredictData(data)
            })
        } catch (error: any) {
            setIsLoading(false)
            setError(error)
        }
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className={css.predict_form}>
            <AutoComplete
                name={"model"}
                control={control}
                error={errors.model}
                label={"Model"}
                helperText={errors.model ? String(errors.model.message) : "Select a trained model to make predictions."}
             />
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.text)}
                helperText={errors.text ? String(errors.text.message) : "Enter the text you want to predict."}
                className={css.input}
                label="Text"
                {...register('text')}/>
            <ErrorResponse error={error}/>
            <SubmitButton isValid={isValid} isLoading={isLoading}/>
        </form>
    )
}

export { PredictForm }