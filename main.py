from fastapi import FastAPI, HTTPException, status
from sqlmodel import SQLModel, Field, create_engine, Session, select

#Modelo de la base de datos
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    apellido: str 
    correo: str
    edad: int = 0

#Schema de la base de datos
class StudentCreate(SQLModel):
    nombre: str
    apellido: str 
    correo: str
    edad: int = 0

class StudentRead(SQLModel):
    nombre: str
    apellido: str 
    correo: str


sqlite_url = "sqlite:///estudiante.db"
engine = create_engine(sqlite_url, echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(lifespan=create_tables())

@app.get("/") # Decorador
def read_root():
    return {"Hello": "Grace"}

@app.post("/estudiantes", status_code=status.HTTP_201_CREATED, response_model=StudentRead)
def create_student(datos: StudentCreate):
    student = Student(nombre=datos.nombre, apellido=datos.apellido, correo=datos.correo, edad=datos.edad)
    with Session(engine) as session:
        session.add(student)
        session.commit()
        session.refresh(student)
        return student
@app.get("/estudiantes")
def read_students():
    with Session(engine) as session:
        return session.exec(select(Student)).all()

@app.get("/estudiantes/{student_id}")
def read_student(student_id: int):
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        return student

@app.delete("/estudiantes/{student_id}")
def delete_student(student_id: int):    
    with Session(engine) as session:
        student = session.get(Student, student_id)
        if student is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        session.delete(student)
        session.commit()
        return {"message": "Estudiante eliminado exitosamente"}


