const tminingUrl = "http://localhost:5000";
const model = "/model";

const urls = {
    train: `${model}/train`,
    validate: `${model}/validate`,
    predict: `${model}/predict`,
    visualize: `${model}/visualize`,
    download: (model_name: string) => `${model}/download/${model_name}`,
    login: `/login`,
    logout: `/logout`,
    model_list: `${model}/list`,
    user_models: `${model}/list/user`,
    update_model: `${model}/update`,
    edit_model: `${model}/edit`,
    upload_model: `${model}/upload`,
    delete_model: `${model}/delete`,
    profile_info: `/profile_info`,
    csrf_token: `/csrf_token`
}

export {
    tminingUrl,
    urls
}