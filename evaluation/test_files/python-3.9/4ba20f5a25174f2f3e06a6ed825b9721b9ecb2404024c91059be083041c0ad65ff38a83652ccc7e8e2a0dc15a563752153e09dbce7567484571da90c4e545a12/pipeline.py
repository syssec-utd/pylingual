from abc import ABC, abstractmethod
import threading
import queue
import time
import uuid
__all__ = ['Worker', 'Workers', 'TaskQueue', 'Doer', 'Operator', 'Controller', 'Team', 'Pipeline']

class Worker(ABC, threading.Thread):
    """Base class of worker classes.
	
	Worker is a processor run in its own working thread to play the specific
	role in a program in paraellel with other workers or program (main thread).
	
	This base class defines the framework of worker classes, so that the 
	worker management will be standardized and flexible for different scale of
	pipeline.

	Program (main thread) takes below actions to manage a worker:

	1. Create an instance of worker class
	2. Call ``hire()`` to activate the worker
	3. Call ``dismiss()`` to deactivate the worker
	4. Delete the instance explicitly or have GC to collect it automatically

	Below methods are overrideable in derived worker class to meet the needs:

	* ``_process()``: Derived class must need to override it to implement the		process logic of a worker.  During the process, use ``self._dismisssNotice.is_set()``		to check whether program had sent notice of dismiss, and make sure		the exit of ``_process()`` as soon as possible to complete the dismiss		workflow.
	
	* ``_pre_working()``: Framework will call it right before the working		thread is started.  It's running in main thread.
	
	* ``_start_working()``: Framework will call it right after the working		thread is started.  It's running in working thread.
	
	* ``_stop_working()``: Framework will call it right before the working		thread is stopped.  It's running in working thread.
	
	* ``_post_working()``: Framework will call it right after the working thread		is stopped.  It's running in main thread.
	
	* ``_enter_idle()``: Framework or some process will call it when the worker		become idle(no task available) in task driven model.  It's running in		working thread.
	
	* ``_leave_idle()``: Framework or some process will call it when the worker		become busy(has task available) in task driven model.  It's running in		working thread.
	
	* ``bind()``: Framework will call it to bind the data passed to the framework.
	"""

    def __init__(self):
        threading.Thread.__init__(self)
        self.__stateLock = threading.Lock()
        self.__state = 0
        self._dismissNotice = threading.Event()
        self._idleLock = threading.Lock()
        self._idle = True
        self.id = ''

    def __del__(self):
        if self.__state == 0:
            pass
        elif self.__state == 1:
            raise Exception('dismiss() must be called explicitly!')
        elif self.__state == 2:
            raise Exception('dismiss() must be called explicitly!')
        else:
            pass

    @abstractmethod
    def _process(self):
        pass

    def _pre_working(self):
        pass

    def _start_working(self):
        pass

    def _stop_working(self):
        pass

    def _post_working(self):
        pass

    def _enter_idle(self):
        with self._idleLock:
            self._idle = True

    def _leave_idle(self):
        with self._idleLock:
            self._idle = False

    def _handle_exception(self, e):
        pass

    def bind(self, data):
        pass

    def hire(self, id=None):
        """Hire a worker.

		:param id: Worker ID.  If it is None, an ID will be generated.

		:returns: Returns True on success and False on failure.
		"""
        with self.__stateLock:
            if self.__state != 0:
                return False
            self.__state = 1
        if id is not None:
            self.id = id
        else:
            self.id = str(uuid.uuid4())
        self._pre_working()
        try:
            self.start()
        except:
            return False
        return True

    def dismiss(self):
        """Dismiss the worker."""
        with self.__stateLock:
            state = self.__state
            if state != 1 and state != 2:
                return
        if state == 2:
            self._dismissNotice.set()
            try:
                self.join()
            except:
                pass
        self._post_working()
        with self.__stateLock:
            if self.__state != 3:
                raise Exception('Unknown error.')

    def run(self):
        with self.__stateLock:
            self.__state = 2
        try:
            self._start_working()
            self._process()
            self._stop_working()
        except Exception as e:
            self._handle_exception(e)
        with self.__stateLock:
            self.__state = 3

    def is_idle(self):
        with self._idleLock:
            return self._idle

