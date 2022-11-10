"""All helper methods are written here."""
import json
import csv


def csv_to_json(csvfilepath, jsonfilepath):
    """CSV to JSON converter."""
    jsonarray = []
    # read csv file
    with open(csvfilepath) as csvf:
        # load csv file data using csv library's dictionary reader
        csvreader = csv.DictReader(csvf)

        # convert each csv row into python dict
        for row in csvreader:
            # add this python dict to json array
            jsonarray.append(row)
    # convert python jsonarray to JSON String and write to file
    with open(jsonfilepath, 'w') as jsonf:
        jsonstring = json.dumps(jsonarray, indent=4)
        jsonf.write(jsonstring)


def load_json(jsonfilename):
    """Load JSON."""
    json_file = open(jsonfilename)
    json_data = json.load(json_file)
    return json_data


def is_date_in_range(payload, date):
    """Check if date in in the range."""
    if payload.get('date'):
        date_range = payload['date']
        if date >= date_range['start_date'] and date <= date_range['end_date']:
            return True
        return False
    return False


def get_filtered_data(payload, data):
    """Get filtered data."""
    res_data = []
    if payload.get('filters'):
        filters = payload['filters']
        for each in data:
            count = 0
            for filter_data in filters:
                if each[filter_data] in filters[filter_data]:
                    count += 1
            if count == len(filters):
                res_data.append(each)
    return res_data


def sort_data(payload, data):
    """Sorted data."""
    if payload.get('sort'):
        sort_array = payload['sort']
        for each in sort_array:
            if each['name'] in data[0].keys():
                if each['order'] == 'ASC':
                    data.sort(
                        key=lambda value: value[each['name']]
                    )
                else:
                    data.sort(
                        key=lambda value: value[each['name']],
                        reverse=True
                    )
    return data


def get_searched_data(payload, data):
    """Search Data."""
    final_data = []
    if payload.get('search'):
        search_array = payload['search']
        for each in data:
            count = 0
            for key in search_array['columns']:
                if search_array['text'] in each[key]:
                    count += 1
            if count > 0:
                final_data.append(each)
        return final_data
    return data


def get_paginated_data(payload, data):
    """Paginated Data."""
    result_data = []
    # if payload.get('pagination'):
    return result_data


def get_result_data(payload, data):
    """Filtered data."""
    if payload.get('dimensions') or payload.get('metrics'):
        column_data = payload['dimensions'] + payload['metrics']
        result_data = []
        for each in data:
            res_data = {}
            if is_date_in_range(payload, each['DATE']):
                for value in each.keys():
                    if value in column_data or value == 'DATE':
                        res_data[value] = each[value]
            if res_data != {}:
                result_data.append(res_data)
        filtered_data = get_filtered_data(payload, result_data)
        sorted_data = sort_data(payload, filtered_data)
        search_data = get_searched_data(payload, sorted_data)
        # final_paginated_data = get_paginated_data(payload, search_data)
        return search_data
    return "No dimensions or metrics specified."
