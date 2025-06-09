def recommend_k_items_slow(self, test, top_k=10, remove_seen=True):
    """Recommend top K items for all users which are in the test set.

        Args:
            test: test Spark dataframe
            top_k: top n items to return
            remove_seen: remove items test users have already seen in the past from the recommended set.
        """
    if remove_seen:
        raise ValueError('Not implemented')
    self.get_user_affinity(test).write.mode('overwrite').saveAsTable(self.f('{prefix}user_affinity'))
    query = self.f('\n        SELECT {col_user}, {col_item}, score\n        FROM\n        (\n          SELECT df.{col_user},\n                 S.i2 {col_item},\n                 SUM(df.{col_rating} * S.value) AS score,\n                 row_number() OVER(PARTITION BY {col_user} ORDER BY SUM(df.{col_rating} * S.value) DESC) rank\n          FROM   \n            {prefix}user_affinity df, \n            {prefix}item_similarity S\n          WHERE df.{col_item} = S.i1\n          GROUP BY df.{col_user}, S.i2\n        )\n        WHERE rank <= {top_k} \n        ', top_k=top_k)
    return self.spark.sql(query)