class Workers:
    """Worker list."""

    def __init__(self):
        self.__listLock = threading.Lock()
        self.__list = []
        self.__total_count = 0
        self.__peak_count = 0

    def __del__(self):
        if len(self.__list) > 0:
            raise Exception('Not all workers had been dismissed!')

    def get_count(self):
        """Get number of current workers.

		:returns: Number of current workers.
		"""
        with self.__listLock:
            return len(self.__list)

    def get_status(self):
        """Get status of workers.
		
		:returns: Returns a dict with summary of workers status.
		"""
        with self.__listLock:
            total_count = self.__total_count
            peak_count = self.__peak_count
            count = 0
            idle_count = 0
            for worker in self.__list:
                count += 1
                if worker.is_idle():
                    idle_count += 1
        idle_rate = 0.0
        if count > 0:
            idle_rate = idle_count / count
        return {'total_count': total_count, 'peak_count': peak_count, 'count': count, 'idle_count': idle_count, 'idle_rate': idle_rate}

    def hire(self, workerClass, data=None, id=None):
        """Hire a worker.

		:param workerClass: Worker class.
		:param data: Data to be passed to ``worker.bind()``.
		:param id: ID of the worker.  If it's None, it will generate an ID automatically.

		:returns: Number of workers had been hired.
		"""
        worker = workerClass()
        worker.bind(data)
        if not worker.hire(id):
            return 0
        with self.__listLock:
            self.__list.append(worker)
            self.__total_count += 1
            if len(self.__list) > self.__peak_count:
                self.__peak_count = len(self.__list)
        return 1

    def hire_n(self, workerClass, n, data=None, ids=None):
        """Hire n workers.

		:param workerClass: Worker class.
		:param n: Number of workers to be hired.
		:param data: Data to be passed to ``worker.bind()``.
		:param ids: List of IDs of the new workers.  
			If it's None or not enough IDs in the list, id will be generated.

		:returns: Number of workers had been hired.
		"""
        if n <= 0:
            return 0
        count = 0
        for i in range(0, n):
            id = None
            if ids is not None:
                if i < len(ids):
                    id = ids[i]
            if self.hire(workerClass, data, id) == 0:
                break
            count += 1
        return count

    def dismiss(self, id=None):
        """Dismiss a worker.

		:param id: ID of the worker to be dismissed.  
			If it's None, it will dismiss the last idle worker hired or			last worker hired.

		:returns: Number of workers had been dismissed.
		"""
        with self.__listLock:
            count = len(self.__list)
            if count <= 0:
                return 0
            if id is not None:
                index = None
                for i in range(0, count):
                    if self.__list[i].id == id:
                        index = i
                        break
                if index is None:
                    return 0
            else:
                index = -1
                for i in range(0, count):
                    if self.__list[count - i - 1].is_idle():
                        index = count - i - 1
                        break
            worker = self.__list.pop(index)
        worker.dismiss()
        del worker
        return 1

    def dismiss_n(self, n):
        """Dismiss n workers.

		:param n: Number of workers to be dismissed.

		:returns: Number of workers had been dismissed.
		"""
        if n <= 0:
            return 0
        count = 0
        for i in range(0, n):
            if self.dismiss() == 0:
                break
            count += 1
        return count

    def dismiss_all(self):
        """Dismiss all workers.

		:returns: Number of workers had been dismissed.
		"""
        count = 0
        with self.__listLock:
            while len(self.__list) > 0:
                worker = self.__list.pop(-1)
                worker.dismiss()
                del worker
                count += 1
        return count

class _TaskQueueItem(object):

    def __init__(self, index, priority, task):
        self.index = index
        self.priority = priority
        self.task = task

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        elif self.priority == other.priority:
            return self.index < other.index
        else:
            return False

class TaskQueue(queue.PriorityQueue):
    """Task queue."""

    def __init__(self, maxsize=0):
        queue.PriorityQueue.__init__(self, maxsize)
        self.__total_count = 0
        self.__peak_count = 0

    def __del__(self):
        if not self.empty():
            pass

    def get_status(self):
        """Get status of the queue.
		
		:returns: Returns a dict with summary of queue status.
		"""
        with self.mutex:
            total_count = self.__total_count
            peak_count = self.__peak_count
            count = self._qsize()
        return {'total_count': total_count, 'peak_count': peak_count, 'count': count}

    def push_task(self, task, priority=100, timeout=None):
        """Push task to the queue.

		:param task: Task.
		:param priority: Priority of the task.  Lower value takes higher priority.
			Default value is 100.
		:param timeout: Timeout in seconds.  If it's None, it's infinite.

		:returns: Returns True on success and False on failure.
		"""
        try:
            if task is None:
                return False
            with self.mutex:
                index = self.__total_count + 1
            self.put(_TaskQueueItem(index, priority, task), block=True, timeout=timeout)
            with self.mutex:
                self.__total_count += 1
                if self._qsize() > self.__peak_count:
                    self.__peak_count = self._qsize()
        except:
            return False
        return True

    def pop_task(self, timeout=None):
        """Pop a task from the queue.

		:param timeout: If it's None, it will not wait for task if no task
			is available at the time.  If it's a postive value (in seconds),
			it will wait for task until time is out.

		:returns: Returns a task.  If no task is available, returns None.
		"""
        try:
            if timeout is None:
                taskItem = self.get(block=False)
            else:
                taskItem = self.get(block=True, timeout=timeout)
            task = taskItem.task
        except:
            task = None
        return task

