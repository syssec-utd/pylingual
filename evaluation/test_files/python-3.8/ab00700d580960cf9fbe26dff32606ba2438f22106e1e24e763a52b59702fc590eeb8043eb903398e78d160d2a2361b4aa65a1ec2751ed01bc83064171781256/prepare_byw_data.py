import ast
from functools import reduce
from operator import itemgetter
import pandas as pd
from offline_results.common.config import CONFIG_HOMEPAGE_PAYTV, CONFIG_HOMEPAGE_NO_PAYTV
from offline_results.common.constants import CUSTOMER_ID, CONTENT_ID, CREATED_ON, VIEW_HISTORY, VIEW_COUNT, RECENT_VIEWED_DATE, DURATION, PAY_TV_CONTENT, LEFT, HOMEPAGE_ID, STATUS, ACTIVE, HOMEPAGE_STATUS, HAS_HOMEPAGE, CLUSTER_ID, PAY_TV, NO_PAY_TV_CONTENT, IS_PAY_TV, MODEL_NAME, TV_CHANNEL_LIST, BYW
from offline_results.repository.graph_db_connection import ANGraphDb
from offline_results.similarity.content_profile.similarity_all_contents import SimilarityAllContents
from offline_results.utils.logger import Logging

class BYWData:

    @staticmethod
    def filter_by_dedicated_homepage_id(df, user_label, filter_on_ubd):
        config_dictionary = CONFIG_HOMEPAGE_PAYTV if user_label == PAY_TV else CONFIG_HOMEPAGE_NO_PAYTV
        config_df = pd.DataFrame(config_dictionary.items())
        config_df.columns = [HOMEPAGE_ID, MODEL_NAME]
        config_df = config_df[config_df[MODEL_NAME] == BYW]
        list_config_homepage_id = config_df[HOMEPAGE_ID].tolist()
        df = df.explode(column=HOMEPAGE_ID)
        df = df[df[HOMEPAGE_ID].isin(list_config_homepage_id)].reset_index(drop=True)
        if len(df.index) == 0:
            return df
        if filter_on_ubd:
            user_content_df = df.drop_duplicates([CONTENT_ID, CLUSTER_ID, HOMEPAGE_ID]).reset_index(drop=True)
        else:
            all_recommendation_dict_df = df.drop_duplicates([CONTENT_ID, CLUSTER_ID, HOMEPAGE_ID]).reset_index(drop=True)
        return user_content_df if filter_on_ubd else all_recommendation_dict_df

    @staticmethod
    def get_recent_viewed_date_and_duration(history):
        history_data = history[VIEW_HISTORY]
        list_history_data = ast.literal_eval(history_data)
        list_history_data = sorted(list_history_data, key=itemgetter(CREATED_ON), reverse=True)
        recent_date = list_history_data[0][CREATED_ON]
        total_duration = 0
        for history in list_history_data:
            duration_content = history[DURATION]
            total_duration += duration_content
        return (recent_date, total_duration)

    @staticmethod
    def get_user_cluster_mapping(user_content_df, user_label, user_cluster_mapping):
        is_pay_tv_status = True if user_label == PAY_TV else False
        Logging.info('Filtering user cluster mapping for ' + PAY_TV + ' user')
        user_cluster_mapping = user_cluster_mapping[user_cluster_mapping[IS_PAY_TV] == is_pay_tv_status].reset_index(drop=True)
        user_cluster_mapping[CUSTOMER_ID] = user_cluster_mapping[CUSTOMER_ID].astype(str)
        user_content_df[CUSTOMER_ID] = user_content_df[CUSTOMER_ID].astype(str)
        user_content_df = pd.merge(user_content_df, user_cluster_mapping, on=CUSTOMER_ID, how=LEFT)
        return user_content_df

    @staticmethod
    def get_content_homepage_id_mapping(graph, user_label, homepage_id_wise):
        content_label = PAY_TV_CONTENT if user_label == PAY_TV else NO_PAY_TV_CONTENT
        queries = graph.custom_query(f'''g.V().hasLabel('{content_label}').match(\n                        __.as("c").valueMap("{CONTENT_ID}","{STATUS}").as("{CONTENT_ID}"),\n                        __.as("c").out("{HAS_HOMEPAGE}")\n                        .valueMap("{HOMEPAGE_ID}","{HOMEPAGE_STATUS}").as("{HOMEPAGE_ID}")\n                        ).select("{CONTENT_ID}", "{HOMEPAGE_ID}")''', payload={content_label: content_label, CONTENT_ID: CONTENT_ID, HAS_HOMEPAGE: HAS_HOMEPAGE, HOMEPAGE_ID: HOMEPAGE_ID, HOMEPAGE_STATUS: HOMEPAGE_STATUS, STATUS: STATUS})
        content_homepage_map_df = pd.DataFrame()
        for query in queries:
            for data in query:
                content_id = data[CONTENT_ID][CONTENT_ID][0]
                content_status = data[CONTENT_ID][STATUS][0]
                homepage_id = data[HOMEPAGE_ID][HOMEPAGE_ID][0]
                homepage_status = data[HOMEPAGE_ID][HOMEPAGE_STATUS][0]
                content_homepage_map = pd.DataFrame([{CONTENT_ID: content_id, STATUS: content_status, HOMEPAGE_ID: homepage_id, HOMEPAGE_STATUS: homepage_status}])
                content_homepage_map_df = pd.concat([content_homepage_map_df, content_homepage_map], axis=0).sort_values(by=CONTENT_ID).reset_index(drop=True)
        if homepage_id_wise:
            content_homepage_map_df = content_homepage_map_df[(content_homepage_map_df[HOMEPAGE_STATUS] == ACTIVE) & (content_homepage_map_df[STATUS] == ACTIVE)].reset_index(drop=True)
        else:
            content_homepage_map_df = content_homepage_map_df[content_homepage_map_df[STATUS] == ACTIVE].reset_index(drop=True)
        content_homepage_map_df_grouped = pd.DataFrame(content_homepage_map_df.groupby(CONTENT_ID)[HOMEPAGE_ID].apply(list).reset_index())
        return content_homepage_map_df_grouped

    @staticmethod
    def get_viewed_content(graph, user_label, homepage_id_wise, viewed_relation_history_df, user_cluster_mapping):
        status = 'homepage_id wise' if homepage_id_wise else 'all content wise'
        try:
            Logging.info('Fetching content homepage mapping for ' + user_label + ' and ' + status)
            content_homepage_mapping = BYWData.get_content_homepage_id_mapping(graph, user_label, homepage_id_wise)
        except Exception:
            Logging.info('Re-trying to get content homepage_id mapping' + user_label + ' and ' + status)
            graph = ANGraphDb.new_connection_config().graph
            content_homepage_mapping = BYWData.get_content_homepage_id_mapping(graph, user_label, homepage_id_wise)
        is_pay_tv_status = True if user_label == PAY_TV else False
        viewed_relation_history_df = viewed_relation_history_df[viewed_relation_history_df[IS_PAY_TV] == is_pay_tv_status].reset_index(drop=True)
        viewed_relation_history_df = viewed_relation_history_df[~viewed_relation_history_df[CONTENT_ID].isin(TV_CHANNEL_LIST)].reset_index(drop=True)
        Logging.info('Generating Viewed Relation Dataframe for ' + user_label + ' users')
        view_history = viewed_relation_history_df[VIEW_HISTORY].to_list()
        view_history2 = [ast.literal_eval(i) for i in view_history]
        intermediate_df = pd.DataFrame({CUSTOMER_ID: viewed_relation_history_df[CUSTOMER_ID].to_list(), CONTENT_ID: viewed_relation_history_df[CONTENT_ID].to_list(), VIEW_HISTORY: view_history2})
        intermediate_df = BYWData.get_user_cluster_mapping(intermediate_df, user_label, user_cluster_mapping)
        cluster_content_grouped = pd.DataFrame(intermediate_df.groupby(CONTENT_ID)[CLUSTER_ID].apply(list).reset_index())
        intermediate_df = intermediate_df.explode(column=VIEW_HISTORY)
        intermediate_df[DURATION] = intermediate_df[VIEW_HISTORY].apply(lambda x: x[DURATION])
        intermediate_df[RECENT_VIEWED_DATE] = intermediate_df[VIEW_HISTORY].apply(lambda x: x[CREATED_ON])
        view_count_df = intermediate_df.groupby([CONTENT_ID]).size().to_frame(VIEW_COUNT)
        recent_date_df = intermediate_df.groupby(CONTENT_ID).agg({RECENT_VIEWED_DATE: 'max'}).rename_axis(CONTENT_ID).reset_index()
        total_duration_df = intermediate_df.groupby(CONTENT_ID).sum().rename_axis(CONTENT_ID).reset_index()[[CONTENT_ID, DURATION]]
        data_frames = [recent_date_df, total_duration_df, view_count_df, cluster_content_grouped, content_homepage_mapping]
        user_content_df = reduce(lambda left, right: pd.merge(left, right, on=[CONTENT_ID], how=LEFT), data_frames)
        user_content_df = user_content_df[~user_content_df[HOMEPAGE_ID].isnull()].reset_index(drop=True)
        user_content_df = user_content_df.explode(column=CLUSTER_ID)
        if len(user_content_df.index) == 0:
            return (user_content_df, content_homepage_mapping)
        user_content_df = user_content_df.sort_values(by=[RECENT_VIEWED_DATE, DURATION, VIEW_COUNT], ascending=False).reset_index(drop=True)
        final_df = pd.DataFrame(user_content_df.groupby(CLUSTER_ID)[CONTENT_ID].apply(list).reset_index())
        return (final_df, content_homepage_mapping)

    @staticmethod
    def get_content_similarity_based_on_all_content(user_label):
        content_label = PAY_TV_CONTENT if user_label == PAY_TV else NO_PAY_TV_CONTENT
        content_similarity_data = SimilarityAllContents.prepare_similarity_based_on_all_content(content_label)
        return content_similarity_data