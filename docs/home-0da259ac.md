<!-- title: Home | url: https://outline.seazone.com.br/doc/home-FBRcKesT8G | area: Tecnologia -->

# Home

### Grid financeiro

### **API**

Com a mudança dos campos do grid de faturamento do proprietário será necessário refatorar a api `/financial_closing/` para trazer os novos campos

* \*Endpoint: \*\* `GET /financial_closing/`**Input:** start_date, end_date, property_id **Output:** Para cada mês:

```

Entradas: {
   Receita: 0.00
   Outras receitas: 0.00
}
Saidas: {
   Despesas: 0.00
   Comissão: 0.00
   Outros: 0.00  #Despesas que não se enquadram nos agrupamentos anteriores;
}
Minha carteira: {
   Saldo Devedor: 0.00  #Valor que deve ser quitado junto à Seazone
   Repasse: 0.00
}
```

Como visto no exemplo do output, os dados permanecerão praticamente os mesmos, no entanto será adicionado os campos "Outros" e "Saldo devedor":

* Campo "Outros": *Ajustes (caso o ajuste for negativo)*
* Campo "Outras receitas": *Ajustes (caso o ajuste for positivo)*
* Campo "Saldo devedor": *Saldo final do mês de referencia*

**OBS¹:** O Input permanecerá o mesmo e a forma como retornada também (as info por mês/ano) **OBS²:** Se informada a propriedade traz só referente à propriedade, se não informada propriedade, traz a soma do agrupado para todos os imóveis do proprietário. **OBS³:** Retorno do faturamento será removido.