import pandas as pd
from model.cursoEG import CursoEG
from conexion.mongo_queries import MongoQueries


class Controller_CursoEG:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_curso(self) -> CursoEG:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        id_curso = input("id do curso (NOVO): ")

        # Verifica se o curso existe na base de dados
        if self.verifica_existencia_curso(id_curso):
            nome = input("nome do curso (novo): ")
            coordenador = input("nome do coordenador: ")

            self.mongo.db["cursoEG"].insert_one(
                {"id_curso": id_curso, "nome": nome, "coordenador": coordenador})

            df_curso = self.recupera_curso(id_curso)

            novo_curso = CursoEG(
                id_curso, df_curso.nome.values[0], df_curso.coordenador.values[0])

            print(novo_curso.to_string())
            self.mongo.close()
            # Retorna o objeto novo_curso para utilização posterior, caso necessário
            return novo_curso
        else:
            self.mongo.close()
            print(f"O curso de id {id_curso} ja esta cadastrado")
            return None

    def atualizar_curso(self) -> CursoEG:
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        id_curso = input("Id do curso que deseja atualizar os dados: ")

        # Verifica se o curso existe na base de dados
        if not self.verifica_existencia_curso(id_curso):
            # solicita a nova descriçao do curso
            novo_nome_curso = input("Novo nome do Curso: ")
            novo_nome_coordenador = input("Novo nome do coordenador: ")

            # Atualiza o nome do curso existente
            self.mongo.db["cursoEG"].update_one({"id_curso": f"{id_curso}"}, {
                                                "set": {"nome": novo_nome_curso}})

            self.mongo.db["cursoEG"].update_one({"id_curso": f"{id_curso}"}, {
                                                "set": {"coordenador": novo_nome_coordenador}})

            # Recupera os dados do novo curso criado transformando em um DataFrame
            df_curso = self.recupera_curso(id_curso)

            # Cria um novo obejto curso
            curso_atualizado = CursoEG(
                id_curso, df_curso.nome.values[0], df_curso.coordenador.values[0])

            # Exibe os atributos do novo curso
            print(curso_atualizado.to_string())
            # Retorna o objeto curso_atualizado para utilização posterior, caso necessário
            return curso_atualizado
        else:
            print(f"O id_curso {id_curso} não existe.")
            return None

    def excluir_curso(self):
        # Cria uma nova conexão com o banco que permite alteração
        self.mongo.connect()

        id_curso = input("Id do curso que deseja excluir: ")

        # Verifica se o curso existe na base de dados
        if not self.verifica_existencia_curso(id_curso):

            # Recupera os dados do novo curso criado transformando em um DataFrame
            df_curso = self.recupera_curso(id_curso)

            opcao_excluir = input(
                f"Tem certeza que deseja excluir o curso {df_curso.nome.values[0]} [S ou N]: ")

            if opcao_excluir in "Ss":
                # Pede uma confirmação ao usuário
                print(
                    "Atenção, caso o curso possua professores ou alunos vinculados, também serão excluídos")
                opcao_excluir = input(
                    f"Tem certeza que deseja excluir o curso {df_curso.nome.values[0]} [S ou N]: ")

                if opcao_excluir in "Ss":

                    # Remove o curso da tabela e as entidades que possuem alguma referência com o curso
                    self.mongo.db["AlunosEG"].delete_one(
                        {"id_curso": f"{id_curso}"})

                    self.mongo.db["ProfessoresEG"].delete_one(
                        {"id_curso": f"{id_curso}"})

                    self.mongo.db["CursoEG"].delete_one(
                        {"id_curso": f"{id_curso}"})

                    # Cria um novo obejto curso exlcuido
                    curso_excluido = CursoEG(
                        id_curso, df_curso.nome.values[0], df_curso.coordenador.values[0])

                    # Exibe os atributos do curso excluido
                    print(curso_excluido.to_string())
        else:
            print(f"O id_curso {id_curso} não existe.")

    def verifica_existencia_curso(self, id_curso: int = None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo curso criado transformando em um DataFrame
        df_curso = pd.DataFrame(self.mongo.db["cursoEG"].find(
            {"id_curso": f"{id_curso}"}, {"id_curso": 1, "nome": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_curso.empty

    def recupera_curso(self, id_curso: int = None, external: bool = False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo curso criado transformando em um DataFrame
        df_curso = pd.DataFrame(list(self.mongo.db["cursoEG"].find(
            {"id_curso": f"{id_curso}"}, {"id_curso": 1, "nome": 1, "_id": 0})))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_curso
