from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING


class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_alunos_curso(self):
        # Cria uma nova conexão com o banco
        mongo = MongoQueries()
        mongo.connect()
        # Realiza uma consulta no mongo e retorna o cursor resultante para a variável
        query_result = mongo.db['cursoEG'].aggregate([{
            '$lookup': {'from': 'AlunosEG',
                        'localField': 'id_curso',
                        'foreignField': 'id_curso',
                        'as': 'aluno'
                        }
        },
            {
            '$unwind': {"path": "$aluno"}
        },
            {'$project': {'id_curso': 1,
                          'matricula': 1,
                          'nome': 1,
                          'cpf': 1,
                          'coordenador': 1,
                          '_id': 0
                          }}
        ])

        # Converte o cursos em lista e em DataFrame
        df_alunos_curso = pd.DataFrame(list(query_result))

        # Fecha a conexão com o mongo
        mongo.close()
        # Exibe o resultado
        print(df_alunos_curso[["id_curso", "matricula", "nome",
                               "cpf", "coordenador"]])
        input("Pressione Enter para Sair do Relatório de alunos por curso")

    def get_alunos(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db['alunosEG'].find()

        df_alunos = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_alunos[["matricula", "nome", "cpf", "id_curso"]])

    def get_cursos(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db['cursoEG'].find()

        df_cursos = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_cursos[["id_curso", "nome", "coordenador"]])

    def get_professores(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db['professoresEG'].find()

        df_professores = pd.DataFrame(list(query_result))

        mongo.close()

        print(df_professores[["id_professor",
              "nome", "qtde_turmas", "id_curso"]])
