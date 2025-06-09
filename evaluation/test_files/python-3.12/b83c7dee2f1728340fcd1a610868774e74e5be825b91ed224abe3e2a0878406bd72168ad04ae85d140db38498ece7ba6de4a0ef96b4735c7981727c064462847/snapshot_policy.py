import logging
import requests
from PyPowerFlex import base_client
from PyPowerFlex import exceptions
LOG = logging.getLogger(__name__)

class AutoSnapshotRemovalAction:
    """Auto snapshot deletion strategy."""
    detach = 'Detach'
    remove = 'Remove'

class SnapshotPolicy(base_client.EntityRequest):

    def add_source_volume(self, snapshot_policy_id, volume_id):
        """Add source volume to PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type volume_id: str
        :rtype: dict
        """
        action = 'addSourceVolumeToSnapshotPolicy'
        params = dict(sourceVolumeId=volume_id)
        r, response = self.send_post_request(self.base_action_url, action=action, entity=self.entity, entity_id=snapshot_policy_id, params=params)
        if r.status_code != requests.codes.ok:
            msg = 'Failed to add source volume to PowerFlex {entity} with id {_id}. Error: {response}'.format(entity=self.entity, _id=snapshot_policy_id, response=response)
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return self.get(entity_id=snapshot_policy_id)

    def create(self, auto_snap_creation_cadence_in_min, retained_snaps_per_level, name=None, paused=None):
        """Create PowerFlex snapshot policy.

        :type auto_snap_creation_cadence_in_min: int
        :type retained_snaps_per_level: list[int]
        :type name: str
        :type paused: bool
        :rtype: dict
        """
        params = dict(autoSnapshotCreationCadenceInMin=auto_snap_creation_cadence_in_min, numOfRetainedSnapshotsPerLevel=retained_snaps_per_level, name=name, paused=paused)
        return self._create_entity(params)

    def delete(self, snapshot_policy_id):
        """Remove PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :rtype: None
        """
        return self._delete_entity(snapshot_policy_id)

    def modify(self, snapshot_policy_id, auto_snap_creation_cadence_in_min, retained_snaps_per_level):
        """Modify PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type auto_snap_creation_cadence_in_min: int
        :type retained_snaps_per_level: list[int]
        :rtype: dict
        """
        action = 'modifySnapshotPolicy'
        params = dict(autoSnapshotCreationCadenceInMin=auto_snap_creation_cadence_in_min, numOfRetainedSnapshotsPerLevel=retained_snaps_per_level)
        r, response = self.send_post_request(self.base_action_url, action=action, entity=self.entity, entity_id=snapshot_policy_id, params=params)
        if r.status_code != requests.codes.ok:
            msg = 'Failed to modify PowerFlex {entity} with id {_id}. Error: {response}'.format(entity=self.entity, _id=snapshot_policy_id, response=response)
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return self.get(entity_id=snapshot_policy_id)

    def pause(self, snapshot_policy_id):
        """Pause PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :rtype: dict
        """
        action = 'pauseSnapshotPolicy'
        r, response = self.send_post_request(self.base_action_url, action=action, entity=self.entity, entity_id=snapshot_policy_id)
        if r.status_code != requests.codes.ok:
            msg = 'Failed to pause PowerFlex {entity} with id {_id}. Error: {response}'.format(entity=self.entity, _id=snapshot_policy_id, response=response)
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return self.get(entity_id=snapshot_policy_id)

    def remove_source_volume(self, snapshot_policy_id, volume_id, auto_snap_removal_action, detach_locked_auto_snaps=None):
        """Remove source volume from PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type volume_id: str
        :param auto_snap_removal_action: one of predefined attributes of
                                         AutoSnapshotRemovalAction
        :type auto_snap_removal_action: str
        :type detach_locked_auto_snaps: bool
        :rtype: dict
        """
        action = 'removeSourceVolumeFromSnapshotPolicy'
        params = dict(sourceVolumeId=volume_id, autoSnapshotRemovalAction=auto_snap_removal_action, detachLockedAutoSnapshots=detach_locked_auto_snaps)
        r, response = self.send_post_request(self.base_action_url, action=action, entity=self.entity, entity_id=snapshot_policy_id, params=params)
        if r.status_code != requests.codes.ok:
            msg = 'Failed to remove source volume from PowerFlex {entity} with id {_id}. Error: {response}'.format(entity=self.entity, _id=snapshot_policy_id, response=response)
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return self.get(entity_id=snapshot_policy_id)

    def rename(self, snapshot_policy_id, name):
        """Rename PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :type name: str
        :rtype: dict
        """
        action = 'renameSnapshotPolicy'
        params = dict(newName=name)
        return self._rename_entity(action, snapshot_policy_id, params)

    def resume(self, snapshot_policy_id):
        """Resume PowerFlex snapshot policy.

        :type snapshot_policy_id: str
        :rtype: dict
        """
        action = 'resumeSnapshotPolicy'
        r, response = self.send_post_request(self.base_action_url, action=action, entity=self.entity, entity_id=snapshot_policy_id)
        if r.status_code != requests.codes.ok:
            msg = 'Failed to resume PowerFlex {entity} with id {_id}. Error: {response}'.format(entity=self.entity, _id=snapshot_policy_id, response=response)
            LOG.error(msg)
            raise exceptions.PowerFlexClientException(msg)
        return self.get(entity_id=snapshot_policy_id)