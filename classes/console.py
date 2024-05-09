class Console:
    '''
    
    '''
    __clear_before_output = False
    __row_separator = ''
    __column_separator = ''
    def __init__(self, clear_before_output, row_separator = '\n\n', column_separator = '    |    '):
        self.set_clear_before_output(clear_before_output)
        self.set_row_separator(row_separator)
        self.set_column_separator(column_separator)

    def set_clear_before_output(self, clear_before_output):
        self.__clear_before_output = clear_before_output

    def set_row_separator(self, row_separator):
        self.__row_separator = row_separator

    def set_column_separator(self, column_separator):
        self.__column_separator = column_separator    

    def output(self, structure_of_output):
        self.__get_ready_to_the_output_strings(self, structure_of_output)
    
    def __get_ready_to_the_output_strings(self, structure_of_output):
        structure_of_input = {}
        for item in structure_of_output:
            if type(item) is str:
                if structure_of_output['item']['name'] == 'message':
                    self.__get_ready_to_the_message()
                else:
                    raise ValueError('Ошибка передаваемого')
    def __get_ready_to_the_message(self):
        pass

    def ask_question_to_user(self, dict_of_data):
        output_string = ''
        if dict_of_data['title'] != '' and not dict_of_data['title'] is None:
            output_string += self.__row_separator + dict_of_data['title']
        output_string += self.__row_separator + self.get_string_for_out_put(dict_of_data['value'], self.get_data_dict_for_proccessing(dict_of_data['row_column'])) 
        print(output_string)
        
    def get_string_for_out_put(self, value, data_dict_for_proccessing):
        if type(value) == list:
            separator = ''
            if data_dict_for_proccessing['row_column'] == 'row':
                data_dict_for_proccessing['separator'] = self.__row_separator
            else:
                data_dict_for_proccessing['separator'] = self.__column_separator
            for element in value:
                if data_dict_for_proccessing['row_column'] == 'column':
                    data_dict_for_proccessing['current_string_index'] = 0
                self.get_string_for_out_put(element, data_dict_for_proccessing) 
            return '\n'.join(data_dict_for_proccessing['list_of_strings']) + self.__row_separator
        elif type(value) == dict:
            hidden = value.get('hidden')
            if hidden is None:
                hidden = False
            if  value['type'] == 'table':
                list_max_size_of_colomns = []
                have_title_of_rows = False
                have_title_of_columns = False
                total_width_of_row_string = 0
                index_title = None
                index_column_titles = None
                title = None
                # if not value['title'] is None:
                #     if len(value['title']) > 0:
                #         data_dict_for_proccessing['list_of_strings'].append('')
                #         index_title = data_dict_for_proccessing['current_string_index']
                #         data_dict_for_proccessing['current_string_index'] += 1
                # if not value['title_of_columns'] is None:
                #     if len(value['title_of_columns']) > 0:
                #         data_dict_for_proccessing['list_of_strings'].append('')
                #         index_column_titles = data_dict_for_proccessing['current_string_index']
                #         data_dict_for_proccessing['current_string_index'] += 1
                if not value['title_of_rows'] is None:
                    if len(value['title_of_rows']) > 0:
                        list_max_size_of_colomns.append(max(map(len, value['title_of_rows'])) + 2)
                        have_title_of_rows = True
                list_of_column_elements = []
                for x in value['value']:
                    index = 0
                    for y in x:
                        if index < len(list_of_column_elements):
                            list_of_column_elements[index].append(y)
                        else:
                            list_of_column_elements.append([y])     
                        index += 1
                if not value['title_of_columns'] is None:
                    if len(value['title_of_columns']) > 0:
                        index = 0
                        if have_title_of_rows:
                            index += 1
                        for i in range(index, len(list_of_column_elements)):
                            try:
                                list_of_column_elements[i].append(value['title_of_columns'][i])
                            except IndexError:
                                break
                    
                for element in list_of_column_elements:
                    list_max_size_of_colomns.append(max(map(len, element)) + 2)
                
                total_width_of_row_string = sum(list_max_size_of_colomns) + len(list_max_size_of_colomns)
                if not value['title'] is None:
                    if len(value['title']) > 0:
                        title = self.get_string_in_need_size(value['title'], total_width_of_row_string, False, '')
                        self.__add_string_to_list_of_strings(title, data_dict_for_proccessing)
                        data_dict_for_proccessing['current_string_index'] += 1

                if not value['title_of_columns'] is None:
                    if len(value['title_of_columns']) > 0:
                        title_of_row = ''
                        index = 0
                        list_row_strings = []
                        if have_title_of_rows:
                            title_of_row = ' ' * list_max_size_of_colomns[index]
                            index += 1
                        for i in range(len(list_max_size_of_colomns) - index):
                            string = ''
                            try:
                                string = self.get_string_in_need_size(value['title_of_columns'][i], list_max_size_of_colomns[index], False)
                            except IndexError:
                                string = ' ' * list_max_size_of_colomns[index]
                            list_row_strings.append(string)    
                            index += 1
                        row_string = f'{title_of_row}|{"|".join(list_row_strings)}|'
                        self.__add_string_to_list_of_strings(row_string, data_dict_for_proccessing)
                        data_dict_for_proccessing['current_string_index'] += 1

                title_of_row = ''
                x_index = 0          
                for x in value['value']:
                    y_index = 0
                    list_row_strings = []
                    if have_title_of_rows:
                        title_of_row = self.get_string_in_need_size(value['title_of_rows'][x_index], list_max_size_of_colomns[y_index], hidden)
                        y_index += 1
                    for y in x:
                        list_row_strings.append(self.get_string_in_need_size(y, list_max_size_of_colomns[y_index], hidden))     
                        y_index += 1
                        row_string = f'{title_of_row}|{"|".join(list_row_strings)}|'
                    self.__add_string_to_list_of_strings(row_string, data_dict_for_proccessing)
                    x_index += 1
                    data_dict_for_proccessing['current_string_index'] += 1
                if data_dict_for_proccessing['row_column'] == 'row':
                    data_dict_for_proccessing['list_of_strings'][-1] += data_dict_for_proccessing['separator']
                data_dict_for_proccessing['total_width_of_row_string'] += total_width_of_row_string

    def get_data_dict_for_proccessing(self, row_column, list_of_strings = None, current_string_index = 0, separator = '', total_width_of_row_string = 0):
        if list_of_strings is None:
            list_of_strings = []
        data_dict_for_proccessing = {
            'row_column': row_column,
            'list_of_strings': list_of_strings,
            'current_string_index': current_string_index,
            'separator': separator,
            'total_width_of_row_string': total_width_of_row_string,
        }  
        return data_dict_for_proccessing 

    def __add_string_to_list_of_strings(self, string, data_dict_for_proccessing):
        if data_dict_for_proccessing['row_column'] == 'row':
            data_dict_for_proccessing['list_of_strings'].append(string)
        else:
            if data_dict_for_proccessing['current_string_index'] < len(data_dict_for_proccessing['list_of_strings']):
                data_dict_for_proccessing['list_of_strings'][data_dict_for_proccessing['current_string_index']] += data_dict_for_proccessing['separator'] + string
            else:
                data_dict_for_proccessing['list_of_strings'].append((' ' * data_dict_for_proccessing['total_width_of_row_string']) + (data_dict_for_proccessing['separator'] if data_dict_for_proccessing['total_width_of_row_string'] > 0 else '') + string)

    def get_string_in_need_size(self, object_to_string, max_size, hidden, offset_from_edge = ' ') -> str:
        from cells import Cells
        string = ''
        if type(object_to_string) == Cells:
            string = object_to_string.value.get_symbol(hidden)
        else:
            string = str(object_to_string)
        if len(string) + 2 == max_size:
            return f'{offset_from_edge}{string}{offset_from_edge}'
        else:
            count_of_space = max_size - (len(string) + len(offset_from_edge) * 2)
            count_of_space_for_other_sites = int(count_of_space / 2)
            space_string = ' ' * count_of_space_for_other_sites
            if (count_of_space % 2) == 0:  
                return f'{offset_from_edge}{space_string}{string}{space_string}{offset_from_edge}'
            else:
                return f'{offset_from_edge}{space_string}{string}{space_string + " "}{offset_from_edge}'

    def output_message(self, message):
        title = message.title
        # print('IT WORK')
        if type(title) is str and not title is '':
            print(title + '\n') 
        content = message.content
        for string in content:
            print(string + '\n')

    @staticmethod
    def __short_name__():
        return 'Co'