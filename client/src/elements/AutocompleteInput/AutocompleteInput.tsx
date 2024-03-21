import { Autocomplete, TextField } from "@mui/material";
import { FC } from "react"
import { Control, Controller, FieldError, FieldErrorsImpl, Merge } from "react-hook-form";


interface IProps {
    name: string
    label: string
    control: Control
    error: FieldError | Merge<FieldError, FieldErrorsImpl<any>> | undefined
    helperText: string
    autocomplete: "vectorizers" | "models"
}

const AutocompleteInput: FC<IProps> = ({name, label, control, error, helperText, autocomplete}) => {
    return (
        <Controller
                control={control}
                name={name}
                render={({ field }) => {
                    const { onChange, value, ref } = field; 
                    return (
                        <Autocomplete
                        sx={{marginBottom: "20px", width: "100%"}} 
                        value={
                            value
                              ? listAutocompletes[autocomplete].find((option) => {
                                  return value === option;
                                }) ?? null
                              : null
                          }
                        options={listAutocompletes[autocomplete]}
                        getOptionLabel={(option) => option}
                        renderInput={(params) => (
                          <TextField error={Boolean(error)} helperText={error ? String(error.message) : helperText}  {...params} label={label} inputRef={ref}/>
                        )}
                        onChange={(_, data) => onChange(data)}/>
                    )
                }}
            />
    )
}

export { AutocompleteInput }

const listAutocompletes = {
    vectorizers: [
        "TfidfVectorizer", 
        "CountVectorizer",   
        "HashingVectorizer"
    ],
    models: [
        "SVC",
        "SVR",
        "LogisticRegression",
    ]
}


