import {Control, FieldError, FieldErrorsImpl, Merge} from "react-hook-form";

export interface ModelOption {
    name: string;
    uuid: string;
    shared: number;
}

export interface IProps {
    name: string
    label: string
    control: Control
    error: FieldError | Merge<FieldError, FieldErrorsImpl<any>> | undefined
    helperText: string
}