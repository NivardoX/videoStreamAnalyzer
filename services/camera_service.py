from app import db
from models.camera import Camera, UserCamera
from sqlalchemy.dialects.postgresql import insert


def get_cameras_by_user_id(user_id):
    return Camera.query.join(UserCamera).filter_by(user_id=user_id).all()


def create_camera_if_not_exists(camera_id,url):
        insert_table = insert(Camera).values({'id': camera_id, 'url': url})
        insert_table_sql = insert_table.on_conflict_do_nothing(
            index_elements=['id']
        )

        db.session.execute(insert_table_sql)
        db.session.commit()





def get_all_cameras():
    return Camera.query.all()
