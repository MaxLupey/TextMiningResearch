import Joi from "joi";


const visualizeVaidator = Joi.object({
    model: Joi.string().min(1).required().messages({
        'string.pattern.base': 'model is required'
    }),
    text: Joi.string().min(1).required().messages({
        'string.pattern.base': 'model is required'
    }),
})

export {
    visualizeVaidator
}