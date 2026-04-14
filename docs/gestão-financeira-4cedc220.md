<!-- title: Gestão Financeira | url: https://outline.seazone.com.br/doc/gestao-financeira-ZUMjKEclaE | area: Tecnologia -->

# Gestão Financeira

# PROMPT COMPLETO — FinFran: Controle Financeiro Seazone

## 1. VISÃO GERAL

Crie um sistema web de controle financeiro para franqueados da rede **Seazone** (aluguel por temporada). Stack: **React 18 + Vite + TypeScript + Tailwind CSS + shadcn/ui + Supabase (auth + database + RLS + storage)**. Toda a interface em **português brasileiro (pt-BR)**.


---

## 2. IDENTIDADE VISUAL

### Design Tokens (index.css)

`:root {   --background: 0 0% 99%;   --foreground: 220 40% 13%;   --card: 0 0% 100%;   --card-foreground: 220 40% 13%;   --popover: 0 0% 100%;   --popover-foreground: 220 40% 13%;   --primary: 217 70% 15%;          /* Navy Blue Seazone */   --primary-foreground: 0 0% 100%;   --secondary: 210 20% 96%;   --secondary-foreground: 220 40% 13%;   --muted: 210 20% 96%;   --muted-foreground: 215 16% 47%;   --accent: 6 100% 68%;             /* Coral Seazone */   --accent-foreground: 0 0% 100%;   --destructive: 0 84% 60%;   --destructive-foreground: 0 0% 100%;   --success: 142 76% 36%;   --success-foreground: 0 0% 100%;   --warning: 38 92% 50%;   --warning-foreground: 0 0% 100%;   --info: 199 89% 48%;   --info-foreground: 0 0% 100%;   --border: 214 32% 91%;   --input: 214 32% 91%;   --ring: 217 70% 15%;   --radius: 0.5rem;   --sidebar-background: 217 70% 15%;   --sidebar-foreground: 210 20% 96%;   --sidebar-primary: 6 100% 68%;   --sidebar-primary-foreground: 0 0% 100%;   --sidebar-accent: 217 60% 22%;   --sidebar-accent-foreground: 210 20% 96%;   --sidebar-border: 217 60% 22%;   --sidebar-ring: 6 100% 68%;   --chart-1: 217 70% 15%;   --chart-2: 6 100% 68%;   --chart-3: 142 76% 36%;   --chart-4: 38 92% 50%;   --chart-5: 199 89% 48%; }`

* Marca: texto "sea" em --primary + "zone" em --accent (sem logo/imagem)
* Dark mode com tokens invertidos
* Custom scrollbar com scrollbar-thin


---

## 3. BANCO DE DADOS (Supabase SQL)

### 3.1 Funções auxiliares

