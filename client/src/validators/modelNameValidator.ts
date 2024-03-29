import Joi from "joi";

const modelNameValidator = Joi.object({
    modelName: Joi.string()
        .regex(/^\w+$/)
        .messages({
            'string.pattern.base': 'Model name contains invalid characters. Only alphanumeric characters and underscores are allowed.'
        }),
});

export { modelNameValidator };