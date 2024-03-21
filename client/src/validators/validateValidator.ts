import Joi from "joi";



const validateValidator = Joi.object({
    x: Joi.string().max(100).empty('').messages({
        'string.pattern.base': 'x must have max 100 letters'
    }),
    y: Joi.string().max(100).empty('').messages({
        'string.pattern.base': 'y must have max 100 letters'
    }),
    test_size: Joi.number().max(1).empty('').custom((value, helper) => {
        if (value <= 0) {
            return helper.message({ custom: '"test_size" must be greater than 0' })
        }
  
        return value;
    }),
    model: Joi.string().required().empty('').messages({
        'string.pattern.base': 'model is required'
    }),
    dataset: Joi.custom((value, helper) => {
        if (value.length === 0) {
            return helper.message({ custom: 'dataset is required' });
        }

        const dataset = value[0];
    
        if (dataset?.type !== "text/csv") {
            return helper.message({ custom: 'file must have the text/csv extension' });
        }
    
        return value;
    }),
    // model_file: Joi.any()
})


export {
    validateValidator
}

