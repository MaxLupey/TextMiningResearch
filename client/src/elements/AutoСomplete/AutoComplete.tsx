import { Autocomplete, TextField } from "@mui/material";
import { FC } from "react"
import { Controller} from "react-hook-form";
import { useEffect, useState } from "react";
import {tminginRequest} from "../../api/requests/tminingRequests";
import {IProps, ModelOption} from "../../interfaces/auto.complete.interface"

const AutoComplete: FC<IProps> = ({name, label, control, error, helperText}) => {
    const [models, setModels] = useState<ModelOption[]>([]);

    const requestModels = async () => {
    tminginRequest.getModelList()
        .then(response => {
            setModels(response.data.models.map((model: any) => ({name: model.name, uuid: model.uuid, shared: model.shared})));
        })
        .catch(error => {
            console.error(error);
        });
}

    useEffect(() => {
        requestModels()
    }, []);

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
                              ? models.find((option) => {
                                  return value === option.uuid;
                                }) ?? null
                              : null
                          }
                        options={models}
                        getOptionLabel={(option: ModelOption) => option.name}
                        groupBy={(option) => option.shared === 1 ? 'Shared' : 'Unshared'}
                        renderInput={(params) => (
                          <TextField error={Boolean(error)} helperText={error ? String(error.message) : helperText}  {...params} label={label} inputRef={ref}/>
                        )}
                        onChange={(_, data) => onChange(data?.uuid)}
                        onOpen={requestModels}
                    />
                )
            }}
        />
    )
}

export { AutoComplete }