import os
from celery.app.base import Celery
# from flask_socketio import SocketIO, emit, join_room, rooms
from app.extensions import socketio, mongo
from app.flask_app import create_app, configure_app
from app.config import VsmAPIConfig
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta

logger = get_task_logger(__name__)

# ========================================
# SOCKET.IO
# ========================================

NAMESPACE = '/test'


def init_app(socketio):
    @socketio.on('connect', namespace=NAMESPACE)
    def on_connect():
        # TODO: check auth here
        logger.info("on_connect")
        print("on_connect")
        pass

    @socketio.on('fetch', namespace=NAMESPACE)
    def on_fetch():
        logger.info("on_fetch")
        print("on_fetch")
        data = {
            "test": True
        }
        socketio.emit('init-data', {'data': data}, namespace=NAMESPACE)


# ========================================
# CELERY
# ========================================

# init flask
flask_app = create_app()
configure_app(flask_app)


def make_celery(app):
    celery = Celery(
        app.import_name,
        # backend=app.config['CELERY_RESULT_BACKEND'],
        # broker=app.config['CELERY_BROKER_URL']
    )
    # celery.conf.update(app.config)
    print app.config
    celery.conf.update(VsmAPIConfig.__dict__)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


celery = make_celery(flask_app)
# celery.config_from_object(VsmAPIConfig)
default_config = dict(
    task_ignore_result=True,
    task_store_errors_even_if_ignored=True
)
celery.conf.update(default_config)

routes = {
    'events.*': {'queue': 'export'}
}
celery.conf.task_routes = routes


@celery.task(name='events.export_vuln')
# @fail_on_error
def export_vuln(query={}, actor='sadmin'):
    logger.info('start export_data...')
    # query
    data = mongo.db.vulnerability.find({"deleted": False, "is_latest": True}).limit(10000)

    # save file
    file_path, msg = _save(data, "json", actor)

    # notify to client
    status = {"status": msg, "path": file_path}
    socketio.emit("status", status, namespace=NAMESPACE)

    return msg


def _save(content, file_type, actor="sadmin"):
    logger.debug('Trying save file...')
    # base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../..')
    # if os.path.isabs(SCAN_LOG_LOCATION):
    #     path = os.path.normpath(SCAN_LOG_LOCATION)
    # else:
    #     path = os.path.normpath("{0}/{1}".format(base_dir, SCAN_LOG_LOCATION))
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'export_data')

    if not os.path.isdir(path):
        try:
            os.makedirs(path)
        except OSError as ex:
            if not os.path.isdir(path):
                logger.exception("Exception while create log folder! {}".format(ex))
                return

    _id = datetime.now().strftime("%Y%m%d_%H%M")
    log_path = "{}/{}_{}_{}.{}".format(path, "vuln", actor, _id, file_type)
    try:
        with open(log_path, 'wb') as flog:
            flog.write(content)
        logger.debug('Exported log file')
        return log_path, "ok"
    except IOError as ex:
        logger.exception("Exception while logging data! {}".format(ex))

    return None, "error"
