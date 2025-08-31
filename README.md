O que o código faz
O script busca a chave privada de uma carteira Bitcoin, conhecida como Puzzle #71. Esse "puzzle" é um desafio em que a chave privada de uma carteira Bitcoin com saldo é revelada, mas em um intervalo de 256 bits (um número enorme). O objetivo é encontrar a chave exata para acessar o saldo.

O código faz o seguinte:

Define o Alvo: A constante TARGET_ADDRESS define o endereço Bitcoin que o script deve encontrar.

Calcula o Intervalo: Ele define um intervalo de pesquisa (SEARCH_START a SEARCH_END) que corresponde a 15% do intervalo total de chaves (entre 75% e 90%).

Carrega Progresso: O script lê o arquivo puzzle71_controle.txt para carregar as chaves que já foram testadas. Isso permite que a busca continue de onde parou em execuções anteriores, evitando retrabalho.

Pesquisa Aleatória: A linha private_key_int = random.randint(SEARCH_START, SEARCH_END) é a parte fundamental. Ela usa a biblioteca random para gerar um número inteiro aleatório dentro do intervalo de busca.

Valida e Salva: Para cada chave gerada, o script verifica se ela já foi testada. Se não, ele a converte para o formato hexadecimal, gera o endereço Bitcoin correspondente e compara com o TARGET_ADDRESS. Ele também salva a chave testada no arquivo de controle para futuras execuções.

Exibe o Progresso: A cada 1.000 chaves testadas, ele exibe a velocidade da busca.

Salva a Solução: Se o endereço gerado for o mesmo do alvo, ele salva a chave privada e o endereço no arquivo puzzle71_solucao.txt e encerra a execução.

Dependências
Para executar o código, você precisa instalar as seguintes bibliotecas Python usando o comando pip:

ecdsa

base58

Você pode instalá-las com o seguinte comando no seu terminal ou prompt de comando:

Bash

pip install ecdsa base58
