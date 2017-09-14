# coding=UTF-8
""" Crawler libraries. """
import requests
from bs4 import BeautifulSoup

class SimpleParser():
    """ Crawler in NBINET website until target website is found. Return web html code. """

    layer_check_list = ['browseEntry', 'browseSuperEntry', 'bibMain']
    """
    # browseEntry - First Layer
    # browseSuperEntry - Second Layer
    # bibMain - Third Layer
    """

    library_list = ['淡江大學', '成功大學', '臺北市立圖書', '國家圖書', '新書書訊']
    data = ''

    def __init__(self, isbn):
        url = 'http://nbinet3.ncl.edu.tw/search*cht/i?SEARCH=%d+&searchscope=1' % isbn
        source_code = self.get_filter_code(url)
        book_layer = self.set_layer(source_code, self.layer_check_list)

        if self.is_file_not_found(source_code):
            print('%d: File no found.' % isbn)
            self.data = ''
        else:
            if book_layer == 'browseEntry':
                url = self.get_first_layer_data(source_code)
                source_code = self.get_filter_code(url)
                book_layer = self.set_layer(source_code, self.layer_check_list)
            if book_layer == 'browseSuperEntry':
                url = self.get_second_layer_data(source_code)
                source_code = self.get_filter_code(url)
                book_layer = self.set_layer(source_code, self.layer_check_list)
            self.data = source_code
            print('%d: Done.' % isbn)

    @staticmethod
    def get_filter_code(url):
        """ Set hearder. """
        browser = 'Chrome/55.0.2924.87'
        header = {'user-agent': browser}
        resource = requests.get(url, headers=header)
        source_code = BeautifulSoup(resource.text, 'html.parser')
        return source_code

    @staticmethod
    def set_layer(source_code, layer_check_list):
        """ Find where is first website when start run crawler. Return string. """
        for i in layer_check_list:
            if source_code.prettify().find('%s' % i) > -1:
                return i
        return None

    @staticmethod
    def is_file_not_found(source_code):
        """ Check whether result is found. Return boolean. """
        string_code = source_code.get_text()
        if string_code.find('沒有查獲符合查詢條件的館藏') != -1:
            return True
        return False

    # --- First Layer Domain | Start ---
    def get_first_layer_data(self, source_code):
        """ Searching target url for getting better book information. Return url. """
        data = self.set_data_list(source_code, 'browseEntryData')
        data = self.set_first_data_all_url(source_code, data)
        data = self.set_first_data_all_library(source_code, data)
        result = self.get_target_library(data, self.library_list)
        return result

    @staticmethod
    def set_first_data_all_url(source_code, data):
        """ Scan all url on current website. Set data['url']. """
        parser = source_code.find_all(class_='browseEntryData')
        for i in range(len(data)):
            result = parser[i].find_all('a')
            result = result[1]['href']
            result = 'http://nbinet3.ncl.edu.tw%s' % result
            data[i]['url'] = result
        return data

    @staticmethod
    def set_first_data_all_library(source_code, data):
        """ Scan all libraries on current website. Set data['library']. """
        temp_index_data = []
        index = 0
        while index < len(source_code.prettify()):
            index = source_code.prettify().find('browseEntryData', index)
            if index == -1:
                break
            temp_index_data.append(index)
            index += 15

        # set temp_index_subdata
        temp_index_subdata = []
        index = 0
        while index < len(source_code.prettify()):
            index = source_code.prettify().find('browseSubEntryData', index)
            if index == -1:
                break
            temp_index_subdata.append(index)
            index += 18

        # set Library
        temp_library = source_code.find_all(class_='browseSubEntryData')
        for i in range(len(temp_index_subdata)):
            try:
                target_library = temp_library[i].find('strong').get_text()
                target_data_index = 0
                for j in range(len(temp_index_data)):
                    if temp_index_subdata[i] > temp_index_data[j]:
                        target_data_index = j
                        data[target_data_index]['library'].append(target_library)
            except:
                continue
        return data
	# --- First Layer Domain | End ---

	# --- Second Layer Domain | Start ---
    def get_second_layer_data(self, source_code):
        """ Searching target url for getting better book information. Return url. """
        data = self.set_data_list(source_code, 'briefCitRow')
        data = self.set_second_data_all_url(source_code, data)
        data = self.set_second_data_all_library(source_code, data)
        result = self.get_target_library(data, self.library_list)
        return result

    @staticmethod
    def set_second_data_all_url(source_code, data):
        """ Scan all url on current website. Set data['url']. """
        parser = source_code.find_all(class_='briefcitTitle')
        for i in range(len(data)):
            result = parser[i].find_all('a')
            result = result[0]['href']
            result = 'http://nbinet3.ncl.edu.tw%s' % result
            data[i]['url'] = result
        return data

    @staticmethod
    def set_second_data_all_library(source_code, data):
        """ Scan all libraries on current website. Set data['library']. """
        parser = source_code.find_all(class_='briefcitStatus')
        for i in range(len(data)):
            result = parser[i].get_text()
            data[i]['library'] = result
        return data
	# --- Second Layer Domain | End ---

	# --- First & Second Layer Domain | Start ---
    @staticmethod
    def set_data_list(source_code, target_class_name):
        """ Set template follow count of targets found. Return list. """
        data = []
        source_code_string = source_code.prettify()
        count = source_code_string.count(target_class_name)
        for i in range(count):
            temp = {'url': None, 'library': []}
            data.append(temp)
        return data

    @staticmethod
    def get_target_library(data, library_list):
        """
        Find/set target library depend on self.library_list.
        If no found, set first library from data list.
        Return data['url'].
        """
        for j in library_list:
            for i in data:
                temp = str(i['library'])
                if temp.find(j) > 0:
		    		# if library includes in library_list.
                    return i['url']
		# if no library includes in libraryList.
        return data[0]['url']

# Demo
if __name__ == '__main__':
    print("Run demo")
    CHECK_ISBN = 9789861943107
    GET_DATA = SimpleParser(CHECK_ISBN)
    print(GET_DATA)
