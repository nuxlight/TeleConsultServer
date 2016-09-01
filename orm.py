# coding: utf-8
from sqlalchemy import Column, Date, ForeignKey, Index, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Avi(Base):
    __tablename__ = 'avis'

    DMPCSUBMISSION_ID = Column(Integer, primary_key=True, index=True)
    CONSULTATION_ID = Column(ForeignKey('consultation.CONSULTATION_ID', ondelete='CASCADE'), nullable=False, index=True)
    AVIS = Column(String(500), nullable=False)
    FLAG_FINAL = Column(Integer)

    consultation = relationship('Consultation')


class Consultation(Base):
    __tablename__ = 'consultation'

    CONSULTATION_ID = Column(Integer, primary_key=True, index=True)
    SSN_ID = Column(ForeignKey('dmpcpatient.SSN_ID', ondelete='CASCADE'), nullable=False, index=True)
    CONSULTATION_DATE = Column(Date, nullable=False)
    TRAITEMENT = Column(String(500), nullable=False)
    HISTORIQUE = Column(String(500), nullable=False)
    PERSONNELSANTE_ID = Column(ForeignKey('dmpcpersonnelsante.PERSONNELSANTE_ID'), index=True)

    dmpcpersonnelsante = relationship('Dmpcpersonnelsante')
    dmpcpatient = relationship('Dmpcpatient')


