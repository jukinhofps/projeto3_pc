import datetime

from jogo import Jogo
from filabacklog import FilaBacklog
from pilharecentes import PilhasRecentes
from sessaojogo import SessaoJogo

catalogo = []
indice_jogos = {}
backlog = FilaBacklog()
recentes = PilhasRecentes()
historico = []
tempo_por_jogo = {}

def carregar_jogos(nome_arquivo):
    
    global catalogo, indice_jogos
    catalogo = []
    indice_jogos = {}
    try:
        arquivo = open(nome_arquivo, encoding='utf-8')
        linhas = arquivo.readlines()
        arquivo.close()

        if len(linhas) > 0:
            linhas = linhas[1:]

        id_atual = 1
        jogos_carregados = 0
        jogos_pulados = 0

        for linha in linhas:
            linha = linha.strip()
            if not linha:
                continue

            partes = [p.strip() for p in linha.split(',')]

            try:
                if len(partes) < 13:
                    jogos_pulados += 1
                    continue

                img = partes[0]
                titulo = partes[1]
                console = partes[2]
                genero = partes[3]
                publisher = partes[4]
                developer = partes[5]

                try:
                    critic_score = float(partes[6])
                except:
                    critic_score = 0.0
                try:
                    total_vendas = float(partes[7])
                except:
                    total_vendas = 0.0
                try:
                    vendas_an = float(partes[8])
                except:
                    vendas_an = 0.0
                try:
                    vendas_jp = float(partes[9])
                except:
                    vendas_jp = 0.0
                try:
                    vendas_eu = float(partes[10])   # PAL sales
                except:
                    vendas_eu = 0.0
                try:
                    outras_vendas = float(partes[11])
                except:
                    outras_vendas = 0.0

                data_lanc = partes[12]

                jogo = Jogo(id_atual, titulo, console, genero, publisher, 
                           developer, critic_score, total_vendas, vendas_an, 
                           vendas_jp, vendas_eu, outras_vendas, data_lanc)
                
                catalogo.append(jogo)
                indice_jogos[id_atual] = jogo
                id_atual += 1
                jogos_carregados += 1

            except Exception:
                jogos_pulados += 1
                continue

        print(f'Catálogo carregado com sucesso!')
        print(f'→ Jogos carregados: {jogos_carregados}')
        print(f'→ Jogos pulados: {jogos_pulados}')
        print(f'→ Total no catálogo: {len(catalogo)}')

    except Exception as e:
        print(f'Erro ao carregar o arquivo: {e}')

def listar_jogos():
    if len(catalogo) == 0:
        print('Catálogo vazio. Carregue o catálogo primeiro.')
        return
    for jogo in catalogo:
        jogo.exibir()


def buscar_jogo_por_nome(termo):
    resultado = []
    for jogo in catalogo:
        if termo.lower() in jogo.titulo.lower():
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_genero(genero):
    resultado = []
    for jogo in catalogo:
        if jogo.genero.lower() == genero.lower():
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado para esse gênero.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_console(console):
    resultado = []
    for jogo in catalogo:
        if jogo.console.lower() == console.lower():
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado para esse console.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_nota(nota_minima):
    resultado = []
    for jogo in catalogo:
        if jogo.critic_score >= nota_minima:
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado com essa nota mínima.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_vendas(vendas_minimas):
    resultado = []
    for jogo in catalogo:
        if jogo.total_vendas >= vendas_minimas:
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado com esse mínimo de vendas.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def filtrar_por_publisher(publisher):
    resultado = []
    for jogo in catalogo:
        if jogo.publisher.lower() == publisher.lower():
            resultado.append(jogo)
    if len(resultado) == 0:
        print('Nenhum jogo encontrado para essa publisher.')
    else:
        for jogo in resultado:
            jogo.exibir()
    return resultado


