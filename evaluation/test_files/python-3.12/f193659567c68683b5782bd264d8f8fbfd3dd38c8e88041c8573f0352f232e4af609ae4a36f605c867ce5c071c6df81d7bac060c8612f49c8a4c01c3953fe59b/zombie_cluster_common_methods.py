import json
import os
from ast import literal_eval
from copy import deepcopy
import boto3
from cloud_governance.common.ldap.ldap_search import LdapSearch
from cloud_governance.common.logger.init_logger import logger
from cloud_governance.common.mails.mail_message import MailMessage
from cloud_governance.common.mails.postfix import Postfix

class ZombieClusterCommonMethods:
    DAYS_TO_TRIGGER_RESOURCE_MAIL = 4
    DAYS_TO_DELETE_RESOURCE = 7

    def __init__(self, region: str):
        self.region = region
        self.dry_run = os.environ.get('dry_run', 'yes')
        self.policy = os.environ.get('policy', '')
        self.ec2_client = boto3.client('ec2', region_name=region)
        self.ec2_resource = boto3.resource('ec2', region_name=region)
        self.elb_client = boto3.client('elb', region_name=region)
        self.elbv2_client = boto3.client('elbv2', region_name=region)
        self.iam_client = boto3.client('iam', region_name=region)
        self.s3_client = boto3.client('s3')
        self.s3_resource = boto3.resource('s3')
        self.__ldap_host_name = os.environ.get('LDAP_HOST_NAME', '')
        self._special_user_mails = os.environ.get('special_user_mails', '{}')
        self._account_admin = os.environ.get('account_admin', '')
        self._ldap = LdapSearch(ldap_host_name=self.__ldap_host_name)
        self._mail = Postfix()
        self._mail_description = MailMessage()

    def _literal_eval(self, data: any):
        tags = {}
        if data:
            tags = literal_eval(data)
        return tags

    def get_tag_name_from_tags(self, tags: list, tag_name: str):
        """
        This method return tag_name from resource_tags
        @param tags:
        @param tag_name:
        @return:
        """
        if tags:
            for tag in tags:
                if tag.get('Key') == tag_name:
                    return tag.get('Value')
        return ''

    def get_zombie_cluster_user_tag(self, zombies: dict, resources: list, resource_id: str, tag: str='Tags'):
        """
        This method returns the zombie_cluster tag and with user_tag i.e {cluster_tag: user_name}
        @param zombies:
        @param resources:
        @param resource_id:
        @return:
        """
        zombie_cluster_user_tag = {}
        for resource in resources:
            zombie_id = resource.get(resource_id)
            if zombie_id in zombies:
                zombie_cluster_user_tag[zombies[zombie_id]] = self.get_tag_name_from_tags(tags=resource.get(tag), tag_name='User')
        return zombie_cluster_user_tag

    def _get_tags_of_zombie_resources(self, resources: list, resource_id_name: str, zombies: dict, aws_service: str, aws_tag: str='Tags'):
        """
        This method return tags of the resource i.e {resource_id: tags}
        @param resources:
        @param tags:
        @return:
        """
        resources_tags = {}
        for resource in resources:
            aws_tags = []
            resource_id = resource.get(resource_id_name)
            if aws_service == 'elbv1':
                try:
                    aws_tags = self.elb_client.describe_tags(LoadBalancerNames=[resource_id]).get('TagDescriptions')
                    if len(aws_tags) > 0:
                        aws_tags = aws_tags[0].get(aws_tag)
                except:
                    return []
            elif aws_service == 'elbv2':
                try:
                    aws_tags = self.elbv2_client.describe_tags(ResourceArns=[resource_id]).get('TagDescriptions')
                    if len(aws_tags) > 0:
                        aws_tags = aws_tags[0].get(aws_tag)
                except:
                    return []
            elif aws_service == 'role' and resource_id in zombies:
                try:
                    role_data = self.iam_client.get_role(RoleName=resource_id)['Role']
                    if role_data.get(aws_tag):
                        aws_tags = role_data.get(aws_tag)
                except:
                    return []
            elif aws_service == 'user' and resource_id in zombies:
                try:
                    user_data = self.iam_client.get_user(UserName=resource_id)['User']
                    if user_data.get(aws_tag):
                        aws_tags = user_data.get(aws_tag)
                except Exception as err:
                    return []
            elif aws_service == 'bucket' and resource_id in zombies:
                try:
                    bucket_data = self.s3_client.get_bucket_tagging(Bucket=resource_id)
                    if bucket_data.get(aws_tag):
                        aws_tags = bucket_data.get(aws_tag)
                except Exception as err:
                    return []
            elif resource.get(aws_tag):
                aws_tags = resource.get(aws_tag)
            if aws_tags:
                old_tags = deepcopy(aws_tags)
                tags = aws_tags[:]
                cluster_delete_days = self.get_tag_name_from_tags(tags=tags, tag_name='ClusterDeleteDays')
                if cluster_delete_days:
                    if resource_id in zombies:
                        tags = self.update_resource_tags(tags=tags, tag_name='ClusterDeleteDays', tag_value=str(int(cluster_delete_days) + 1))
                    else:
                        tags = self.update_resource_tags(tags=tags, tag_name='ClusterDeleteDays', tag_value=str(0))
                elif resource_id in zombies:
                    tags = self.update_resource_tags(tags=tags, tag_name='ClusterDeleteDays', tag_value=str(1))
                if old_tags != tags:
                    try:
                        if aws_service == 'ec2':
                            self.ec2_client.create_tags(Resources=[resource_id], Tags=tags)
                        elif aws_service == 'elbv1':
                            self.elb_client.add_tags(LoadBalancerNames=[resource_id], Tags=tags)
                        elif aws_service == 'elbv2':
                            self.elbv2_client.add_tags(ResourceArns=[resource_id], Tags=tags)
                        elif aws_service == 'role':
                            self.iam_client.tag_role(RoleName=resource_id, Tags=tags)
                        elif aws_service == 'user':
                            self.iam_client.tag_user(UserName=resource_id, Tags=tags)
                        elif aws_service == 'bucket':
                            self.s3_client.put_bucket_tagging(Bucket=resource_id, Tagging={'TagSet': tags})
                    except:
                        return []
                if resource_id in zombies:
                    resources_tags[resource_id] = tags
        return resources_tags

    def update_resource_tags(self, tags: list, tag_name: str, tag_value: str):
        """
        This method updates tags of the resource
        @param tags:
        @param tag_name:
        @param tag_value:
        @param resource_id:
        @return:
        """
        found = False
        if tags:
            for tag in tags:
                if tag.get('Key') == tag_name:
                    tag['Value'] = str(tag_value)
                    found = True
            if not found:
                tags.append({'Key': tag_name, 'Value': str(tag_value)})
            return tags
        return [{'Key': tag_name, 'Value': str(tag_value)}]

    def get_cluster_delete_days(self, tags: list) -> int:
        """
        This method return the ClusterDeleteDays tag
        @param tags:
        @return:
        """
        cluster_delete_days = self.get_tag_name_from_tags(tags=tags, tag_name='ClusterDeleteDays')
        if not cluster_delete_days:
            cluster_delete_days = 1
        else:
            cluster_delete_days = int(cluster_delete_days) + 1
        return cluster_delete_days

    def trigger_mail(self, tags: list, resource_id: str, days: int, resources: list):
        """
        This method send triggering mail
        @param resources:
        @param days:
        @param tags:
        @param resource_id:
        @return:
        """
        try:
            special_user_mails = self._literal_eval(self._special_user_mails)
            user, resource_name = (self.get_tag_name_from_tags(tags=tags, tag_name='User'), self.get_tag_name_from_tags(tags=tags, tag_name='Name'))
            if not resource_name:
                resource_name = self.get_tag_name_from_tags(tags=tags, tag_name='cg-Name')
            to = user if user not in special_user_mails else special_user_mails[user]
            ldap_data = self._ldap.get_user_details(user_name=to)
            cc = [self._account_admin, f"{ldap_data.get('managerId')}@redhat.com"]
            name = to
            if ldap_data:
                name = ldap_data.get('displayName')
            file_name = os.path.join('/tmp', f"{resource_name.replace('/', '-')}.json")
            with open(file_name, 'w') as file:
                json.dump(resources, file, indent=4)
            subject, body = self._mail_description.zombie_cluster_mail_message(name=name, days=days, notification_days=self.DAYS_TO_TRIGGER_RESOURCE_MAIL, resource_name=resource_name, delete_days=self.DAYS_TO_DELETE_RESOURCE)
            self._mail.send_email_postfix(to=to, content=body, subject=subject, cc=cc, resource_id=resource_id, filename=file_name)
        except Exception as err:
            logger.info(err)

    def collect_notify_cluster_data(self, resource_data: dict, cluster_left_out_days: dict, notify_data: dict, delete_data: dict, cluster_data: dict, func_name: str):
        """
        This method store the notify_data, delete_data of clusters
        @param func_name:
        @param cluster_data:
        @param resource_data:
        @param cluster_left_out_days:
        @param notify_data:
        @param delete_data:
        @return:
        """
        notify_tag_data = {}
        delete_tag_data = {}
        cluster_tags = set()
        for resource_id, cluster_tag in resource_data.items():
            if cluster_tag in cluster_left_out_days:
                cluster_tags.add(cluster_tag)
                zombie_days = int(self.get_tag_name_from_tags(tags=cluster_left_out_days[cluster_tag], tag_name='ClusterDeleteDays'))
                if zombie_days == self.DAYS_TO_TRIGGER_RESOURCE_MAIL:
                    notify_tag_data.setdefault(cluster_tag, []).append(resource_id)
                elif zombie_days >= self.DAYS_TO_DELETE_RESOURCE:
                    delete_tag_data.setdefault(cluster_tag, []).append(resource_id)
                if cluster_tag not in cluster_data:
                    cluster_data[cluster_tag] = cluster_left_out_days[cluster_tag]
        for cluster_tag in cluster_tags:
            if cluster_tag in cluster_left_out_days:
                if cluster_tag in notify_tag_data:
                    notify_data.setdefault(cluster_tag, []).append({func_name: notify_tag_data[cluster_tag]})
                if cluster_tag in delete_tag_data:
                    delete_data.setdefault(cluster_tag, []).append({func_name: delete_tag_data[cluster_tag]})
        return (notify_data, delete_data, cluster_data)

    def send_mails_to_cluster_user(self, notify_data: dict, delete_data: dict, cluster_data: dict):
        """
        This method send mail to the user to notify cluster status
        @param cluster_data:
        @param notify_data:
        @param delete_data:
        @return:
        """
        for cluster_tag, resource_ids in notify_data.items():
            self.update_resource_tags(tags=cluster_data[cluster_tag], tag_name='Name', tag_value=cluster_tag)
            self.trigger_mail(tags=cluster_data[cluster_tag], resource_id='Cluster', days=self.DAYS_TO_TRIGGER_RESOURCE_MAIL, resources=resource_ids)
        for cluster_tag, resource_ids in delete_data.items():
            self.update_resource_tags(tags=cluster_data[cluster_tag], tag_name='Name', tag_value=cluster_tag)
            self.trigger_mail(tags=cluster_data[cluster_tag], resource_id='Cluster', days=self.DAYS_TO_DELETE_RESOURCE, resources=resource_ids)

    def _check_zombie_cluster_deleted_days(self, resources: dict, cluster_left_out_days: dict, zombie: str, cluster_tag: str):
        """
        This method check the cluster delete days and return the clusters
        @param resources:
        @param cluster_left_out_days:
        @return:
        """
        delete_cluster_resource = False
        if resources:
            cluster_delete_days = int(self.get_tag_name_from_tags(tags=resources[zombie], tag_name='ClusterDeleteDays'))
            if cluster_tag not in cluster_left_out_days:
                cluster_left_out_days[cluster_tag] = resources[zombie]
            if cluster_delete_days >= self.DAYS_TO_DELETE_RESOURCE:
                delete_cluster_resource = True
        return (cluster_left_out_days, delete_cluster_resource)