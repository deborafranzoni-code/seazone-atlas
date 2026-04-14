<!-- title: Definição Automática de Código do Imóvel | url: https://outline.seazone.com.br/doc/definicao-automatica-de-codigo-do-imovel-r3tmV6Zpjq | area: Tecnologia -->

# Definição Automática de Código do Imóvel

## ℹ️ Descrição

Este documento detalha o discovery técnico do [sistema de padronização de códigos de imóveis via N8N, Pipedrive e Google Sheets](https://n8n.seazone.com.br/workflow/a86s8PuhkOd8eErL). O objetivo é estabelecer uma lógica inteligente que identifique condomínios já cadastrados (mesmo com variações de nome) para reutilizar siglas existentes.

 ![](/api/attachments.redirect?id=e54691eb-9149-4374-b5c7-60c65f5630c9 " =1572x216")

##  🎁 Cenário Atual do [Workflow](https://n8n.seazone.com.br/workflow/a86s8PuhkOd8eErL)


1. Recebe `dealId` via [Webhook](https://workflows.seazone.com.br/webhook-test/8d29b9a7-85bc-4eb4-8269-5870871faeea).
2. Busca dados do Deal no Pipedrive
3. Baixa **toda** a base de códigos (Google Sheets).
4. Processamento (Nó `Code`):

   
   1. Mapeia os campos personalizados do Pipedrive (Hashes de ID) para variáveis legíveis.
   2. Aplica **Regex Inteligente** para localizar o número do apartamento no endereço completo (ex: transforma *"Rua X, apto 202"* em *"202"*) caso o campo dedicado esteja vazio.
   3. Formata o número do apartamento sempre com 4 dígitos (ex: `0202`).
   4. Normaliza o texto (remove espaços extras e padroniza caixa baixa/alta).
   5. Verifica se o nome do condomínio é válido através de uma *Blocklist* (rejeita termos como "Casa", "Não tem", "N/A", "---"), impedindo tentativas de matching em imóveis avulsos.
   6. Se o condomínio for válido, executa um loop comparando o nome de entrada com **cada linha** da base de dados (Google Sheets).
   7. Utiliza o algoritmo de **Distância de Levenshtein** para calcular uma nota de similaridade (0 a 100%) entre o texto digitado e o texto da base.
   8. Realiza uma validação secundária comparando o nome da Rua, caso a base possua esse dado, para desempatar homônimos.
   9. Define o veredito final baseado nos limiares de similaridade:
      * `**MATCH_FOUND**` **(≥ 90%):** Alta confiança de que é o mesmo prédio.
      * `**REVIEW_REQUIRED**` **(70% - 89%):** Similaridade média (possível variação de nome).
      * `**NO_MATCH_IN_DATABASE**` **(< 70%):** Nenhuma correspondência encontrada.
      * `**CODE_GENERATED_FROM_STREET**`**:** Caso o condomínio tenha sido invalidado na etapa 2 (gera sigla pela rua).
5. Decisão Binária (Nó `If`):

   
   1. **Caminho TRUE:** Se `status == MATCH_FOUND`, reutiliza a sigla e atualiza o Pipedrive.
   2. **Caminho FALSE:** Para **qualquer outro status** (incluindo *Review Required*), ele executa o nó `Code1`, que gera uma **nova sigla** e grava na base.

## 👨‍💻 Código dos Nós `Code` e `Code1`

```javascript
// ============================================================================
// CODE - MATCHING E GERAÇÃO DE CÓDIGO (VERSÃO FINAL)
// Threshold 90%, validação de endereço, mantém vogais, extração inteligente
// ============================================================================

// --- 1. FUNÇÃO DE SIMILARIDADE (FUZZY MATCHING) ---
function getSimilarityScore(s1, s2) {
    s1 = String(s1 || '').toLowerCase();
    s2 = String(s2 || '').toLowerCase();
    const len1 = s1.length;
    const len2 = s2.length;
    
    if (len1 === 0) return len2 === 0 ? 1 : 0;
    if (len2 === 0) return len1 === 0 ? 1 : 0;

    const matrix = [];
    for (let i = 0; i <= len1; i++) matrix[i] = [i];
    for (let j = 0; j <= len2; j++) matrix[0][j] = j;

    for (let i = 1; i <= len1; i++) {
        for (let j = 1; j <= len2; j++) {
            const cost = (s1.charAt(i - 1) === s2.charAt(j - 1)) ? 0 : 1;
            matrix[i][j] = Math.min(
                matrix[i - 1][j] + 1,
                matrix[i][j - 1] + 1,
                matrix[i - 1][j - 1] + cost
            );
        }
    }
    
    const distance = matrix[len1][len2];
    const maxLength = Math.max(len1, len2);
    if (maxLength === 0) return 1;
    return 1 - (distance / maxLength);
}

// --- 2. FUNÇÃO PARA GERAR CÓDIGO DA RUA ---
function removeAccents(str) {
    const accentsMap = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n',
        'Á': 'A', 'À': 'A', 'Ã': 'A', 'Â': 'A', 'Ä': 'A',
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'Í': 'I', 'Ì': 'I', 'Î': 'I', 'Ï': 'I',
        'Ó': 'O', 'Ò': 'O', 'Õ': 'O', 'Ô': 'O', 'Ö': 'O',
        'Ú': 'U', 'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ç': 'C', 'Ñ': 'N'
    };
    
    return str.split('').map(char => accentsMap[char] || char).join('');
}

function generateCodeFromStreet(streetName) {
    if (!streetName || typeof streetName !== 'string') return null;

    const cleanedStreet = streetName.replace(/^(rua|r\.|avenida|av\.|travessa|servidão)\s+/i, '').trim();
    const parts = cleanedStreet.split(' ').filter(p => p.length > 0 && isNaN(p));

    if (parts.length === 0) return null;

    let generatedCode = '';

    if (parts.length === 1) {
        const cleaned = removeAccents(parts[0].toUpperCase()).replace(/[^A-Z]/g, '');
        generatedCode = cleaned.substring(0, 3);
    } else if (parts.length === 2) {
        const first = removeAccents(parts[0].toUpperCase()).replace(/[^A-Z]/g, '');
        const second = removeAccents(parts[1].toUpperCase()).replace(/[^A-Z]/g, '');
        generatedCode = first.charAt(0) + second.substring(0, 2);
    } else {
        const first = removeAccents(parts[0].toUpperCase()).replace(/[^A-Z]/g, '');
        const second = removeAccents(parts[1].toUpperCase()).replace(/[^A-Z]/g, '');
        const last = removeAccents(parts[parts.length - 1].toUpperCase()).replace(/[^A-Z]/g, '');
        generatedCode = first.charAt(0) + second.charAt(0) + last.charAt(last.length - 1);
    }

    return generatedCode.toUpperCase().padEnd(3, 'X');
}

// --- 3. FUNÇÃO PARA EXTRAIR NÚMERO DO APARTAMENTO ---
function extractApartmentNumber(fullAddress) {
    if (!fullAddress || typeof fullAddress !== 'string') return null;
    
    const patterns = [
        /(?:apto?\.?\s*)(\d+)/i,
        /(?:apartamento\s+)(\d+)/i,
        /(?:ap\.?\s+)(\d+)/i,
        /(?:unidade\s+)(\d+)/i,
        /(?:sala\s+)(\d+)/i,
        /(?:conjunto\s+)(\d+)/i,
        /(?:número\s+)(\d+)/i,
        /(?:numero\s+)(\d+)/i,
        /(?:num\.?\s*)(\d+)/i,          // num 874, num. 874
        /(?:nr\.?\s*)(\d+)/i,           // nr 874, nr. 874
        /(?:n\.\s*)(\d+)/i,             // n. 874
        /(?:n[º°]\s*)(\d+)/i,           // nº 874, n° 874
        /(?:n\s+)(\d+)/i,               // n 874 (com espaço)
        /,\s*(\d+)\s*[-,]/,
        /-\s*(\d+)\s*[-,]/,
    ];
    
    for (const pattern of patterns) {
        const match = fullAddress.match(pattern);
        if (match && match[1]) {
            return match[1];
        }
    }
    
    const numbers = fullAddress.match(/\b(\d{2,4})\b/g);
    if (numbers && numbers.length > 0) {
        return numbers[numbers.length - 1];
    }
    
    return null;
}

// --- 4. FUNÇÃO PARA FORMATAR NÚMERO DO APARTAMENTO ---
function formatApartmentNumber(aptNumber) {
    if (!aptNumber) return '0000';
    const cleanNumber = String(aptNumber).replace(/\D/g, '');
    if (!cleanNumber) return '0000';
    return cleanNumber.padStart(4, '0');
}

// --- 5. FUNÇÃO DE VALIDAÇÃO DE CONDOMÍNIO ---
function isValidCondominium(condominiumValue) {
    if (!condominiumValue || typeof condominiumValue !== 'string') {
        return false;
    }
    
    const normalized = condominiumValue.trim().toLowerCase();
    
    // PROTEÇÃO 1: Rejeita strings vazias após trim
    if (normalized === '') {
        return false;
    }
    
    // PROTEÇÃO 2: Rejeita strings muito curtas (< 3 caracteres)
    // Condomínios reais têm nomes com pelo menos 3 caracteres
    if (normalized.length < 3) {
        return false;
    }
    
    // PROTEÇÃO 3: Rejeita strings que só contêm caracteres especiais/números
    // Condomínios reais devem ter pelo menos UMA letra
    if (!/[a-záàãâéêíóôõúç]/i.test(normalized)) {
        return false;
    }
    
    const invalidValues = [
        'não é condomínio', 'não é condominio', 'nao é condomínio', 'nao é condominio',
        'não tem condomínio', 'não tem condominio', 'sem condomínio', 'sem condominio',
        'n/a', 'na', 'não', 'nao', 'não se aplica', 'nao se aplica',
        'não informado', 'nao informado', 'indefinido', 'a definir',
        'casa', 'casa térrea', 'casa terrea', 'imóvel', 'imovel',
        '-', '--', '---', 'x', 'xx', 'xxx',
        '.', '..', '...', ',', ',,', ',,,',  // Caracteres especiais comuns
        '0', '00', '000', '1', '11', '111'   // Números sozinhos
    ];
    
    if (invalidValues.includes(normalized)) {
        return false;
    }
    
    const invalidPatterns = [
        /^n[ãa]o\s/i, /^sem\s/i, /^casa\s/i, /^casa$/i,
        /^resid[eê]ncia$/i, /^im[óo]vel$/i, 
        /^[-x\s.,:;!?@#$%&*()\[\]{}]{1,10}$/i  // Apenas caracteres especiais (até 10)
    ];
    
    for (const pattern of invalidPatterns) {
        if (pattern.test(normalized)) {
            return false;
        }
    }
    
    return true;
}

// --- 6. EXTRAÇÃO DE DADOS ---
const CONDOMINIUM_KEY = '0991df803259514d51f357faf6c34a88dea9408a';
const ADDRESS_KEY = 'efeaf16b0bc4ca4f43cc2cce7522886cc47995b3';
const APARTMENT_KEY = `${ADDRESS_KEY}_subpremise`;
const STREET_KEY = `${ADDRESS_KEY}_route`;

const dealData = $node["Get a deal"].json;
const baseData = items.map(item => item.json);

const dealCondominium = (dealData[CONDOMINIUM_KEY] || '').trim();
const dealAddress = dealData[ADDRESS_KEY] || '';
const dealStreet = dealData[STREET_KEY] || '';
const dealApartmentField = dealData[APARTMENT_KEY] || '';
const dealId = dealData.id || null;

// --- 7. VALIDAÇÃO DO CONDOMÍNIO ---
// Validação reforçada: condomínio deve estar preenchido E ser válido
const isCondominiumValid = dealCondominium !== '' && isValidCondominium(dealCondominium);

// --- 8. EXTRAÇÃO INTELIGENTE DO NÚMERO DO APARTAMENTO ---
let dealApartment = dealApartmentField;

if (!dealApartment && dealAddress) {
    const extractedNumber = extractApartmentNumber(dealAddress);
    if (extractedNumber) {
        dealApartment = extractedNumber;
    }
}

// --- 9. DADOS DE RETORNO BASE ---
const returnData = {
    dealId: dealId,
    condominiumName: dealCondominium,
    streetName: dealStreet,
    apartmentNumber: dealApartment,
    apartmentFormatted: formatApartmentNumber(dealApartment),
    apartmentSource: dealApartmentField ? 'field' : 'extracted',
    fullAddress: dealAddress,
    condominiumValid: isCondominiumValid
};

// --- 10. LÓGICA PRINCIPAL ---

// CENÁRIO 1: Condomínio válido → Tenta matching
if (isCondominiumValid && dealCondominium) {
    let bestMatch = null;
    let highestScore = 0;
    let suggestions = [];
    
    // THRESHOLDS AJUSTADOS
    const MATCH_THRESHOLD = 0.90;      // >= 90%: Aceita automaticamente
    const REVIEW_THRESHOLD = 0.70;     // 70-89%: Revisão manual
    const STREET_VALIDATION_THRESHOLD = 0.50;  // Rua deve ter >= 50% similaridade

    for (const baseItem of baseData) {
        const baseCondominium = (baseItem.Condomíno || baseItem.Condomínio || '').trim();
        
        // PROTEÇÃO: Pula registros da base com condomínio vazio
        // Evita falso positivo onde "vazio = vazio" resulta em 100% similaridade
        if (baseCondominium === '') {
            continue;
        }
        
        const score = getSimilarityScore(dealCondominium, baseCondominium); 

        // Se score >= 70%, considera como candidato
        if (score >= REVIEW_THRESHOLD) {
            const baseStreet = baseItem.Rua || '';
            const streetScore = getSimilarityScore(dealStreet, baseStreet);
            
            // VALIDAÇÃO CONDICIONAL DE RUA:
            // - Se base TEM rua → valida similaridade (≥50%)
            // - Se base NÃO TEM rua → aceita apenas pelo condomínio
            const baseHasStreet = baseStreet.trim() !== '';
            const streetValidationPassed = !baseHasStreet || streetScore >= STREET_VALIDATION_THRESHOLD;
            
            if (streetValidationPassed) {
                const suggestion = {
                    ...baseItem,
                    matchScore: score,
                    streetScore: streetScore,
                    similarityPercent: Math.round(score * 100),
                    original: baseCondominium,
                    code: baseItem.Código || baseItem.Codigo || '',
                    streetValidation: baseHasStreet ? 'validated' : 'skipped_empty'
                };
                
                suggestions.push(suggestion);
                
                // Se score >= 90% E validação de rua passou, considera como melhor match
                if (score >= MATCH_THRESHOLD && score > highestScore) {
                    highestScore = score;
                    bestMatch = suggestion;
                }
            }
        }
    }

    // Ordena sugestões por score
    suggestions.sort((a, b) => b.matchScore - a.matchScore);

    // CENÁRIO 1A: MATCH FORTE (>= 90% + rua similar)
    if (bestMatch) {
        const sigla = bestMatch.Sigla || bestMatch.code.substring(0, 3);
        const finalCode = sigla + returnData.apartmentFormatted;
        
        return [{ 
            json: { 
                ...returnData, 
                status: 'MATCH_FOUND',
                finalCode: finalCode,
                siglaUsed: sigla,
                matchDetails: bestMatch,
                matchScore: highestScore
            } 
        }];
    } 
    // CENÁRIO 1B: MATCH FRACO (70-89%): REVISÃO MANUAL
    else if (suggestions.length > 0) {
        return [{ 
            json: { 
                ...returnData, 
                status: 'REVIEW_REQUIRED',
                action: 'review_required',
                finalCode: 'REVIEW_REQUIRED',
                suggestions: suggestions.slice(0, 5),
                success: false
            } 
        }];
    }
    // CENÁRIO 1C: SEM MATCH (< 70%)
    else {
        return [{ 
            json: { 
                ...returnData, 
                status: 'NO_MATCH_IN_DATABASE', 
                finalCode: 'NO_MATCH',
                success: false
            } 
        }];
    }
}
// CENÁRIO 2: Condomínio inválido ou vazio → Gera pela rua
else {
    const generatedSigla = generateCodeFromStreet(dealStreet);

    if (generatedSigla) {
        const finalCode = generatedSigla + returnData.apartmentFormatted;
        
        return [{ 
            json: { 
                ...returnData, 
                status: 'CODE_GENERATED_FROM_STREET', 
                finalCode: finalCode,
                siglaGenerated: generatedSigla,
                nameUsedForCode: dealStreet
            } 
        }];
    } else {
        return [{ 
            json: { 
                ...returnData, 
                status: 'STREET_CODE_GENERATION_FAILED', 
                finalCode: 'GENERATION_FAILED'
            } 
        }];
    }
}
```


## 🎲 IDs do Workflow

* **Pipedrive Field ID (Código):** `5ae1b70b2c84cb6af6ca817167bed75a47cbeca4`
* **Pipedrive Field ID (Condomínio):** `0991df803259514d51f357faf6c34a88dea9408a`
* **Pipedrive Field ID (Endereço):** `efeaf16b0bc4ca4f43cc2cce7522886cc47995b3`
* **Spreadsheet ID:** `1okEa2-ZzgsbTHFwr8ffB1LEP-XviMmGa4e6XtmdhdkY`

## ⚒️ Melhorias

* **Lógica de "Review" ignorada:** O PRD exige revisão manual para scores entre 70-89%. O workflow atual ignora isso e força a criação de um novo código, gerando duplicidade (ex: criar `ICV` para um imóvel que deveria ser `ILC`).
* **Comparação Ineficiente:** O script compara o input com cada unidade individual (ex: compara com `ILC101`, `ILC102`...). Isso gera ruído no matching e perda de performance.
* **Manutenção Duplicada:** As funções de limpeza de endereço, regex de apartamento e validação estão copiadas nos nós `Code` e `Code1`. Alterar em um exige alterar no outro.
* **Criação da Tabela no Banco:** Migrar planilha de 'Base de código de imóveis' para uma tabela

## 🤖 Melhoria com IA 

Para superar as limitações do *Fuzzy Matching* tradicional (que compara apenas caracteres e falha em variações semânticas) e eliminar a complexidade de manutenção de RegEx, propõe-se a substituição do motor de decisão atual por um nó de **LLM (Large Language Model)** no n8n.

### 1. O Conceito: Matching Semântico

Ao contrário do algoritmo de Levenshtein, que calcula distância de caracteres, a IA realiza um **Matching Semântico**.

* **Cenário Atual (Levenshtein):** "Edifício Ocean" vs "Ocean Residence". Score baixo (palavras muito diferentes). **Resultado:** Cria duplicidade.
* **Cenário com IA:** A IA entende que "Edifício" e "Residence" são sinônimos irrelevantes e foca na identidade "Ocean". **Resultado:** Match Encontrado.

### 2. Implementação no N8N

Substituição dos nós `Code` e `Code1` complexos por um nó **Basic LLM Chain**.

**Fluxo Sugerido:**


1. **Entrada:** Dados do Deal.
2. **Contexto:** O n8n passa para a IA uma lista contendo informações dos apartamentos como o `Nome do Condomínio` e `Sigla`
3. Prompt do Sistema:

   ```javascript
   "Você é um especialista em gestão de propriedades. Sua tarefa é analisar o nome de um condomínio de entrada e encontrar a melhor correspondência na lista fornecida.
   
   Regras:
   
       Ignore termos genéricos (Residencial, Edifício, Spa, Home).
   
       Se a confiança for alta (>90%), retorne a sigla existente.
   
       Se houver dúvida (ex: homônimos), retorne 'REVIEW_REQUIRED'.
   
       Extraia o número do apartamento do endereço fornecido.
   
   Responda APENAS em JSON no formato: { 'status': 'MATCH_FOUND' | 'NEW_CODE', 'sigla': 'XYZ', 'confidence': 0.95, 'apartment': '0202' }"
   ```

## 3. Benefícios

| Problema Atual | Solução via IA |
|----|----|
| Lista de Stopwords Manual | **Automático:** A IA entende nativamente o que é irrelevante ("Residencial", "Apto", "Bl.") sem precisar hardcodar listas. |
| Regex Complexo | **Extração Natural:** A IA extrai o número do apartamento ("apto duzentos e dois", "sala 02") com muito mais precisão que expressões regulares. |
| Falsos Negativos | **Inferência:** A IA conecta "Jurerê Beach Village" com "JBV Resort" baseada no contexto, evitando a criação de siglas duplicadas. |
| Decisão de Review | **Análise de Sentimento/Confiança:** O nó `Switch` passa a operar baseado no `confidence` score da IA, enviando para revisão humana apenas casos genuinamente ambíguos. |