def ordenar_jogos(criterio):
    if len(catalogo) == 0:
        print('Catálogo vazio.')
        return

    lista = catalogo[:]

    if criterio == 'titulo':
        lista.sort(key=lambda x: x.titulo)
    elif criterio == 'nota':
        lista.sort(key=lambda x: x.critic_score, reverse=True)
    elif criterio == 'vendas':
        lista.sort(key=lambda x: x.total_vendas, reverse=True)
    elif criterio == 'data':
        lista.sort(key=lambda x: x.data_lanc, reverse=True)
    elif criterio == 'console':
        lista.sort(key=lambda x: x.console)
    elif criterio == 'genero':
        lista.sort(key=lambda x: x.genero)
    else:
        print('Critério inválido.')
        return

    for jogo in lista:
        jogo.exibir()

def adicionar_ao_backlog(jogo):
    if backlog.contem(jogo.id_jogo):
        print('Esse jogo já está no backlog.')
        return
    backlog.enqueue(jogo)
    print(f'{jogo.titulo} adicionado ao backlog.')


def mostrar_backlog():
    backlog.mostrar()


def jogar_proximo():
    jogo = backlog.dequeue()
    if jogo is None:
        print('Backlog vazio.')
        return
    print(f'Iniciando: {jogo.titulo}')
    recentes.push(jogo)
    tempo = float(input('Quantas horas você jogou nessa sessão? '))
    registrar_sessao(jogo, tempo)


def salvar_backlog():
    arquivo = open('backlog.txt', 'w', encoding='utf-8')
    arquivo.write('id;titulo;console\n')
    for jogo in backlog.dados:
        arquivo.write(f'{jogo.id_jogo};{jogo.titulo};{jogo.console}\n')
    arquivo.close()
    print('Backlog salvo com sucesso.')


def carregar_backlog():
    try:
        arquivo = open('backlog.txt', 'r', encoding='utf-8')
        linhas = arquivo.readlines()
        arquivo.close()
        linhas = linhas[1:]
        for linha in linhas:
            linha = linha.strip()
            if linha == '':
                continue
            partes = linha.split(';')
            if len(partes) < 3:
                continue
            try:
                id_jogo = int(partes[0])
            except:
                continue
            if id_jogo in indice_jogos:
                jogo = indice_jogos[id_jogo]
                if not backlog.contem(id_jogo):
                    backlog.enqueue(jogo)
        print('Backlog carregado.')
    except:
        print('Nenhum backlog salvo encontrado.')


def _calcular_status(tempo_total):
    if tempo_total < 2:
        return 'iniciado'
    elif tempo_total < 10:
        return 'em andamento'
    elif tempo_total < 20:
        return 'muito jogado'
    else:
        return 'concluído simbolicamente'


def registrar_sessao(jogo, tempo):
    if jogo.id_jogo not in tempo_por_jogo:
        tempo_por_jogo[jogo.id_jogo] = 0.0
    tempo_por_jogo[jogo.id_jogo] += tempo
    tempo_total = tempo_por_jogo[jogo.id_jogo]
    status = _calcular_status(tempo_total)
    data_sessao = datetime.date.today().strftime('%Y-%m-%d')
    sessao = SessaoJogo(jogo, tempo, data_sessao, tempo_total, status)
    historico.append(sessao)
    recentes.push(jogo)
    print(f'Sessão registrada! Total em {jogo.titulo}: {tempo_total}h | Status: {status}')
    salvar_historico()


def mostrar_recentes():
    if recentes.is_empty():
        print('Nenhum jogo recente.')
        return
    recentes.mostrar()


def retomar_ultimo_jogo():
    jogo = recentes.topo()
    if jogo is None:
        print('Nenhum jogo recente para retomar.')
        return
    print(f'Retomando: {jogo.titulo}')
    recentes.push(jogo)
    tempo = float(input('Quantas horas você jogou nessa sessão? '))
    registrar_sessao(jogo, tempo)


def salvar_historico():
    arquivo = open('historico_jogo.txt', 'w', encoding='utf-8')
    arquivo.write('titulo;tempo_sessao;tempo_total;status\n')
    for sessao in historico:
        arquivo.write(f'{sessao.jogo.titulo};{sessao.tempo_jogado};{sessao.tempo_total};{sessao.status}\n')
    arquivo.close()


