# Project team
- Pedro Pinho 109986
- Rafael Ferreira 107340
- Tiago Figueiredo 107263


## Passos lógicos da nossa web app:

    Entrar na main page
    Ler a informação presente, inclusive em outras linguas (Muda-se na Navbaar)
    Ver as reviews na tab reviews
    Ver quais os quartos disponiveis (selecionando uma janela temporal)
    
    Neste momento ja nao sera possivel progredir sem efetuar login
    
    Apos o login podemos continuar com a nossa jornada, selecionando os extras e procedento para o checkout
    Apos o pagamento, teremos tambem uma fatura disponivel, e podemos regressar à home page
    
    Uma vez que ja estamos logged in podemos tb ir deixar uma review
    
    Na aba do profile, podemos efetuar alterações à nossa informação, bem como adicionar uma imagem de perfil
    
    Por baixo do perfile temos acesso às nossas reservas anteriores se formos um utilizador normal
    E acesso ao admin panel se formos o admin
    
    Uma vez ja com permissoes de admin, podemos entao aceder a à informação de qualquer utilizador, quarto, reserva ou review
    
    agh4m.pythonanywhere.com
    
    A funcionalidade de reset password requere ser testada em localhost
    
    
## Especificações:
- Password reset 
    Utilizamos a funcionalidade do django que - no nosso caso - cria um ficheiro local (onde estiver o servidor) que contém o link para mudar a sua password.
    (IMPORTANTE: existe um BUG que faz com que esta funcionalidade só funcione com utilizadores novos - Não descobri o porquê. Pensei inicialmente que fosse devido a hashable password ou inactive user, mas não é o caso...) 
    Os seguintes passes são necessários para fazer uso desta funcionalidade:
	- Criar um utilizador novo
	- Fazer reset à password
	- Ir ao ficheiro encontrado em [path]/mysite/sent_emails/
	- Abrir link no ficheiro e mudar a password

- Fixtures
    Para inicialmente carregar informação para a nossa aplicação nós utilizamos fixtures que fazem uso de JSON
    
- Pagination 
    Funcionalidade django
    (IMPORTANTE: Por não fazer refresh à pagina, ao criar uma review, só na próxima refresh (ou criando uma outra review) é que a paginação leva refresh)

- Translation
    Funcionalidade django - utilizamos o i18n - que praticamente força-nos a validar as pastas localizadas no "locale" (lugar onde se encontram as traduções) 
