import {FC, useState} from "react";
import css from './Visualize.module.css'
import {VisualizeForm} from "./VisualizeForm/VisualizeForm";
import {DeviderSection} from "../../elements/DividerSections/DeviderSections";


const Visualize: FC = () => {
    const [visualizeData, setVisualizeData] = useState<null | any>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [outputFormat, setOutputFormat] = useState<boolean>(false);
    return (
        <>
            <section id='visualization' style={{width: "100%"}}>
                <h1 className={css.visualize_title}>Visualize</h1>
                <div className={css.visualize_description}>
                    <p>
                        Generate an HTML visualization of model predictions for a given text input.
                    </p>
                </div>
                <div className={css.visualize_contents_container}>
                    <VisualizeForm
                        setVisualizeData={setVisualizeData}
                        setIsLoading={setIsLoading}
                        isLoading={isLoading}
                        setOutputFormat={setOutputFormat}
                    />
                    <div className={css.visualize_response_wrapper}>
                        <h1 className={css.visualize_response_subtitle}>Response: {isLoading ? "Loading..." : ""}</h1>
                        {visualizeData ?
                            (outputFormat ? <div dangerouslySetInnerHTML={{__html: visualizeData}}></div> : <div>
                                    <img src={`data:image/png;base64,${visualizeData}`} alt="visualization"/>
                                </div>
                            )
                            : ""}
                    </div>
                </div>
            </section>
            <DeviderSection/>
        </>
    )
}

export {Visualize}