def carregar_historico():
    global historico
    try:
        arquivo = open('historico_jogo.txt', 'r', encoding='utf-8')
        linhas = arquivo.readlines()
        arquivo.close()
        linhas = linhas[1:]
        for linha in linhas:
            linha = linha.strip()
            if linha == '':
                continue
            partes = linha.split(';')
            if len(partes) < 4:
                continue
            titulo = partes[0]
            try:
                tempo_sessao = float(partes[1])
            except:
                tempo_sessao = 0.0
            try:
                tempo_total = float(partes[2])
            except:
                tempo_total = 0.0
            status = partes[3]
            jogo_encontrado = None
            for j in catalogo:
                if j.titulo == titulo:
                    jogo_encontrado = j
                    break
            if jogo_encontrado is None:
                continue
            data_sessao = 'carregado'
            sessao = SessaoJogo(jogo_encontrado, tempo_sessao, data_sessao, tempo_total, status)
            historico.append(sessao)
            tempo_por_jogo[jogo_encontrado.id_jogo] = max(tempo_por_jogo.get(jogo_encontrado.id_jogo, 0.0), tempo_total)
        print('Histórico carregado.')
    except:
        print('Nenhum histórico salvo encontrado.')


def salvar_recentes():
    arquivo = open('recentes.txt', 'w', encoding='utf-8')
    arquivo.write('id;titulo;console\n')
    for jogo in recentes.dados:
        arquivo.write(f'{jogo.id_jogo};{jogo.titulo};{jogo.console}\n')
    arquivo.close()


def carregar_recentes():
    try:
        arquivo = open('recentes.txt', 'r', encoding='utf-8')
        linhas = arquivo.readlines()
        arquivo.close()
        linhas = linhas[1:]
        for linha in linhas:
            linha = linha.strip()
            if linha == '':
                continue
            partes = linha.split(';')
            if len(partes) < 3:
                continue
            try:
                id_jogo = int(partes[0])
            except:
                continue
            if id_jogo in indice_jogos:
                recentes.push(indice_jogos[id_jogo])
        print('Recentes carregados.')
    except:
        print('Nenhum arquivo de recentes encontrado.')


def mostrar_historico():
    if len(historico) == 0:
        print('Nenhuma sessão registrada.')
        return
    for sessao in historico:
        sessao.exibir()


def _obter_jogos_jogados():
    return {sessao.jogo.id_jogo for sessao in historico}


def _obter_ids_backlog():
    return {jogo.id_jogo for jogo in backlog.dados}


def recomendar_jogos():
    if len(historico) == 0:
        print('Sem histórico suficiente para recomendar jogos.')
        return []

    genero_tempo = {}
    console_tempo = {}
    nota_total = 0.0
    nota_cont = 0
    for sessao in historico:
        genero_tempo[sessao.jogo.genero] = genero_tempo.get(sessao.jogo.genero, 0) + sessao.tempo_jogado
        console_tempo[sessao.jogo.console] = console_tempo.get(sessao.jogo.console, 0) + sessao.tempo_jogado
        nota_total += sessao.jogo.critic_score
        nota_cont += 1

    genero_preferido = max(genero_tempo, key=genero_tempo.get) if genero_tempo else ""
    console_preferido = max(console_tempo, key=console_tempo.get) if console_tempo else ""
    nota_media = nota_total / nota_cont if nota_cont else 0.0

    jogados = _obter_jogos_jogados()
    ids_backlog = _obter_ids_backlog()
    recomendados = []

    for jogo in catalogo:
        if jogo.id_jogo in jogados or jogo.id_jogo in ids_backlog:
            continue
        score = 0
        if jogo.genero.lower() == genero_preferido.lower():
            score += 2
        if jogo.console.lower() == console_preferido.lower():
            score += 2
        if jogo.critic_score >= nota_media:
            score += 1
        if jogo.total_vendas >= 1.0:
            score += 1
        if score > 0:
            recomendados.append((score, jogo))

    if len(recomendados) == 0:
        print('Sem recomendações novas no momento.')
        return []

    recomendados.sort(key=lambda item: (-item[0], -item[1].critic_score, -item[1].total_vendas))

    print('Critérios usados para recomendação:')
    print(f'- Gênero preferido: {genero_preferido}')
    print(f'- Console preferido: {console_preferido}')
    print(f'- Nota média dos jogos jogados: {nota_media:.1f}')
    print('- Evitando jogos já jogados ou presentes no backlog')
    print('Sugestões:')
    for score, jogo in recomendados[:5]:
        print(f'[{score}]', end=' ')
        jogo.exibir()

    return [jogo for score, jogo in recomendados[:5]]


