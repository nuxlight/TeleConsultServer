# coding: utf-8
from sqlalchemy import Column, ForeignKey, Index, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AVI(Base):
    __tablename__ = 'AVIS'
    __table_args__ = (
        Index('IDX_AVIS_ID', 'CONSULTATION_ID', 'MEDECIN_ID'),
    )

    CONSULTATION_ID = Column(ForeignKey('CONSULTATION.CONSULTATION_ID', ondelete='CASCADE'), primary_key=True, nullable=False)
    MEDECIN_ID = Column(ForeignKey('MEDECIN.MEDECIN_ID', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    AVIS = Column(String(500), nullable=False)
    FLAG_FINAL = Column(Integer)

    CONSULTATION = relationship('CONSULTATION')
    MEDECIN = relationship('MEDECIN')


class CENTREHOSPITALIER(Base):
    __tablename__ = 'CENTRE_HOSPITALIER'

    CENTRE_HOSPITALIER_ID = Column(Integer, primary_key=True, index=True)
    CENTRE_HOSPITALIER_NOM = Column(String(20), nullable=False)
    CENTRE_HOSPITALIER_ADRESSE = Column(String(500))

    MEDECIN = relationship('MEDECIN', secondary='CENTRE_HOSPITALIER_REFERENT')
    MEDECIN1 = relationship('MEDECIN', secondary='CENTRE_HOSPITALIER_MEDECIN')


t_CENTRE_HOSPITALIER_MEDECIN = Table(
    'CENTRE_HOSPITALIER_MEDECIN', metadata,
    Column('CENTRE_HOSPITALIER_ID', ForeignKey('CENTRE_HOSPITALIER.CENTRE_HOSPITALIER_ID', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('MEDECIN_ID', ForeignKey('MEDECIN.MEDECIN_ID', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Index('IDX_CENTRE_HOSPITALIER_REFERENT', 'CENTRE_HOSPITALIER_ID', 'MEDECIN_ID')
)


t_CENTRE_HOSPITALIER_REFERENT = Table(
    'CENTRE_HOSPITALIER_REFERENT', metadata,
    Column('CENTRE_HOSPITALIER_ID', ForeignKey('CENTRE_HOSPITALIER.CENTRE_HOSPITALIER_ID', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('MEDECIN_ID', ForeignKey('MEDECIN.MEDECIN_ID', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Index('IDX_CENTRE_HOSPITALIER_REFERENT', 'CENTRE_HOSPITALIER_ID', 'MEDECIN_ID')
)


class CONSULTATION(Base):
    __tablename__ = 'CONSULTATION'

    CONSULTATION_ID = Column(Integer, primary_key=True, index=True)
    SSN_ID = Column(ForeignKey('PATIENT.SSN_ID', ondelete='CASCADE'), nullable=False, index=True)
    TRAITEMENT = Column(String(500), nullable=False)
    HISTORIQUE = Column(String(500), nullable=False)

    PATIENT = relationship('PATIENT')


class DMP(Base):
    __tablename__ = 'DMP'

    DMP_ID = Column(Integer, primary_key=True, index=True)
    SSN_ID = Column(ForeignKey('PATIENT.SSN_ID', ondelete='CASCADE'), nullable=False, index=True)

    PATIENT = relationship('PATIENT')


class EXAMEN(Base):
    __tablename__ = 'EXAMEN'

    EXAMEN_ID = Column(Integer, primary_key=True, index=True)
    MEDECIN_ID = Column(ForeignKey('MEDECIN.MEDECIN_ID', ondelete='CASCADE'), nullable=False, index=True)
    EXAMEN_NOM = Column(String(20), nullable=False)
    
    MEDECIN = relationship('MEDECIN')


class MEDECIN(Base):
    __tablename__ = 'MEDECIN'

    MEDECIN_ID = Column(Integer, primary_key=True, index=True)
    MEDECIN_NOM = Column(String(20), nullable=False)
    MEDECIN_PRENOM = Column(String(20), nullable=False)
    MEDECIN_PASSWORD = Column(String(20), nullable=False)
    MEDECIN_GENRE = Column(String(1), nullable=False)
    MEDECIN_ADDR = Column(String(250), nullable=False)
    SPECIALITE_ID = Column(ForeignKey('SPECIALITE.SPECIALITE_ID'), index=True)

    SPECIALITE = relationship('SPECIALITE')


class PATIENT(Base):
    __tablename__ = 'PATIENT'

    SSN_ID = Column(String(15), primary_key=True, index=True)
    MEDECIN_ID = Column(ForeignKey('MEDECIN.MEDECIN_ID', ondelete='CASCADE'), nullable=False, index=True)
    PATIENT_NOM = Column(String(20), nullable=False)
    PATIENT_PRENOM = Column(String(20), nullable=False)
    PATIENT_AGE = Column(Integer, nullable=False)
    PATIENT_GENRE = Column(String(1), nullable=False)

    MEDECIN = relationship('MEDECIN')


class DOSSIER(Base):
    __tablename__ = 'DOSSIER'
    __table_args__ = (
        Index('IDX_DOSSIER_ID', 'CONSULTATION_ID', 'EXAMEN_ID'),
    )

    DOSSIER_ID = Column(Integer, primary_key=True, index=True)
    DOSSIER_STATUS = Column(String(100), nullable=False)
    CONSULTATION_ID = Column(ForeignKey('CONSULTATION.CONSULTATION_ID', ondelete='CASCADE'), primary_key=True, nullable=False)
    MEDECIN_ID = Column(ForeignKey('MEDECIN.MEDECIN_ID', ondelete='CASCADE'), nullable=False, index=True)
    SSN_ID = Column(ForeignKey('PATIENT.SSN_ID', ondelete='CASCADE'), nullable=False, index=True)
    EXAMEN_ID = Column(ForeignKey('EXAMEN.EXAMEN_ID', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    IMAGE_NOM = Column(String(100), nullable=False)
    IMAGE_PATH = Column(String(100), nullable=False)

    CONSULTATION = relationship('CONSULTATION')
    EXAMEN = relationship('EXAMEN')


class SPECIALITE(Base):
    __tablename__ = 'SPECIALITE'

    SPECIALITE_ID = Column(Integer, primary_key=True, index=True)
    SPECIALITE_NOM = Column(String(20), nullable=False)
