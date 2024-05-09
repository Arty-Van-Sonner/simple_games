import global_variables as gv

class MessageStorage:
    '''

    '''
    __length = 0
    __main_storage = {}
    __list_of_error_id = []
    __list_of_message_for_show_id = []
    __list_of_show_right_now_message_id = []
    __list_of_showed_id = []
    __list_of_showed_error_id = []
    __max_key = None
    def __init__(self) -> None:
        self.__main_storage = {}
        self.__list_of_error_id = []
        self.__list_of_message_for_show_id = []
        self.__list_of_show_right_now_message_id = []
        self.__list_of_showed_id = []
        self.__list_of_showed_error_id = []
        self.__max_key = -1

    def add_message(self, message):
        _id = self.__add_message(message)
        self.__list_of_message_for_show_id.append(_id)
        return _id

    def add_error(self, error):
        _id = self.__add_message(error)
        self.__list_of_error_id.append(_id)
        if error.is_show:
            self.__list_of_message_for_show_id.append(_id)
        return _id

    def __add_message(self, message):
        from messages import Messages
        if not type(message) is Messages:
            gv.interface.add_and_raise_error(**gv.interface.get_standard_dict_of_error(MessageStorage, '__add_message', 'error_when_adding_message__message_is_not_correct_type', '01', 1, True, True))
        _id = message._get_id(self.__main_storage.keys())
        self.__main_storage.update({_id: message})
        if message.is_show_right_now:
            self.__list_of_show_right_now_message_id.append(_id)
        self.__max_key = _id
        return _id

    def get_list_of_errors_by_group(self, group):
        return self._get_list_of_any_message_by_group(group, self.__list_of_error_id)

    def get_list_of_message_by_group(self, group):
        return self._get_list_of_any_message_by_group(group, self.__list_of_message_for_show_id)

    def _get_list_of_any_message_by_group(self, group, list_of_id):
        list_of_messages = []
        for message_id in list_of_id:
            message = self.__main_storage[message_id]
            if message.group == group:
                list_of_messages.append(message)
        return list_of_messages

    def get_list_of_errors_for_show_all(self, for_show = False) -> list:
        return_list = self._get_list_of_all_message_for_show(self.__list_of_error_id)
        print(return_list)
        if for_show:
            for _id in return_list:
                self.__list_of_error_id.remove(_id)
                self.__list_of_showed_id.append(_id)
        return return_list

    def get_list_of_messages_for_show_all(self, for_show = False) -> list:
        return_list = self._get_list_of_all_message_for_show(self.__list_of_message_for_show_id)
        if for_show:
            for message in return_list:
                self.__list_of_message_for_show_id.remove(message.message_id)
                self.__list_of_showed_error_id.append(message.message_id)
        return return_list

    def _get_list_of_all_message_for_show(self, list_of_id) -> list:
        list_of_messages = []
        for message_id in list_of_id:
            message = self.__main_storage[message_id]
            if message.is_show:
                list_of_messages.append(message)
        return list_of_messages

    def get_message_by_id(self, id):
        return self.__main_storage.get(id)

    def message_is_showed(self, message):
        message_id = message.message_id
        if message.is_error:
            self.__list_of_error_id.remove(message_id)
            self.__list_of_showed_error_id.append(message_id)
        else:
            self.__list_of_message_for_show_id.remove(message_id)
            self.__list_of_showed_id.append(message)

    def show_all(self):
        from console import Console
        list_of_showing_messages = self.get_list_of_messages_for_show_all(True)
        # list_of_showing_messages.extend(self.get_list_of_errors_for_show_all(True))
        for message in list_of_showing_messages:
            message.output()
        # if type(gv.interface.current_environment) == Console and len(list_of_showing_messages) > 0:
        #     print()

    @property
    def max_key(self):
        return self.__max_key

    def __len__(self):
        return self.__length

    @staticmethod
    def __short_name__():
        return 'MS'