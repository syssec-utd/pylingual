import json
import neo4j.data
from tornado.options import options
import logging
import traceback
from neo4j import WorkspaceConfig
from lesscode.db.page import Page
from lesscode.utils.encryption_algorithm import AES

class Neo4jHelper:
    """
    Neo4j   数据库操作实现
    """

    def __init__(self, pool, access=neo4j.READ_ACCESS):
        """
        初始化sql工具
        :param pool: 连接池名称
        """
        if isinstance(pool, str):
            self.pool, self.dialect = options.database[pool]
            self.pool = self.pool.session(database=pool, default_access_mode=access)
        else:
            self.pool = pool

    def __repr__(self):
        printer = 'o(>﹏<)o ......Neo4j old driver "{0}" carry me fly...... o(^o^)o'.format(self.pool)
        return printer

    async def listreader(self, cypher, keys):
        """
        Read data from Neo4j in specified cypher.
        Read and parse data straightly from cypher field result.
        :param cypher: string
            Valid query cypher statement.
        :param keys: list
            Cypher query columns to return.
        :return: list
            Each returned record constructs a list and stored in a big list, [[...], [...], ...].
        """
        tx = await self.pool.begin_transaction()
        data = []
        result = await tx.run(cypher)
        async for record in result:
            rows = []
            for key in keys:
                rows.append(record[key])
            data.append(rows)
        await self.pool.close()
        return data

    async def dictreader(self, cypher):
        """
        Read data from Neo4j in specified cypher.
        The function depends on constructing dict method of dict(key = value) and any error may occur if the "key" is invalid to Python.
        you can choose function dictreaderopted() below to read data by hand(via the args "keys").
        :param cypher: string
            Valid query cypher statement.
        :return: list
            Each returned record constructs a dict in "key : value" pairs and stored in a big list, [{...}, {...}, ...].
        """
        tx = await self.pool.begin_transaction()
        data = []
        result = await tx.run(cypher)
        async for record in result.records():
            item = {}
            for args in str(record).split('>')[0].split()[1:]:
                exec
                'item.update(dict({0}))'.format(args)
            data.append(item)
        await self.pool.close()
        return data

    async def dictreaderopted(self, cypher, keys=None):
        """
        Optimized function of dictreader().
        Read and parse data straightly from cypher field result.
        :param cypher: string
            Valid query cypher statement.
        :param keys: list, default : none(call dictreader())
            Cypher query columns to return.
        :return: list.
            Each returned record constructs an dict in "key : value" pairs and stored in a list, [{...}, {...}, ...].
        """
        if not keys:
            return await self.dictreader(cypher)
        else:
            tx = await self.pool.begin_transaction()
            data = []
            result = await tx.run(cypher)
            async for record in result:
                item = {}
                for key in keys:
                    item.update({key: record[key]})
                data.append(item)
            await self.pool.close()
            return data

    async def cypherexecuter(self, cypher):
        """
        Execute manipulation into Neo4j in specified cypher.
        :param cypher: string
            Valid handle cypher statement.
        :return: none.
        """
        async with self.pool.begin_transaction() as tx:
            res = await tx.run(cypher)
        await self.pool.close()
        return res

    async def parse_relation_data(self, cql, result_list, id_key='id', name_key='name'):
        data = []
        num = 0
        stock_strike = True
        while stock_strike and num < 3:
            try:
                res = await self.listreader(cql, result_list)
                for item in res:
                    level = 1
                    if len(item) > 1:
                        if isinstance(item[1], list):
                            for item_item in item[1]:
                                relation_item = parse_relation_item(item_item, id_key, name_key, level)
                                level = level + 1
                                data.append(relation_item)
                        else:
                            relation_item = parse_relation_item(item[1], id_key, name_key, level)
                            data.append(relation_item)
                    elif isinstance(item[0], list):
                        for item_item in item[0]:
                            relation_item_list = parse_relation_item_more_relation(item_item, id_key, name_key)
                            data = data + relation_item_list
                    else:
                        relation_item_list = parse_relation_item_more_relation(item[0], id_key, name_key)
                        data = data + relation_item_list
                stock_strike = False
            except Exception:
                logging.error(traceback.format_exc())
            num = num + 1
        return data

    async def create_node(self, node_name: str, label_name: str, node_property: dict={}):
        sql = f'CREATE ({node_name}:{label_name} {dict_str(node_property)})'
        result = await self.execute_write(sql)
        return result

    async def create_node_relationship(self, relationship_list: list):
        sql = f'CREATE '
        sql += ','.join(relationship_list)
        result = await self.execute_write(sql)
        return result

    async def delete_node(self, node_name: str, label_name: str, match_property_dict: dict={}, node_property_dict: dict={}):
        sql = f'MATCH ({node_name}:{label_name}'
        if match_property_dict:
            sql += f'{dict_str(match_property_dict)})'
        else:
            sql += ')'
        if node_property_dict:
            node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
            sql += f' WHERE {node_property_str}'
        sql += f' DELETE {node_name}'
        result = await self.execute_write(sql)
        return result

    async def delete_property(self, node_name: str, label_name: str, delete_node_property_list: list, match_property_dict: dict={}, node_property_dict: dict={}):
        sql = f'MATCH ({node_name}:{label_name}'
        if match_property_dict:
            sql += f'{dict_str(match_property_dict)})'
        else:
            sql += ')'
        if node_property_dict:
            node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
            sql += f' WHERE {node_property_str}'
        delete_node_property_str = ','.join([f'{node_name}.{p}' for p in delete_node_property_list])
        sql += f' REMOVE {delete_node_property_str} RETURN {node_name}'
        result = await self.execute_write(sql)
        return result

    async def update_node(self, node_name: str, label_name: str, new_node_property_dict: dict, match_property_dict: dict={}, node_property_dict: dict={}):
        new_node_property_str = ','.join(['%s.%s=%r' % (node_name, property_name, property_value) for property_name, property_value in new_node_property_dict.items()])
        sql = f'MATCH ({node_name}:{label_name}'
        if match_property_dict:
            sql += f'{dict_str(match_property_dict)})'
        else:
            sql += ')'
        if node_property_dict:
            node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
            sql += f' WHERE {node_property_str}'
        sql += f' SET {new_node_property_str} RETURN {node_name}'
        result = await self.execute_write(sql)
        return result

    async def delete_two_node_relationship(self, relationship_name: str, relationship: str, node1_name: str=None, label1_name: str=None, node1_match_property_dict: dict={}, node2_name: str=None, label2_name: str=None, node2_match_property_dict: dict={}):
        if node1_name:
            if label1_name and (not node1_match_property_dict):
                sql = f'MATCH ({node1_name}:{label1_name}'
            elif node1_match_property_dict and (not label1_name):
                sql = f'MATCH ({node1_name} {dict_str(node1_match_property_dict)}'
            elif node1_match_property_dict and label1_name:
                sql = f'MATCH ({node1_name}:{label1_name} {dict_str(node1_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and match_property_dict')
            sql += ')'
        else:
            if label1_name and (not node1_match_property_dict):
                sql = f'MATCH ({label1_name}'
            elif node1_match_property_dict and label1_name:
                sql = f'MATCH ({label1_name} {dict_str(node1_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and node_name')
            sql += ')'
        node2_str = f'('
        if node2_name:
            if label2_name and (not node2_match_property_dict):
                node2_str += f'{node2_name}:{label2_name}'
            elif node2_match_property_dict and (not label2_name):
                node2_str += f'{node2_name} {dict_str(node2_match_property_dict)}'
            elif node2_match_property_dict and label2_name:
                node2_str += f'{node2_name}:{label2_name} {dict_str(node2_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label2_name and (not node2_match_property_dict):
            node2_str += f'{label2_name}'
        elif node2_match_property_dict and label2_name:
            node2_str += f'{label2_name} {dict_str(node2_match_property_dict)}'
        else:
            raise Exception('At least one of label_name and node_name')
        node2_str += ')'
        sql += f'{relationship}{node2_str} DELETE {relationship_name}'
        result = await self.execute_write(sql)
        return result

    async def delete_node_and_all_relationship(self, node_name: str=None, label_name: str=None, match_property_dict: dict={}, node_property_dict: dict={}):
        if node_name:
            if label_name and (not match_property_dict):
                sql = f'MATCH ({node_name}:{label_name})'
            elif match_property_dict and (not label_name):
                sql = f'MATCH ({node_name} {dict_str(match_property_dict)})'
            elif match_property_dict and label_name:
                sql = f'MATCH ({node_name}:{label_name} {dict_str(match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label_name and (not match_property_dict):
            sql = f'MATCH ({label_name})'
        elif match_property_dict and label_name:
            sql = f'MATCH ({label_name} {dict_str(match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        if node_name:
            sql += f' DETACH DELETE {node_name}'
        else:
            sql += f' DETACH DELETE {label_name}'
        result = await self.execute_write(sql)
        return result

    async def query_node_relationship(self, relationship: str, node1_name: str=None, label1_name: str=None, node1_match_property_dict: dict={}, property_dict: dict={}, node2_name: str=None, label2_name: str=None, node2_match_property_dict: dict={}, result_list: list=None):
        if node1_name:
            if label1_name and (not node1_match_property_dict):
                sql = f'MATCH ({node1_name}:{label1_name})'
            elif node1_match_property_dict and (not label1_name):
                sql = f'MATCH ({node1_name} {dict_str(node1_match_property_dict)})'
            elif node1_match_property_dict and label1_name:
                sql = f'MATCH ({node1_name}:{label1_name} {dict_str(node1_match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label1_name and (not node1_match_property_dict):
            sql = f'MATCH ({label1_name})'
        elif node1_match_property_dict and label1_name:
            sql = f'MATCH ({label1_name} {dict_str(node1_match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node2_str = f'('
        if node2_name:
            if label2_name and (not node2_match_property_dict):
                node2_str += f'{node2_name}:{label2_name}'
            elif node2_match_property_dict and (not label2_name):
                node2_str += f'{node2_name} {dict_str(node2_match_property_dict)}'
            elif node2_match_property_dict and label2_name:
                node2_str += f'{node2_name}:{label2_name} {dict_str(node2_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label2_name and (not node2_match_property_dict):
            node2_str += f'{label2_name}'
        elif node2_match_property_dict and label2_name:
            node2_str += f'{label2_name} {dict_str(node2_match_property_dict)}'
        else:
            raise Exception('At least one of label_name and node_name')
        node2_str += ')'
        sql += relationship
        sql += node2_str
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        if result_list:
            sql += f" RETURN {','.join(result_list)}"
        elif node1_name and (not node2_name) and label2_name:
            sql += f' RETURN {node1_name},{label2_name}'
        elif node1_name and node2_name:
            sql += f' RETURN {node1_name},{node2_name}'
        elif not node1_name and label1_name and node2_name:
            sql += f' RETURN {label1_name},{node2_name}'
        elif not node1_name and label1_name and (not node2_name) and label2_name:
            sql += f' RETURN {label1_name},{label2_name}'
        else:
            raise Exception('node1 and node2 are not exist')
        results = await self.pool.read_transaction(self.query_work, sql)
        await self.pool.close()
        records = []
        for record in results:
            records.append(parse_record(record, flag=True))
        return records

    async def query_all_node(self, node_name: str=None, label_name: str=None, match_property_dict: dict={}, node_property_dict: dict={}, result_list: list=None):
        if node_name:
            if label_name and (not match_property_dict):
                sql = f'MATCH ({node_name}:{label_name})'
            elif match_property_dict and (not label_name):
                sql = f'MATCH ({node_name} {dict_str(match_property_dict)})'
            elif match_property_dict and label_name:
                sql = f'MATCH ({node_name}:{label_name} {dict_str(match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label_name and (not match_property_dict):
            sql = f'MATCH ({label_name})'
        elif match_property_dict and label_name:
            sql = f'MATCH ({label_name} {dict_str(match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        if result_list:
            sql += f" RETURN {','.join(result_list)}"
        elif node_name:
            sql += f' RETURN {node_name}'
        else:
            sql += f' RETURN {label_name}'
        results = await self.pool.read_transaction(self.query_work, sql)
        records = []
        for record in results:
            records.append(parse_record(record, flag=False))
        await self.pool.close()
        return records

    async def query_node_count(self, node_name: str=None, label_name: str=None, match_property_dict: dict={}, node_property_dict: dict={}):
        if node_name:
            if label_name and (not match_property_dict):
                sql = f'MATCH ({node_name}:{label_name})'
            elif match_property_dict and (not label_name):
                sql = f'MATCH ({node_name} {dict_str(match_property_dict)})'
            elif match_property_dict and label_name:
                sql = f'MATCH ({node_name}:{label_name} {dict_str(match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label_name and (not match_property_dict):
            sql = f'MATCH ({label_name})'
        elif match_property_dict and label_name:
            sql = f'MATCH ({label_name} {dict_str(match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        sql = sql + ' RETURN COUNT(*)'
        result = await self.pool.read_transaction(self.query_work, sql)
        count = result[0].value()
        return count

    async def query_node_page(self, node_name: str=None, label_name: str=None, match_property_dict: dict={}, node_property_dict: dict={}, result_list: list=None, page_num: int=1, page_size: int=10):
        if node_name:
            if label_name and (not match_property_dict):
                sql = f'MATCH ({node_name}:{label_name})'
            elif match_property_dict and (not label_name):
                sql = f'MATCH ({node_name} {dict_str(match_property_dict)})'
            elif match_property_dict and label_name:
                sql = f'MATCH ({node_name}:{label_name} {dict_str(match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label_name and (not match_property_dict):
            sql = f'MATCH ({label_name})'
        elif match_property_dict and label_name:
            sql = f'MATCH ({label_name} {dict_str(match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        page_num = page_num if page_num > 1 else 1
        num = (page_num - 1) * page_size
        total = await self.query_node_count(node_name, label_name, match_property_dict, node_property_dict)
        if result_list:
            sql += f" RETURN {','.join(result_list)} SKIP {num} LIMIT {page_size}"
        elif node_name:
            sql += f' RETURN {node_name} SKIP {num} LIMIT {page_size}'
        else:
            sql += f' RETURN {label_name} SKIP {num} LIMIT {page_size}'
        results = await self.pool.read_transaction(self.query_work, sql)
        records = []
        for record in results:
            records.append(parse_record(record, flag=False))
        await self.pool.close()
        return Page(records=records, current=page_num, page_size=page_size, total=total).__dict__

    async def execute_fetchall(self, sql, flag=True):
        results = await self.pool.read_transaction(self.query_work, sql)
        records = []
        for record in results:
            records.append(parse_record(record, flag=flag))
        return records

    async def query_work(self, tx, sql):
        result = await tx.run(sql)
        return [record async for record in result]

    async def write_work(self, tx, sql):
        result = await tx.run(sql)
        return await result.consume()

    async def execute_write(self, sql):
        summary = await self.pool.write_transaction(self.sync_write_work, sql)
        res = eval(summary.counters.__repr__())
        await self.pool.close()
        return res

    def sync_listreader(self, cypher, keys):
        """
        Read data from Neo4j in specified cypher.
        Read and parse data straightly from cypher field result.
        :param cypher: string
            Valid query cypher statement.
        :param keys: list
            Cypher query columns to return.
        :return: list
            Each returned record constructs a list and stored in a big list, [[...], [...], ...].
        """
        data = []
        with self.pool.begin_transaction() as tx:
            result = tx.run(cypher)
            for record in result:
                rows = []
                for key in keys:
                    rows.append(record[key])
                data.append(rows)
        self.pool.close()
        return data

    def sync_dictreader(self, cypher):
        """
        Read data from Neo4j in specified cypher.
        The function depends on constructing dict method of dict(key = value) and any error may occur if the "key" is invalid to Python.
        you can choose function dictreaderopted() below to read data by hand(via the args "keys").
        :param cypher: string
            Valid query cypher statement.
        :return: list
            Each returned record constructs a dict in "key : value" pairs and stored in a big list, [{...}, {...}, ...].
        """
        data = []
        with self.pool.begin_transaction() as tx:
            for record in tx.run(cypher).records():
                item = {}
                for args in str(record).split('>')[0].split()[1:]:
                    exec
                    'item.update(dict({0}))'.format(args)
                data.append(item)
        return data

    def sync_dictreaderopted(self, cypher, keys=None):
        """
        Optimized function of dictreader().
        Read and parse data straightly from cypher field result.
        :param cypher: string
            Valid query cypher statement.
        :param keys: list, default : none(call dictreader())
            Cypher query columns to return.
        :return: list.
            Each returned record constructs an dict in "key : value" pairs and stored in a list, [{...}, {...}, ...].
        """
        if not keys:
            return self.sync_dictreader(cypher)
        else:
            data = []
            with self.pool.begin_transaction() as tx:
                result = tx.run(cypher)
                for record in result:
                    item = {}
                    for key in keys:
                        item.update({key: record[key]})
                    data.append(item)
            return data

    def sync_cypherexecuter(self, cypher):
        """
        Execute manipulation into Neo4j in specified cypher.
        :param cypher: string
            Valid handle cypher statement.
        :return: none.
        """
        with self.pool.begin_transaction() as tx:
            return tx.run(cypher)

    def sync_parse_relation_data(self, cql, result_list, id_key='id', name_key='name'):
        data = []
        num = 0
        stock_strike = True
        while stock_strike and num < 3:
            try:
                res = self.sync_listreader(cql, result_list)
                for item in res:
                    level = 1
                    if len(item) > 1:
                        if isinstance(item[1], list):
                            for item_item in item[1]:
                                relation_item = parse_relation_item(item_item, id_key, name_key, level)
                                level = level + 1
                                data.append(relation_item)
                        else:
                            relation_item = parse_relation_item(item[1], id_key, name_key, level)
                            data.append(relation_item)
                    elif isinstance(item[0], list):
                        for item_item in item[0]:
                            relation_item_list = parse_relation_item_more_relation(item_item, id_key, name_key)
                            data = data + relation_item_list
                    else:
                        relation_item_list = parse_relation_item_more_relation(item[0], id_key, name_key)
                        data = data + relation_item_list
                stock_strike = False
            except Exception:
                logging.error(traceback.format_exc())
            num = num + 1
        return data

    def sync_create_node(self, node_name: str, label_name: str, node_property: dict={}):
        sql = f'CREATE ({node_name}:{label_name} {dict_str(node_property)})'
        result = self.sync_execute_write(sql)
        return result

    def sync_create_node_relationship(self, relationship_list: list):
        sql = f'CREATE '
        sql += ','.join(relationship_list)
        result = self.sync_execute_write(sql)
        return result

    def sync_delete_node(self, node_name: str, label_name: str, match_property_dict: dict={}, node_property_dict: dict={}):
        sql = f'MATCH ({node_name}:{label_name}'
        if match_property_dict:
            sql += f'{dict_str(match_property_dict)})'
        else:
            sql += ')'
        if node_property_dict:
            node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
            sql += f' WHERE {node_property_str}'
        sql += f' DELETE {node_name}'
        result = self.sync_execute_write(sql)
        return result

    def sync_delete_property(self, node_name: str, label_name: str, delete_node_property_list: list, match_property_dict: dict={}, node_property_dict: dict={}):
        sql = f'MATCH ({node_name}:{label_name}'
        if match_property_dict:
            sql += f'{dict_str(match_property_dict)})'
        else:
            sql += ')'
        if node_property_dict:
            node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
            sql += f' WHERE {node_property_str}'
        delete_node_property_str = ','.join([f'{node_name}.{p}' for p in delete_node_property_list])
        sql += f' REMOVE {delete_node_property_str} RETURN {node_name}'
        result = self.sync_execute_write(sql)
        return result

    def sync_update_node(self, node_name: str, label_name: str, new_node_property_dict: dict, match_property_dict: dict={}, node_property_dict: dict={}):
        new_node_property_str = ','.join(['%s.%s=%r' % (node_name, property_name, property_value) for property_name, property_value in new_node_property_dict.items()])
        sql = f'MATCH ({node_name}:{label_name}'
        if match_property_dict:
            sql += f'{dict_str(match_property_dict)})'
        else:
            sql += ')'
        if node_property_dict:
            node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
            sql += f' WHERE {node_property_str}'
        sql += f' SET {new_node_property_str} RETURN {node_name}'
        result = self.sync_execute_write(sql)
        return result

    def sync_delete_two_node_relationship(self, relationship_name: str, relationship: str, node1_name: str=None, label1_name: str=None, node1_match_property_dict: dict={}, node2_name: str=None, label2_name: str=None, node2_match_property_dict: dict={}):
        if node1_name:
            if label1_name and (not node1_match_property_dict):
                sql = f'MATCH ({node1_name}:{label1_name}'
            elif node1_match_property_dict and (not label1_name):
                sql = f'MATCH ({node1_name} {dict_str(node1_match_property_dict)}'
            elif node1_match_property_dict and label1_name:
                sql = f'MATCH ({node1_name}:{label1_name} {dict_str(node1_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and match_property_dict')
            sql += ')'
        else:
            if label1_name and (not node1_match_property_dict):
                sql = f'MATCH ({label1_name}'
            elif node1_match_property_dict and label1_name:
                sql = f'MATCH ({label1_name} {dict_str(node1_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and node_name')
            sql += ')'
        node2_str = f'('
        if node2_name:
            if label2_name and (not node2_match_property_dict):
                node2_str += f'{node2_name}:{label2_name}'
            elif node2_match_property_dict and (not label2_name):
                node2_str += f'{node2_name} {dict_str(node2_match_property_dict)}'
            elif node2_match_property_dict and label2_name:
                node2_str += f'{node2_name}:{label2_name} {dict_str(node2_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label2_name and (not node2_match_property_dict):
            node2_str += f'{label2_name}'
        elif node2_match_property_dict and label2_name:
            node2_str += f'{label2_name} {dict_str(node2_match_property_dict)}'
        else:
            raise Exception('At least one of label_name and node_name')
        node2_str += ')'
        sql += f'{relationship}{node2_str} DELETE {relationship_name}'
        result = self.sync_execute_write(sql)
        return result

    def sync_delete_node_and_all_relationship(self, node_name: str=None, label_name: str=None, match_property_dict: dict={}, node_property_dict: dict={}):
        if node_name:
            if label_name and (not match_property_dict):
                sql = f'MATCH ({node_name}:{label_name})'
            elif match_property_dict and (not label_name):
                sql = f'MATCH ({node_name} {dict_str(match_property_dict)})'
            elif match_property_dict and label_name:
                sql = f'MATCH ({node_name}:{label_name} {dict_str(match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label_name and (not match_property_dict):
            sql = f'MATCH ({label_name})'
        elif match_property_dict and label_name:
            sql = f'MATCH ({label_name} {dict_str(match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        if node_name:
            sql += f' DETACH DELETE {node_name}'
        else:
            sql += f' DETACH DELETE {label_name}'
        result = self.sync_execute_write(sql)
        return result

    def sync_query_node_relationship(self, relationship: str, node1_name: str=None, label1_name: str=None, node1_match_property_dict: dict={}, property_dict: dict={}, node2_name: str=None, label2_name: str=None, node2_match_property_dict: dict={}, result_list: list=None):
        if node1_name:
            if label1_name and (not node1_match_property_dict):
                sql = f'MATCH ({node1_name}:{label1_name}'
            elif node1_match_property_dict and (not label1_name):
                sql = f'MATCH ({node1_name} {dict_str(node1_match_property_dict)}'
            elif node1_match_property_dict and label1_name:
                sql = f'MATCH ({node1_name}:{label1_name} {dict_str(node1_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and match_property_dict')
            sql += ')'
        else:
            if label1_name and (not node1_match_property_dict):
                sql = f'MATCH ({label1_name}'
            elif node1_match_property_dict and label1_name:
                sql = f'MATCH ({label1_name} {dict_str(node1_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and node_name')
            sql += ')'
        node2_str = f'('
        if node2_name:
            if label2_name and (not node2_match_property_dict):
                node2_str += f'{node2_name}:{label2_name}'
            elif node2_match_property_dict and (not label2_name):
                node2_str += f'{node2_name} {dict_str(node2_match_property_dict)}'
            elif node2_match_property_dict and label2_name:
                node2_str += f'{node2_name}:{label2_name} {dict_str(node2_match_property_dict)}'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label2_name and (not node2_match_property_dict):
            node2_str += f'{label2_name}'
        elif node2_match_property_dict and label2_name:
            node2_str += f'{label2_name} {dict_str(node2_match_property_dict)}'
        else:
            raise Exception('At least one of label_name and node_name')
        node2_str += ')'
        sql += relationship
        sql += node2_str
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        if result_list:
            sql += f" RETURN {','.join(result_list)}"
        elif node1_name and (not node2_name) and label2_name:
            sql += f' RETURN {node1_name},{label2_name}'
        elif node1_name and node2_name:
            sql += f' RETURN {node1_name},{node2_name}'
        elif not node1_name and label1_name and node2_name:
            sql += f' RETURN {label1_name},{node2_name}'
        elif not node1_name and label1_name and (not node2_name) and label2_name:
            sql += f' RETURN {label1_name},{label2_name}'
        else:
            raise Exception('node1 and node2 are not exist')
        results = self.pool.read_transaction(self.sync_query_work, sql)
        records = []
        for record in results:
            records.append(parse_record(record, flag=True))
        return records

    def sync_query_all_node(self, node_name: str=None, label_name: str=None, match_property_dict: dict={}, node_property_dict: dict={}, result_list: list=None):
        if node_name:
            if label_name and (not match_property_dict):
                sql = f'MATCH ({node_name}:{label_name})'
            elif match_property_dict and (not label_name):
                sql = f'MATCH ({node_name} {dict_str(match_property_dict)})'
            elif match_property_dict and label_name:
                sql = f'MATCH ({node_name}:{label_name} {dict_str(match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label_name and (not match_property_dict):
            sql = f'MATCH ({label_name})'
        elif match_property_dict and label_name:
            sql = f'MATCH ({label_name} {dict_str(match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        if result_list:
            sql += f" RETURN {','.join(result_list)}"
        elif node_name:
            sql += f' RETURN {node_name}'
        else:
            sql += f' RETURN {label_name}'
        results = self.pool.read_transaction(self.sync_query_work, sql)
        records = []
        for record in results:
            records.append(parse_record(record, flag=False))
        return records

    def sync_query_node_count(self, node_name: str=None, label_name: str=None, match_property_dict: dict={}, node_property_dict: dict={}):
        if node_name:
            if label_name and (not match_property_dict):
                sql = f'MATCH ({node_name}:{label_name})'
            elif match_property_dict and (not label_name):
                sql = f'MATCH ({node_name} {dict_str(match_property_dict)})'
            elif match_property_dict and label_name:
                sql = f'MATCH ({node_name}:{label_name} {dict_str(match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label_name and (not match_property_dict):
            sql = f'MATCH ({label_name})'
        elif match_property_dict and label_name:
            sql = f'MATCH ({label_name} {dict_str(match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        sql = sql + ' RETURN COUNT(*)'
        count = self.pool.read_transaction(self.sync_query_work, sql)[0].value()
        return count

    def sync_query_node_page(self, node_name: str=None, label_name: str=None, match_property_dict: dict={}, node_property_dict: dict={}, result_list: list=None, page_num: int=1, page_size: int=10):
        if node_name:
            if label_name and (not match_property_dict):
                sql = f'MATCH ({node_name}:{label_name})'
            elif match_property_dict and (not label_name):
                sql = f'MATCH ({node_name} {dict_str(match_property_dict)})'
            elif match_property_dict and label_name:
                sql = f'MATCH ({node_name}:{label_name} {dict_str(match_property_dict)})'
            else:
                raise Exception('At least one of label_name and match_property_dict')
        elif label_name and (not match_property_dict):
            sql = f'MATCH ({label_name})'
        elif match_property_dict and label_name:
            sql = f'MATCH ({label_name} {dict_str(match_property_dict)})'
        else:
            raise Exception('At least one of label_name and node_name')
        node_property_str = ','.join(['%s=%r' % (property_name, property_value) for property_name, property_value in node_property_dict.items()])
        if node_property_str:
            sql += f' WHERE {node_property_str}'
        page_num = page_num if page_num > 1 else 1
        num = (page_num - 1) * page_size
        total = self.sync_query_node_count(node_name, label_name, match_property_dict, node_property_dict)
        if result_list:
            sql += f" RETURN {','.join(result_list)} SKIP {num} LIMIT {page_size}"
        elif node_name:
            sql += f' RETURN {node_name} SKIP {num} LIMIT {page_size}'
        else:
            sql += f' RETURN {label_name} SKIP {num} LIMIT {page_size}'
        results = self.pool.read_transaction(self.sync_query_work, sql)
        records = []
        for record in results:
            records.append(parse_record(record, flag=False))
        self.pool.close()
        return Page(records=records, current=page_num, page_size=page_size, total=total).__dict__

    def sync_query_work(self, tx, sql):
        return list(tx.run(sql))

    def sync_execute_fetchall(self, sql, flag=True):
        results = self.pool.read_transaction(self.sync_query_work, sql)
        records = []
        for record in results:
            records.append(parse_record(record, flag=flag))
        self.pool.close()
        return records

    def sync_write_work(self, tx, sql):
        return tx.run(sql).consume()

    def sync_execute_write(self, sql):
        summary = self.pool.write_transaction(self.sync_write_work, sql)
        res = eval(summary.counters.__repr__())
        self.pool.close()
        return res

