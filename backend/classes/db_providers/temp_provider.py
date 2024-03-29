import builtins


class TempProvider:
    def __init__(self):
        self.data = {}

    def add_user(self, uuid, token, google_payload):
        sub = google_payload['sub']
        if sub in self.data:
            return self.data[sub]
        user = {
            'sub': sub,
            'uuid': uuid,
            'token': token,
            'auth_info': google_payload,
            'models': []
        }
        self.data[sub] = user
        self.__print__(sub, 'User added')
        return user

    def update_user(self, token, google_payload):
        sub = google_payload['sub']
        user = self.data[sub]
        user['token'] = token
        del google_payload['sub']
        user['auth_info'] = google_payload
        self.data[sub] = user
        self.__print__(sub, 'User updated')
        return user

    def remove_user(self, sub):
        del self.data[sub]
        self.__print__(sub, 'User removed')
        return None

    def get_user_by_sub(self, sub):
        return self.data.get(sub)

    def get_user_by_uuid(self, uuid):
        for user in self.data.values():
            if user['uuid'] == uuid:
                return user
        return None

    # add model to user
    # def add_model(self, uuid, model, name=None, shared=False):
    #     if name is None:
    #         name = model
    #     # check if model name already exists
    #     for user in self.data.values():
    #         for model in user['models']:
    #             if model['name'] == name:
    #                 return None
    #     user = self.get_user_by_uuid(uuid)
    #     user['models'].append({'name': name, 'uuid': model, 'shared': shared})
    #     self.data[user['sub']] = user
    #     return user

    def add_model(self, uuid, model, name=None, shared=False):
        sub = self.convert_uuid_to_sub(uuid)
        if name is None or name == '':
            name = model
        else:
            for user in self.data.values():
                for model_user in user['models']:
                    if model_user['name'] == name:
                        return None
        user = self.get_user_by_sub(sub)
        print(user['models'])
        user['models'].append({'name': name, 'uuid': model, 'shared': shared})
        self.data[sub] = user
        self.__print__(sub, f'Model {name} added')
        return user

    def remove_model(self, uuid_user, uuid_model):
        sub = self.convert_uuid_to_sub(uuid_user)
        user = self.get_user_by_uuid(uuid_user)
        name = self.get_model_by_uuid(uuid_user, uuid_model)['name']
        user['models'] = [model for model in user['models'] if model['uuid'] != uuid_model]
        self.data[sub] = user
        self.__print__(sub, f'Model {name} removed')
        return user

    # get all models for user
    def get_models(self, uuid, shared=False):
        sub = self.convert_uuid_to_sub(uuid)
        user = self.data[sub]
        if shared:
            return [model for model in user['models'] if model['shared']]
        return user['models']

    # get model by uuid
    def get_model_by_uuid(self, uuid_user, uuid_model):
        sub = self.convert_uuid_to_sub(uuid_user)
        user = self.data[sub]
        for model in user['models']:
            if model['uuid'] == uuid_model:
                return model
        return None

    # get model by name
    def get_model_by_name(self, uuid_user, name):
        sub = self.convert_uuid_to_sub(uuid_user)
        user = self.data[sub]
        for model in user['models']:
            if model['name'] == name:
                return model
        return None

    # get all shared models for all users
    def get_shared_models(self):
        shared_models = []
        for user in self.data.values():
            for model in user['models']:
                if model['shared']:
                    shared_models.append(model)
        return shared_models

    # bool if model is shared
    def model_is_shared(self, sub, uuid):
        model = self.get_model_by_uuid(sub, uuid)
        return model['shared']

    def convert_uuid_to_sub(self, uuid):
        user = self.get_user_by_uuid(uuid)
        return user['sub']

    def convert_sub_to_uuid(self, sub):
        user = self.get_user_by_sub(sub)
        return user['uuid']

    def __print__(self, sub, message):
        builtins.print(f'{sub}: {message}')

    def edit_model(self, user_uuid, uuid, new_name=None, shared=None):
        sub = self.convert_uuid_to_sub(user_uuid)
        user = self.data[sub]
        for model in user['models']:
            if model['uuid'] == uuid:
                if new_name is not None:
                    model['name'] = new_name
                if shared is not None:
                    model['shared'] = shared
                break
        self.data[sub] = user
        return user
