import { FC, useState } from "react";

import css from './Train.module.css'
import { TrainForm } from "./TrainForm/TrainForm";
import { DeviderSection } from "../../elements/DividerSections/DeviderSections";
import { ITrainData } from "../../interfaces/train.interface";
import { DownloadModel } from "../../elements/DownloadModel/DownloadModel";

const Train: FC = () => {

    const [trainData, setTrainData] = useState<null | ITrainData>(null)
    const [isLoading, setIsLoading] = useState<boolean>(false)

    return (
        <>
            <section id="training">
                <h1 className={css.train_title}>Train</h1>
                <div className={css.train_description}>
                    <p>
                        Train the model using uploaded user's dataset.
                    </p>
                </div>
                <div className={css.train_contents_container}>
                    <TrainForm setTrainData={setTrainData} setIsLoading={setIsLoading} isLoading={isLoading}/>
                    <div className={css.train_response_wrapper}>
                        <h1 className={css.train_subtitle}>Response: {isLoading ? "Loading..." : ""}</h1>
                        { trainData ? 
                            <ul className={css.train_response}>
                                <li className={css.train_item_response}>Accuracy: {trainData.accuracy ? trainData.accuracy : "Not defined"}</li>
                                <li className={css.train_item_response}>F1: {trainData.f1 ? trainData.f1 : "Not defined"}</li> 
                                <li className={css.train_item_response}>Download model: <DownloadModel url={trainData.link}/></li>
                            </ul>  
                        : ""}
                    </div>
                </div>
            </section>
            <DeviderSection/>
        </>
    )
}

export { Train }