class Contributeur(Base):
    __tablename__ = 'contributeur'
    __table_args__ = (
        Index('IDX_CONTRIBUTEUR', 'DMPCSUBMISSION_ID', 'PERSONNELSANTE_ID'),
    )

    DMPCSUBMISSION_ID = Column(ForeignKey('avis.DMPCSUBMISSION_ID', ondelete='CASCADE'), primary_key=True, nullable=False)
    PERSONNELSANTE_ID = Column(ForeignKey('dmpcpersonnelsante.PERSONNELSANTE_ID', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    TEMPS_PASSE = Column(String(20), nullable=False)

    avi = relationship('Avi')
    dmpcpersonnelsante = relationship('Dmpcpersonnelsante')


class Dmpcadresse(Base):
    __tablename__ = 'dmpcadresse'

    ADRESSE_ID = Column(Integer, primary_key=True)
    ADRESSE_LIGNEADRESSE = Column(String(200), nullable=False)
    ADRESSE_VILLE = Column(String(20), nullable=False)
    ADRESSE_CODEPOSTAL = Column(String(20), nullable=False)
    ADRESSE_PAYS = Column(String(20), nullable=False)


class Dmpcpatient(Base):
    __tablename__ = 'dmpcpatient'

    SSN_ID = Column(String(15), primary_key=True, index=True)
    PERSONNELSANTE_ID = Column(ForeignKey('dmpcpersonnelsante.PERSONNELSANTE_ID', ondelete='CASCADE'), nullable=False, index=True)
    ADRESSE_ID = Column(ForeignKey('dmpcadresse.ADRESSE_ID', ondelete='CASCADE'), nullable=False, index=True)
    PATIENT_NOM = Column(String(20), nullable=False)
    PATIENT_PRENOM = Column(String(20), nullable=False)
    PATIENT_DATENAISSANCE = Column(String(20), nullable=False)
    PATIENT_NOMEPOUSE = Column(String(20))
    PATIENT_DMPCSEXE = Column(String(1))
    PATIENT_INSC = Column(String(20))
    PATIENT_ORDREDENAISSANCE = Column(Integer)
    PATIENT_EMAIL = Column(String(200))
    PATIENT_TELEPHONE = Column(String(20))

    dmpcadresse = relationship('Dmpcadresse')
    dmpcpersonnelsante = relationship('Dmpcpersonnelsante')


class Dmpcpersonnelsante(Base):
    __tablename__ = 'dmpcpersonnelsante'

    PERSONNELSANTE_ID = Column(Integer, primary_key=True, index=True)
    PERSONNELSANTE_NOM = Column(String(20), nullable=False)
    PERSONNELSANTE_PRENOM = Column(String(20), nullable=False)
    PERSONNELSANTE_MDP = Column(String(20), nullable=False)
    PERSONNELSANTE_EMAIL = Column(String(200), nullable=False)
    PERSONNELSANTE_ADELI = Column(String(20))
    PERSONNELSANTE_RPPS = Column(String(20))
    PERSONNELSANTE_ROLE = Column(String(20))
    PERSONNELSANTE_SECTEURACTIVITE = Column(String(20))
    PERSONNELSANTE_TELEPHONE = Column(String(20))
    SPECIALITE_ID = Column(ForeignKey('specialite.SPECIALITE_ID'), index=True)

    specialite = relationship('Specialite')
    dmpcstructuresante = relationship('Dmpcstructuresante', secondary='dmpcstructuresante_referent')
    dmpcstructuresante1 = relationship('Dmpcstructuresante', secondary='dmpcstructuresante_medecin')


class Dmpcstructuresante(Base):
    __tablename__ = 'dmpcstructuresante'

    STRUCTURESANTE_ID = Column(Integer, primary_key=True, index=True)
    ADRESSE_ID = Column(ForeignKey('dmpcadresse.ADRESSE_ID', ondelete='CASCADE'), nullable=False, index=True)
    STRUCTURESANTE_NOM = Column(String(20), nullable=False)
    STRUCTURESANTE_LOGIN = Column(String(20), nullable=False)
    STRUCTURESANTE_MDP = Column(String(20), nullable=False)
    STRUCTURESANTE_EMAIL = Column(String(200), nullable=False)

    dmpcadresse = relationship('Dmpcadresse')


t_dmpcstructuresante_medecin = Table(
    'dmpcstructuresante_medecin', metadata,
    Column('STRUCTURESANTE_ID', ForeignKey('dmpcstructuresante.STRUCTURESANTE_ID', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('PERSONNELSANTE_ID', ForeignKey('dmpcpersonnelsante.PERSONNELSANTE_ID', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Index('IDX_CENTRE_HOSPITALIER_REFERENT', 'STRUCTURESANTE_ID', 'PERSONNELSANTE_ID')
)


t_dmpcstructuresante_referent = Table(
    'dmpcstructuresante_referent', metadata,
    Column('STRUCTURESANTE_ID', ForeignKey('dmpcstructuresante.STRUCTURESANTE_ID', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('PERSONNELSANTE_ID', ForeignKey('dmpcpersonnelsante.PERSONNELSANTE_ID', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Index('IDX_CENTRE_HOSPITALIER_REFERENT', 'STRUCTURESANTE_ID', 'PERSONNELSANTE_ID')
)


class Examan(Base):
    __tablename__ = 'examen'

    EXAMEN_ID = Column(Integer, primary_key=True, index=True)
    PERSONNELSANTE_ID = Column(ForeignKey('dmpcpersonnelsante.PERSONNELSANTE_ID', ondelete='CASCADE'), nullable=False, index=True)
    EXAMEN_NOM = Column(String(20), nullable=False)

    dmpcpersonnelsante = relationship('Dmpcpersonnelsante')


class Resultat(Base):
    __tablename__ = 'resultat'

    DMPCDOCUMENT_ID = Column(Integer, primary_key=True, index=True)
    CONSULTATION_ID = Column(ForeignKey('consultation.CONSULTATION_ID', ondelete='CASCADE'), nullable=False, index=True)
    EXAMEN_ID = Column(ForeignKey('examen.EXAMEN_ID', ondelete='CASCADE'), nullable=False, index=True)
    IMAGE_NOM = Column(String(100), nullable=False)
    IMAGE_PATH = Column(String(100), nullable=False)
    HEART_MEASURE = Column(String(250), nullable=False)

    consultation = relationship('Consultation')
    examan = relationship('Examan')


class Specialite(Base):
    __tablename__ = 'specialite'

    SPECIALITE_ID = Column(Integer, primary_key=True, index=True)
    SPECIALITE_NOM = Column(String(200), nullable=False)
