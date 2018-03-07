import os
from project.codes.Common import Common
from flask import request, current_app, url_for, make_response
from flask_login import current_user


class Upload():
    @staticmethod
    def ckupload_file():
        """CKEditor file upload"""
        error = ''
        url = ''
        callback = request.args.get("CKEditorFuncNum")
        if request.method == 'POST' and 'upload' in request.files:
            fileobj = request.files['upload']
            fname, fext = os.path.splitext(fileobj.filename)
            rnd_name = '%s%s' % (Common.gen_filename(fname), fext)
            filepath = os.path.join(current_app.static_folder, 'upload', current_user.username, rnd_name)
            dirname = os.path.dirname(filepath)
            if not os.path.exists(dirname):
                try:
                    os.makedirs(dirname)
                except:
                    error = 'ERROR_CREATE_DIR'
            elif not os.access(dirname, os.W_OK):
                error = 'ERROR_DIR_NOT_WRITEABLE'
            if not error:
                fileobj.save(filepath)
                url = url_for('static', filename='%s/%s/%s' % ('upload', current_user.username, rnd_name))
        else:
            error = 'Post error'
        res = """<script type="text/javascript"> 
                 window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
                 </script>""" % (callback, url, error)
        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
        return response

    @staticmethod
    def upload_image():
        error = ''
        url = ''
        if request.method == 'POST' and 'image' in request.files:
            fileobj = request.files['image']
            fname, fext = os.path.splitext(fileobj.filename)
            if fname != '':
                rnd_name = '%s%s' % (Common.gen_filename(fname), fext)
                filepath = os.path.join(current_app.static_folder, 'upload', current_user.username, rnd_name)
                dirname = os.path.dirname(filepath)
                if not os.path.exists(dirname):
                    try:
                        os.makedirs(dirname)
                    except:
                        error = 'ERROR_CREATE_DIR'
                elif not os.access(dirname, os.W_OK):
                    error = 'ERROR_DIR_NOT_WRITEABLE'
                if not error:
                    fileobj.save(filepath)
                    url = url_for('static', filename='%s/%s/%s' % ('upload', current_user.username, rnd_name))
            else:
                error = 'No file selected'
        else:
            error = 'Post error'

        if not error:
            return url
        else:
            return None