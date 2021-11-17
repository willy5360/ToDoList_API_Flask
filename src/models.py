from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Boolean(), nullable=False)
    label = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return f'The task is {self.label}, done {self.done}'


    def to_dict(self):
        return {
            "id": self.id,
            "done": self.done,
            "label": self.label,
        }
    

    @classmethod
    def get_all_tasks(cls):
        all_tasks = cls.query.all()
        return all_tasks
    

    @classmethod
    def get_task_id(cls, id_task):
        task = cls.query.filter_by(id = id_task).one_or_none()
        return task


    def create_new_task(self):
        db.session.add(self)
        db.session.commit()
        return self


    def delete_task(self):
        db.session.delete(self)
        db.session.commit()


    def task_finished(self):
        self.done = True
        db.session.commit() 
        return self

