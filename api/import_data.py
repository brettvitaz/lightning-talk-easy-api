from csv import DictReader


def import_from_file(db, table):
    if table.query.all():
        return
    with open('../import_data/{}.csv'.format(table.__tablename__)) as f:
        reader = DictReader(f)
        try:
            db.session.add_all([table(**line) for line in reader])
            db.session.commit()
        finally:
            db.session.close()