`-- Buscar profile_id pelo auth user id CREATE OR REPLACE FUNCTION public.get_user_profile_id(user_id uuid) RETURNS uuid LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'public' AS $$   SELECT id FROM public.profiles WHERE auth_user_id = user_id LIMIT 1; $$;  -- Verificar se o usuário é dono do recurso CREATE OR REPLACE FUNCTION public.user_owns_resource(user_id uuid, resource_profile_id uuid) RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'public' AS $$   SELECT EXISTS (     SELECT 1 FROM public.profiles WHERE auth_user_id = user_id AND id = resource_profile_id   ); $$;  -- Atualizar updated_at automaticamente CREATE OR REPLACE FUNCTION public.update_updated_at_column() RETURNS trigger LANGUAGE plpgsql SET search_path TO 'public' AS $$ BEGIN NEW.updated_at = now(); RETURN NEW; END; $$;  -- Criar profile automaticamente ao cadastrar usuário CREATE OR REPLACE FUNCTION public.handle_new_user() RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public' AS $$ BEGIN   INSERT INTO public.profiles (auth_user_id, name, email)   VALUES (NEW.id, COALESCE(NEW.raw_user_meta_data->>'name', 'Franqueado'), NEW.email);   RETURN NEW; END; $$;  -- Seed de categorias padrão ao criar profile CREATE OR REPLACE FUNCTION public.seed_default_cost_categories() RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path TO 'public' AS $$ BEGIN   INSERT INTO public.cost_categories (profile_id, category_group, name, description, is_default) VALUES     -- Fixos e Estruturais     (NEW.id, 'fixed_structural', 'Aluguel', 'Custos com aluguel do imóvel', true),     (NEW.id, 'fixed_structural', 'Condomínio', 'Despesas com o condomínio do imóvel', true),     (NEW.id, 'fixed_structural', 'IPTU', 'Impostos sobre o imóvel', true),     (NEW.id, 'fixed_structural', 'Mobiliário', 'Custos com móveis e equipamentos fixos', true),     (NEW.id, 'fixed_structural', 'Telefone', 'Despesas com plano de telefone fixo', true),     (NEW.id, 'fixed_structural', 'Internet', 'Despesas com plano de internet', true),     -- Operacionais     (NEW.id, 'operational', 'Produtos de Limpeza', 'Custos com materiais de limpeza utilizados nos imóveis', true),     (NEW.id, 'operational', 'Amenities', 'Itens de cortesia fornecidos aos hóspedes', true),     (NEW.id, 'operational', 'Manutenção e Reparos', 'Custos com manutenção preventiva e corretiva', true),     (NEW.id, 'operational', 'Lavanderia', 'Custos com lavagem de roupas de cama e banho', true),     (NEW.id, 'operational', 'Consumo de Água', 'Custos com consumo de água nos imóveis', true),     (NEW.id, 'operational', 'Consumo de Energia', 'Custos com eletricidade e gás', true),     (NEW.id, 'operational', 'Itens de Reposição', 'Reposição de utensílios ou objetos danificados', true),     (NEW.id, 'operational', 'Deslocamento de Equipe', 'Custos com transporte de funcionários ou prestadores', true),     (NEW.id, 'operational', 'Gasolina', 'Custos com combustível para os veículos da operação', true),     (NEW.id, 'operational', 'Veículo', 'Depreciação do veículo usado para a operação', true),     (NEW.id, 'operational', 'Manutenção de Veículo', 'Custos com manutenção dos veículos usados', true),     -- Pessoal     (NEW.id, 'personnel', 'Salários', 'Custos com salários pagos aos funcionários', true),     (NEW.id, 'personnel', 'Encargos Trabalhistas', 'Custos com INSS, FGTS e encargos trabalhistas', true),     (NEW.id, 'personnel', 'Benefícios', 'Custos com benefícios (vale-alimentação, plano de saúde, etc.)', true),     (NEW.id, 'personnel', 'Uniformes', 'Custos com uniformes para funcionários', true),     (NEW.id, 'personnel', 'Pró-labore do Franqueado', 'Valor pago ao franqueado pela gestão do negócio', true),     -- Variáveis     (NEW.id, 'variable', 'Impostos', 'Impostos sobre as transações e operações realizadas', true),     (NEW.id, 'variable', 'Taxas Bancárias', 'Custos com taxas de manutenção de contas bancárias', true),     (NEW.id, 'variable', 'Captação de Imóveis', 'Custos com visitas, contratos, materiais de apresentação', true),     (NEW.id, 'variable', 'Treinamentos e Reciclagens', 'Custos com capacitação e atualizações da equipe', true),     (NEW.id, 'variable', 'Software e Tecnologia', 'Custos com softwares pagos (ex: CRM, plataformas de gestão)', true),     (NEW.id, 'variable', 'Seguro do Imóvel', 'Custos com seguro do imóvel ou seguro de responsabilidade civil', true);   RETURN NEW; END; $$;`

### 3.2 Triggers

`-- Profile automático ao criar usuário no auth CREATE TRIGGER on_auth_user_created AFTER INSERT ON auth.users   FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();  -- Categorias padrão ao criar profile CREATE TRIGGER on_profile_created AFTER INSERT ON public.profiles   FOR EACH ROW EXECUTE FUNCTION public.seed_default_cost_categories();  -- updated_at em todas as tabelas CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); CREATE TRIGGER update_transactions_updated_at BEFORE UPDATE ON transactions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); CREATE TRIGGER update_cost_categories_updated_at BEFORE UPDATE ON cost_categories FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); CREATE TRIGGER update_recurring_bills_updated_at BEFORE UPDATE ON recurring_bills FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); CREATE TRIGGER update_recurring_bill_payments_updated_at BEFORE UPDATE ON recurring_bill_payments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); CREATE TRIGGER update_receipts_updated_at BEFORE UPDATE ON receipts FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); CREATE TRIGGER update_invoices_updated_at BEFORE UPDATE ON invoices FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); CREATE TRIGGER update_suppliers_updated_at BEFORE UPDATE ON suppliers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();`

