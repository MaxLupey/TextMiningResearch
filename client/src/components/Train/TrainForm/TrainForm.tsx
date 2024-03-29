import {FC, useContext, useState} from "react";
import { SubmitHandler, useForm } from "react-hook-form";
import { joiResolver } from "@hookform/resolvers/joi";
import {TextField} from "@mui/material";

import css from './TrainForm.module.css'
import { trainValidator } from "../../../validators/trainValidator";
import { tminginRequest } from "../../../api/requests/tminingRequests";
import { AutocompleteInput } from "../../../elements/AutocompleteInput/AutocompleteInput";
import { ErrorResponse } from "../../../elements/ErrorResponse/ErrorResponse";
import { AxiosError } from "axios";
import { SubmitButton } from "../../../elements/SubmitButton/SubmitButton";
import { UploadFileInput } from "../../../elements/UplodaFileInput/UploadFileInput";
import { ITrainData } from "../../../interfaces/train.interface";
import { CSRFTokenContext } from '../../../api/contexts/CSRFTokenContext';


interface IProps {
    setTrainData: React.Dispatch<React.SetStateAction<ITrainData | null>>
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>
    isLoading: boolean
}


const TrainForm: FC<IProps> = ({setTrainData, setIsLoading, isLoading}) => {
    const {register, control, handleSubmit, formState:{errors, isValid}} = useForm({mode: 'all', resolver: joiResolver(trainValidator)});
    const csrfToken = useContext(CSRFTokenContext);
    const [error, setError] = useState<null | AxiosError>(null)

    const onSubmit: SubmitHandler<any> = async (data) => {
        setIsLoading(true)
        setError(null)
        setTrainData(null)
        const formData = new FormData()
        formData.append("dataset", data?.dataset[0])

        let queries = {
            name: data.name,
            x: data.x,
            y: data.y,
            save_to: data.save_to,
            model: data.model,
            vectorizer: data.vectorizer,
            kfold: data.kfold,
            test_size: data.test_size,
        }
        try {
            await tminginRequest.trainModel(queries, formData, csrfToken).then(({data}) => {
                setIsLoading(false)
                setTrainData(data)
            })
        } catch (error: any) {
            setIsLoading(false)
            setError(error)
        }


    }


    return (
        <form onSubmit={handleSubmit(onSubmit)} className={css.train_form}>
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.name)}
                helperText={errors.name ? String(errors.name.message) : "Enter a name for the future model."}
                className={css.input}
                label="Name"
                {...register('name')}/>
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.x)}
                helperText={errors.x ? String(errors.x.message) : "Enter the name of the column containing the input text. Default, if the field is empty: text"}
                className={css.input}
                label="X"
                {...register('x')}/>
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.y)}
                helperText={errors.y ? String(errors.y.message) : "Enter the name of the column containing the output labels. Default, if the field is empty: target"}
                className={css.input}
                label="Y"
                {...register('y')}/>
            <AutocompleteInput
                name={"vectorizer"}
                label={"Vectorizer"}
                control={control}
                error={errors.vectorizer}
                helperText={"Select the text vectorization. Three approaches are available. CountVectorizer, TfidfVectorizer, and HashingVectorizer. Default vectorizer, if the field is empty: TfidfVectorizer"}
                autocomplete={"vectorizers"}
            />
            <AutocompleteInput
                name={"model"}
                label={"Model"}
                control={control}
                error={errors.model}
                helperText={"Select a training model. Three models are available: SVC, SVR, and LogisticRegression. Default model, if the field is empty: SVC"}
                autocomplete={"models"}
            />
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.kfold)}
                helperText={errors.kfold ? String(errors.kfold.message) : "Enter the number of folds for cross-validation. Default, if the field is empty: 1"}
                className={css.input}
                label="Kfold"
                {...register('kfold')}/>
            <TextField
                sx={{marginBottom: "20px"}}
                error={Boolean(errors.test_size)}
                helperText={errors.test_size ? String(errors.test_size.message) : "Enter the size of the test set. The test size must be at least 0.0 and less than 1.0. Default, if the field is empty: 0"}
                className={css.input}
                label="Test size"
                {...register('test_size')}/>
            <UploadFileInput
                fileName={"dataset"}
                register={register}
                registerAs={"dataset"}
                fileError={errors.dataset}
                />
            <ErrorResponse error={error}/>
            <SubmitButton isValid={isValid} isLoading={isLoading} />
        </form>
    )
}

export { TrainForm }