<!-- title: Parceiro - Mapa de indicações de terrenos | url: https://outline.seazone.com.br/doc/parceiro-mapa-de-indicacoes-de-terrenos-zyGM1DJINv | area: Tecnologia -->

# Parceiro - Mapa de indicações de terrenos

# Atividades limitadoras

O primeiro passo é importar os dados atuais de terrenos para a base do Sapron de tal forma que os dados mantenham-se sincronizados.

Vide [Carga do BD Terrenos para o BD Sapron](/doc/carga-do-bd-terrenos-para-o-bd-sapron-DZI5svCIMq).

# Etapas

* Criar endpoints de listagem de indicações do parceiro;
* Integrar API do mapa no repo `sapron-frontend`;
* Integrar API de terrenos para recuperar os polígonos;
* Mostrar no mapa os marcadores dos terrenos indicados + polígonos;