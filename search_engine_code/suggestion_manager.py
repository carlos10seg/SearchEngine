import pandas as pd
import numpy as np
import datetime as dt
from os import path

class SuggestionManager():

    #max_session_time = 0
    #max_frequency = 0

    def set_max_values(self, logs):
        # set the maximum frequency of occurrence of any query in QL
        max_frequency = logs.groupby('Query').count()[['UserId']].sort_values('UserId', ascending=False).iloc(0)[0][0]
        # get the longest session
        max_session_time = 0
        current_user_id = logs.head().iloc(0)[0]['UserId']
        current_time = logs.head().iloc(0)[0]['QueryTime']    
        for index, row in logs.iterrows():
            user_id = row[0]
            q_time = row[2]
            if current_user_id != user_id:
                if index-1 >= 0:
                    dif_time = (logs.loc[index-1]['QueryTime'] - q_time).total_seconds()
                    if (dif_time > max_session_time):
                        self.max_session_time = dif_time
                    current_user_id = user_id
                    current_time = q_time
        max_session_time

    def load_logs(self):        
        #if redisManager.getValue(self.log_name) == None:
        logs = pd.read_csv('../data/logs.csv')
        logs['Query'] = logs['Query'].str.strip()
        logs = logs.rename(columns={'AnonID': 'UserId'})
        logs['QueryTime'] = pd.to_datetime(logs['QueryTime'], format='%Y-%m-%d %H:%M:%S')
        # 3,942,354 queries on logs
        #set_max_values(logs)
        logs.to_pickle("./logs.pkl")

    def get_suggestions(self, query):
        query = query.strip()
        logs = pd.read_pickle("./logs.pkl")
        max_session_time = 7943593  # hard code it to improve performance
        max_frequency = 83677 # hard code it to improve performance
        N_suggestions = 10

        # gets a subset from the query
        queries_equal_to_q = logs[logs['Query'] == query]
        arr_unique_sessions_queries = []
        current_user_id = 0
        # get the unique sessions for the query because users could search 2 or more times the same query immediately in the same session.
        for index, row in queries_equal_to_q.iterrows():
            user_id = row[0]
            if current_user_id != user_id:
                arr_unique_sessions_queries.append(row)
                current_user_id = user_id
        queries_equal_to_q = pd.DataFrame(arr_unique_sessions_queries)
        
        # Get query candidates for suggestions, the ones which in the same session changed from query text to query text + something else
        arr_candidate_queries = []
        time_differences = []
        # loop through queries_equal_to_q to get the real candidates 
        for index, row in queries_equal_to_q.iterrows():
            user_id = row[0]
            query = row[1]
            q_time = row[2]
            current_index = index + 1
            current_user_id = logs.loc[current_index, 'UserId']
            has_next = False
            is_invalid = False
            while (user_id == current_user_id):
                # check for current query text 
                current_query = logs.loc[current_index, 'Query']
                if (not pd.isna(current_query) and current_query.startswith(query) and len(current_query) > len(query)):
                    arr_candidate_queries.append(logs.loc[current_index])
                    time_differences.append((logs.loc[current_index]['QueryTime'] - q_time).total_seconds())
                # move to next row    
                current_index += 1
                current_user_id = logs.loc[current_index, 'UserId']

        candidate_queries = pd.DataFrame(arr_candidate_queries)
        # if there are no candidate queries to process then return empty array.
        if len(candidate_queries) == 0:
            return []

        candidate_queries['Time_Dif'] =  time_differences
        candidate_queries = candidate_queries.join(candidate_queries.groupby('Query')['Time_Dif'].min(), on="Query", rsuffix="_Min")
        # only get the queries that have the min difference in time
        # and remove duplicated queries based on 'Query', 'Time_Dif'
        candidate_queries[candidate_queries['Time_Dif'] == candidate_queries['Time_Dif_Min']].drop_duplicates(subset=['Query', 'Time_Dif'])        

        # set the frequency - 𝐹𝑟𝑒𝑞(𝐶𝑄)
        query_counts = logs[logs['Query'].isin(candidate_queries['Query'])].groupby('Query')['Query'].count()
        query_results = candidate_queries.join(query_counts, on='Query', lsuffix='_text')
        query_results = query_results.rename(columns={'Query': 'Count', 'Query_text': 'Query'})
        query_results['Freq'] = query_results['Count'] / max_frequency

        # set the mod - 𝑀𝑜𝑑(𝐶𝑄,𝑞′)
        sessions_count = candidate_queries.groupby('Query')['Query'].count().astype(object)
        query_results = query_results.join(sessions_count, on='Query', lsuffix='_text').rename(columns={'Query': 'CountInSession', 'Query_text': 'Query'})
        query_results['Mod'] = query_results['CountInSession'] / len(queries_equal_to_q) 

        # set the time - 𝑇𝑖𝑚𝑒(𝐶𝑄, 𝑞′)
        query_results['Time'] = query_results['Time_Dif_Min'] / max_session_time

        # set the min values
        min_freq = query_results['Freq'].min()
        min_mod = query_results['Mod'].min()
        min_time = query_results['Time'].min()

        # calculate scores and sort
        query_results['Score'] = (query_results['Freq'] + query_results['Mod'] + query_results['Time']) / 1 - (min_freq + min_mod + min_time)
        #query_results['Score'] = query_results['Score'].astype('float64')
        n = N_suggestions if len(query_results) > N_suggestions else len(query_results)
        suggestions_list = query_results.drop_duplicates(subset=['Query', 'Score']).sort_values('Score', ascending=False).head(n)
        print(suggestions_list)
        return suggestions_list['Query'].tolist()