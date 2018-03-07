import os
from project import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8088))
    app.run('127.0.0.1', port=port, debug=True)