import {FC, useState} from "react";
import css from './Visualize.module.css'
import {VisualizeForm} from "./VisualizeForm/VisualizeForm";
import {DeviderSection} from "../../elements/DividerSections/DeviderSections";


const Visualize: FC = () => {
    const [visualizeData, setVisualizeData] = useState<null | HTMLElement>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [outputFormat, setOutputFormat] = useState<boolean>(false);

    const htmlElementToString = (element: HTMLElement | null): string => {
      return element ? element.outerHTML : '';
    };

    function renderVisualizeData() {
        if (outputFormat) {
            return <div dangerouslySetInnerHTML={{__html: htmlElementToString(visualizeData) || ''}}></div>;
        } else {
            return <div>
                <img src={`data:image/png;base64,${visualizeData}`} alt="visualization"/>
            </div>;
        }
    }
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
                            (renderVisualizeData())
                            : ""}
                    </div>
                </div>
            </section>
            <DeviderSection/>
        </>
    )
}

export {Visualize}