def gerar_ranking_pessoal():
    if len(tempo_por_jogo) == 0:
        print('Nenhum tempo registrado para gerar ranking pessoal.')
        return

    print('=== Ranking pessoal ===')
    ranking_jogos = sorted(tempo_por_jogo.items(), key=lambda item: item[1], reverse=True)
    print('Jogos mais jogados:')
    for id_jogo, tempo in ranking_jogos[:5]:
        jogo = indice_jogos.get(id_jogo)
        if jogo:
            print(f'- {jogo.titulo}: {tempo:.1f}h')

    genero_tempo = {}
    console_tempo = {}
    for id_jogo, tempo in tempo_por_jogo.items():
        jogo = indice_jogos.get(id_jogo)
        if jogo:
            genero_tempo[jogo.genero] = genero_tempo.get(jogo.genero, 0) + tempo
            console_tempo[jogo.console] = console_tempo.get(jogo.console, 0) + tempo

    if genero_tempo:
        genero_favorito = max(genero_tempo, key=genero_tempo.get)
        print(f'Gênero favorito: {genero_favorito} ({genero_tempo[genero_favorito]:.1f}h)')
    if console_tempo:
        console_favorito = max(console_tempo, key=console_tempo.get)
        print(f'Console favorito: {console_favorito} ({console_tempo[console_favorito]:.1f}h)')

    notas_jogados = []
    for id_jogo in _obter_jogos_jogados():
        jogo = indice_jogos.get(id_jogo)
        if jogo:
            notas_jogados.append((jogo.critic_score, jogo.titulo))
    if notas_jogados:
        notas_jogados.sort(reverse=True)
        print('Top jogos por nota entre os jogados:')
        for nota, titulo in notas_jogados[:5]:
            print(f'- {titulo}: {nota}')


def exibir_dashboard():
    total_catalogo = len(catalogo)
    total_backlog = backlog.tamanho()
    total_recentes = recentes.tamanho()
    total_sessoes = len(historico)
    tempo_total = sum(tempo_por_jogo.values())
    media_horas = tempo_total / total_sessoes if total_sessoes > 0 else 0.0

    jogo_mais_jogado = None
    if tempo_por_jogo:
        id_mais = max(tempo_por_jogo, key=tempo_por_jogo.get)
        jogo_mais_jogado = indice_jogos.get(id_mais)

    genero_tempo = {}
    console_tempo = {}
    for id_jogo, tempo in tempo_por_jogo.items():
        jogo = indice_jogos.get(id_jogo)
        if jogo:
            genero_tempo[jogo.genero] = genero_tempo.get(jogo.genero, 0) + tempo
            console_tempo[jogo.console] = console_tempo.get(jogo.console, 0) + tempo

    genero_favorito = max(genero_tempo, key=genero_tempo.get) if genero_tempo else 'N/A'
    console_favorito = max(console_tempo, key=console_tempo.get) if console_tempo else 'N/A'

    nota_media = 0.0
    if _obter_jogos_jogados():
        notas = [indice_jogos[id_jogo].critic_score for id_jogo in _obter_jogos_jogados() if indice_jogos.get(id_jogo)]
        if notas:
            nota_media = sum(notas) / len(notas)

    total_iniciados = sum(1 for tempo in tempo_por_jogo.values() if tempo > 0)
    total_concluidos = sum(1 for tempo in tempo_por_jogo.values() if tempo >= 20)

    print('=== DASHBOARD ===')
    print(f'Total de jogos no catálogo: {total_catalogo}')
    print(f'Total de jogos no backlog: {total_backlog}')
    print(f'Total de jogos recentes: {total_recentes}')
    print(f'Total de sessões jogadas: {total_sessoes}')
    print(f'Tempo total jogado: {tempo_total:.1f}h')
    if jogo_mais_jogado:
        print(f'Jogo mais jogado: {jogo_mais_jogado.titulo} ({tempo_por_jogo[jogo_mais_jogado.id_jogo]:.1f}h)')
    print(f'Gênero favorito: {genero_favorito}')
    print(f'Console favorito: {console_favorito}')
    print(f'Nota média dos jogos jogados: {nota_media:.1f}')
    print(f'Total de jogos já iniciados: {total_iniciados}')
    print(f'Total de jogos concluídos simbolicamente: {total_concluidos}')
    print(f'Média de horas por sessão: {media_horas:.1f}h')


