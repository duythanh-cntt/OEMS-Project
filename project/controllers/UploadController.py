from project import app
from flask_login import login_required
from project.models.UploadModel import Upload


@app.route('/admin/ckupload/', methods=['POST', 'OPTIONS'])
@login_required
def ckupload():
    return Upload.ckupload_file()