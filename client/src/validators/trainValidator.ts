import Joi from "joi";


const trainValidator = Joi.object({
    name: Joi.string().required().max(100).empty('').regex(/^\w+$/).messages({
        'string.pattern.base': 'name must have max 100 letters and must contain only alphanumeric characters and underscores.',
    }),
    x: Joi.string().max(100).empty('').messages({
        'string.pattern.base': 'x must have max 100 letters'
    }),
    y: Joi.string().max(100).empty('').messages({
        'string.pattern.base': 'y must have max 100 letters'
    }),
    kfold: Joi.number().min(0).empty(''),
    test_size: Joi.number().min(0).empty('').custom((value, helper) => {
        if (value >= 1) {
            return helper.message({ custom: '"test_size" must be less than 1' })
        }
  
        return value;
      }),
    vectorizer: Joi.string().empty('').allow(null),
    model: Joi.string().empty('').allow(null),
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
})

export {
    trainValidator
}