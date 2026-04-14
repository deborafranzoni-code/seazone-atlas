<!-- title: OMIE | url: https://outline.seazone.com.br/doc/omie-iJOfQgi7Ts | area: Administrativo Financeiro -->

# OMIE

# **==__________________Sobre_______________________==**

## *==———Descrição———————————-==*

* Código para requisição dos dados do OMIE

## *==———Planilha Base———————————-==*

* [Full OMIE API](https://docs.google.com/spreadsheets/d/1JllOxKO7m-sfMRkvbg1op5xhQlBAZaYMPDDzIyOFPCQ/edit?gid=446169915#gid=446169915)

## *==———Documentação———————————-==*

* [Link da documentação](https://developer.omie.com.br/service-list/)
* Não há observação

## *==———Sugestão———————————-==*

* Não há sugestões

# **==__________________Scripts______________________==**

## *==———==*==Token==

### `OmieAPI`

* **Objetivo**: gerar token do OMIE

```jsx
async function OmieAPI(complemento_url,call,parametros){

  var app_Key = "4352638314024" // Seazone
  var app_Secreat = "2631d15e0214380cb4674da01cad6885" // Seazone

  var url = 'https://app.omie.com.br/api/v1/' + complemento_url;
  var payload = {
    "call": call,
    "app_key": app_Key,
    "app_secret": app_Secreat,
    "param": parametros
  };
  
  var options = {
    'method': 'post',
    'muteHttpExceptions': true,
    'headers': {
      'Content-type': 'application/json'
    },
    'payload': JSON.stringify(payload)
  };
  
  var response = UrlFetchApp.fetch(url, options);
  var data = JSON.parse(response.getContentText())
  
  return data
}
```

## **==———Categoria==**

### `listarCategoria`

* **Objetivo**: listar todas as categorias

```jsx
async function listarCategoria(){
  var page = 1
  var lastPage = 1
  
  var complemento_url = "geral/categorias/"
  var call =  "ListarCategorias"

  var arrayPrint=[]

  const processData = async () => {
    while(page <= lastPage){
      
      var parametros = [
        {
          "pagina": page,
          "registros_por_pagina": 999,
        }
      ]
      
      try{  
        var allData = await OmieAPI(complemento_url,call,parametros)
        lastPage = allData.total_de_paginas
        var lista = allData.categoria_cadastro
        
        if(lista){
          lista.forEach(item => {
            if (item.conta_inativa == "N" && item.conta_despesa == "S" ) {
              arrayPrint.push([
                item.codigo,              
                item.descricao,
              ])
            }
          })
        }
      }catch(error){
        console.error("Error processing data for page", page, error);        
      }
      page++
    }
  }

  
  await processData()

  return arrayPrint
}
```

### `incluirCategoria`

* **Objetivo**: Incluir categoria

```jsx
async function incluirCategoria() {
  const processData = async () => {
    var complemento_url = "geral/categorias/"
    var call =  "IncluirCategoria"
    
    sAtualCatFull.forEach(row=> {

      var parametros = [{
        'categoria_superior':row[saCatFullCodSup-1],
        'descricao':row[saCatFullDesc-1],
      }]

      var result = await OmieAPI(complemento_url,call,parametros)

      console.log(result.faultstring)
      var resposta = result.faultstring == undefined? "Dado Incluído!" : result.faultstring
       
    }
  })
  await processData()
  
}
```

### `alterarCategoria`

* **Objetivo**: Alterar categoria

```jsx
async function alterarCategoria() {
  const processData = async () => {
    var complemento_url = "geral/categorias/"
    var call =  "AlterarCategoria"
    
    sAtualCatFull.forEach(row=> {

      var parametros = [{
        'categoria_superior':row[saCatFullCodSup-1],
        'descricao':row[saCatFullDesc-1],
      }]

      var result = await OmieAPI(complemento_url,call,parametros)

      console.log(result.faultstring)
      var resposta = result.faultstring == undefined? "Dado Alterado!" : result.faultstring
       
    }
  })
  await processData()
  
}
```


## **==———Conta Corrente==**

### `listarCategoria`

* **Objetivo**: listar todas as categorias

```jsx
async function listarContaCorrente(){
  var page = 1
  var lastPage = 1
  
  var complemento_url = "geral/contacorrente/"
  var call =  "ListarContasCorrentes"

  var arrayPrint=[]

  const processData = async () => {
    while(page <= lastPage){
      
      var parametros = [
        {
          "pagina": page,
          "registros_por_pagina": 999,
        }
      ]
      
      try{  
        var allData = await OmieAPI(complemento_url,call,parametros)
        lastPage = allData.total_de_paginas
        var lista = allData.ListarContasCorrentes

        if(lista){
          lista.forEach(item => {
            if (item.bloqueado == "N" && item.inativo == "N") {
              arrayPrint.push([
                item.nCodCC,
                item.descricao,                               
              ])
            }
          })
        }
      

      }catch(error){
        console.error("Error processing data for page", page, error);        
      }
      page++
    }
  }

  
  await processData()

  return arrayPrint
}
```

## **==———Departamento==**

### `ListarDepartamentos`

* **Objetivo**: listar todos os departamentos

```jsx
async function listarDepartamento(){
  var page = 1
  var lastPage = 1
  
  var complemento_url = "geral/departamentos/"
  var call =  "ListarDepartamentos"

  var arrayPrint=[]

  const processData = async () => {
    while(page <= lastPage){
      
      var parametros = [
        {
          "pagina": page,
          "registros_por_pagina": 999,
        }
      ]
      
      try{  
        var allData = await OmieAPI(complemento_url,call,parametros)
        lastPage = allData.total_de_paginas
        var lista = allData.departamentos

        if(lista){
          lista.forEach(item => {
            if (item.inativo == "N") {
              arrayPrint.push([
                item.codigo,
                item.descricao,
              ])
            }
          })
        }

      }catch(error){
        console.error("Error processing data for page", page, error);        
      }
      page++
    }
  }

  await processData()

  return arrayPrint
}
```

* Incluir

  ```jsx
  async function incluirDepartamento() {
    var sAtualDep = ss.getSheetByName(sAtualDepName)
    var sAtualDepFull = sAtualDep.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "geral/departamentos/"
      var call =  "IncluirDepartamento"
      
      for(var i=1;i<sAtualDepFull.length;i++){
        if(sAtualDepFull[i][saDepFullCheck-1] == true){
          var parametros = [{
            'codigo': sAtualDepFull[i][saDepFullCod-1],
            'descricao': sAtualDepFull[i][saDepFullDesc-1] == "" ? "":    sAtualDepFull[i][saDepFullDesc-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.faultstring)
          var resposta = result.faultstring == undefined? "Dado Incluído!" : result.faultstring
  
          sAtualDep.getRange(i+1,saDepFullStatus).setValue(resposta)
          sAtualDep.getRange(i+1,saDepFullCheck).setValue(false)
          sAtualDep.getRange(i+1,saDepFullEstr).setValue(result.estrutura)
          sAtualDep.getRange(i+1,saDepFullCod).setValue(result.codigo)
          
        }
      }
    }
    await processData()
    
  }
  ```
* Alterar

  ```jsx
  async function alterarDepartamento() {
    var sAtualDep = ss.getSheetByName(sAtualDepName)
    var sAtualDepFull = sAtualDep.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "geral/departamentos/"
      var call =  "AlterarDepartamento"
      
      for(var i=1;i<sAtualDepFull.length;i++){
        if(sAtualDepFull[i][saDepFullCheck-1] == true){
          var parametros = [{
            'codigo': sAtualDepFull[i][saDepFullCod-1],
            'descricao': sAtualDepFull[i][saDepFullDesc-1] == "" ? "":    sAtualDepFull[i][saDepFullDesc-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.faultstring)
          var resposta = result.faultstring == undefined? "Dado Alterado!" : result.faultstring
  
          sAtualDep.getRange(i+1,saDepFullStatus).setValue(resposta)
          sAtualDep.getRange(i+1,saDepFullCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
  }
  ```
* Excluir

  ```jsx
  async function excluirDepartamento() {
    var sAtualDep = ss.getSheetByName(sAtualDepName)
    var sAtualDepFull = sAtualDep.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "geral/departamentos/"
      var call =  "ExcluirDepartamento"
      
      for(var i=1;i<sAtualDepFull.length;i++){
        if(sAtualDepFull[i][saDepFullCheck-1] == true){
          var parametros = [{
            'codigo': sAtualDepFull[i][saDepFullCod-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.faultstring)
          var resposta = result.faultstring == undefined? "Dado Excluído!" : result.faultstring
  
          sAtualDep.getRange(i+1,saDepFullStatus).setValue(resposta)
          sAtualDep.getRange(i+1,saDepFullCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
  }
  ```

## **==———Projeto==**

### `ListarProjetos`

* **Objetivo**: listar todos os projetos

```jsx
async function listarProjeto(){
  var page = 1
  var lastPage = 1
  
  var complemento_url = "geral/projetos/"
  var call =  "ListarProjetos"

  var arrayPrint=[]

  const processData = async () => {
    while(page <= lastPage){
      
      var parametros = [
        {
          "pagina": page,
          "registros_por_pagina": 999,
          "apenas_importado_api": "N",
        }
      ]
      
      try{  
        var allData = await OmieAPI(complemento_url,call,parametros)
        lastPage = allData.total_de_paginas
        var lista = allData.cadastro

        if(lista){
          lista.forEach(item => {
            if (item.inativo == "N") {
              arrayPrint.push([
                item.codigo,
                item.nome,
              ])
            }
          })
        }

      }catch(error){
        console.error("Error processing data for page", page, error);        
      }
      page++
    }
  }

  
  await processData()

  return arrayPrint
}
```

* Incluir

  ```jsx
  async function incluirProjeto() {
    var sAtualProj = ss.getSheetByName(sAtualProjName)
    var sAtualProjFull = sAtualProj.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "/geral/projetos/"
      var call =  "IncluirProjeto"
      
      for(var i=1;i<sAtualProjFull.length;i++){
        if(sAtualProjFull[i][saCatFullCheck-1] == true){
          var parametros = [{
            'codInt':sAtualProjFull[i][saProjFullCodInt-1],
            'nome':sAtualProjFull[i][saProjFullNome-1],
            'inativo':sAtualProjFull[i][saProjFullInat-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.faultstring)
          var resposta = result.faultstring == undefined? "Dado Incluído!" : result.faultstring
  
          sAtualProj.getRange(i+1,saCatFullStatus).setValue(resposta)
          sAtualProj.getRange(i+1,saCatFullCheck).setValue(false)
          sAtualProj.getRange(i+1,saProjFullCod).setValue(result.codigo)
          sAtualProj.getRange(i+1,saProjFullCodInt).setValue(result.codInt)
        }
      }
    }
    await processData()
    
  }
  ```
* Alterar

  ```jsx
  async function alterarProjeto() {
    var sAtualProj = ss.getSheetByName(sAtualProjName)
    var sAtualProjFull = sAtualProj.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "/geral/projetos/"
      var call =  "AlterarProjeto"
      
      for(var i=1;i<sAtualProjFull.length;i++){
        if(sAtualProjFull[i][saCatFullCheck-1] == true){
          var parametros = [{
            'codigo':sAtualProjFull[i][saProjFullCod-1],
            'nome':sAtualProjFull[i][saProjFullNome-1],
            'inativo':sAtualProjFull[i][saProjFullInat-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.faultstring)
          var resposta = result.faultstring == undefined? "Dado Alterado!" : result.faultstring
  
          sAtualProj.getRange(i+1,saCatFullStatus).setValue(resposta)
          sAtualProj.getRange(i+1,saCatFullCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
  }
  
  ```
* Excluir

  ```jsx
  async function excluirProjeto() {
    var sAtualProj = ss.getSheetByName(sAtualProjName)
    var sAtualProjFull = sAtualProj.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "/geral/projetos/"
      var call =  "ExcluirProjeto"
      
      for(var i=1;i<sAtualProjFull.length;i++){
        if(sAtualProjFull[i][saCatFullCheck-1] == true){
          var parametros = [{
            'codigo':sAtualProjFull[i][saProjFullCod-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.faultstring)
          var resposta = result.faultstring == undefined? "Dado Excluído!" : result.faultstring
  
          sAtualProj.getRange(i+1,saCatFullStatus).setValue(resposta)
          sAtualProj.getRange(i+1,saCatFullCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
  }
  ```

## **==———Clientes==**

### `ListarClientes`

* **Objetivo**: listar todos os clientes

```jsx
async function extratoFornClient(){
  var page = 1
  var lastPage = 1
  
  var complemento_url = "/geral/clientes/"
  var call =  "ListarClientes"

  var arrayPrint=[]

  const processData = async () => {
    while(page <= lastPage){
      
      var parametros = [
        {
          "pagina": page,
          "registros_por_pagina": 999,
          "apenas_importado_api": "N"
        }
      ]
      
      try{  
        var allData = await OmieAPI(complemento_url,call,parametros)
        lastPage = allData.total_de_paginas
        var lista = allData.clientes_cadastro

        if(lista){
          lista.forEach(item => {
              arrayPrint.push([
                item.codigo_cliente_omie,  
                item.razao_social.toString().slice(0, 60), 
                "",
              ])
          })
        }

      }catch(error){
        console.error('Error processing data for page', page, error);        
      }
      page++
    }
  }

  
  await processData()

  return arrayPrint
}
```

* Incluir

  ```jsx
  async function incluirFC() {
    var sAtualClForn = ss.getSheetByName(sAtualClFornName)
    var sAtualClFornFull = sAtualClForn.getDataRange().getValues()
  
    //var mapFPName = sAtualSheetDeParaNameFull.map(row=> row[asDPFName-1]).flat()
  
    const processData = async () => {
      var complemento_url = "/geral/clientes/"
      var call =  "IncluirCliente"
      
      for(var i=1;i<sAtualClFornFull.length;i++){
        if(sAtualClFornFull[i][saCFFullCheck-1] == true)
            console.log(i+1)
  
            var parametros = [{
              'codigo_cliente_integracao': sAtualClFornFull[i][saCFFullCodInteg-1]?sAtualClFornFull[i][saCFFullCodInteg-1]: Array.from({length: 12}, () => Math.floor(Math.random() * 10)).join(""),
              'razao_social': sAtualClFornFull[i][saCFFullRaz-1] == "" ? "":    sAtualClFornFull[i][saCFFullRaz-1].toString().slice(0, 60),
              'nome_fantasia': sAtualClFornFull[i][saCFFullNoFan-1] == "" ? "":  sAtualClFornFull[i][saCFFullNoFan-1].toString().slice(0, 60),
              'cnpj_cpf': sAtualClFornFull[i][saCFFullCPFCNPJ-1] == "" ? "": sAtualClFornFull[i][saCFFullCPFCNPJ-1],
              'email': sAtualClFornFull[i][saCFFullEmail-1] == "" ? "":  sAtualClFornFull[i][saCFFullEmail-1],
            }]
  
            var result = await OmieAPI(complemento_url,call,parametros)
  
            console.log(result.faultstring)
            var resposta = result.faultstring == undefined? "Imputado!" : result.faultstring
  
            sAtualClForn.getRange(i+1,saCFFullStatus).setValue(resposta)
            sAtualClForn.getRange(i+1,saCFFullCheck).setValue(false)
            sAtualClForn.getRange(i+1,saCFFullCodOmie).setValue(result.codigo_cliente_omie)
            sAtualClForn.getRange(i+1,saCFFullCodInteg).setValue(result.codigo_cliente_integracao)        
          
        }
      }
    }
    await processData()
  }
  ```
* Alterar

  ```jsx
  async function alterarFC() {
  
    const processData = async () => {
      var sAtualClForn = ss.getSheetByName(sAtualClFornName)
      var sAtualClFornFull = sAtualClForn.getDataRange().getValues()
  
      var complemento_url = "/geral/clientes/"
      var call =  "AlterarCliente"
      
      for(var i=1;i<sAtualClFornFull.length;i++){
        if(sAtualClFornFull[i][saCFFullCheck-1] == true){
          console.log(i+1)
  
          var parametros = [{
            'codigo_cliente_omie':sAtualClFornFull[i][saCFFullCodOmie-1],
            'codigo_cliente_integracao': sAtualClFornFull[i][saCFFullCodInteg-1],
            'razao_social': sAtualClFornFull[i][saCFFullRaz-1] == "" ? "":    sAtualClFornFull[i][saCFFullRaz-1].toString().slice(0, 60),
            'nome_fantasia': sAtualClFornFull[i][saCFFullNoFan-1] == "" ? "":  sAtualClFornFull[i][saCFFullNoFan-1].toString().slice(0, 60),
            'cnpj_cpf': sAtualClFornFull[i][saCFFullCPFCNPJ-1] == "" ? "": sAtualClFornFull[i][saCFFullCPFCNPJ-1],
            'email': sAtualClFornFull[i][saCFFullEmail-1] == "" ? "":  sAtualClFornFull[i][saCFFullEmail-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.faultstring)
          var resposta = result.faultstring == undefined? "Dado Alterado!" : result.faultstring
  
          sAtualClForn.getRange(i+1,saCFFullStatus).setValue(resposta)
          sAtualClForn.getRange(i+1,saCFFullCheck).setValue(false)
          
        }
      }
    }
    await processData()
  }
  ```
* Excluir

  ```jsx
  async function excluirFC() {
    var sAtualClForn = ss.getSheetByName(sAtualClFornName)
    var sAtualClFornFull = sAtualClForn.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "/geral/clientes/"
      var call =  "ExcluirCliente"
      
      for(var i=1;i<sAtualClFornFull.length;i++){
        if(sAtualClFornFull[i][saCFFullCheck-1] == true){
          console.log(i+1)
  
          var parametros = [{
            'codigo_cliente_omie': sAtualClFornFull[i][saCFFullCodOmie-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.faultstring)
          var resposta = result.faultstring == undefined? "Dado Excluído!" : result.faultstring
  
          sAtualClForn.getRange(i+1,saCFFullStatus).setValue(resposta)
          sAtualClForn.getRange(i+1,saCFFullCheck).setValue(false)
          
        }
      }
    }
    await processData()
  }
  ```

## **==———Movimento==**

### `ListarMovimentos`

* **Objetivo**: listar todos os movimentos

```jsx
async function listarMovimento(){
  var sAtualMovimento = ss.getSheetByName(sAtualMovimentoName)

  var sAtualDash = ss.getSheetByName(sAtualDashName)
  var dashDataInicio = new Date(sAtualDash.getRange(sAtualDashDataInicio).getValues())
  var dashDataFim = new Date(sAtualDash.getRange(sAtualDashDataFim).getValues())

  var page = 1
  var lastPage = 1
  
  var complemento_url = "financas/mf/"
  var call =  "ListarMovimentos"

  var arrayPrint=[]

  const processData = async () => {
    while(page <= lastPage){
      
      var parametros = [
        {
          "nPagina": page,
          "nRegPorPagina": 999,
        }
      ]
      
      var allData = await OmieAPI(complemento_url,call,parametros)
      lastPage = allData.nTotPaginas
      var lista = allData.movimentos

      console.log(lista.length)

      if (lista) {
        lista.forEach(item => {

        try{ 
          //console.log(item.detalhes.dDtPagamento)
          var dataO = item.detalhes.dDtVenc? item.detalhes.dDtVenc : item.detalhes.dDtPagamento 
          var dataOmie = dataO.toString().split("/")
          var dataLista = new Date(dataOmie[2],dataOmie[1]-1,dataOmie[0])

          if(dataLista >= dashDataInicio && dataLista <= dashDataFim){
          
            arrayPrint.push([
              
              item.detalhes.nCodMovCC,
              item.detalhes.nCodTitulo,
              item.detalhes.nCodBaixa,
              
              item.detalhes.nCodCC,
              item.detalhes.nCodCliente,
              item.detalhes.cCodCateg,
              item.resumo.nValPago,
              item.detalhes.cNatureza,
              
              item.detalhes.dDtVenc,
              item.detalhes.dDtPagamento,
              
  
            ])
          }
          
        }catch(error){
          console.error("Error processing data for page", page,item, error);        
        }
        })
      }

      
      page++
    }
  }

  
  await processData()

  sAtualMovimento.getRange(linhaInicio,sAtualMovimentoCheck,sAtualMovimento.getMaxRows()+1-linhaInicio,sAtualMovimento.getLastColumn()).clearContent().setBackground(null)
  sAtualMovimento.getRange(linhaInicio,sAtualMovimentoCodID,arrayPrint.length,arrayPrint[0].length).setValues(arrayPrint)

  return arrayPrint
}
```

## **==———Contas a Pagar==**

### `ListarContasPagar`

* **Objetivo**: listar todas as contas a pagar

```jsx
async function listarContPgto(){
  var sAtualConPgto = ss.getSheetByName(sAtualConPgtoName)
  var sAtualDash = ss.getSheetByName(sAtualDashName)
  var dashDataInicio = new Date(sAtualDash.getRange(sAtualDashDataInicio).getValues())
  var dashDataFim = new Date(sAtualDash.getRange(sAtualDashDataFim).getValues())

  var sAtualUsuario = ss.getSheetByName(sAtualUsuarioName)
  var sAtualUsuarioFull = sAtualUsuario.getDataRange().getValues()

  var sAtualClForn = ss.getSheetByName(sAtualClFornName)
  var sAtualClFornFull = sAtualClForn.getDataRange().getValues()

  var sAtualDep = ss.getSheetByName(sAtualDepName)
  var sAtualDepFull = sAtualDep.getDataRange().getValues()

  var sAtualCat = ss.getSheetByName(sAtualCatName)
  var sAtualCatFull = sAtualCat.getDataRange().getValues().filter(rows => rows[saCatFullCoDesp-1] == "S" )

  var sAtualProj = ss.getSheetByName(sAtualProjName)
  var sAtualProjFull = sAtualProj.getDataRange().getValues()

  var sAtualCC = ss.getSheetByName(sAtualCCName)
  var sAtualCCFull = sAtualCC.getDataRange().getValues()

  var sAtualMovimento = ss.getSheetByName(sAtualMovimentoName)
  var sAtualMovimentoFull = sAtualMovimento.getDataRange().getValues().filter(rows=> rows[sAtualMovimentoCodBaixa-1] !== "" && rows[sAtualMovimentoNatureza-1] =="P")

  
  var clienteMap = sAtualClFornFull.map(row=> parseInt(row[saCFFullCodOmie-1])).flat()
  var departamentoMap = sAtualDepFull.map(row=> parseInt(row[saDepFullCod-1])).flat()
  var categoriaMap = sAtualCatFull.map(row=> row[saCatFullCod-1]).flat()
  var projetoMap = sAtualProjFull.map(row=> parseInt(row[saProjFullCod-1])).flat()
  var contaMap = sAtualCCFull.map(row=> parseInt(row[saCCFullNCodCC-1])).flat()
  var usuarioMap = sAtualUsuarioFull.map(row=> parseInt(row[sAtualCodUsuario-1])).flat()
  var movimentoMap = sAtualMovimentoFull.map(row=> parseInt(row[sAtualMovimentoCodTitulo-1])).flat()

  var page = 1
  var lastPage = 1
  
  var complemento_url = "financas/contapagar/"
  var call =  "ListarContasPagar"

  var arrayPrint=[]

  const processData = async () => {
    while(page <= lastPage){
      
      var parametros = [
        {
          "pagina": page,
          "registros_por_pagina": 999,
          "exibir_obs":"S"
        }
      ]
      
      
      var allData = await OmieAPI(complemento_url,call,parametros)
      lastPage = allData.total_de_paginas
      var lista = allData.conta_pagar_cadastro

      console.log(allData.pagina)

      if (lista) {
        lista.forEach(item => {
          try{
            var dataOmie = item.data_vencimento.toString().split("/")
            var dataLista = new Date(dataOmie[2],dataOmie[1]-1,dataOmie[0])

            if(dataLista >= dashDataInicio && dataLista <= dashDataFim){         
              
              var departamentoIndex = item.distribuicao? item.distribuicao[0].cCodDep? departamentoMap.indexOf(parseInt(item.distribuicao[0].cCodDep)): -1:-1
              
              var clienteIndex = item.codigo_cliente_fornecedor? clienteMap.indexOf(parseInt(item.codigo_cliente_fornecedor)):-1
              var categoriaIndex = item.codigo_categoria? categoriaMap.indexOf(item.codigo_categoria):-1
              var projetoIndex = item.codigo_projeto? projetoMap.indexOf(parseInt(item.codigo_projeto)):-1
              var contaIndex = item.id_conta_corrente? contaMap.indexOf(parseInt(item.id_conta_corrente)):-1
              var usuarioInclusaoIndex = item.info.uInc? usuarioMap.indexOf(parseInt(item.info.uInc)):-1
              var usuarioAlteracaoIndex = item.info.uAlt? usuarioMap.indexOf(parseInt(item.info.uAlt)):-1
              var movimentoIndex = item.codigo_lancamento_omie? movimentoMap.indexOf(parseInt(item.codigo_lancamento_omie)):-1

              var departamentoDescricao = departamentoIndex !== -1 ? sAtualDepFull[departamentoIndex][saDepFullDesc-1] : item.distribuicao[0].cCodDep
              var categoriaDescricao = categoriaIndex !== -1 ? sAtualCatFull[categoriaIndex][saCatFullDesc-1] : item.codigo_categoria
              var projetoDescricao = projetoIndex !== -1 ? sAtualProjFull[projetoIndex][saProjFullNome-1] : item.codigo_projeto
              var contaDescricao = contaIndex !== -1 ? sAtualCCFull[contaIndex][saCCFullDescr-1] : item.id_conta_corrente
              var usuarioInclusaoDescricao = usuarioInclusaoIndex !== -1 ? sAtualUsuarioFull[usuarioInclusaoIndex][sAtualDescUsuario-1] : item.info.uInc
              var usuarioAlteracaoDescricao = usuarioAlteracaoIndex !== -1 ? sAtualUsuarioFull[usuarioAlteracaoIndex][sAtualDescUsuario-1] : item.info.uAlt
              var clienteDescricao = clienteIndex !== -1 ? sAtualClFornFull[clienteIndex][saCFFullRaz-1] : item.codigo_cliente_fornecedor
              var movimentoBaixa = movimentoIndex !== -1 ? sAtualMovimentoFull[movimentoIndex][sAtualMovimentoCodBaixa-1] : ""
              var movimentoData = movimentoIndex !== -1 ? sAtualMovimentoFull[movimentoIndex][sAtualMovimentoData-1] : ""
              var movimentoValor = movimentoIndex !== -1 ? sAtualMovimentoFull[movimentoIndex][sAtualMovimentoValor-1] : ""
              var movimentoID = movimentoIndex !== -1 ? sAtualMovimentoFull[movimentoIndex][sAtualMovimentoCodID-1] : ""
              

              arrayPrint.push([
                item.codigo_lancamento_omie,
                item.codigo_lancamento_integracao,

                contaDescricao,
                departamentoDescricao,
                categoriaDescricao,
                projetoDescricao,
                clienteDescricao,
                
                item.data_vencimento,
                item.numero_parcela,
                item.valor_documento,
                item.observacao,

                movimentoID,
                movimentoBaixa,
                movimentoData,
                movimentoValor,

                usuarioInclusaoDescricao,
                usuarioAlteracaoDescricao,
                item.info.dInc,
                item.info.dAlt,

              ])
            }
          }catch(error){
            console.error("Error processing data for page", page, error);        
          }
        })
      }

      
      page++
    }
  }

  
  await processData()

  sAtualConPgto.getRange(linhaInicioCPG,sAtualConPgtocCheck,sAtualConPgto.getMaxRows()+1-linhaInicioCPG,sAtualConPgto.getLastColumn()).clearContent().setBackground(null)
  sAtualConPgto.getRange(linhaInicioCPG,sAtualConPgtocCodOmie,arrayPrint.length,arrayPrint[0].length).setValues(arrayPrint)

}
```

* Incluir

  ```jsx
  async function incluirCPG() {
  
    var sAtualConPgto = ss.getSheetByName(sAtualConPgtoName)
    var sAtualConPgtoFull = sAtualConPgto.getDataRange().getValues()
  
    var sAtualClForn = ss.getSheetByName(sAtualClFornName)
    var sAtualClFornFull = sAtualClForn.getDataRange().getValues()
  
    var sAtualDep = ss.getSheetByName(sAtualDepName)
    var sAtualDepFull = sAtualDep.getDataRange().getValues().filter(rows => rows[saDepFullInativo-1] == "N")
  
    var sAtualCat = ss.getSheetByName(sAtualCatName)
    var sAtualCatFull = sAtualCat.getDataRange().getValues().filter(rows => rows[saCatFullCoDesp-1] == "S" && rows[saCatFullInativo-1] == "N")
  
    var sAtualProj = ss.getSheetByName(sAtualProjName)
    var sAtualProjFull = sAtualProj.getDataRange().getValues().filter(rows => rows[saProjFullInat-1] == "N")
  
    var sAtualCC = ss.getSheetByName(sAtualCCName)
    var sAtualCCFull = sAtualCC.getDataRange().getValues().filter(rows => rows[saCCFullInat-1] == "N")
  
    var clienteMap = sAtualClFornFull.map(row=> row[saCFFullRaz-1]).flat()
    var departamentoMap = sAtualDepFull.map(row=> row[saDepFullDesc-1]).flat()
    var categoriaMap = sAtualCatFull.map(row=> row[saCatFullDesc-1]).flat()
    var projetoMap = sAtualProjFull.map(row=> row[saProjFullNome-1]).flat()
    var contaMap = sAtualCCFull.map(row=> row[saCCFullDescr-1]).flat()
    
  
    const processData = async () => {
      var complemento_url = "financas/contapagar/"
      var call =  "IncluirContaPagar"
      
      for(var i=1;i<sAtualConPgtoFull.length;i++){
        if(sAtualConPgtoFull[i][sAtualConPgtocCheck-1] == true){
        console.log(i+1)
          var clienteIndex = clienteMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocCliente-1])
          var categoriaIndex = categoriaMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocCategoria-1])
          var projetoIndex =  projetoMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocProjeto-1])
          var contaIndex = contaMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocCC-1])
          var departamentoIndex = departamentoMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocDepart-1])
  
          var departamentoDescricao =  sAtualDepFull[departamentoIndex][saDepFullCod-1]
          var categoriaDescricao =  sAtualCatFull[categoriaIndex][saCatFullCod-1]
          var projetoDescricao = sAtualProjFull[projetoIndex][saProjFullCod-1]
          var contaDescricao = sAtualCCFull[contaIndex][saCCFullNCodCC-1]
          var clienteDescricao = sAtualClFornFull[clienteIndex][saCFFullCodOmie-1]
  
          var parametros = [{
            'data_entrada': new Date().toLocaleDateString("pt-br"),
  
            'codigo_lancamento_integracao': sAtualConPgtoFull[i][sAtualConPgtocCodInteg-1],
            'codigo_categoria': categoriaDescricao,
            'codigo_cliente_fornecedor': clienteDescricao,
            'codigo_projeto': projetoDescricao,
            'data_vencimento': new Date(sAtualConPgtoFull[i][sAtualConPgtocDVencimento-1]).toLocaleDateString("pt-br"),
            'distribuicao': [{ 
              "cCodDep": departamentoDescricao,
              "nPerDep": 100
            }],
            'id_conta_corrente': contaDescricao,
            'numero_parcela': sAtualConPgtoFull[i][sAtualConPgtocParcela-1].toString(),
            'valor_documento': sAtualConPgtoFull[i][sAtualConPgtocValor-1],
            'observacao': sAtualConPgtoFull[i][sAtualConPgtocObserv-1].toString()
  
          }]
  
          console.log(parametros)
          console.log(departamentoDescricao)
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.distribuicao)
          console.log(result)
          var resposta = result.faultstring == undefined? "Dado Incluído!" : result.faultstring
  
          sAtualConPgto.getRange(i+1,sAtualConPgtocStatus).setValue(resposta)
          sAtualConPgto.getRange(i+1,sAtualConPgtocCheck).setValue(false)
          sAtualConPgto.getRange(i+1,sAtualConPgtocCodOmie).setValue(result.codigo_lancamento_omie)
          
        }
      }
    }
    await processData()
    
    //Browser.msgBox("Itens Imputados:\n" + arrayPrint)
  }
  
  ```
* Alterar

  ```jsx
  async function alterarCPG() {
    var sAtualConPgto = ss.getSheetByName(sAtualConPgtoName)
    var sAtualConPgtoFull = sAtualConPgto.getDataRange().getValues()
  
    var sAtualClForn = ss.getSheetByName(sAtualClFornName)
    var sAtualClFornFull = sAtualClForn.getDataRange().getValues()
  
    var sAtualDep = ss.getSheetByName(sAtualDepName)
    var sAtualDepFull = sAtualDep.getDataRange().getValues().filter(rows => rows[saDepFullInativo-1] == "N")
  
    var sAtualCat = ss.getSheetByName(sAtualCatName)
    var sAtualCatFull = sAtualCat.getDataRange().getValues().filter(rows => rows[saCatFullCoDesp-1] == "S" && rows[saCatFullInativo-1] == "N")
  
    var sAtualProj = ss.getSheetByName(sAtualProjName)
    var sAtualProjFull = sAtualProj.getDataRange().getValues().filter(rows => rows[saProjFullInat-1] == "N")
  
    var sAtualCC = ss.getSheetByName(sAtualCCName)
    var sAtualCCFull = sAtualCC.getDataRange().getValues().filter(rows => rows[saCCFullInat-1] == "N")
  
    var clienteMap = sAtualClFornFull.map(row=> row[saCFFullRaz-1]).flat()
    var departamentoMap = sAtualDepFull.map(row=> row[saDepFullDesc-1]).flat()
    var categoriaMap = sAtualCatFull.map(row=> row[saCatFullDesc-1]).flat()
    var projetoMap = sAtualProjFull.map(row=> row[saProjFullNome-1]).flat()
    var contaMap = sAtualCCFull.map(row=> row[saCCFullDescr-1]).flat()
  
    const processData = async () => {
      var complemento_url = "financas/contapagar/"
      var call =  "AlterarContaPagar"
      
      for(var i=1;i<sAtualConPgtoFull.length;i++){
        if(sAtualConPgtoFull[i][sAtualConPgtocCheck-1] == true){
          var clienteIndex = clienteMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocCliente-1])
          var categoriaIndex = categoriaMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocCategoria-1])
          var projetoIndex =  projetoMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocProjeto-1])
          var contaIndex = contaMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocCC-1])
          var departamentoIndex = departamentoMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocDepart-1])
  
          var departamentoDescricao =  sAtualDepFull[departamentoIndex][saDepFullCod-1]
          var categoriaDescricao =  sAtualCatFull[categoriaIndex][saCatFullCod-1]
          var projetoDescricao = sAtualProjFull[projetoIndex][saProjFullCod-1]
          var contaDescricao = sAtualCCFull[contaIndex][saCCFullNCodCC-1]
          var clienteDescricao = sAtualClFornFull[clienteIndex][saCFFullCodOmie-1]
  
          var parametros = [{
            'codigo_lancamento_omie': sAtualConPgtoFull[i][sAtualConPgtocCodOmie-1],
            'codigo_categoria': categoriaDescricao,
            'codigo_cliente_fornecedor': clienteDescricao,
            'codigo_projeto': projetoDescricao,
            'data_vencimento': new Date(sAtualConPgtoFull[i][sAtualConPgtocDVencimento-1]).toLocaleDateString("pt-br"),
            'distribuicao': [{ 
              "cCodDep": departamentoDescricao,
              "nPerDep": 100
            }],
            'id_conta_corrente': contaDescricao,
            'numero_parcela':  sAtualConPgtoFull[i][sAtualConPgtocParcela-1].toString(),
            'valor_documento': sAtualConPgtoFull[i][sAtualConPgtocValor-1], 
            'observacao': sAtualConPgtoFull[i][sAtualConPgtocObserv-1],
  
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result)
          var resposta = result.faultstring == undefined? "Dado Alterado!" : result.faultstring
  
          sAtualConPgto.getRange(i+1,sAtualConPgtocStatus).setValue(resposta)
          sAtualConPgto.getRange(i+1,sAtualConPgtocCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
    //Browser.msgBox("Itens Imputados:\n" + arrayPrint)
  }
  
  ```
* Excluir

  ```jsx
  async function excluirCPG() {
    var sAtualConPgto = ss.getSheetByName(sAtualConPgtoName)
    var sAtualConPgtoFull = sAtualConPgto.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "financas/contapagar/"
      var call =  "ExcluirContaPagar"
      
      for(var i=1;i<sAtualConPgtoFull.length;i++){
        if(sAtualConPgtoFull[i][sAtualConPgtocCheck-1] == true){
        console.log(i+1)
  
          var parametros = [{
            'codigo_lancamento_omie': sAtualConPgtoFull[i][sAtualConPgtocCodOmie-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
          var status = result.descricao_status
          
          sAtualConPgto.getRange(i+1,sAtualConPgtocCheck).setValue(false)
          sAtualConPgto.getRange(i+1,sAtualConPgtocStatus).setValue(status)
  
          console.log(result)
        }
      }
    }
    await processData()
  }
  
  ```
* Dar Baixar

  ```jsx
  async function lancarPgto() {
    var sAtualConPgto = ss.getSheetByName(sAtualConPgtoName)
    var sAtualConPgtoFull = sAtualConPgto.getDataRange().getValues()
  
    var sAtualCC = ss.getSheetByName(sAtualCCName)
    var sAtualCCFull = sAtualCC.getDataRange().getValues().filter(rows => rows[saCCFullInat-1] == "N")
    var contaMap = sAtualCCFull.map(row=> row[saCCFullDescr-1]).flat()
  
    const processData = async () => {
      var complemento_url = "financas/contapagar/"
      var call =  "LancarPagamento"
      
      for(var i=1;i<sAtualConPgtoFull.length;i++){
        if(sAtualConPgtoFull[i][sAtualConPgtocCheck-1] == true ){
        console.log(i+1)
  
        var contaIndex = contaMap.indexOf(sAtualConPgtoFull[i][sAtualConPgtocCC-1])
        var contaDescricao = sAtualCCFull[contaIndex][saCCFullNCodCC-1]
  
          var parametros = [{
            'codigo_lancamento': sAtualConPgtoFull[i][sAtualConPgtocCodOmie-1],//sAtualConPgtoFull[i][sAtualConPgtocCodMov-1],
            'codigo_conta_corrente': contaDescricao,
            'valor': sAtualConPgtoFull[i][sAtualConPgtocValorBaixa-1],
            'data': new Date(sAtualConPgtoFull[i][sAtualConPgtocDataBaixa-1]).toLocaleDateString("pt-br"),
            'observacao':  "Baixa de documento realizada via API.",
          }]
  
          console.log(parametros)
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result)
          var resposta = result.faultstring == undefined? "Dado Lançado!" : result.faultstring
  
          sAtualConPgto.getRange(i+1,sAtualConPgtocStatus).setValue(resposta)
          sAtualConPgto.getRange(i+1,sAtualConPgtocCodBaixa).setValue(result.codigo_baixa)
          sAtualConPgto.getRange(i+1,sAtualConPgtocCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
    //Browser.msgBox("Itens Imputados:\n" + arrayPrint)
  }
  
  ```
* Cancelar Baixar

  ```jsx
  async function cancelarPgto() {
    var sAtualConPgto = ss.getSheetByName(sAtualConPgtoName)
    var sAtualConPgtoFull = sAtualConPgto.getDataRange().getValues()
  
    //var data = transformaDadosArray(fullContPgto,1)
  
    const processData = async () => {
      var complemento_url = "financas/contapagar/"
      var call =  "CancelarPagamento"
      
      for(var i=1;i<sAtualConPgtoFull.length;i++){
        if(sAtualConPgtoFull[i][sAtualConPgtocCheck-1] == true){
        console.log(i+1)
          var parametros = [{
            'codigo_baixa': parseInt(sAtualConPgtoFull[i][sAtualConPgtocCodBaixa-1])
  
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result)
          var resposta = result.faultstring == undefined? "Dado Excluído!" : result.faultstring
  
          sAtualConPgto.getRange(i+1,sAtualConPgtocStatus).setValue(resposta)
          sAtualConPgto.getRange(i+1,sAtualConPgtocCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
    //Browser.msgBox("Itens Imputados:\n" + arrayPrint)
  }
  
  ```

## **==———Contas a Receber==**

### `ListarContasReceber`

* **Objetivo**: listar todas as contas a receber

```jsx
async function listarContReceber(){
  var sAtualConRec = ss.getSheetByName(sAtualConRecName)
  var sAtualDash = ss.getSheetByName(sAtualDashName)
  var dashDataInicio = new Date(sAtualDash.getRange(sAtualDashDataInicio).getValues())
  var dashDataFim = new Date(sAtualDash.getRange(sAtualDashDataFim).getValues())

  //console.log(dashDataInicio)
  //console.log(dashDataFim)

  var sAtualUsuario = ss.getSheetByName(sAtualUsuarioName)
  var sAtualUsuarioFull = sAtualUsuario.getDataRange().getValues()

  var sAtualClForn = ss.getSheetByName(sAtualClFornName)
  var sAtualClFornFull = sAtualClForn.getDataRange().getValues()

  var sAtualDep = ss.getSheetByName(sAtualDepName)
  var sAtualDepFull = sAtualDep.getDataRange().getValues()

  var sAtualCat = ss.getSheetByName(sAtualCatName)
  var sAtualCatFull = sAtualCat.getDataRange().getValues().filter(rows => rows[saCatFullCoRec-1] == "S" )

  var sAtualProj = ss.getSheetByName(sAtualProjName)
  var sAtualProjFull = sAtualProj.getDataRange().getValues()

  var sAtualCC = ss.getSheetByName(sAtualCCName)
  var sAtualCCFull = sAtualCC.getDataRange().getValues()

  var sAtualMovimento = ss.getSheetByName(sAtualMovimentoName)
  var sAtualMovimentoFull = sAtualMovimento.getDataRange().getValues().filter(rows=> rows[sAtualMovimentoCodBaixa-1] !== "" && rows[sAtualMovimentoNatureza-1] =="R")

  
  

  var clienteMap = sAtualClFornFull.map(row=> parseInt(row[saCFFullCodOmie-1])).flat()
  var departamentoMap = sAtualDepFull.map(row=> parseInt(row[saDepFullCod-1])).flat()
  var categoriaMap = sAtualCatFull.map(row=> row[saCatFullCod-1]).flat()
  var projetoMap = sAtualProjFull.map(row=> parseInt(row[saProjFullCod-1])).flat()
  var contaMap = sAtualCCFull.map(row=> parseInt(row[saCCFullNCodCC-1])).flat()
  var usuarioMap = sAtualUsuarioFull.map(row=> parseInt(row[sAtualCodUsuario-1])).flat()
  var movimentoMap = sAtualMovimentoFull.map(row=> parseInt(row[sAtualMovimentoCodTitulo-1])).flat()

  var page = 1
  var lastPage = 1
  
  var complemento_url = "financas/contareceber/"
  var call =  "ListarContasReceber"

  var arrayPrint=[]

  const processData = async () => {
    while(page <= lastPage){
      
      var parametros = [
        {
          "pagina": page,
          "registros_por_pagina": 999,
          "exibir_obs":"S"
        }
      ]
      
      var allData = await OmieAPI(complemento_url,call,parametros)
      lastPage = allData.total_de_paginas
      var lista = allData.conta_receber_cadastro

      console.log(allData.pagina)

      if (lista) {
        lista.forEach(item => {
          try{
            var dataOmie = item.data_vencimento.toString().split("/")
            var dataLista = new Date(dataOmie[2],dataOmie[1]-1,dataOmie[0])

            //console.log(item.data_vencimento)
            //console.log(dataLista)

            if(dataLista >= dashDataInicio && dataLista <= dashDataFim){         
              
              var departamentoIndex = item.distribuicao? item.distribuicao[0].cCodDep? departamentoMap.indexOf(parseInt(item.distribuicao[0].cCodDep)): -1:-1
              
              var clienteIndex = item.codigo_cliente_fornecedor? clienteMap.indexOf(parseInt(item.codigo_cliente_fornecedor)):-1
              var categoriaIndex = item.codigo_categoria? categoriaMap.indexOf(item.codigo_categoria):-1
              var projetoIndex = item.codigo_projeto? projetoMap.indexOf(parseInt(item.codigo_projeto)):-1
              var contaIndex = item.id_conta_corrente? contaMap.indexOf(parseInt(item.id_conta_corrente)):-1
              var usuarioInclusaoIndex = item.info.uInc? usuarioMap.indexOf(parseInt(item.info.uInc)):-1
              var usuarioAlteracaoIndex = item.info.uAlt? usuarioMap.indexOf(parseInt(item.info.uAlt)):-1
              var movimentoIndex = item.codigo_lancamento_omie? movimentoMap.indexOf(parseInt(item.codigo_lancamento_omie)):-1

              var departamentoDescricao = departamentoIndex !== -1 ? sAtualDepFull[departamentoIndex][saDepFullDesc-1] : item.distribuicao[0].cCodDep
              var categoriaDescricao = categoriaIndex !== -1 ? sAtualCatFull[categoriaIndex][saCatFullDesc-1] : item.codigo_categoria
              var projetoDescricao = projetoIndex !== -1 ? sAtualProjFull[projetoIndex][saProjFullNome-1] : item.codigo_projeto
              var contaDescricao = contaIndex !== -1 ? sAtualCCFull[contaIndex][saCCFullDescr-1] : item.id_conta_corrente
              var usuarioInclusaoDescricao = usuarioInclusaoIndex !== -1 ? sAtualUsuarioFull[usuarioInclusaoIndex][sAtualDescUsuario-1] : item.info.uInc
              var usuarioAlteracaoDescricao = usuarioAlteracaoIndex !== -1 ? sAtualUsuarioFull[usuarioAlteracaoIndex][sAtualDescUsuario-1] : item.info.uAlt
              var clienteDescricao = clienteIndex !== -1 ? sAtualClFornFull[clienteIndex][saCFFullRaz-1] : item.codigo_cliente_fornecedor
              var movimentoBaixa = movimentoIndex !== -1 ? sAtualMovimentoFull[movimentoIndex][sAtualMovimentoCodBaixa-1] : ""
              var movimentoData = movimentoIndex !== -1 ? sAtualMovimentoFull[movimentoIndex][sAtualMovimentoData-1] : ""
              var movimentoValor = movimentoIndex !== -1 ? sAtualMovimentoFull[movimentoIndex][sAtualMovimentoValor-1] : ""
              var movimentoID = movimentoIndex !== -1 ? sAtualMovimentoFull[movimentoIndex][sAtualMovimentoCodID-1] : ""
              

              arrayPrint.push([
                item.codigo_lancamento_omie,
                item.codigo_lancamento_integracao,

                contaDescricao,
                departamentoDescricao,
                categoriaDescricao,
                projetoDescricao,
                clienteDescricao,
                
                item.data_vencimento,
                item.numero_parcela,
                item.valor_documento,
                item.observacao,

                movimentoID,
                movimentoBaixa,
                movimentoData,
                movimentoValor,

                usuarioInclusaoDescricao,
                usuarioAlteracaoDescricao,
                item.info.dInc,
                item.info.dAlt,

              ])
            }
          }catch(error){
            console.error("Error processing data for page", page, error);        
          }
        })
      }

      
      page++
    }
  }

  
  await processData()

  sAtualConRec.getRange(linhaInicioCPG,sAtualConReccCheck,sAtualConRec.getMaxRows()+1-linhaInicioCPG,sAtualConRec.getLastColumn()).clearContent().setBackground(null)
  sAtualConRec.getRange(linhaInicioCPG,sAtualConReccCodOmie,arrayPrint.length,arrayPrint[0].length).setValues(arrayPrint)

}
```

* Incluir

  ```jsx
  async function incluirCRC() {
  
    var sAtualConRec = ss.getSheetByName(sAtualConRecName)
    var sAtualConRecFull = sAtualConRec.getDataRange().getValues()
  
    var sAtualClForn = ss.getSheetByName(sAtualClFornName)
    var sAtualClFornFull = sAtualClForn.getDataRange().getValues()
  
    var sAtualDep = ss.getSheetByName(sAtualDepName)
    var sAtualDepFull = sAtualDep.getDataRange().getValues().filter(rows => rows[saDepFullInativo-1] == "N")
  
    var sAtualCat = ss.getSheetByName(sAtualCatName)
    var sAtualCatFull = sAtualCat.getDataRange().getValues().filter(rows => rows[saCatFullCoRec-1] == "S" && rows[saCatFullInativo-1] == "N")
  
    var sAtualProj = ss.getSheetByName(sAtualProjName)
    var sAtualProjFull = sAtualProj.getDataRange().getValues().filter(rows => rows[saProjFullInat-1] == "N")
  
    var sAtualCC = ss.getSheetByName(sAtualCCName)
    var sAtualCCFull = sAtualCC.getDataRange().getValues().filter(rows => rows[saCCFullInat-1] == "N")
  
    var clienteMap = sAtualClFornFull.map(row=> row[saCFFullRaz-1]).flat()
    var departamentoMap = sAtualDepFull.map(row=> row[saDepFullDesc-1]).flat()
    var categoriaMap = sAtualCatFull.map(row=> row[saCatFullDesc-1]).flat()
    var projetoMap = sAtualProjFull.map(row=> row[saProjFullNome-1]).flat()
    var contaMap = sAtualCCFull.map(row=> row[saCCFullDescr-1]).flat()
    
  
    const processData = async () => {
      var complemento_url = "financas/contareceber/"
      var call =  "IncluirContaReceber"
      
      for(var i=1;i<sAtualConRecFull.length;i++){
        if(sAtualConRecFull[i][sAtualConReccCheck-1] == true){
        console.log(i+1)
          var clienteIndex = clienteMap.indexOf(sAtualConRecFull[i][sAtualConReccCliente-1])
          var categoriaIndex = categoriaMap.indexOf(sAtualConRecFull[i][sAtualConReccCategoria-1])
          var projetoIndex =  projetoMap.indexOf(sAtualConRecFull[i][sAtualConReccProjeto-1])
          var contaIndex = contaMap.indexOf(sAtualConRecFull[i][sAtualConReccCC-1])
          var departamentoIndex = departamentoMap.indexOf(sAtualConRecFull[i][sAtualConReccDepart-1])
  
          var departamentoDescricao =  sAtualDepFull[departamentoIndex][saDepFullCod-1]
          var categoriaDescricao =  sAtualCatFull[categoriaIndex][saCatFullCod-1]
          var projetoDescricao = sAtualProjFull[projetoIndex][saProjFullCod-1]
          var contaDescricao = sAtualCCFull[contaIndex][saCCFullNCodCC-1]
          var clienteDescricao = sAtualClFornFull[clienteIndex][saCFFullCodOmie-1]
  
          var parametros = [{
            //'data_entrada': new Date().toLocaleDateString("pt-br"),
  
            'codigo_lancamento_integracao': sAtualConRecFull[i][sAtualConReccCodInteg-1],
            'codigo_categoria': categoriaDescricao,
            'codigo_cliente_fornecedor': clienteDescricao,
            'codigo_projeto': projetoDescricao,
            'data_vencimento': new Date(sAtualConRecFull[i][sAtualConReccDVencimento-1]).toLocaleDateString("pt-br"),
            'distribuicao': [{ 
              "cCodDep": departamentoDescricao,
              "nPerDep": 100
            }],
            'id_conta_corrente': contaDescricao,
            'numero_parcela': sAtualConRecFull[i][sAtualConReccParcela-1].toString(),
            'valor_documento': sAtualConRecFull[i][sAtualConReccValor-1],
            'observacao': sAtualConRecFull[i][sAtualConReccObserv-1].toString()
  
          }]
  
          console.log(parametros)
          console.log(departamentoDescricao)
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result.distribuicao)
          console.log(result)
          var resposta = result.faultstring == undefined? "Dado Incluído!" : result.faultstring
  
          sAtualConRec.getRange(i+1,sAtualConReccStatus).setValue(resposta)
          sAtualConRec.getRange(i+1,sAtualConReccCheck).setValue(false)
          sAtualConRec.getRange(i+1,sAtualConReccCodOmie).setValue(result.codigo_lancamento_omie)
          
        }
      }
    }
    await processData()
    
    //Browser.msgBox("Itens Imputados:\n" + arrayPrint)
  }
  
  ```
* Alterar

  ```jsx
  async function alterarCRC() {
    var sAtualConRec = ss.getSheetByName(sAtualConRecName)
    var sAtualConRecFull = sAtualConRec.getDataRange().getValues()
  
    var sAtualClForn = ss.getSheetByName(sAtualClFornName)
    var sAtualClFornFull = sAtualClForn.getDataRange().getValues()
  
    var sAtualDep = ss.getSheetByName(sAtualDepName)
    var sAtualDepFull = sAtualDep.getDataRange().getValues().filter(rows => rows[saDepFullInativo-1] == "N")
  
    var sAtualCat = ss.getSheetByName(sAtualCatName)
    var sAtualCatFull = sAtualCat.getDataRange().getValues().filter(rows => rows[saCatFullCoRec-1] == "S" && rows[saCatFullInativo-1] == "N")
  
    var sAtualProj = ss.getSheetByName(sAtualProjName)
    var sAtualProjFull = sAtualProj.getDataRange().getValues().filter(rows => rows[saProjFullInat-1] == "N")
  
    var sAtualCC = ss.getSheetByName(sAtualCCName)
    var sAtualCCFull = sAtualCC.getDataRange().getValues().filter(rows => rows[saCCFullInat-1] == "N")
  
    var clienteMap = sAtualClFornFull.map(row=> row[saCFFullRaz-1]).flat()
    var departamentoMap = sAtualDepFull.map(row=> row[saDepFullDesc-1]).flat()
    var categoriaMap = sAtualCatFull.map(row=> row[saCatFullDesc-1]).flat()
    var projetoMap = sAtualProjFull.map(row=> row[saProjFullNome-1]).flat()
    var contaMap = sAtualCCFull.map(row=> row[saCCFullDescr-1]).flat()
  
    const processData = async () => {
      var complemento_url = "financas/contareceber/"
      var call =  "AlterarContaReceber"
      
      for(var i=1;i<sAtualConRecFull.length;i++){
        if(sAtualConRecFull[i][sAtualConReccCheck-1] == true){
          var clienteIndex = clienteMap.indexOf(sAtualConRecFull[i][sAtualConReccCliente-1])
          var categoriaIndex = categoriaMap.indexOf(sAtualConRecFull[i][sAtualConReccCategoria-1])
          var projetoIndex =  projetoMap.indexOf(sAtualConRecFull[i][sAtualConReccProjeto-1])
          var contaIndex = contaMap.indexOf(sAtualConRecFull[i][sAtualConReccCC-1])
          var departamentoIndex = departamentoMap.indexOf(sAtualConRecFull[i][sAtualConReccDepart-1])
  
          var departamentoDescricao =  sAtualDepFull[departamentoIndex][saDepFullCod-1]
          var categoriaDescricao =  sAtualCatFull[categoriaIndex][saCatFullCod-1]
          var projetoDescricao = sAtualProjFull[projetoIndex][saProjFullCod-1]
          var contaDescricao = sAtualCCFull[contaIndex][saCCFullNCodCC-1]
          var clienteDescricao = sAtualClFornFull[clienteIndex][saCFFullCodOmie-1]
  
          var parametros = [{
            'codigo_lancamento_omie': sAtualConRecFull[i][sAtualConReccCodOmie-1],
            'codigo_categoria': categoriaDescricao,
            'codigo_cliente_fornecedor': clienteDescricao,
            'codigo_projeto': projetoDescricao,
            'data_vencimento': new Date(sAtualConRecFull[i][sAtualConReccDVencimento-1]).toLocaleDateString("pt-br"),
            'distribuicao': [{ 
              "cCodDep": departamentoDescricao,
              "nPerDep": 100
            }],
            'id_conta_corrente': contaDescricao,
            'numero_parcela':  sAtualConRecFull[i][sAtualConReccParcela-1].toString(),
            'valor_documento': sAtualConRecFull[i][sAtualConReccValor-1], 
            'observacao': sAtualConRecFull[i][sAtualConReccObserv-1],
  
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result)
          var resposta = result.faultstring == undefined? "Dado Alterado!" : result.faultstring
  
          sAtualConRec.getRange(i+1,sAtualConReccStatus).setValue(resposta)
          sAtualConRec.getRange(i+1,sAtualConReccCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
    //Browser.msgBox("Itens Imputados:\n" + arrayPrint)
  }
  
  ```
* Excluir

  ```jsx
  async function excluirCRC() {
    var sAtualConRec = ss.getSheetByName(sAtualConRecName)
    var sAtualConRecFull = sAtualConRec.getDataRange().getValues()
  
    const processData = async () => {
      var complemento_url = "financas/contareceber/"
      var call =  "ExcluirContaReceber"
      
      for(var i=1;i<sAtualConRecFull.length;i++){
        if(sAtualConRecFull[i][sAtualConReccCheck-1] == true){
        console.log(i+1)
  
          var parametros = [{
            'chave_lancamento': sAtualConRecFull[i][sAtualConReccCodOmie-1],
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
          
          sAtualConRec.getRange(i+1,sAtualConReccCheck).setValue(false)
          sAtualConRec.getRange(i+1,sAtualConReccStatus).setValue(result.descricao_status)
  
          console.log(result)
        }
      }
    }
    await processData()
  }
  ```
* Dar Baixa

  ```jsx
  async function lancarRec() {
    var sAtualConRec = ss.getSheetByName(sAtualConRecName)
    var sAtualConRecFull = sAtualConRec.getDataRange().getValues()
  
    var sAtualCC = ss.getSheetByName(sAtualCCName)
    var sAtualCCFull = sAtualCC.getDataRange().getValues().filter(rows => rows[saCCFullInat-1] == "N")
    var contaMap = sAtualCCFull.map(row=> row[saCCFullDescr-1]).flat()
  
    const processData = async () => {
      var complemento_url = "financas/contareceber/"
      var call =  "LancarRecebimento"
      
      for(var i=1;i<sAtualConRecFull.length;i++){
        if(sAtualConRecFull[i][sAtualConReccCheck-1] == true ){
        console.log(i+1)
  
        var contaIndex = contaMap.indexOf(sAtualConRecFull[i][sAtualConReccCC-1])
        var contaDescricao = sAtualCCFull[contaIndex][saCCFullNCodCC-1]
  
          var parametros = [{
            'codigo_lancamento': sAtualConRecFull[i][sAtualConReccCodOmie-1],//sAtualConRecFull[i][sAtualConReccCodMov-1],
            'codigo_conta_corrente': contaDescricao,
            'valor': sAtualConRecFull[i][sAtualConReccValorBaixa-1],
            'data': new Date(sAtualConRecFull[i][sAtualConReccDataBaixa-1]).toLocaleDateString("pt-br"),
            'observacao':  "Baixa de documento realizada via API.",
          }]
  
          console.log(parametros)
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result)
          var resposta = result.faultstring == undefined? "Dado Lançado!" : result.faultstring
  
          sAtualConRec.getRange(i+1,sAtualConReccStatus).setValue(resposta)
          sAtualConRec.getRange(i+1,sAtualConReccCodBaixa).setValue(result.codigo_baixa)
          sAtualConRec.getRange(i+1,sAtualConReccCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
    //Browser.msgBox("Itens Imputados:\n" + arrayPrint)
  }
  
  ```
* Cancelar Baixa

  ```jsx
  async function cancelarRec() {
    var sAtualConRec = ss.getSheetByName(sAtualConRecName)
    var sAtualConRecFull = sAtualConRec.getDataRange().getValues()
  
    //var data = transformaDadosArray(fullContRec,1)
  
    const processData = async () => {
      var complemento_url = "financas/contareceber/"
      var call =  "CancelarRecebimento"
      
      for(var i=1;i<sAtualConRecFull.length;i++){
        if(sAtualConRecFull[i][sAtualConReccCheck-1] == true){
        console.log(i+1)
          var parametros = [{
            'codigo_baixa': parseInt(sAtualConRecFull[i][sAtualConReccCodBaixa-1])
  
          }]
  
          var result = await OmieAPI(complemento_url,call,parametros)
  
          console.log(result)
          var resposta = result.faultstring == undefined? "Dado Excluído!" : result.faultstring
  
          sAtualConRec.getRange(i+1,sAtualConReccStatus).setValue(resposta)
          sAtualConRec.getRange(i+1,sAtualConReccCheck).setValue(false)
          
        }
      }
    }
    await processData()
    
    //Browser.msgBox("Itens Imputados:\n" + arrayPrint)
  }
  
  ```