### 3.3 Tabelas

`-- PROFILES CREATE TABLE public.profiles (   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),   auth_user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,   name text NOT NULL,   email text NOT NULL,   phone text, cpf text, franchise_name text, cnpj text,   address text, city text, bank_name text, bank_agency text, bank_account text,   notifications_email boolean DEFAULT true,   notifications_due_bills boolean DEFAULT true,   notifications_weekly_report boolean DEFAULT false,   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() ); ALTER TABLE profiles ENABLE ROW LEVEL SECURITY; CREATE POLICY "Users can view their own profile" ON profiles FOR SELECT USING (auth.uid() = auth_user_id); CREATE POLICY "Users can insert their own profile" ON profiles FOR INSERT WITH CHECK (auth.uid() = auth_user_id); CREATE POLICY "Users can update their own profile" ON profiles FOR UPDATE USING (auth.uid() = auth_user_id);  -- COST_CATEGORIES CREATE TABLE public.cost_categories (   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),   profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,   name text NOT NULL, description text,   category_group text NOT NULL, -- 'fixed_structural' | 'operational' | 'personnel' | 'variable'   is_default boolean DEFAULT false,   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() ); ALTER TABLE cost_categories ENABLE ROW LEVEL SECURITY; CREATE POLICY "Users can view their own cost categories" ON cost_categories FOR SELECT USING (user_owns_resource(auth.uid(), profile_id)); CREATE POLICY "Users can insert their own cost categories" ON cost_categories FOR INSERT WITH CHECK (user_owns_resource(auth.uid(), profile_id)); CREATE POLICY "Users can update their own cost categories" ON cost_categories FOR UPDATE USING (user_owns_resource(auth.uid(), profile_id)); CREATE POLICY "Users can delete their own cost categories" ON cost_categories FOR DELETE USING (user_owns_resource(auth.uid(), profile_id));  -- SUPPLIERS CREATE TABLE public.suppliers (   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),   profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,   name text NOT NULL, category text, document text,   email text, phone text, address text,   bank_name text, bank_agency text, bank_account text, notes text,   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() ); ALTER TABLE suppliers ENABLE ROW LEVEL SECURITY; -- (mesmas 4 policies CRUD com user_owns_resource)  -- TRANSACTIONS CREATE TABLE public.transactions (   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),   profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,   type text NOT NULL, -- 'revenue' | 'cost'   amount numeric NOT NULL,   description text NOT NULL,   transaction_date date NOT NULL DEFAULT CURRENT_DATE,   revenue_category text, -- usado quando type='revenue'   cost_category_id uuid REFERENCES cost_categories(id),   supplier_id uuid REFERENCES suppliers(id),   notes text, attachment_url text,   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() ); ALTER TABLE transactions ENABLE ROW LEVEL SECURITY; -- (mesmas 4 policies CRUD com user_owns_resource)  -- RECURRING_BILLS CREATE TABLE public.recurring_bills (   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),   profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,   name text NOT NULL, description text,   amount numeric NOT NULL,   frequency text NOT NULL, -- 'weekly'|'biweekly'|'monthly'|'quarterly'|'semiannual'|'annual'   due_day integer NOT NULL, -- 1-31   start_date date NOT NULL DEFAULT CURRENT_DATE,   end_date date,   is_active boolean DEFAULT true,   cost_category_id uuid REFERENCES cost_categories(id),   supplier_id uuid REFERENCES suppliers(id),   payment_link text, attachment_url text,   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() ); ALTER TABLE recurring_bills ENABLE ROW LEVEL SECURITY; -- (mesmas 4 policies CRUD)  -- RECURRING_BILL_PAYMENTS CREATE TABLE public.recurring_bill_payments (   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),   recurring_bill_id uuid NOT NULL REFERENCES recurring_bills(id) ON DELETE CASCADE,   profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,   amount numeric NOT NULL,   due_date date NOT NULL,   payment_date date,   status text NOT NULL DEFAULT 'pending', -- 'pending'|'paid'|'overdue'   notes text,   transaction_id uuid REFERENCES transactions(id),   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() ); ALTER TABLE recurring_bill_payments ENABLE ROW LEVEL SECURITY; -- (mesmas 4 policies CRUD)  -- RECEIPTS CREATE TABLE public.receipts (   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),   profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,   receipt_number text NOT NULL, -- auto: REC-0001   receipt_type text NOT NULL, -- 'maintenance'|'damage'|'guest_payment'|'other'   receipt_date date NOT NULL DEFAULT CURRENT_DATE,   description text NOT NULL,   amount numeric NOT NULL,   client_name text NOT NULL,   client_document text, client_email text,   status text NOT NULL DEFAULT 'pending', -- 'pending'|'generated'|'sent'   pdf_url text,   transaction_id uuid REFERENCES transactions(id),   sent_at timestamptz,   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() ); ALTER TABLE receipts ENABLE ROW LEVEL SECURITY; -- (mesmas 4 policies CRUD)  -- INVOICES CREATE TABLE public.invoices (   id uuid PRIMARY KEY DEFAULT gen_random_uuid(),   profile_id uuid NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,   invoice_number text NOT NULL,   issue_date date NOT NULL DEFAULT CURRENT_DATE,   due_date date,   client_name text NOT NULL, client_document text,   description text NOT NULL,   amount numeric NOT NULL,   status text NOT NULL DEFAULT 'pending', -- 'pending'|'issued'|'cancelled'   pdf_url text,   created_at timestamptz NOT NULL DEFAULT now(),   updated_at timestamptz NOT NULL DEFAULT now() ); ALTER TABLE invoices ENABLE ROW LEVEL SECURITY; -- (mesmas 4 policies CRUD)`

