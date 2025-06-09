def handle_control(self, req, worker_id, req_info):
    """
        Handles a control_request received from a worker.
        Returns:
            string or dict: response

            'stop' - the worker should quit
            'wait' - wait for 1 second
            'eval' - evaluate on valid and test set to start a new epoch
            'sync_hyperparams' - set learning rate
            'valid' - evaluate on valid and test set, then save the params
            'train' - train next batches
        """
    if self.start_time is None:
        self.start_time = time.time()
    response = ''
    if req == 'next':
        if self.num_train_batches == 0:
            response = 'get_num_batches'
        elif self._done:
            response = 'stop'
            self.worker_is_done(worker_id)
        elif self._evaluating:
            response = 'wait'
        elif not self.batch_pool:
            if self._train_costs:
                with self._lock:
                    sys.stdout.write('\r')
                    sys.stdout.flush()
                    mean_costs = []
                    for i in range(len(self._training_names)):
                        mean_costs.append(np.mean([c[i] for c in self._train_costs]))
                    self.log('train   (epoch={:2d}) {}'.format(self.epoch, self.get_monitor_string(zip(self._training_names, mean_costs))))
            response = {'eval': None, 'best_valid_cost': self._best_valid_cost}
            self._evaluating = True
        elif worker_id not in self.prepared_worker_pool:
            response = {'sync_hyperparams': self.feed_hyperparams()}
            self.prepared_worker_pool.add(worker_id)
        elif self._iters_from_last_valid >= self._valid_freq:
            response = {'valid': None, 'best_valid_cost': self._best_valid_cost}
            self._iters_from_last_valid = 0
        else:
            response = {'train': self.feed_batches()}
    elif 'eval_done' in req:
        with self._lock:
            self._evaluating = False
            sys.stdout.write('\r')
            sys.stdout.flush()
            if 'test_costs' in req and req['test_costs']:
                self.log('test    (epoch={:2d}) {} (worker {})'.format(self.epoch, self.get_monitor_string(req['test_costs']), worker_id))
            if 'valid_costs' in req and req['test_costs']:
                valid_J = req['valid_costs'][0][1]
                if valid_J < self._best_valid_cost:
                    self._best_valid_cost = valid_J
                    star_str = '*'
                else:
                    star_str = ''
                    self.log('valid   (epoch={:2d}) {} {} (worker {})'.format(self.epoch, self.get_monitor_string(req['valid_costs']), star_str, worker_id))
            continue_training = self.prepare_epoch()
            self._epoch_start_time = time.time()
            if not continue_training:
                self._done = True
                self.log('training time {:.4f}s'.format(time.time() - self.start_time))
                response = 'stop'
    elif 'valid_done' in req:
        with self._lock:
            sys.stdout.write('\r')
            sys.stdout.flush()
            if 'valid_costs' in req:
                valid_J = req['valid_costs'][0][1]
                if valid_J < self._best_valid_cost:
                    self._best_valid_cost = valid_J
                    star_str = '*'
                else:
                    star_str = ''
                self.log('valid   ( dryrun ) {} {} (worker {})'.format(self.get_monitor_string(req['valid_costs']), star_str, worker_id))
    elif 'train_done' in req:
        costs = req['costs']
        self._train_costs.append(costs)
        sys.stdout.write('\x1b[2K\r> %d%% | J=%.2f | %.1f batch/s' % (self._current_iter * 100 / self.num_train_batches, costs[0], float(len(self._train_costs) * self.sync_freq) / (time.time() - self._epoch_start_time)))
        sys.stdout.flush()
    elif 'get_num_batches_done' in req:
        self.num_train_batches = req['get_num_batches_done']
    elif 'get_easgd_alpha' in req:
        response = self._easgd_alpha
    elif 'sync_hyperparams' in req:
        response = {'sync_hyperparams': self.feed_hyperparams()}
    elif 'init_schedule' in req:
        with self._lock:
            sys.stdout.write('\r')
            sys.stdout.flush()
            self.log('worker {} connected'.format(worker_id))
            if self.epoch == 0:
                schedule_params = req['init_schedule']
                sch_str = ' '.join(('{}={}'.format(a, b) for a, b in schedule_params.items()))
                self.log('initialize the schedule with {}'.format(sch_str))
                for key, val in schedule_params.items():
                    if not val:
                        continue
                    if key == 'learning_rate':
                        self._lr = val
                    elif key == 'start_halving_at':
                        self.epoch_start_halving = val
                    elif key == 'halving_freq':
                        self._halving_freq = val
                    elif key == 'end_at':
                        self.end_at = val
                    elif key == 'sync_freq':
                        self.sync_freq = val
                    elif key == 'valid_freq':
                        self._valid_freq = val
    elif 'set_names' in req:
        self._training_names = req['training_names']
        self._evaluation_names = req['evaluation_names']
    return response