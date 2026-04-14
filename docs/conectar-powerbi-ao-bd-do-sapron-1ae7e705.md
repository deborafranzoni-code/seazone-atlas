<!-- title: Conectar PowerBI ao BD do Sapron | url: https://outline.seazone.com.br/doc/conectar-powerbi-ao-bd-do-sapron-kwQxiFuXNe | area: Tecnologia -->

# Conectar PowerBI ao BD do Sapron

**Conexão Power BI - Banco de Dados RDS Sapron**

Faça seu login AWS na Seazone Technology e certifique que seu IP está no **Security Group** do banco de dados que você deseja fazer a solicitação.

Nesse passo a passo, irei fazer a conexão com o Banco de Dados **sapron_production**

Para conectar um banco de dados ao Power BI é necessário seguir o passo a passo de conexão:.


1. Clique em "Obter dados"
2. Vá em "mais"
3. Procure por "Banco de dados PostgreSQL"
4. No servidor coloque o site do servidor do banco + :5432 (número da portaria).

   > *O endereço do servidor, nome do banco de dados, usuário e senha você vai encontrar no Vault.*
5. Selecione "Import"
6. Siga os demais passos indicados pelo BI normalmente.

Caso ocorra o erro: *"O certificado remoto é inválido de acordo com o procedimento de validação",* realize o seguinte passo a passo:


1. Faça download do instalador .msi apropriado na página de [\*\*versões do Npgsql](https://github.com/npgsql/Npgsql/releases).\*\*

   > *A versão utilizada neste tutorial foi [\*\*4.0.12](https://drive.google.com/file/d/1pX5jHG1dPdVI5doiWozZdXHejkmJmkvS/view?usp=sharing).*\*\*
2. Execute o instalador. Durante a instalação, há uma opção para instalar no GAC *que está desativada por padrão* - você deve selecionar para ter os arquivos instalados no GAC, como mostra a imagem a seguir.

   <https://lh3.googleusercontent.com/IfpMq2esszS3vuCyKEVevyIuHuhcAS8lgHFNDzXFz7dm3nfaqErkW01wTO86Jzh6e1_BsIwahvZacLV3AIu1qkliYgevH0VpzGlDpcWToofmjlYN6mjlGHLcBc2zB7f1_p86ouFmfbJzrM-LJChWAeeDWKo-ACkPk9ptS7tRwAgdGby4MInIm-TK-94S-A>
3. Finalize a instalação.
4. Faça download das chaves públicas para regiões do AWS RDS: [keys.](https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem)
5. Converta o pacote em um certificado do Windows no formato P7B/PKCS#7. Realizei através do [site](https://www.sslshopper.com/ssl-converter.html) .
6. No Windows, procure o utilitário "Gerenciar certificados do usuário" e abra-o.
   * Clique com o botão direito do mouse em: "Autoridades de certificação raiz confiáveis" > "Todas as tarefas" > "Importar..."
   * Selecione o arquivo `.p7b` que foi a saída da conversão das chaves AWS para o formato P7B.
   * Escolha colocar todos os certificados no armazenamento de Autoridades de Certificação Raiz Confiáveis.
   * Você provavelmente terá que confirmar para cada certificado - há um por região da AWS
   * Reinicie o computador.

Após esses passos, o certificado da AWS está ativo em seu computador. Você deve conseguir conectar ao banco de dados AWS RDS Postgres do PowerBI. Refaça o primeiro processo de conexão.

A princípio, para publicar o dashboard online não haverá problemas e você pode realizar esse procedimento normalmente.


---

Tutorial importado deste [\*\*docs](https://docs.google.com/document/d/13eKpDbENDb2Y8WgzLXYj7CDGVjc9R48jAM_dZTU1G9U/edit)\*\* criado pela **@Bárbara Farah de Almeida**