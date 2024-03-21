import { AxiosResponse } from "axios"
import { axiosService } from "../../utils/axiosService"
import { urls } from "../routers/tminingRouters"
import { ITrainData } from "../../interfaces/train.interface"

interface IBaseQueries {
    name: string,
    x: string,
    y: string,
    save_to: string,
    model: EModel,
    vectorizer: EVectorizer,
    kfold: number,
    test_size: number,
    text: string
}

interface ITrainQuery extends Omit<IBaseQueries, 'text'> {}


interface IValidateQuery extends Pick<IBaseQueries, "x" | "y" | "test_size"> {
    model: string
}

interface IPredictQuery extends Pick<IBaseQueries, 'text'>{
    model: string
}

interface IVisualizeQuery extends Pick<IBaseQueries, 'text'>{
    model: string
}




enum EVectorizer {
    CountVectorizer = "CountVectorizer",
    TfidfVectorizer = "TfidfVectorizer",
    HashingVectorizer = "HashingVectorizer"
}

enum EModel {
    SVC = "SVC",
    SVR = 'SVR',
    LogisticRegression = "LogisticRegression"
}




export const tminginRequest = {
    trainModel: (queries: ITrainQuery, formData: FormData): Promise<AxiosResponse<ITrainData>> => axiosService.post(urls.train, formData, { params: queries, withCredentials: true }),
    validateModel: (queries: IValidateQuery, formData: FormData) => axiosService.post(urls.validate, formData, { params: queries, withCredentials: true  }),
    predictModel: (queries: IPredictQuery) => axiosService.get(urls.predict, { params: queries, withCredentials: true  }),
    visualizeModel: (queries: IVisualizeQuery) => axiosService.get(urls.visualize, { params: queries, withCredentials: true  }),
    downloadModel: (model_name: string) => axiosService.get(urls.download(model_name)),
    login: (): Promise<AxiosResponse<{redirect_url: string}>> => axiosService.get(urls.login),
    logout: () => axiosService.get(urls.logout, {withCredentials: true}),
    getModelList: () => axiosService.get(urls.model_list, {withCredentials: true}),
    getUserModels: () => axiosService.get(urls.user_models, {withCredentials: true}),
    editModel: (queries: { shared: boolean; new_model_name: string; model_uuid: string }, formData: FormData) => axiosService.put(urls.edit_model, formData, { params: queries, withCredentials: true }),
    uploadModel: (queries: { shared: boolean; model_name: string }, formData: FormData) => axiosService.post(urls.upload_model, formData, { params: queries, withCredentials: true }),
    deleteModel: (model_name: string) => axiosService.delete(urls.delete_model, { params: {model_uuid: model_name}, withCredentials: true }),
    profileInfo: () => axiosService.get(urls.profile_info, {withCredentials: true})
}