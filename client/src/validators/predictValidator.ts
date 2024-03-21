import Joi from "joi";

const predictValidator = Joi.object({
    model: Joi.string().required().empty('').messages({
        'string.pattern.base': 'model is required'
    }),
    text: Joi.string().required().empty('').messages({
        'string.pattern.base': 'text is required'
    })
})

export {
    predictValidator
}