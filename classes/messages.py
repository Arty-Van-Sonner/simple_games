import global_variables as gv

class Messages:
    '''
    
    '''
    __id = None
    __message_storage = None
    __show = None
    __show_right_now = None
    __showed = None
    __title = None
    __content = None
    __is_error = None
    __main_options = None
    __other_options = None
    __tuple_options = None
    __string_for_input = None
    __axis = None
    __answer = None
    __group = None
    __status = None
    __error_code = None
    __type = None
    def __init__(self, message_storage, title, content, show, show_right_now = False, axis = 'row', dict_of_options = None, is_error = False, group = None, status = None, error_code = None, _type = None) -> None:
        self.__is_error = is_error
        self.__message_storage = message_storage
        self.__title = title
        self.__content = [content]
        self.__showed = False
        self.__show = show
        # if show:
        #     print(content)
        self.__show_right_now = show_right_now
        self.__axis = axis
        self.__group = group
        if self.__is_error:
            self.__status = status
            self.__error_code = error_code
            self.__type = _type
        else:
            if not dict_of_options is None:
                key_list = []
                key_list.append(('main_options', list))
                key_list.append(('other_options', list))
                key_list.append(('tuple_options', list))
                key_list.append(('string_for_input', str))
                list_of_error = []
                language = gv.interface.current_language
                for key_tuple in key_list:
                    key = key_tuple[0]
                    value = dict_of_options[key]
                    if type(value) == key_tuple[1]:
                        getattr(self, f'__{key}', value)
                    else:
                        list_of_error.append() 
                if len(list_of_error) > 0:
                    for error in list_of_error:
                        pass
                    text = 'error' 
                    group = 'error'
                    status = 3
                    error_code = '124324'

    def _get_id(self, list_of_key):
        #max_key = max(list_of_key)
        max_key = self.__message_storage.max_key
        self.__id = max_key + 1
        return self.__id

    def _check_and_show_right_now(self):
        if self.__show_right_now and not self.__showed:
            self.__showed = True

    def output(self):
        gv.interface.output_message(self)
        self.__showed = True
        self.__show = False
        self.__show_right_now = False       

    @property
    def is_show_right_now(self):
        return self.__show_right_now

    @property
    def is_show(self):
        return self.__show

    @property
    def showed(self):
        return self.__showed

    @property
    def message_id(self):
        return self.__id

    @property
    def is_error(self):
        return self.__is_error

    @property
    def group(self):
        return self.__group

    @property
    def title(self):
        return self.__title

    @property
    def content(self):
        return self.__content

    # @showed.getter
    # def showed(self, showed):
    #     if not type(showed) is bool:
    #         gv.interface.add_and_raise_error(text, group, status, error_code, ValueError, True, True) #NFC
    #     if showed:
    #         self.__show = False
    #         self.__show_right_now = False
    #     self.showed = showed

    @staticmethod
    def __short_name__():
        return 'Me'