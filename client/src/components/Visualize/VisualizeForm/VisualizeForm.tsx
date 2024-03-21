import { joiResolver } from "@hookform/resolvers/joi";
import {SubmitHandler, useForm} from "react-hook-form";
import { FC, useState } from "react";
import {Switch, TextField} from "@mui/material";
import { AxiosError } from "axios";

import { visualizeVaidator } from "../../../validators/visualizeValidator";
import { tminginRequest } from "../../../api/requests/tminingRequests";
import { ErrorResponse } from "../../../elements/ErrorResponse/ErrorResponse";
import { SubmitButton } from "../../../elements/SubmitButton/SubmitButton";
import css from './VisualizeForm.module.css'
import { AutoComplete } from "../../../elements/AutoСomplete/AutoComplete";
import {tminingUrl, urls} from "../../../api/routers/tminingRouters";

interface IProps {
    setVisualizeData: React.Dispatch<React.SetStateAction<null | HTMLElement>>
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>
    isLoading: boolean
    setOutputFormat: React.Dispatch<React.SetStateAction<boolean>>
}

const VisualizeForm: FC<IProps> = ({setVisualizeData, isLoading, setIsLoading, setOutputFormat}) => {
    const {register, control, handleSubmit, formState:{errors, isValid}} = useForm({mode: 'all', resolver: joiResolver(visualizeVaidator)});
    const [outputFormat, _setOutputFormat] = useState<boolean>(false)
    const [error, setError] = useState<null | AxiosError>(null)
    const [isRedirect, setIsRedirect] = useState<boolean>(false)
    const onSubmit: SubmitHandler<any> = async (data) => {
        setOutputFormat(outputFormat)
        setIsLoading(true)
        setError(null)
        setVisualizeData(null)
        let queries = {
            text: data.text,
            model: data.model,
            output_format: outputFormat ? "html" : "image",
        }

        try {
            if (outputFormat) {
                setIsRedirect(true)
                let params = new URLSearchParams(queries).toString();
                window.location.href = `${tminingUrl}${urls.visualize}?${params}`;
                setIsLoading(false)
            }
            else {
                await tminginRequest.visualizeModel(queries).then(({data}) => {
                    setIsLoading(false)
                    setVisualizeData(data)
                })
            }
        } catch (error: any) {
            setIsLoading(false)
            setError(error)
        }
    }

    return (
        <form onSubmit={handleSubmit(onSubmit)} className={css.visualize_form}>
            <AutoComplete
                name={"model"}
                control={control}
                error={errors.model}
                label={"Model"}
                helperText={errors.model ? String(errors.model.message) : "Select a trained model to visualize predictions."}
             />
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.text)}
                helperText={errors.text ? String(errors.text.message) : "Enter the text you want to visualize predictions for."}
                className={css.input}
                label="Text"
                {...register('text')}/>
            <div style={{ display: 'flex', alignItems: 'center' }}>
                <Switch
                    checked={outputFormat}
                    onChange={() => _setOutputFormat(!outputFormat)}
                    inputProps={{ 'aria-label': 'Output format' }}
                /><label style={{ marginLeft: '10px' }}>Output format: {outputFormat ? "html" : "image"}</label>
            </div>
            <ErrorResponse error={error}/>
            <SubmitButton isValid={isValid} isLoading={isLoading} name={
                isRedirect ? "Loading..." : "Sumbit"
            }/>
        </form>
    )
}

export {VisualizeForm}