def _buscar_jogo_por_id(id_jogo):
    return indice_jogos.get(id_jogo)


def menu():
    carregar_jogos('dataset.csv')
    carregar_backlog()
    carregar_historico()
    carregar_recentes()

    while True:
        print('\n===== STEAMPY =====')
        print('1.  Carregar catálogo')
        print('2.  Listar jogos')
        print('3.  Buscar jogo por nome')
        print('4.  Filtrar por gênero')
        print('5.  Filtrar por console')
        print('6.  Filtrar por nota mínima')
        print('7.  Filtrar por vendas mínimas')
        print('8.  Filtrar por publisher')
        print('9.  Ordenar catálogo')
        print('10. Adicionar jogo ao backlog')
        print('11. Ver backlog')
        print('12. Jogar próximo do backlog')
        print('13. Ver jogos recentes')
        print('14. Retomar último jogo')
        print('15. Registrar tempo de jogo')
        print('16. Ver histórico completo')
        print('17. Ver recomendações')
        print('18. Ver ranking pessoal')
        print('19. Ver dashboard')
        print('20. Salvar backlog')
        print('21. Sair')
        print('===================')

        opcao = input('Escolha uma opção: ')

        if opcao == '1':
            carregar_jogos('dataset.csv')
        elif opcao == '2':
            listar_jogos()
        elif opcao == '3':
            termo = input('Digite o nome ou parte do nome: ')
            buscar_jogo_por_nome(termo)
        elif opcao == '4':
            genero = input('Digite o gênero: ')
            filtrar_por_genero(genero)
        elif opcao == '5':
            console = input('Digite o console: ')
            filtrar_por_console(console)
        elif opcao == '6':
            try:
                nota = float(input('Digite a nota mínima: '))
                filtrar_por_nota(nota)
            except:
                print('Valor inválido.')
        elif opcao == '7':
            try:
                vendas = float(input('Digite o mínimo de vendas (em milhões): '))
                filtrar_por_vendas(vendas)
            except:
                print('Valor inválido.')
        elif opcao == '8':
            publisher = input('Digite o nome da publisher: ')
            filtrar_por_publisher(publisher)
        elif opcao == '9':
            print('Critérios: titulo, nota, vendas, data, console, genero')
            criterio = input('Digite o critério: ')
            ordenar_jogos(criterio)
        elif opcao == '10':
            try:
                id_jogo = int(input('Digite o ID do jogo: '))
                jogo = _buscar_jogo_por_id(id_jogo)
                if jogo:
                    adicionar_ao_backlog(jogo)
                else:
                    print('Jogo não encontrado.')
            except:
                print('ID inválido.')
        elif opcao == '11':
            mostrar_backlog()
        elif opcao == '12':
            jogar_proximo()
            salvar_backlog()
            salvar_recentes()
        elif opcao == '13':
            mostrar_recentes()
        elif opcao == '14':
            retomar_ultimo_jogo()
            salvar_recentes()
        elif opcao == '15':
            try:
                id_jogo = int(input('Digite o ID do jogo: '))
                jogo = _buscar_jogo_por_id(id_jogo)
                if jogo:
                    tempo = float(input('Quantas horas você jogou? '))
                    recentes.push(jogo)
                    registrar_sessao(jogo, tempo)
                    salvar_recentes()
                else:
                    print('Jogo não encontrado.')
            except:
                print('Valor inválido.')
        elif opcao == '16':
            mostrar_historico()
        elif opcao == '17':
            recomendar_jogos()
        elif opcao == '18':
            gerar_ranking_pessoal()
        elif opcao == '19':
            exibir_dashboard()
        elif opcao == '20':
            salvar_backlog()
        elif opcao == '21':
            salvar_backlog()
            salvar_historico()
            salvar_recentes()
            print('Até logo!')
            break
        else:
            print('Opção inválida.')


if __name__ == "__main__":
    menu()