def parse_relation_item(item, id_key, name_key, level=0):
    relation_item = {'start_node': parse_node_dict(item.start_node, id_key, name_key), 'end_node': parse_node_dict(item.end_node, id_key, name_key), 'type': item.type, 'level': level, 'properties': item._properties}
    return relation_item

def parse_relation_item_more_relation(item, id_key, name_key):
    relation_item_list = []
    for data in item._relationships:
        relation_item_list.append(parse_relation_item(data, id_key, name_key))
    return relation_item_list

def parse_node_dict(node, id_key, name_key):
    return {'id': AES.encrypt(options.aes_key, node._properties[id_key]), 'name': node._properties[name_key], 'label': list(node._labels)[0]}

def dict_str(data: dict):
    ls = []
    for k, v in data.items():
        ls.append('%s:%r' % (k, v))
    string = '{' + ','.join(ls) + '}'
    return string

def node2dict(node: neo4j.data.Node):
    return {'id': node.id, 'labels': list(node.labels), 'properties': node._properties}

def relationship2dict(relationship: neo4j.data.Relationship):
    return {'start_node': node2dict(relationship.start_node), 'end_node': node2dict(relationship.end_node), 'id': relationship.id, 'type': relationship.type, 'properties': relationship._properties}

def path2dict(path: neo4j.graph.Path):
    return {'start_node': node2dict(path.start_node), 'end_node': node2dict(path.end_node), 'nodes': [node2dict(n) for n in path.nodes], 'relationships': [relationship2dict(r) for r in path.relationships]}

