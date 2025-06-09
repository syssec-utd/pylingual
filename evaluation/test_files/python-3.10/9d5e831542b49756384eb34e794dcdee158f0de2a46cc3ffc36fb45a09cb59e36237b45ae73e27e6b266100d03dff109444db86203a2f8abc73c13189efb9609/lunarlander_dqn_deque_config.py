from easydict import EasyDict
nstep = 3
lunarlander_dqn_config = dict(exp_name='lunarlander_dqn_deque_seed0', env=dict(collector_env_num=8, evaluator_env_num=8, env_id='LunarLander-v2', n_evaluator_episode=8, stop_value=200), policy=dict(cuda=False, priority=True, priority_IS_weight=False, model=dict(obs_shape=8, action_shape=4, encoder_hidden_size_list=[512, 64], dueling=True), discount_factor=0.99, nstep=nstep, learn=dict(update_per_collect=10, batch_size=64, learning_rate=0.001, target_update_freq=100), collect=dict(n_sample=64, unroll_len=1), other=dict(eps=dict(type='exp', start=0.95, end=0.1, decay=50000), replay_buffer=dict(replay_buffer_size=100000, priority=True, priority_IS_weight=False))))
lunarlander_dqn_config = EasyDict(lunarlander_dqn_config)
main_config = lunarlander_dqn_config
lunarlander_dqn_create_config = dict(env=dict(type='lunarlander', import_names=['dizoo.box2d.lunarlander.envs.lunarlander_env']), env_manager=dict(type='subprocess'), policy=dict(type='dqn'), replay_buffer=dict(type='deque'))
lunarlander_dqn_create_config = EasyDict(lunarlander_dqn_create_config)
create_config = lunarlander_dqn_create_config
if __name__ == '__main__':
    from ding.entry import serial_pipeline
    serial_pipeline([main_config, create_config], seed=0)