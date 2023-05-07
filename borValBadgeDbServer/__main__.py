import connexion
from threading import Thread

from borValBadgeDbServer import encoder
from borValBadgeDbServer.db.db import loadDatabase, dbScheduler, saveDatabase
from borValBadgeDbServer.db.checker import missingReportWorker
from apscheduler.triggers.interval import IntervalTrigger


def main():
    loadDatabase()

    dbScheduler.add_schedule(saveDatabase, IntervalTrigger(minutes=60))
    dbScheduler.start_in_background()

    Thread(target=missingReportWorker, daemon=True).start()

    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'BoR Valuable Badge Database'},
                pythonic_params=True)

    app.run(port=8080)


if __name__ == '__main__':
    main()