def parse_record(record: neo4j.data.Record, flag=True):
    _record = {'node': [], 'relationship': [], 'path': [], 'other': []}
    if isinstance(record, neo4j.data.Record):
        for rd in record:
            if isinstance(rd, neo4j.data.Node):
                _record['node'].append(node2dict(rd))
            elif issubclass(rd.__class__, neo4j.data.Node):
                _record['node'].append(node2dict(rd))
            elif isinstance(rd, neo4j.data.Relationship):
                _record['relationship'].append(relationship2dict(rd))
            elif issubclass(rd.__class__, neo4j.data.Relationship):
                _record['relationship'].append(relationship2dict(rd))
            elif isinstance(rd, list) or isinstance(rd, tuple):
                for x in rd:
                    if isinstance(x, neo4j.data.Node):
                        _record['node'].append(node2dict(x))
                    elif issubclass(x.__class__, neo4j.data.Node):
                        _record['node'].append(node2dict(x))
                    elif isinstance(x, neo4j.data.Relationship):
                        _record['relationship'].append(relationship2dict(x))
                    elif issubclass(x.__class__, neo4j.data.Relationship):
                        _record['relationship'].append(relationship2dict(x))
                    elif isinstance(rd, neo4j.graph.Path):
                        _record['path'].append(path2dict(rd))
                    else:
                        _record['other'].append(rd)
            elif isinstance(rd, neo4j.graph.Path):
                _record['path'].append(path2dict(rd))
            else:
                _record['other'].append(rd)
    if not flag:
        _record.pop('relationship')
    return _record