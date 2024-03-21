import { FC, useState } from "react";

import css from './Validate.module.css'
import { DeviderSection } from "../../elements/DividerSections/DeviderSections";
import { ValidateForm } from "./ValidateForm/ValidateForm";
import { IValidateData } from "../../interfaces/validate.interface";

const Validate: FC = () => {

    const [validateData, setValidateData] = useState<IValidateData | null>(null)
    const [isLoading, setIsLoading] = useState<boolean>(false)

    return (
       <>
            <section id='validation'>
                <h1 className={css.validate_title}>Validate</h1>
                <div className={css.validate_description}>
                    <p>
                        Validate the model using the provided dataset.
                    </p>
                </div>
                <div className={css.validate_contents_container}>
                    <ValidateForm setValidateData={setValidateData} setIsLoading={setIsLoading} isLoading={isLoading}/>
                    <div className={css.validate_response_wrapper}>
                        <h1 className={css.validate_subtitle}>Response: {isLoading ? "Loading..." : ""}</h1>
                        { validateData ? 
                            <ul className={css.validate_response}>
                                <li className={css.validate_item_response}>Accuracy: {validateData.accuracy ? validateData.accuracy : "Not defined"}</li>
                                <li className={css.validate_item_response}>F1: {validateData.f1 ? validateData.f1 : "Not defined"}</li> 
                            </ul>  
                        : ""}
                    </div>
                </div>
        </section>
        <DeviderSection/>
       </>
    )
}

export { Validate }