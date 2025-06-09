import os
import traceback
from flask import jsonify, redirect, render_template, request, send_from_directory
from flask_login import login_required
from framework import F

@F.app.route('/global/ajax/<sub>', methods=['GET', 'POST'])
@login_required
def global_ajax(sub):
    if sub == 'listdir':
        if 'path' in request.form:
            path = request.form['path']
            if os.path.isfile(path):
                path = os.path.dirname(path)
            result_list = os.listdir(path)
            if 'only_dir' in request.form and request.form['only_dir'].lower() == 'true':
                result_list = [name for name in result_list if os.path.isdir(os.path.join(path, name))]
            result_list.sort()
            result_list = [f'{x}|{os.path.join(path, x)}' for x in result_list]
            tmp = os.path.dirname(path)
            if path != tmp:
                result_list = [f'..|{tmp}'] + result_list
            return jsonify(result_list)
        else:
            return jsonify(None)
    elif sub == 'is_available_edit':
        try:
            if F.PluginManager.all_package_list['flaskcode']['loading']:
                PP = F.PluginManager.all_package_list['flaskcode']['P']
                ret = {'ret': True, 'target': PP.ModelSetting.get('setting_open_target')}
                return jsonify(ret)
            else:
                return jsonify({'ret': False})
        except:
            return jsonify({'ret': False})
    elif sub == 'command_modal_hide':
        from tool import ToolModalCommand
        ToolModalCommand.modal_close()
        return jsonify('')
    elif sub == 'command_modal_input':
        from tool import ToolModalCommand
        cmd = request.form['cmd']
        ToolModalCommand.input_command(cmd)
        return jsonify('')

@F.app.route('/robots.txt')
def robot_to_root():
    return send_from_directory('', 'static/file/robots.txt')

@F.app.route('/')
@F.app.route('/None')
@F.app.route('/home')
def home():
    return redirect('/system/home')

@F.app.route('/version')
def get_version():
    from .version import VERSION
    return VERSION

@F.app.route('/open/<path:path>')
@login_required
def open_file(path):
    return send_from_directory('/', path)

@F.app.route('/file/<path:path>')
@F.check_api
def file2(path):
    import platform
    if platform.system() == 'Windows':
        path = os.path.splitdrive(path)[1][1:]
    return send_from_directory('/', path, as_attachment=True)

@F.app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        if request.method == 'POST':
            f = request.files['file']
            from werkzeug import secure_filename
            upload_path = F.SystemModelSetting.get('path_upload')
            os.makedirs(upload_path, exist_ok=True)
            f.save(os.path.join(upload_path, secure_filename(f.filename)))
            return jsonify('success')
    except Exception as e:
        F.logger.error(f'Exception:{str(e)}')
        F.logger.error(traceback.format_exc())
        return jsonify('fail')

@F.app.route('/videojs', methods=['GET', 'POST'])
def videojs():
    data = {}
    data['play_title'] = request.form['play_title']
    data['play_source_src'] = request.form['play_source_src']
    data['play_source_type'] = request.form['play_source_type']
    if 'play_subtitle_src' in request.form:
        data['play_subtitle_src'] = request.form['play_subtitle_src']
    return render_template('videojs.html', data=data)

@F.app.route('/headers', methods=['GET', 'POST'])
def headers():
    from support import d
    F.logger.info(d(request.headers))
    return jsonify(d(request.headers))

@F.socketio.on('connect', namespace=f'/framework')
def connect():
    pass