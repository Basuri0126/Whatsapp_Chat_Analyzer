import re
import pandas as pd
from datetime import datetime

def preprocessor(data):
    pattern_12_hour = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[APapMm]{2}'
    pattern_24_hour = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'

    # Search for 12-hour pattern in the data
    if re.search(pattern_12_hour, data):
        pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s[APapMm]{2}\s-\s"
        message = re.split(pattern, data)[3:]
        dates = re.findall(pattern, data)
        dates = dates[2:]

        df = pd.DataFrame({'user_message': message, 'message_date': dates})

        df['message_date'] = df['message_date'].str.split(" ").str[:-2]

        def convert_to_24_hour_format(timestamp):
            # Remove extra characters and replace double commas with a single comma
            timestamp = timestamp.replace('[', '').replace(']', '').replace(',', '').replace('\u202f', '').replace('AM',' AM').replace('PM', ' PM').replace('\\u202f', '')

            # Define the input format
            input_format = "'%m/%d/%y' '%I:%M %p'"

            # Parse the timestamp string to a datetime object
            time_obj = datetime.strptime(timestamp, input_format)

            # Format the datetime object in 24-hour time format
            formatted_time = time_obj.strftime('%Y-%m-%d %H:%M:%S')

            return formatted_time

        df['message_date'] = df['message_date'].apply(lambda x: convert_to_24_hour_format(str(x)))

        # Using the format string ensures that pandas can correctly parse the date strings and
        # convert them into datetime objects.
        # Without the format specification, pandas would use its default parsing method,
        # which may not work if the date strings are not in a recognized format.
        # Specifying format helps avoid any ambiguity and ensures the correct conversion of dates to datetime objects.
        df['message_date'] = pd.to_datetime(df['message_date'])
        df.rename(columns={'message_date': 'date'}, inplace=True)

        # separate user message and user dates
        users = []
        messages = []
        for msg in df['user_message']:
            x = re.split('([\w\W]+?):\s', msg)
            if x[1:]:
                users.append(x[1])
                messages.append(x[2])
            else:
                users.append('group notification')
                messages.append(x[0])

        df['users'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)

        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['day_name'] = df['date'].dt.day_name()
        df['month_num'] = df['date'].dt.month
        df['month_day'] = df['month'].astype(str) + '-' + df['day'].astype(str)
        df['message_count'] = df.groupby(['month_day', 'users'])['message'].transform('count')
        df['data_info'] = df['year'].astype(str) + '-' + df['month_num'].astype(str)

        period = []
        for hour in df[['day', 'hour']]['hour']:
            if hour == 23:
                period.append(str(hour) + '-' + str('00'))
            elif hour == 0:
                period.append(str('00') + '-' + str(hour + 1))
            else:
                period.append(str(hour) + '-' + str(hour + 1))

        df['period'] = period

        return df

    # Search for 24-hour pattern in the data
    elif re.search(pattern_24_hour, data):
        pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
        message = re.split(pattern, data)[1:]
        dates = re.findall(pattern, data)

        df = pd.DataFrame({'user_message': message, 'message_date': dates})

        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

        # Using the format string ensures that pandas can correctly parse the date strings and
        # convert them into datetime objects.
        # Without the format specification, pandas would use its default parsing method,
        # which may not work if the date strings are not in a recognized format.
        # Specifying the format helps avoid any ambiguity and ensures the correct conversion of dates to datetime objects.

        df.rename(columns={'message_date': 'date'}, inplace=True)

        # separate user message and user dates
        users = []
        messages = []
        for msg in df['user_message']:
            x = re.split('([\w\W]+?):\s', msg)
            if x[1:]:
                users.append(x[1])
                messages.append(x[2])
            else:
                users.append('group notification')
                messages.append(x[0])

        df['users'] = users
        df['message'] = messages
        df.drop(columns=['user_message'], inplace=True)

        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month_name()
        df['day'] = df['date'].dt.day
        df['hour'] = df['date'].dt.hour
        df['minute'] = df['date'].dt.minute
        df['day_name'] = df['date'].dt.day_name()
        df['month_num'] = df['date'].dt.month
        df['month_day'] = df['month'].astype(str) + '-' + df['day'].astype(str)
        df['message_count'] = df.groupby(['month_day', 'users'])['message'].transform('count')
        df['data_info'] = df['year'].astype(str) + '-' + df['month_num'].astype(str)

        period = []
        for hour in df[['day', 'hour']]['hour']:
            if hour == 23:
                period.append(str(hour) + '-' + str('00'))
            elif hour == 0:
                period.append(str('00') + '-' + str(hour + 1))
            else:
                period.append(str(hour) + '-' + str(hour + 1))

        df['period'] = period

        return df
