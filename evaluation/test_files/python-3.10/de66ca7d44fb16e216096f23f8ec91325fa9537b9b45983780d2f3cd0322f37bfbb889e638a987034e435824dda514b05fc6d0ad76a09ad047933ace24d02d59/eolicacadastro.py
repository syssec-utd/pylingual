from typing import Type, TypeVar, List, Optional, Union
from datetime import datetime
from cfinterface.components.register import Register
from cfinterface.files.registerfile import RegisterFile
from inewave.newave.modelos.eolicacadastro import RegistroEolicaCadastro, RegistroEolicaCadastroConjuntoAerogeradores, RegistroEolicaCadastroAerogerador, RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo, RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva

class EolicaCadastro(RegisterFile):
    """
    Armazena os dados de entrada do NEWAVE referentes ao cadastro
    das usinas eólicas do sistema.
    """
    T = TypeVar('T')
    REGISTERS = [RegistroEolicaCadastroAerogerador, RegistroEolicaCadastroConjuntoAerogeradores, RegistroEolicaCadastro, RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo, RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva]

    def __init__(self, data=...) -> None:
        super().__init__(data)

    @classmethod
    def le_arquivo(cls, diretorio: str, nome_arquivo='eolica-cadastro.csv') -> 'EolicaCadastro':
        return cls.read(diretorio, nome_arquivo)

    def escreve_arquivo(self, diretorio: str, nome_arquivo='eolica-cadastro.csv'):
        self.write(diretorio, nome_arquivo)

    def __registros_por_tipo(self, registro: Type[T]) -> List[T]:
        """
        Obtém os registro de um tipo, se houver algum no arquivo.

        :param registro: Um tipo de registro para ser lido
        :type registro: T
        :param indice: O índice do bloco a ser acessado, dentre os do tipo
        :type indice: int

        """
        return [b for b in self.data.of_type(registro)]

    def __obtem_registros(self, tipo: Type[T]) -> List[T]:
        return self.__registros_por_tipo(tipo)

    def __obtem_registros_com_filtros(self, tipo_registro: Type[T], **kwargs) -> Optional[Union[T, List[T]]]:

        def __atende(r) -> bool:
            condicoes: List[bool] = []
            for (k, v) in kwargs.items():
                if v is not None:
                    condicoes.append(getattr(r, k) == v)
            return all(condicoes)
        regs_filtro = [r for r in self.__obtem_registros(tipo_registro) if __atende(r)]
        if len(regs_filtro) == 0:
            return None
        elif len(regs_filtro) == 1:
            return regs_filtro[0]
        else:
            return regs_filtro

    def cria_registro(self, anterior: Register, registro: Register):
        """
        Adiciona um registro ao arquivo após um outro registro previamente
        existente.

        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.add_after(anterior, registro)

    def deleta_registro(self, registro: Register):
        """
        Remove um registro existente no arquivo.

        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.remove(registro)

    def append_registro(self, registro: Register):
        """
        Adiciona um registro ao arquivo na última posição.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.append(registro)

    def preppend_registro(self, registro: Register):
        """
        Adiciona um registro ao arquivo na primeira posição.
        Este método existe para retrocompatibilidade e deve ser substituído
        quando for suportado na classe :class:`RegisterFile`.
        """
        self.data.preppend(registro)

    def eolica_cadastro(self, codigo_eolica: Optional[int]=None, nome_eolica: Optional[str]=None, quantidade_conjuntos: Optional[str]=None) -> Optional[Union[RegistroEolicaCadastro, List[RegistroEolicaCadastro]]]:
        """
        Obtém um registro que cadastra uma usina eólica.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param nome_eolica: nome da usina
        :type nome_eolica: str | None
        :param quantidade_conjuntos: quantidade de conjuntos de geradores
        :type quantidade_conjuntos: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaCadastro` |
            list[:class:`RegistroEolicaCadastro`] | None
        """
        return self.__obtem_registros_com_filtros(RegistroEolicaCadastro, codigo_eolica=codigo_eolica, nome_eolica=nome_eolica, quantidade_conjuntos=quantidade_conjuntos)

    def eolica_cadastro_conjunto_aerogeradores(self, codigo_eolica: Optional[int]=None, indice_conjunto: Optional[int]=None, nome_conjunto: Optional[str]=None, quantidade_aerogeradores: Optional[int]=None) -> Optional[Union[RegistroEolicaCadastroConjuntoAerogeradores, List[RegistroEolicaCadastroConjuntoAerogeradores]]]:
        """
        Obtém um registro que cadastra um conjunto de aerogeradores
        de uma usina.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param indice_conjunto: código do conjunto de geradores da usina
        :type indice_conjunto: int | None
        :param nome_conjunto: nome do conjunto
        :type nome_conjunto: str | None
        :param quantidade_aerogeradores: quantidade de geradores no conjunto
        :type quantidade_aerogeradores: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaCadastroConjuntoAerogeradores` |
            list[:class:`RegistroEolicaCadastroConjuntoAerogeradores`] | None
        """
        return self.__obtem_registros_com_filtros(RegistroEolicaCadastroConjuntoAerogeradores, codigo_eolica=codigo_eolica, indice_conjunto=indice_conjunto, nome_conjunto=nome_conjunto, quantidade_aerogeradores=quantidade_aerogeradores)

    def eolica_cadastro_aerogerador(self, codigo_eolica: Optional[int]=None, indice_conjunto: Optional[int]=None, velocidade_cutin: Optional[float]=None, velocidade_nominal: Optional[float]=None, velocidade_cutout: Optional[float]=None, potencia_velocidade_cutin: Optional[float]=None, potencia_velocidade_nominal: Optional[float]=None, potencia_velocidade_cutout: Optional[float]=None, altura_torre: Optional[float]=None) -> Optional[Union[RegistroEolicaCadastroAerogerador, List[RegistroEolicaCadastroAerogerador]]]:
        """
        Obtém um registro que o cadastro de um conjunto de aerogeradores
        de uma usina.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: float | None
        :param indice_conjunto: código do conjunto de geradores da usina
        :type indice_conjunto: float | None
        :param velocidade_cutin: velocidade de cutin do gerador
        :type velocidade_cutin: float | None
        :param velocidade_nominal: velocidade nominal do gerador
        :type velocidade_nominal: float | None
        :param velocidade_cutout: velocidade de cutout do gerador
        :type velocidade_cutout: float | None
        :param potencia_velocidade_cutin: potência na velocidade de cutin
        :type potencia_velocidade_cutin: float | None
        :param potencia_velocidade_nominal: potência na velocidade nominal
        :type potencia_velocidade_nominal: float | None
        :param potencia_velocidade_cutout: potência na velocidade cutout
        :type potencia_velocidade_cutout: float | None
        :param altura_torre: altura da torre do gerador
        :type altura_torre: float | None

        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaCadastroAerogerador` |
            list[:class:`RegistroEolicaCadastroAerogerador`] | None
        """
        return self.__obtem_registros_com_filtros(RegistroEolicaCadastroAerogerador, codigo_eolica=codigo_eolica, indice_conjunto=indice_conjunto, velocidade_cutin=velocidade_cutin, velocidade_nominal=velocidade_nominal, velocidade_cutout=velocidade_cutout, potencia_velocidade_cutin=potencia_velocidade_cutin, potencia_velocidade_nominal=potencia_velocidade_nominal, potencia_velocidade_cutout=potencia_velocidade_cutout, altura_torre=altura_torre)

    def eolica_conjunto_aerogeradores_quantidade_operando_periodo(self, codigo_eolica: Optional[int]=None, indice_conjunto: Optional[int]=None, periodo_inicial: Optional[datetime]=None, periodo_final: Optional[datetime]=None, numero_aerogeradores: Optional[int]=None) -> Optional[Union[RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo, List[RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo]]]:
        """
        Obtém um registro que o cadastro de um conjunto de aerogeradores
        de uma usina.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param indice_conjunto: código do conjunto de geradores da usina
        :type indice_conjunto: int | None
        :param periodo_inicial: período de início de operação
        :type periodo_inicial: datetime | None
        :param periodo_final: período de fim de operação
        :type periodo_final: datetime | None
        :param numero_aerogeradores: número de geradores operando
        :type numero_aerogeradores: int | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo` |
            list[:class:`RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo`] | None
        """
        return self.__obtem_registros_com_filtros(RegistroEolicaConjuntoAerogeradoresQuantidadeOperandoPeriodo, codigo_eolica=codigo_eolica, indice_conjunto=indice_conjunto, periodo_inicial=periodo_inicial, periodo_final=periodo_final, numero_aerogeradores=numero_aerogeradores)

    def eolica_conjunto_aerogeradores_potencia_efetiva_periodo(self, codigo_eolica: Optional[int]=None, indice_conjunto: Optional[int]=None, periodo_inicial: Optional[datetime]=None, periodo_final: Optional[datetime]=None, potencia_efetiva: Optional[float]=None) -> Optional[Union[RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva, List[RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva]]]:
        """
        Obtém um registro que contém a potência efetiva por período
        para um conjunto de aerogeradores.

        :param codigo_eolica: código que especifica a usina
        :type codigo_eolica: int | None
        :param indice_conjunto: código do conjunto de geradores da usina
        :type indice_conjunto: int | None
        :param periodo_inicial: período de início de operação
        :type periodo_inicial: datetime | None
        :param periodo_final: período de fim de operação
        :type periodo_final: datetime | None
        :param potencia_efetiva: potência efetiva do conjunto de aerogeradores
        :type potencia_efetiva: float | None
        :return: Um ou mais registros, se existirem.
        :rtype: :class:`RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva` |
            list[:class:`RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva`] | None
        """
        return self.__obtem_registros_com_filtros(RegistroEolicaConjuntoAerogeradoresPotenciaEfetiva, codigo_eolica=codigo_eolica, indice_conjunto=indice_conjunto, periodo_inicial=periodo_inicial, periodo_final=periodo_final, potencia_efetiva=potencia_efetiva)