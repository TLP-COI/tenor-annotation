from typing import Dict, List, Any
import json
import time
import random
from contextlib import contextmanager
import html

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Float,
    create_engine,
    and_,
    MetaData,
    Table,
    Column,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.orm.scoping import ScopedSession

from backend.log import get_logger
# from log import get_logger

PLAYS_TABLE_NAME = 'plays_dev'
# PLAYS_TABLE_NAME = 'plays_prod'

log = get_logger(__name__)

Base = declarative_base()  # pylint: disable=invalid-name

db_url = "sqlite:///backend/data/database.db"

class Database:
    def __init__(self, find_questions=True):
        self._engine = create_engine(
            db_url
        )  # pylint: disable=invalid-name
        Base.metadata.bind = self._engine

        self.sessions = []

    
    def get_playing_times(self):
        s = self.playing_times.select()
        conn = self._engine.connect()
        res = conn.execute(s)
        return [time for time in res]

    def create_all(self):
        Base.metadata.create_all(self._engine, checkfirst=True)

    def drop_all(self):
        Base.metadata.drop_all(self._engine)

    def reset_all(self):
        self.drop_all()
        self.create_all()

    @property
    @contextmanager
    def _session_scope(self) -> ScopedSession:
        session = scoped_session(sessionmaker(bind=self._engine))
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all_qanta_ids(self):
        return self._all_qanta_ids

    def get_random_question(self):
        with self._session_scope as session:
            qanta_id = random.choice(self._all_qanta_ids)
            question = session.query(Question).filter_by(qanta_id=qanta_id).first()
            return question.to_dict()

    def get_question_by_id(self, qanta_id: int):
        with self._session_scope as session:
            question = session.query(Question).filter_by(qanta_id=qanta_id).first()
            return question.to_dict()

    def get_question_by_id_custom(self, q_id: int):
        s = self.spring_novice_data.select().where(self.spring_novice_data.c.id==q_id)
        conn = self._engine.connect()
        result = conn.execute(s)
        row = list(result)[0]
        return row

    def get_table_ids(self):
        s = self.spring_novice_data.select()
        conn = self._engine.connect()
        result = conn.execute(s)
        return [res[0] for res in result]
    
    def get_packet_questions(self, packet):
        s = self.spring_novice_data.select().where(self.spring_novice_data.c.packet_num == packet)
        conn = self._engine.connect()
        result = conn.execute(s)
        result = [res[0] for res in result]
        return result
    
    # def insert_question_play(self, question_play: dict):
    #     try:
    #         serialized = json.dumps(question_play)
    #         insert_params = {
    #             'username': question_play['username'], 
    #             'question_id': question_play['question_id'], 
    #             'start_datetime': question_play['start_datetime'],
    #             'data': serialized}

    #         ins = self.plays.insert()
    #         ins = self.plays.insert().values(**insert_params)
    #         conn = self._engine.connect()
    #         result = conn.execute(ins)
        
    #     except Exception as e:
    #         print(f'error while writing question play: {e}')

    def write_session_data(self, session_data: dict):
        try:
            serialized = json.dumps(session_data)
            insert_params = {
                'username': session_data['username'], 
                'question_id': session_data['question_id'], 
                'start_datetime': session_data['start_datetime'],
                'data': serialized}

            ins = self.sessions.insert()
            ins = self.sessions.insert().values(**insert_params)
            conn = self._engine.connect()
            result = conn.execute(ins)
        except Exception as e:
            print(f'error while writing: {e}')

    # def write_questions(self, questions: Dict[str, Any]):
    #     start = time.time()

    #     with self._session_scope as session:
    #         question_list = []
    #         for question in questions:
    #             question["tokenizations"] = str(question["tokenizations"])
    #             question["tokens"] = json.dumps(question["tokens"])
    #             question_list.append(question)
    #         session.bulk_insert_mappings(Question, question_list)
    #     log.info("Took %s time to write questions", time.time() - start)

    def write_answer_data(self, answer_data):
        print(answer_data)
        # print(answer_data['session_id'])
        with self._session_scope as session:
            session.bulk_insert_mappings(
                Record, [answer_data]
            )
            return True
    
    ### user ###
    def insert_user_game_data(self, user_id, game_data):
        with self._session_scope as session:
            session.query(User).filter(User.user_id == user_id).update({User.game_data: game_data}, synchronize_session = False)

    def get_user_state(self, user_id):
        with self._session_scope as session:
            res = session.query(User).filter(User.user_id == user_id).first()
            session.commit()
            data = res.game_data
            if not data: return {}
            # data = list(res).game_data
            print('game data', data)
            return json.loads(data)

    ### authentication ###

    # def get_password(self, email):
    #     with self._session_scope as session:
    #         results = session.query(User).filter(User.email == email).first()
    #         if results:
    #             return results.password
    #         return None
    def get_password(self, user_id):
        with self._session_scope as session:
            results = session.query(User).filter(User.user_id == user_id).first()
            if results:
                return results.password
            return None

    # registration
    def insert_user_email_password(self, username, password, email):
        with self._session_scope as session:
            if not session.query(User).filter(User.user_id == username).first():
                session.bulk_insert_mappings(
                    User, [{"user_id": username, "email": username, "password": password}]
                )
                return True
            return False

    # easy registration
    def insert_user_password(self, user_id, password):
        with self._session_scope as session:
            if not session.query(User).filter(User.user_id == user_id).first():
                session.bulk_insert_mappings(
                    User, [{"user_id": user_id, "password": password}]
                )
                return True
            return False

    def insert_session(self, user_id, session_id):
        with self._session_scope as session:
            # if not session.query(User).filter(User.user_id == user_id).first():
            session.bulk_insert_mappings(
                Session, [{"user_id": user_id, "session_id": session_id}]
            )
            return True

    def reset_users(self):
        with self._session_scope as session:
            session.query(User).filter(User.password != "").delete()