### 3.4 Storage

`-- Bucket para arquivos de notas fiscais INSERT INTO storage.buckets (id, name, public) VALUES ('invoice-files', 'invoice-files', false);`


---

## 4. AUTENTICAÇÃO

### 4.1 Fluxo de Login com Webhook N8N


1. Usuário preenche email + senha
2. Frontend faz POST https://webhook-n8n.seazone.com.br/webhook/finfran-login com {email, password}
3. Se resposta login_sucesso: true → chama supabase.auth.signInWithPassword({email, password})
4. Se login_sucesso: false → exibe "E-mail ou senha incorretos"
5. Se erro de rede → exibe "Erro ao conectar ao servidor de autenticação"

### 4.2 Cadastro

* Campos: Nome Completo, E-mail, Senha, Confirmar Senha
* Validação Zod: nome ≥ 2 chars, email válido, senha ≥ 6 chars, senhas iguais
* **NÃO habilitar auto-confirm**. Exigir verificação de e-mail.
* signUp com emailRedirectTo: window.location.origin + '/' e data: { name }
* Trigger handle_new_user cria profile automaticamente → trigger seed_default_cost_categories cria categorias

### 4.3 Recuperação de Senha

* Form com email → resetPasswordForEmail com redirectTo: origin + '/reset-password'

### 4.4 AuthProvider

Hook useAuth com Context: user, session, loading, signIn, signUp, signOut, resetPassword. onAuthStateChange + getSession no mount.

### 4.5 ProtectedRoute

Componente wrapper que redireciona para /auth se !user && !loading. Salva location.state.from para redirect pós-login.


---

## 5. NAVEGAÇÃO E LAYOUT

### Sidebar (navy, colapsável)

| **Item** | **Rota** | **Ícone (lucide)** |
|----|----|----|
| Dashboard | /dashboard | LayoutDashboard |
| Lançamentos | /lancamentos | ArrowUpDown |
| Contas Recorrentes | /contas-recorrentes | Calendar |
| Recibos | /recibos | Receipt |
| Notas Fiscais | /notas-fiscais | FileText |
| Fornecedores | /fornecedores | Users |
| Categorias | /categorias | Tag |
| **Footer:** |    |    |
| Configurações | /configuracoes | Settings |
| Sair | (logout) | LogOut |

Header: sea + zone (accent). Subtítulo: "Controle Financeiro".

### Rotas

* / → redirect /dashboard
* /auth → pública
* Todas as demais dentro de ProtectedRoute + AppLayout (sidebar + outlet)


---

## 6. CONSTANTES (Frontend hardcoded)

### Categorias de Receita (fixas, read-only)

`export const REVENUE_CATEGORIES = [   { id: 'reservations_commission', name: 'Comissões sobre Reservas' },   { id: 'cleaning_fee', name: 'Taxa de Limpeza Recebida' },   { id: 'extra_sales', name: 'Vendas Extras Durante a Estadia' },   { id: 'property_implementation', name: 'Implantação de Imóveis' },   { id: 'referral_commission', name: 'Comissões por Indicação' },   { id: 'other_revenue', name: 'Outros Recebimentos' }, ];`

