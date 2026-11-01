
import matplotlib.pyplot as plt
import numpy as np
print("Sistema de Avaliação da Qualidade do Atendimento")
print("Python está funcionando corretamente!")

# Célula 1: Importar bibliotecas

# Configurar gráficos
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)


# Célula 2: Funções de pertinência para Tempo de Espera

def tempo_rapido(x):
    """Função de pertinência para tempo rápido (0-15 min)"""
    if x <= 10:
        return 1.0
    elif x <= 20:
        return (20 - x) / 10
    else:
        return 0.0


def tempo_medio(x):
    """Função de pertinência para tempo médio (10-30 min)"""
    if x <= 10:
        return 0.0
    elif x <= 20:
        return (x - 10) / 10
    elif x <= 30:
        return (30 - x) / 10
    else:
        return 0.0


def tempo_lento(x):
    """Função de pertinência para tempo lento (25-60 min)"""
    if x <= 25:
        return 0.0
    elif x <= 35:
        return (x - 25) / 10
    else:
        return 1.0


# Célula 3: Funções de pertinência para Cordialidade

def cordialidade_baixa(x):
    """Cordialidade baixa (0-4)"""
    if x <= 3:
        return 1.0
    elif x <= 5:
        return (5 - x) / 2
    else:
        return 0.0


def cordialidade_media(x):
    """Cordialidade média (3-7)"""
    if x <= 3:
        return 0.0
    elif x <= 5:
        return (x - 3) / 2
    elif x <= 7:
        return (7 - x) / 2
    else:
        return 0.0


def cordialidade_alta(x):
    """Cordialidade alta (6-10)"""
    if x <= 6:
        return 0.0
    elif x <= 8:
        return (x - 6) / 2
    else:
        return 1.0


# Célula 4: Regras do sistema fuzzy

def avaliar_atendimento(tempo, cordialidade):
    """
    Regras:
    1. Tempo rápido E cordialidade alta -> EXCELENTE
    2. Tempo rápido E cordialidade média -> BOA
    3. Tempo médio E cordialidade alta -> BOA
    4. Tempo médio E cordialidade média -> REGULAR
    5. Caso contrário -> RUIM
    """

    # Calcular graus de pertinência
    t_rapido = tempo_rapido(tempo)
    t_medio = tempo_medio(tempo)
    t_lento = tempo_lento(tempo)

    c_baixa = cordialidade_baixa(cordialidade)
    c_media = cordialidade_media(cordialidade)
    c_alta = cordialidade_alta(cordialidade)

    # Aplicar regras usando MIN para o operador E
    excelente = min(t_rapido, c_alta)

    boa = max(
        min(t_rapido, c_media),
        min(t_medio, c_alta)
    )

    regular = min(t_medio, c_media)

    ruim = max(
        min(t_lento, c_baixa),
        min(t_lento, c_media),
        min(t_lento, c_alta),
        min(t_rapido, c_baixa),
        min(t_medio, c_baixa)
    )

    # Defuzzificação por média ponderada
    qualidade_final = (
        excelente * 9 +
        boa * 7 +
        regular * 5 +
        ruim * 2
    ) / max(excelente + boa + regular + ruim, 0.001)

    return {
        'excelente': excelente,
        'boa': boa,
        'regular': regular,
        'ruim': ruim,
        'qualidade_final': qualidade_final
    }


# Célula 5: Testar o sistema

def testar_sistema():

    casos_teste = [
        {
            "tempo": 8,
            "cordialidade": 9,
            "descricao": "Atendimento rápido e muito cordial"
        },
        {
            "tempo": 15,
            "cordialidade": 6,
            "descricao": "Atendimento médio"
        },
        {
            "tempo": 35,
            "cordialidade": 3,
            "descricao": "Atendimento demorado e pouco cordial"
        },
        {
            "tempo": 12,
            "cordialidade": 8,
            "descricao": "Bom atendimento geral"
        }
    ]

    print("=== TESTE DO SISTEMA DE LÓGICA NEBULOSA ===\n")

    for i, caso in enumerate(casos_teste, 1):

        resultado = avaliar_atendimento(
            caso["tempo"],
            caso["cordialidade"]
        )

        print(f"Caso {i}: {caso['descricao']}")
        print(f"  Tempo de espera: {caso['tempo']} minutos")
        print(f"  Cordialidade: {caso['cordialidade']}/10")
        print("  Graus de pertinência:")
        print(f"  Excelente: {resultado['excelente']:.2f}")
        print(f"  Boa: {resultado['boa']:.2f}")
        print(f"  Regular: {resultado['regular']:.2f}")
        print(f"  Ruim: {resultado['ruim']:.2f}")
        print(
            f"  Qualidade final: "
            f"{resultado['qualidade_final']:.2f}/10\n"
        )


testar_sistema()


# Célula 6: Visualizar funções de pertinência

def plotar_funcoes_pertinencia():

    # Gráfico do tempo
    tempo_range = np.linspace(0, 60, 100)

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)

    plt.plot(
        tempo_range,
        [tempo_rapido(t) for t in tempo_range],
        'g-', label='Rápido', linewidth=2
    )

    plt.plot(
        tempo_range,
        [tempo_medio(t) for t in tempo_range],
        'y-', label='Médio', linewidth=2
    )

    plt.plot(
        tempo_range,
        [tempo_lento(t) for t in tempo_range],
        'r-', label='Lento', linewidth=2
    )

    plt.title('Tempo de Espera')
    plt.xlabel('Minutos')
    plt.ylabel('Grau de Pertinência')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Gráfico da cordialidade
    cord_range = np.linspace(0, 10, 100)

    plt.subplot(1, 3, 2)

    plt.plot(
        cord_range,
        [cordialidade_baixa(c) for c in cord_range],
        'r-', label='Baixa', linewidth=2
    )

    plt.plot(
        cord_range,
        [cordialidade_media(c) for c in cord_range],
        'y-', label='Média', linewidth=2
    )

    plt.plot(
        cord_range,
        [cordialidade_alta(c) for c in cord_range],
        'g-', label='Alta', linewidth=2
    )

    plt.title('Cordialidade')
    plt.xlabel('Pontuação (0-10)')
    plt.ylabel('Grau de Pertinência')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Superfície de qualidade
    plt.subplot(1, 3, 3)

    T, C = np.meshgrid(
        np.linspace(0, 60, 30),
        np.linspace(0, 10, 30)
    )

    Z = np.zeros_like(T)

    for i in range(T.shape[0]):
        for j in range(T.shape[1]):

            resultado = avaliar_atendimento(
                T[i, j],
                C[i, j]
            )

            Z[i, j] = resultado['qualidade_final']

    contour = plt.contourf(
        T, C, Z,
        levels=20,
        cmap='RdYlGn'
    )

    plt.colorbar(contour)
    plt.title('Superfície de Qualidade')
    plt.xlabel('Tempo (min)')
    plt.ylabel('Cordialidade')

    plt.tight_layout()
    plt.show()


plotar_funcoes_pertinencia()
