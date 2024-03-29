import { FC, useState } from "react"

import css from './Predict.module.css'
import { DeviderSection } from "../../elements/DividerSections/DeviderSections";
import { PredictForm } from "./PredictForm/PredictForm";
import { IPredictData } from "../../interfaces/predict.interface";

const Predict: FC = () => {
    
    const [predictData, setPredictData] = useState<IPredictData>()
    const [isLoading, setIsLoading] = useState<boolean>(false)

    return (
       <>
            <section id='predicaton' style={{width: "100%"}}>
                <h1 className={css.predict_title}>Predict</h1>
                <div className={css.predict_description}>
                    <p>
                        Predict the model using the provided dataset.
                    </p>
                </div>
                <div className={css.predict_contents_container}>
                    <PredictForm setPredictData={setPredictData} setIsLoading={setIsLoading} isLoading={isLoading}/>
                    <div className={css.predict_response_wrapper}>
                        <h1 className={css.predict_subtitle}>Response: {isLoading ? "Loading..." : ""}</h1>
                        { predictData ?
                            <ul className={css.predict_response}>
                                <li className={css.predict_item_response}>Prediction: {predictData.prediction ? predictData.prediction.replace(/'+/g, '') : "Not defined"}</li>
                                {/*<li className={css.predict_item_response}>Text: {PredictData.text ? PredictData.text : "Not defined"}</li> */}
                            </ul>  
                        : ""}
                    </div>
                </div>
        </section>
        <DeviderSection/>
       </>
    )
}

export { Predict }