### Grupos de Custo

`export const COST_CATEGORY_GROUPS = [   { id: 'fixed_structural', name: 'Custos Fixos e Estruturais' },   { id: 'operational', name: 'Custos Operacionais' },   { id: 'personnel', name: 'Custos de Pessoal' },   { id: 'variable', name: 'Custos Variáveis' }, ];`

### Tipos de Recibo

`export const RECEIPT_TYPES = [   { id: 'maintenance', name: 'Recibo de Manutenção' },   { id: 'damage', name: 'Recibo de Danos' },   { id: 'guest_payment', name: 'Recibo de Recebimento de Hóspede' },   { id: 'other', name: 'Outro' }, ];`

### Frequências

`export const BILL_FREQUENCIES = [   { id: 'weekly', name: 'Semanal' },   { id: 'biweekly', name: 'Quinzenal' },   { id: 'monthly', name: 'Mensal' },   { id: 'quarterly', name: 'Trimestral' },   { id: 'semiannual', name: 'Semestral' },   { id: 'annual', name: 'Anual' }, ];`


---

## 7. MÓDULOS DETALHADOS

### 7.1 Dashboard (/dashboard)

* **Cards KPI**: Receitas do mês (verde), Custos do mês (vermelho), Resultado (verde/vermelho), Contas a Vencer (7 dias, count + valor), Contas em Atraso (count + valor, variant danger)
* **Gráfico Fluxo de Caixa** (Recharts BarChart): barras receitas vs custos + linha saldo acumulado. Filtro: 30d/3m/6m/1 ano
* **Cards laterais**: Recibos Pendentes (count), Lançamentos do Mês (count)
* **2 PieCharts (Recharts)**: Distribuição Receitas por categoria, Distribuição Custos por grupo

### 7.2 Lançamentos (/lancamentos)

* **Filtros**: Select de mês (últimos 12), busca textual, tabs Todos/Receitas/Custos
* **Cards resumo**: Total Receitas (verde), Total Custos (vermelho), Resultado
* **Tabela**: Data, Tipo (badge verde=Receita/vermelho=Custo com ícone seta), Categoria, Descrição, Valor, Ações (editar/excluir)
* **Paginação**: 20 por página
* **Exportar CSV**: filtrado por mês, separador ;, BOM UTF-8
* **Dialog Novo/Editar**: Tabs Receita/Custo, seleção de categoria (receita=fixas / custo=agrupadas por grupo), fornecedor (opcional), valor com máscara, date picker pt-BR, descrição, notas
* **Validação Zod**: tipo, valor > 0, descrição obrigatória, data obrigatória, categoria obrigatória conforme tipo

### 7.3 Contas Recorrentes (/contas-recorrentes)

* **Navegação**: mês atual + 11 meses para frente (SEM retroativo)
* **Cards**: Contas do Mês, Total Mensal, Pagas (verde), Atrasadas (vermelho)
* **Alertas visuais**: Card vermelho com lista de atrasadas + botão "Registrar Pagamento". Card amarelo com vencendo em 7 dias.
* **Tabela**: Nome, Categoria, Fornecedor, Frequência, Dia Venc., Status (badge Pago=verde/A Vencer=amarelo/Atrasado=vermelho), Valor, Ações (editar/excluir/pagar)
* **Fluxo "Registrar Pagamento"**:

  
  1. Atualiza ou cria recurring_bill_payments com status=paid, payment_date=hoje
  2. Insere transaction tipo=cost com descrição "NomeConta (conta recorrente)", category_id e supplier_id da conta
  3. Cria payment do próximo mês com status=pending se não existir
  4. Toast com resumo do que foi feito
* **Dialog Novo/Editar**: nome, valor, dia vencimento (1-31), frequência (select), fornecedor (select opcional), categoria de custo (select agrupado), link de pagamento, descrição

### 7.4 Recibos (/recibos)

