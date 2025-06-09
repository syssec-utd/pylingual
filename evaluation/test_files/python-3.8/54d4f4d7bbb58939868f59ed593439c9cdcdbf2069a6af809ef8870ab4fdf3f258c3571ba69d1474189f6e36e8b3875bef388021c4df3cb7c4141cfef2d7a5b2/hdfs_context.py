from dpdispatcher.base_context import BaseContext
import os, shutil, hashlib, tarfile
from glob import glob
from dpdispatcher import dlog
from dpdispatcher.hdfs_cli import HDFS

class HDFSContext(BaseContext):

    def __init__(self, local_root, remote_root, remote_profile={}, *args, **kwargs):
        assert type(local_root) == str
        self.init_local_root = local_root
        self.init_remote_root = remote_root
        self.temp_local_root = os.path.abspath(local_root)
        self.temp_remote_root = remote_root
        self.remote_profile = remote_profile

    @classmethod
    def load_from_dict(cls, context_dict):
        local_root = context_dict['local_root']
        remote_root = context_dict['remote_root']
        remote_profile = context_dict.get('remote_profile', {})
        instance = cls(local_root=local_root, remote_root=remote_root, remote_profile=remote_profile)
        return instance

    def get_job_root(self):
        return self.remote_root

    def bind_submission(self, submission):
        self.submission = submission
        self.local_root = os.path.join(self.temp_local_root, submission.work_base)
        self.remote_root = os.path.join(self.temp_remote_root, submission.submission_hash)
        HDFS.mkdir(self.remote_root)

    def _put_files(self, files, dereference=True):
        of = self.submission.submission_hash + '_upload.tgz'
        if os.path.isfile(os.path.join(self.local_root, of)):
            os.remove(os.path.join(self.local_root, of))
        with tarfile.open(os.path.join(self.local_root, of), 'w:gz', dereference=dereference) as tar:
            for ii in files:
                ii_full = os.path.join(self.local_root, ii)
                tar.add(ii_full, arcname=ii)
        from_f = os.path.join(self.local_root, of)
        HDFS.copy_from_local(os.path.join(self.local_root, of), self.remote_root)
        os.remove(from_f)

    def upload(self, submission, dereference=True):
        """ upload forward files and forward command files to HDFS root dir

        Parameters
        ----------
        submission : Submission class instance
            represents a collection of tasks, such as forward file names

        Returns
        -------
        none
        """
        file_list = []
        for task in submission.belonging_tasks:
            local_job = os.path.join(self.local_root, task.task_work_path)
            for ff in task.forward_files:
                abs_file_list = glob(os.path.join(local_job, ff))
                if not abs_file_list:
                    raise RuntimeError('cannot find upload file ' + os.path.join(local_job, ff))
                rel_file_list = [os.path.relpath(ii, self.local_root) for ii in abs_file_list]
                file_list.extend(rel_file_list)
        local_job = self.local_root
        for fc in submission.forward_common_files:
            abs_file_list = glob(os.path.join(local_job, fc))
            if not abs_file_list:
                raise RuntimeError('cannot find upload file ' + os.path.join(local_job, fc))
            rel_file_list = [os.path.relpath(ii, self.local_root) for ii in abs_file_list]
            file_list.extend(rel_file_list)
        self._put_files(file_list, dereference=dereference)

    def download(self, submission, check_exists=False, mark_failure=True, back_error=False):
        """ download backward files from HDFS root dir

        Parameters
        ----------
        submission : Submission class instance
            represents a collection of tasks, such as backward file names

        Returns
        -------
        none
        """
        cwd = os.getcwd()
        gz_dir = os.path.join(self.local_root, 'tmp')
        if os.path.exists(gz_dir):
            shutil.rmtree(gz_dir, ignore_errors=True)
        os.mkdir(os.path.join(self.local_root, 'tmp'))
        rfile_tgz = '%s/%s_*_download.tar.gz' % (self.remote_root, submission.submission_hash)
        lfile_tgz = '%s/tmp/' % self.local_root
        HDFS.copy_to_local(rfile_tgz, lfile_tgz)
        tgz_file_list = glob(os.path.join(self.local_root, 'tmp/*_download.tar.gz'))
        for tgz in tgz_file_list:
            with tarfile.open(tgz, 'r:gz') as tar:
                tar.extractall(path=gz_dir)
        for task in submission.belonging_tasks:
            local_job = os.path.join(self.local_root, task.task_work_path)
            remote_job = os.path.join(gz_dir, task.task_work_path)
            flist = task.backward_files
            if back_error:
                errors = glob(os.path.join(remote_job, 'error*'))
                flist.extend(errors)
            for jj in flist:
                rfile = os.path.join(remote_job, jj)
                lfile = os.path.join(local_job, jj)
                if not os.path.exists(rfile):
                    if check_exists:
                        if mark_failure:
                            with open(os.path.join(self.local_root, task.task_work_path, 'tag_failure_download_%s' % jj), 'w') as fp:
                                pass
                        else:
                            raise RuntimeError('do not find download file ' + rfile)
                    else:
                        raise RuntimeError('do not find download file ' + rfile)
                else:
                    if os.path.exists(lfile):
                        dlog.info('find existing %s, replacing by %s' % (lfile, rfile))
                        if os.path.isdir(lfile):
                            shutil.rmtree(lfile, ignore_errors=True)
                        elif os.path.isfile(lfile):
                            os.remove(lfile)
                    shutil.move(rfile, lfile)
        local_job = self.local_root
        remote_job = gz_dir
        flist = submission.backward_common_files
        if back_error:
            errors = glob(os.path.join(remote_job, 'error*'))
            flist.extend(errors)
        for jj in flist:
            rfile = os.path.join(remote_job, jj)
            lfile = os.path.join(local_job, jj)
            if not os.path.exists(rfile):
                if check_exists:
                    if mark_failure:
                        with open(os.path.join(self.local_root, 'tag_failure_download_%s' % jj), 'w') as fp:
                            pass
                    else:
                        raise RuntimeError('do not find download file ' + rfile)
                else:
                    raise RuntimeError('do not find download file ' + rfile)
            else:
                if os.path.exists(lfile):
                    dlog.info('find existing %s, replacing by %s' % (lfile, rfile))
                    if os.path.isdir(lfile):
                        shutil.rmtree(lfile, ignore_errors=True)
                    elif os.path.isfile(lfile):
                        os.remove(lfile)
                shutil.move(rfile, lfile)
        shutil.rmtree(gz_dir, ignore_errors=True)

    def check_file_exists(self, fname):
        """ check whether the given file exists, often used in checking whether the belonging job has finished

         Parameters
         ----------
         fname : string
             file name to be checked

         Returns
         -------
         status: boolean
         """
        return HDFS.exists(os.path.join(self.remote_root, fname))

    def clean(self):
        HDFS.remove(self.remote_root)

    def write_file(self, fname, write_str):
        local_file = os.path.join('/tmp/', fname)
        with open(local_file, 'w') as fp:
            fp.write(write_str)
        HDFS.copy_from_local(local_file, os.path.join(self.remote_root, fname))
        return local_file

    def read_file(self, fname):
        return HDFS.read_hdfs_file(os.path.join(self.remote_root, fname))

    def kill(self, job_id):
        pass