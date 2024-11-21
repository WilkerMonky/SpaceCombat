### **Criadores:**
- **Atos Santana Antunes** - Matrícula: 29715776  
- **Gabriel Dantas Viana Ferreira** - Matrícula: 29338123  
- **Weslley Wilker Oliveira da Costa** - Matrícula: 32089660  

---
### **Tecnologias Utilizadas**
- **Python: Linguagem principal utilizada para a lógica do jogo e integração das bibliotecas.**
- **Pygame: Biblioteca principal para o desenvolvimento de jogos em 2D, fornecendo suporte para gráficos, sons, eventos e controle de entrada do usuário.**
- **Random: Biblioteca padrão do Python usada para gerar números aleatórios, ideal para criar elementos como movimentação, posição de inimigos ou itens.**
- **Visual Studio Code**
- **Git: Controle de versão para gerenciar alterações no código.**
- **GitHub: Hospedagem de repositórios e colaboração.**

---
### **Identificação da Complexidade do Jogo**
O SpaceCombat apresenta uma complexidade computacional gerenciada por estratégias de otimização e uso eficiente de algoritmos. As principais operações incluem:
- **Movimentação e Atualização: A atualização dos objetos por frame possui complexidade O(n), com remoção de itens fora da tela para manter listas enxutas.**
- **Geração de Inimigos: A criação de inimigos verifica colisões iniciais com complexidade O(k × n). O número de inimigos é controlado para evitar sobrecarga.**
- **Detecção de Colisões: Realizada entre mísseis e inimigos com complexidade O(m × n), otimizando com remoção rápida de objetos destruídos ou fora da tela.**
- **Disparos Automáticos: Os inimigos verificam o intervalo antes de disparar, com complexidade O(n).**
- **Renderização: A interface gráfica processa todos os elementos visíveis por frame com complexidade O(n), limitada a 60 FPS.**

Gerenciamento:
- **Estratégias como remoção de objetos desnecessários, cálculo oportuno, e limitação de FPS mantêm o desempenho estável.**
- **A dificuldade escala gradualmente, equilibrando a complexidade do jogo com a capacidade do hardware.**

---
### **Objetivo do Jogo**
- **O jogador deve pilotar sua nave espacial, destruir naves inimigas e desviar de seus ataques para sobreviver o maior tempo possível.**
- **Pontos são ganhos ao destruir inimigos e sobreviver mais tempo.**
- **O objetivo final é alcançar a maior pontuação possível.**
  
---
### **Jogabilidade**
Teclas de Movimento:
- **Seta para cima (↑) ou a tecla (W): Move a nave para cima.**
- **Seta para baixo (↓) ou a tecla (S): Move a nave para baixo.**
- **Seta para a esquerda (←) ou a tecla (A): Move a nave para a esquerda.**
- **Seta para a direita (→) ou a tecla (D): Move a nave para a direita.**

Ataque:
- **Espaço (Spacebar): Dispara mísseis para destruir naves inimigas.**

Pontuação:
- **Cada nave inimiga destruída concede 10 pontos.**
- **Pontos são concedidos por tempo de sobrevivência.**
- **Um contador de "kills" (inimigos destruídos) também é mantido.**

Perder o Jogo:
- **Se nave do jogador for atingida por um míssil inimigo.**
- **Se nave do jogador colidir com uma nave inimiga.**
        
--- 
### **Checklist para o jogo**
Fase 1: Análise  

    [ Atos ] Problema selecionado e definido claramente.
    [ Gabriel ] Compreensão aprofundada da natureza e desafios do problema.
    [ Wilker ] Modelo matemático ou teórico desenvolvido para representar o problema.

Fase 2: Planejamento 

    [ Atos e Wilker ] Objetivos do algoritmo definidos com clareza.
    [ Atos ] Métricas para avaliação de eficiência do algoritmo estabelecidas.
    [ Wilker ] Estratégia geral de resolução do problema proposta.
    [ Gabriel ] Subproblemas identificados e divididos, se aplicável.
    [ Wilker ] Estrutura geral do algoritmo esboçada.
    [ Gabriel ] Casos limite ou situações especiais identificados.
    [ Atos ] Análise teórica realizada para verificar a correção do algoritmo.

Fase 3: Desenho 

    [ Atos ] Análise de complexidade realizada para avaliar a eficiência teórica do algoritmo.
    [ Atos ] Pontos críticos do algoritmo identificados para otimização, se necessário.

Fase 4: Programação e Teste 

    [ Wilker ] Algoritmo traduzido com precisão em código de programação.
    [ Wilker ] Código de programação escrito de forma clara e organizada.
    [ Atos e Wilker ] Testes rigorosos realizados em uma variedade de casos de teste.
    [ Gabriel ] Casos limite e situações especiais testados.
    [ Atos ] Erros e problemas durante o teste de programa identificados e corrigidos.

Fase 5: Documentação e Avaliação do Projeto  

    [ Gabriel ] Documentação completa, incluindo especificação do algoritmo e análise de complexidade.
    [ Gabriel ] Documentação revisada para clareza e rigor técnico.
    [ Gabriel ] Avaliação da eficácia do algoritmo em termos de tempo de execução, uso de recursos e precisão na resolução do problema.
    [ Gabriel ] Avaliação da colaboração da equipe e cumprimento dos prazos.

Fase 6: Apresentação e Conclusão do Projeto  

    [ Atos ] Apresentação do projeto preparada com informações claras e objetivas.
    [ Gabriel ] Conclusões do projeto destacando os resultados e aprendizados.
    [ Wilker ] Discussão sobre o projeto e respostas a perguntas da audiência.