* **Cards**: Total Gerado, Pendentes (warning), Enviados (primary), Valor Total
* **Tabela**: Nº Recibo, Data, Tipo (badge), Descrição, Cliente, Status (Select inline editável: Pendente→Gerado→Enviado), Valor, Ações (download/editar/excluir)
* **Numeração automática**: REC-0001 incremental
* **Download**: Gera HTML estilizado do recibo (com dados emitente do profile, dados pagador, valor, descrição, assinatura) e abre em nova aba para impressão/save
* **Dialog Novo/Editar**: tipo recibo (select), cliente, CPF/CNPJ, email, descrição, valor, data, status

### 7.5 Notas Fiscais (/notas-fiscais)

* **Cards**: Emitidas, Pendentes (warning), Valor Total Emitido
* **Tabela**: Nº Nota, Data, Cliente, Descrição, Status (Emitida=primary/Pendente=warning/Cancelada=destructive), Valor, Ações (editar/excluir)
* **Dialog Novo/Editar**: número, status, cliente, CNPJ/CPF, descrição, valor, data emissão, data vencimento

### 7.6 Fornecedores (/fornecedores)

* **Cards**: Total Cadastrados, Categorias (count), Maior Fornecedor
* **Tabela**: Nome (com avatar ícone Building2), Categoria (badge colorido), CNPJ/CPF, Contato (phone+email empilhados), Ações
* **Dialog Novo/Editar**: nome, categoria (texto livre), documento, email, telefone, endereço, banco, agência, conta, observações
* **Hook useSuppliers**: CRUD encapsulado com profile_id automático

### 7.7 Categorias (/categorias)

* **Tabs**: Custos / Receitas
* **Custos**: 4 cards (um por grupo), cada um com tabela de categorias (nome, descrição, tipo Padrão/Custom). CRUD via dialog (nome, descrição, grupo select)
* **Receitas**: Tabela read-only das 6 categorias fixas
* **Hook useCostCategories**: usa React Query com invalidação

### 7.8 Configurações (/configuracoes)

* **Tabs**: Perfil / Franquia / Notificações
* **Perfil**: Nome, E-mail (disabled), Telefone, CPF + Botão salvar. Seção "Alterar Senha" com nova senha + confirmar + botão (usa supabase.auth.updateUser)
* **Franquia**: Nome Franquia, CNPJ, Endereço, Cidade + Separador + Dados Bancários (Banco, Agência, Conta) + Botão salvar
* **Notificações**: 3 switches (E-mail, Alertas Vencimento, Relatório Semanal) + Botão salvar


---

## 8. HOOKS CUSTOMIZADOS

| **Hook** | **Responsabilidade** |
|----|----|
| useAuth | AuthProvider + contexto (user, session, signIn, signUp, signOut, resetPassword) |
| useProfile | Carrega profile por auth_user_id. Retorna {profile, loading} |
| useCostCategories | React Query para cost_categories por profile_id. Retorna {categories, loading, invalidate} |
| useSuppliers | CRUD completo de suppliers por profile_id. Retorna {suppliers, loading, createSupplier, updateSupplier, deleteSupplier} |


---

## 9. DEPENDÊNCIAS NPM

react@^18, react-dom@^18, react-router-dom@^6,  @tanstack/react-query, @supabase/supabase-js, tailwindcss, tailwindcss-animate, tailwind-merge, clsx, class-variance-authority, react-hook-form, @hookform/resolvers, zod, recharts, date-fns, lucide-react, sonner, shadcn/ui (todos os componentes: card, table, badge, dialog, alert-dialog, select, tabs, form, button, input, textarea, calendar, popover, separator, switch, sidebar, tooltip, toast, skeleton, scroll-area, etc.) 


---

## 10. REGRAS DE NEGÓCIO IMPORTANTES


1. **Isolamento de dados**: Cada franqueado só vê seus próprios dados (RLS com user_owns_resource)
2. **Categorias de receita são fixas** — não editáveis pelo franqueado
3. **Categorias de custo são editáveis** — 28 categorias padrão criadas automaticamente + custom
4. **Contas recorrentes**: Navegação APENAS para frente (mês atual + 11 meses). Ao pagar → gera custo + cria próximo mês
5. **Recibos**: Numeração sequencial automática (REC-XXXX). Download como HTML formatado
6. **Exportação CSV**: BOM UTF-8, separador ;, filtrado por mês
7. **Formato monetário**: R$ X.XXX,XX (pt-BR)
8. **Datas**: Formato dd/MM/yyyy (pt-BR)
9. **Login dupla validação**: Webhook N8N primeiro, depois Supabase Auth