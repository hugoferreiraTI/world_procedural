# Segunda execução — interrupção na hora 650

A segunda execução, seed **Vaelmir-521**, terminou na verificação de integridade
da hora **650**. O erro foi `Decisão letal inválida: 890`, relativo a **Ruan Stone**.
O núcleo executado foi `aa03516980df5b6d1ddfd4fc111df943156fe85a59451942bba81afc49355b07`.
Não houve troca de seed ou alteração de parâmetros durante a execução.

Desta vez, as métricas e o material narrativo da hora 650 foram preservados em
`campanha_1000h_reinicio/evidencia_parcial_falha.json`. Não houve save final.
A falha de memória da hora 582 não se repetiu; os 37 alertas de referências
históricas futuras também não reapareceram.

## Evidência natural disponível

| Etapa até 650h | Ocorrências |
| --- | --- |
| Candidatos avaliados | 1.475 |
| Candidatos rejeitados | 1.314 |
| Considerações avançadas | 161 |
| Decisões letais | 156 |
| Ataques letais | 789 |
| Oportunidades terminais | 47 |
| Poupar | 21 |
| Finalizar | 1 |
| Retirar-se | 4 |
| Capturar | 3 |
| Morte intencional em combate | 1 |
| Finalização deliberada | 1 |
| Avaliações pós-morte | 2 |
| Aumentos de DeathAffinity | 0 |
| Decisões abandonadas | 38 |
| Decisões resolvidas | 3 |

São contagens de episódios/eventos, não pessoas distintas. A composição
religiosa preservada tinha **299 Actors de Aurion, 92 de Neruma e 49 de Elar**.

O caçador **Cael Corven**, de Vallen, finalizou **Mira Stone** na hora **431**.
Sua intenção inicial de reação a ameaça havia se tornado retributiva por danos
conhecidos repetidos. Na escolha final, finalizar marcou **77,68**, retirar-se
**56,50** e poupar **38,20**. Cael tinha compaixão **8**, vingatividade **95**
e sadismo **3**. A morte foi registrada como `deliberate_finish` e teve
avaliação pós-morte: alívio **55**, culpa **20,34**, orgulho **17,65**, prazer
e fascinação **0**. DeathAffinity permaneceu zero. A decisão foi resolvida
quando a morte ficou conhecida. Eventos **469810, 469812, 469813 e 469815**.

O lenhador **Cael Vale**, de Eliven, poupou **Lyra Kars** na hora **343**.
Apesar do sadismo **73**, a decisão era protetiva: a incapacidade da vítima
removeu a ameaça imediata. Poupar marcou **78,40**, retirar-se **75** e finalizar
**−6,68**. Esse episódio demonstra que sadismo não obriga homicídio.
Evento **369269**.

## Defeito de consistência e correção posterior

A decisão de Ruan Stone foi criada na hora **642**, contra o NPC **3728**,
em modo retributivo, por ferimento atribuído não resolvido. O registro de
criação preserva intensidade **45,13**, WorldPressure **45**, ruminação
**65,53** e fatos **712913, 714248 e 715498**. A mensagem do validador
agrupa várias condições; o estado completo de Ruan na hora 650 não foi
exportado. Portanto, não se identifica aqui qual ID estava ausente nesse
instante somente a partir da mensagem genérica.

Foram reproduzidos **dois caminhos reais** que deixam uma decisão ativa
referenciando uma memória ausente:

1. Uma reação aprende muitos fatos antes de o sistema letal proteger o novo
   fato como reforço da decisão. O fato expulso continua sendo entregue pela
   referência local, mas a decisão acaba guardando seu ID sem memória associada.
2. Os próprios eventos de deliberação podem expulsar uma causa antiga de uma
   memória cheia antes de a nova decisão passar a protegê-la. A sondagem
   controlada criou uma decisão com o fato **265** ausente após a deliberação.

A correção posterior protege temporariamente os fatos em processamento e
as causas já conhecidas durante a criação de uma decisão. Depois disso,
valem as proteções e limites normais. Não recupera informação remota, não
aumenta a memória, não altera escores e não muda dano. Os seis testes focados,
incluindo os dois cenários de memória, e quatro regressões passaram.

Essa correção **não rodou nesta segunda execução**. É uma correção testada
em cenários controlados; a confirmação natural depende de uma execução posterior.
O erro estrutural não invalida retroativamente os dois episódios de morte
registrados, mas impede declarar completa a validação de 1.000 horas.
