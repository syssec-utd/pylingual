from datetime import datetime
from traceback import print_exc
import pandas as pd
from pandas import DataFrame
from offline_results.common.config import MOST_VIEWED_CONTENTS_LIMIT
from offline_results.common.constants import CLUSTER_ID, HOMEPAGE_ID, RECORDS, CREATED_ON, VIEW_COUNT, CONTENT_ID, HOMEPAGE_STATUS, ACTIVE, PAY_TV_CONTENT, NO_PAY_TV_CONTENT, HAS_HOMEPAGE, STATUS, INNER, PAY_TV, REC_TYPE
from offline_results.utils.logger import Logging

class MVUtils:

    @staticmethod
    def get_json_format_output(df, key_prefix, homepage_id_wise):
        try:
            if homepage_id_wise:
                output_dict = {}
                unique_cluster_id = df[CLUSTER_ID].unique()
                for cluster_id in unique_cluster_id:
                    temp_output_dict = {}
                    key_prefix_cls = key_prefix + ':' + str(cluster_id)
                    cluster_wise_df = df.loc[df[CLUSTER_ID] == cluster_id]
                    unique_homepage_id = cluster_wise_df[HOMEPAGE_ID].unique()
                    for homepage_id in unique_homepage_id:
                        key_prefix_cls_hid = key_prefix_cls + ':' + str(homepage_id)
                        homepage_wise_df = cluster_wise_df.loc[cluster_wise_df[HOMEPAGE_ID] == homepage_id]
                        homepage_wise_df = homepage_wise_df[[CONTENT_ID, CREATED_ON, REC_TYPE]]
                        temp_output_dict[key_prefix_cls_hid] = homepage_wise_df.to_dict(RECORDS)
                    output_dict.update(temp_output_dict)
            else:
                output_dict = {}
                unique_cluster_id = df[CLUSTER_ID].unique()
                for cluster_id in unique_cluster_id:
                    temp_output_dict = {}
                    key_prefix_cls = key_prefix + ':' + str(cluster_id)
                    output_df = df.loc[df[CLUSTER_ID] == cluster_id]
                    output_df = output_df[[CONTENT_ID, HOMEPAGE_ID, CREATED_ON, REC_TYPE]]
                    temp_output_dict[key_prefix_cls] = output_df.to_dict(RECORDS)
                    output_dict.update(temp_output_dict)
            return output_dict
        except Exception as e:
            Logging.error(f'Error while converting df to json format for{key_prefix}, Error: {e}')

    @staticmethod
    def get_label_wise_homepage_for_contents(graph, user_label, homepage_id_wise) -> DataFrame:
        try:
            content_label = PAY_TV_CONTENT if user_label == PAY_TV else NO_PAY_TV_CONTENT
            content_response = graph.custom_query(query=f"""g.V().hasLabel('{content_label}').match(\n                __.as("c").valueMap('{CONTENT_ID}','{STATUS}').as('{CONTENT_ID}'),\n                __.as("c").out('{HAS_HOMEPAGE}')\n                .valueMap('{HOMEPAGE_ID}','{HOMEPAGE_STATUS}').as('{HOMEPAGE_ID}')\n                ).select('{CONTENT_ID}', '{HOMEPAGE_ID}')""", payload={content_label: content_label, CONTENT_ID: CONTENT_ID, HAS_HOMEPAGE: HAS_HOMEPAGE, HOMEPAGE_ID: HOMEPAGE_ID, HOMEPAGE_STATUS: HOMEPAGE_STATUS, STATUS: STATUS})
            content_homepage_map_df = pd.DataFrame()
            for query in content_response:
                for data in query:
                    content_id = data[CONTENT_ID][CONTENT_ID][0]
                    content_status = data[CONTENT_ID][STATUS][0]
                    homepage_id = data[HOMEPAGE_ID][HOMEPAGE_ID][0]
                    homepage_status = data[HOMEPAGE_ID][HOMEPAGE_STATUS][0]
                    content_homepage_map = pd.DataFrame([{CONTENT_ID: content_id, STATUS: content_status, HOMEPAGE_ID: homepage_id, HOMEPAGE_STATUS: homepage_status}])
                    content_homepage_map_df = pd.concat([content_homepage_map_df, content_homepage_map], axis=0).reset_index(drop=True)
            if homepage_id_wise:
                content_homepage_map_df = content_homepage_map_df[content_homepage_map_df[HOMEPAGE_STATUS] == ACTIVE].reset_index(drop=True)
            content_homepage_map_df = content_homepage_map_df[content_homepage_map_df[STATUS] == ACTIVE].reset_index(drop=True)
            content_homepage_map_df_grouped = pd.DataFrame(content_homepage_map_df.groupby(CONTENT_ID)[HOMEPAGE_ID].apply(list).reset_index())
        except Exception:
            print_exc()
            content_homepage_map_df_grouped = []
        return content_homepage_map_df_grouped

    @staticmethod
    def get_cluster_wise_most_viewed_contents(ubd):
        try:
            Logging.info('Finding cluster-wise most-viewed contents')
            cluster_wise_most_viewed_contents = pd.DataFrame()
            unique_cluster_id = ubd[CLUSTER_ID].unique()
            for cluster_id in unique_cluster_id:
                cluster_ubd = ubd.loc[ubd[CLUSTER_ID] == cluster_id]
                content_views_df = cluster_ubd.groupby([CONTENT_ID], as_index=False).agg(view_count=(VIEW_COUNT, sum))
                content_views_df[CLUSTER_ID] = cluster_id
                content_views_df = content_views_df.sort_values([VIEW_COUNT], ascending=False).reset_index(drop=True)
                content_views_df = content_views_df.head(MOST_VIEWED_CONTENTS_LIMIT)
                cluster_wise_most_viewed_contents = pd.concat([cluster_wise_most_viewed_contents, content_views_df], axis=0).reset_index(drop=True)
            cluster_wise_most_viewed_contents = cluster_wise_most_viewed_contents.sort_values([CLUSTER_ID, VIEW_COUNT], ascending=(True, False)).reset_index(drop=True)
            return cluster_wise_most_viewed_contents
        except Exception as e:
            Logging.error(f'Error while Finding cluster-wise most-viewed contents, Error: {e}')

    @staticmethod
    def get_cluster_and_homepage_wise_most_viewed_contents(ubd):
        try:
            Logging.info('Finding cluster-and-homepage-wise most-viewed contents')
            cluster_homepage_wise_most_viewed_contents = pd.DataFrame()
            unique_cluster_id = ubd[CLUSTER_ID].unique()
            for cluster_id in unique_cluster_id:
                cluster_ubd = ubd.loc[ubd[CLUSTER_ID] == cluster_id]
                homepage_wise_most_viewed_contents = pd.DataFrame()
                unique_homepage_id = cluster_ubd[HOMEPAGE_ID].unique()
                for homepage_id in unique_homepage_id:
                    homepage_in_cluster_ubd = cluster_ubd.loc[cluster_ubd[HOMEPAGE_ID] == homepage_id]
                    content_views_df = homepage_in_cluster_ubd.groupby([CONTENT_ID], as_index=False).agg(view_count=(VIEW_COUNT, sum))
                    content_views_df[HOMEPAGE_ID] = homepage_id
                    content_views_df = content_views_df.sort_values([VIEW_COUNT], ascending=False).reset_index(drop=True)
                    content_views_df = content_views_df.head(MOST_VIEWED_CONTENTS_LIMIT)
                    homepage_wise_most_viewed_contents = pd.concat([homepage_wise_most_viewed_contents, content_views_df], axis=0).reset_index(drop=True)
                homepage_wise_most_viewed_contents[CLUSTER_ID] = cluster_id
                cluster_homepage_wise_most_viewed_contents = pd.concat([cluster_homepage_wise_most_viewed_contents, homepage_wise_most_viewed_contents], axis=0).reset_index(drop=True)
            cluster_homepage_wise_most_viewed_contents = cluster_homepage_wise_most_viewed_contents.sort_values([CLUSTER_ID, HOMEPAGE_ID, VIEW_COUNT], ascending=(True, True, False)).reset_index(drop=True)
            return cluster_homepage_wise_most_viewed_contents
        except Exception as e:
            Logging.error(f'Error while Finding cluster-and-homepage-wise most viewed contents , Error: {e}')

    @staticmethod
    def add_created_on_attribute(dataframe) -> DataFrame:
        try:
            dataframe[CREATED_ON] = datetime.utcnow().isoformat()
            return dataframe
        except Exception as e:
            Logging.error(f'Error while adding time created attribute, Error: {e}')

    @staticmethod
    def add_recommendation_type_attribute(dataframe, rec_type) -> DataFrame:
        try:
            dataframe[REC_TYPE] = rec_type
            return dataframe
        except Exception as e:
            Logging.error(f'Error while adding recommendation type attribute, Error: {e}')

    @staticmethod
    def get_inner_merged_df(data1, data2, on):
        try:
            df = pd.merge(data1, data2, on=on, how=INNER)
            return df
        except Exception as e:
            Logging.error(f'Error while merging on {on}, Error: {e}')

    @staticmethod
    def get_default_most_viewed_contents(ubd):
        try:
            Logging.info('Finding most-viewed contents')
            content_views_df = ubd.groupby([CONTENT_ID], as_index=False).agg(view_count=(VIEW_COUNT, sum))
            most_viewed_contents = content_views_df.sort_values([VIEW_COUNT], ascending=False).reset_index(drop=True)
            most_viewed_contents = most_viewed_contents.head(MOST_VIEWED_CONTENTS_LIMIT)
            return most_viewed_contents
        except Exception as e:
            Logging.error(f'Error while Finding FALLBACK most-viewed contents, Error: {e}')

    @staticmethod
    def get_default_homepage_wise_most_viewed_contents(ubd):
        try:
            Logging.info('Finding homepage-wise most-viewed contents')
            homepage_wise_most_viewed_contents = pd.DataFrame()
            unique_homepage_id = ubd[HOMEPAGE_ID].unique()
            for homepage_id in unique_homepage_id:
                homepage_ubd = ubd.loc[ubd[HOMEPAGE_ID] == homepage_id]
                content_views_df = homepage_ubd.groupby([CONTENT_ID], as_index=False).agg(view_count=(VIEW_COUNT, sum))
                content_views_df[HOMEPAGE_ID] = homepage_id
                content_views_df = content_views_df.sort_values([VIEW_COUNT], ascending=False).reset_index(drop=True)
                content_views_df = content_views_df.head(MOST_VIEWED_CONTENTS_LIMIT)
                homepage_wise_most_viewed_contents = pd.concat([homepage_wise_most_viewed_contents, content_views_df], axis=0).reset_index(drop=True)
            homepage_wise_most_viewed_contents = homepage_wise_most_viewed_contents.sort_values([HOMEPAGE_ID, VIEW_COUNT], ascending=(True, False)).reset_index(drop=True)
            return homepage_wise_most_viewed_contents
        except Exception as e:
            Logging.error(f'Error while Finding FALLBACK most viewed contents , Error: {e}')

    @staticmethod
    def get_default_json_format_output(df, key_prefix, homepage_id_wise):
        try:
            if homepage_id_wise:
                output_dict = {}
                unique_homepage_id = df[HOMEPAGE_ID].unique()
                key_prefix_cls = key_prefix
                for homepage_id in unique_homepage_id:
                    key_prefix_cls_hid = key_prefix_cls + ':' + str(homepage_id)
                    homepage_wise_df = df.loc[df[HOMEPAGE_ID] == homepage_id]
                    homepage_wise_df = homepage_wise_df[[CONTENT_ID, CREATED_ON, REC_TYPE]]
                    output_dict[key_prefix_cls_hid] = homepage_wise_df.to_dict(RECORDS)
                    output_dict.update(output_dict)
            else:
                key_prefix_cls = key_prefix
                df = df[[CONTENT_ID, HOMEPAGE_ID, CREATED_ON, REC_TYPE]]
                output_dict = {key_prefix_cls: df.to_dict(RECORDS)}
                output_dict.update(output_dict)
            return output_dict
        except Exception as e:
            Logging.error(f'Error while converting df to json format for{key_prefix}, Error: {e}')