class Doer(Worker):
    """Base class of doer classes.

	Doer is the worker who is task drivern and typically working independently.
	It is with it's own task queue and be reponsible to finish all tasks 
	in the queue before it's dismissed.

	Program pushes the tasks in the queue and just wait them processed by the doer.

	It defines a more specific framework and workflow than worker class.

	Override below methods to implement the logic for specific Doer:

	* ``_process_task()``: Called by framework when need to process a task.
	"""

    def __init__(self, maxsize=0):
        Worker.__init__(self)
        self.task_queue = TaskQueue(maxsize)

    def __del__(self):
        if self.task_queue is not None:
            del self.task_queue
            self.task_queue = None
        Worker.__del__(self)

    @abstractmethod
    def _process_task(self, task):
        pass

    def _process(self):
        stopping = False
        while True:
            self._leave_idle()
            while True:
                task = self.task_queue.pop_task()
                if task is None:
                    break
                self._process_task(task)
            self._enter_idle()
            if stopping:
                break
            if self._dismissNotice.is_set():
                time.sleep(1)
                stopping = True

class Operator(Worker):
    """Base class of operator classes.

	Operator is the worker who is task drivern and working as part of team.
	It is using the shared task queue and be reponsible to finish current task
	only.

	Override below methods to implement the logic for specific Operator:

	* ``_pop_task()``: Called by framework when need to get a task from some task queue.
		
	* ``_process_task()``: Called by framework when need to process a task.
	"""

    def __init__(self):
        Worker.__init__(self)

    def __del__(self):
        Worker.__del__(self)

    @abstractmethod
    def _pop_task(self):
        return None

    @abstractmethod
    def _process_task(task):
        pass

    def _process(self):
        while True:
            task = self._pop_task()
            if task is not None:
                self._leave_idle()
                self._process_task(task)
                self._enter_idle()
            if self._dismissNotice.is_set():
                break

class Controller(Worker):
    """Base class of controller classes.

	Controller is the worker who is not task driven.
	It's typically working in parallel with other Operators to monitor and 
	facilitate the pipeline.  Or it may take some special processes no matter
	it's once or repeating.
	"""

    def __init__(self):
        Worker.__init__(self)

    def __del__(self):
        Worker.__del__(self)

class Team(ABC):
    """Base class of team classes.

	Team is an organization with Operators and Controllers to typically process
	a single kind of task.  Team is typically with:

	* ``task_queue``: A shared task queue.  Program could send the tasks to it,		and team is responsible to process the task in quality and timing.
	
	* ``operators``: A list of operators who is processing the tasks.  The list		could be dynamic based on the workload by controllers.

	* (controllers)`: Optional, to be defined in actual team class based on needs.

	Derived class needs to implement below logic as minimum:

	* ``__init__()``: Define the ``self.operator_class`` with operator class,		so that framework could manage operators automatically.

	* ``hire()``: Override it with logic to create the task queue, hire initial		operators and hire controllers.

	* ``dismiss()``: Override it with logic to wait for task queue empty, dismiss		operators, dismiss controllers, and clear and delete the task queue.
	"""

    def __init__(self):
        self.task_queue = None
        self.operator_class = None
        self.operators = Workers()

    def __del__(self):
        if self.task_queue is not None:
            del self.task_queue
            self.task_queue = None

    @abstractmethod
    def hire(self):
        return False

    @abstractmethod
    def dismiss(self):
        pass

    def finish_all_tasks(self):
        while not self.task_queue.empty():
            if self.operators.get_count() <= 0:
                if self.hire_operator(1) < 1:
                    raise Exception('Failed to hire operator to finish remaining tasks!')
            time.sleep(0.5)

    def hire_operator(self, count=1):
        if self.operator_class is None:
            return 0
        return self.operators.hire_n(self.operator_class, count, self, None)

    def dismiss_operator(self, count=1):
        return self.operators.dismiss_n(count)

class Pipeline(ABC):
    """Base class of pipeline classes.
	
	Pipeline is an organization with Teams and Controllers to process complex
	tasks and jobs.  Pipeline is typically with:

	* (job queue): An input job queue.  Job could be considered as a complex		task which could be broken down into tasks.  Program could send the		job to the job queue.  Pipeline controller will break it down into		tasks based on the procedure and send the task to different Teams in		pipeline in order or in parallel.  Once all the tasks of a job had		been complete, the job could be delivered and leave the pipeline.

	* (teams): Teams for different kind of tasks.  Each team is focusing on		a single task type.  Teams could be working in parallel or in sequence		based on actual needs.

	* (controllers): Roles to facilitate the pipeline process.

	This class is not defining any workflow, and it's more link a model for
	developer to build the pipeline.  Override and implement below methods 
	are suggested:

	* ``__init__()``: Define pipeline attributes.

	* ``hire()``: Logic to initialize the pipeline with create the job queue,		prepare resources, hire teams, hire controllers, etc.

	* ``dismiss()``: Logic to clean up the pipeline by handling remaining job		queue, dismiss teams, dismiss controllers, etc.
	"""

    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def hire(self):
        return False

    @abstractmethod
    def dismiss(self):
        pass