class Question(Base):
    __tablename__ = "questions"
    qanta_id = Column(Integer, primary_key=True)
    text = Column(String)
    first_sentence = Column(String)
    tokenizations = Column(String)
    answer = Column(String)
    page = Column(String)
    fold = Column(String)
    gameplay = Column(Boolean)
    category = Column(String)
    subcategory = Column(String)
    tournament = Column(String)
    difficulty = Column(String)
    year = Column(Integer)
    proto_id = Column(Integer)
    qdb_id = Column(Integer)
    dataset = Column(String)
    # tokens = Column(String)
    

    def from_dict(self, d):
        for k in d:
            setattr(self, k, d[k])

    def to_dict(self):
        return {
            "qanta_id": self.qanta_id,
            "text": self.text,
            "tokenizations": json.loads(self.tokenizations),
            "answer": self.answer,
            "page": self.page,
            "fold": self.fold,
            "gameplay": self.gameplay,
            "category": self.category,
            "subcategory": self.subcategory,
            "tournament": self.tournament,
            "difficulty": self.difficulty,
            "year": self.year,
            "proto_id": self.proto_id,
            "qdb_id": self.proto_id,
            "dataset": self.dataset,
            # "tokens": json.loads(self.tokens),
        }

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    email = Column(String)
    password = Column(String)
    sessions = relationship('Session')
    # score = Column(Integer)
    game_data = Column(String)


    def __str__(self):
        return self.user_id

# record_question_table = Table('record_question_table', Base.metadata,
#     Column('record_id', String, ForeignKey('questions.qanta_id')),
#     Column('question_id', Integer, ForeignKey('records.record_id'))
# )

class Session(Base): # data on a single session
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True)
    user_id = Column(String,ForeignKey('users.user_id'))
    records = relationship('Record')

# class Session(Base): # data on a single session
#     __tablename__ = "sessions"

#     session_id = Column(String, primary_key=True)
#     user_id = Column(String,ForeignKey('users.user_id'))
#     records = relationship('Record')

class Record(Base): # a single question attempt during a session
    __tablename__ = "records"
    
    record_id = Column(Integer, primary_key=True)
    # user_id = Column(Integer,ForeignKey('users.user_id'))
    session_id = Column(String, ForeignKey('sessions.session_id'))
    # question_id = relationship('Question', secondary=record_question_table)
    question_id = Column(Integer, ForeignKey('questions.qanta_id'))
    answer = Column(String)
    query = Column(String)
    evidence = Column(String)
    stop_position = Column(Integer)

    

