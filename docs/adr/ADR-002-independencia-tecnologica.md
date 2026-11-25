# ADR-002 — Independência tecnológica e custódia institucional

Status: decisão de projeto; implementação e conformidade pendentes.
Baseline: 881e50a72e04a43c0a5e1f304c319a0b67f56bf4
Data: 2026-11-24 (America/Cuiaba).

OpenSUS preserva Debian, PHP, MariaDB, Git e OpenEMR GPL-3.0-or-later. Componentes originais separáveis podem usar AGPL-3.0-or-later, após revisão de compatibilidade. Custódia brasileira não implica pureza de licença do custodiante. SERPRO, Dataprev, datacenters públicos e provedores nacionais qualificados são elegíveis; nenhum hyperscaler estrangeiro ou serviço Microsoft é obrigatório no produto.

Achados: 1191 entradas npm com registry público, 188 Composer produção e 63 desenvolvimento com dist GitHub. TypeScript 5.8.2 chega via eslint-plugin-jest 28.14.0 -> @typescript-eslint/utils 8.28.0 -> typescript-estree; remover com paridade de lint. npm postinstall chama napa com cinco URLs GitHub e duas jqueryui.com. Composer contém três repositórios externos declarados. Selenium/Panther já existem. Compose usa credenciais de exemplo inseguras e imagem OpenEMR upstream, não uma distribuição OpenSUS construída localmente.

Separar controle do produto e canal: A Microsoft, B canal Microsoft, C independente verificado, D desconhecido. A e D bloqueiam promoção; B bloqueia canal operacional, mas aquisição histórica segregada de software independente é permitida mediante aprovação e hashes. Não confundir metadados históricos com acesso operacional. Espelhar produto Microsoft não o torna independente.

Ordem: baseline e inventário total; remover TypeScript e auditar CLI npm/pnpm; substituir Napa e remapear Composer e registries; migrar Git para Forgejo, CI para Woodpecker, OCI para Harbor; validar Firefox ESR/Selenium; auditar Stone/Orthanc e toolchain; testar instalação sem rede pública, exportação, restauração e federação. Não apagar histórico nem branches existentes. Não declarar conformidade com base em grep ou SBOM parcial.

Gate final: ambiente Debian limpo, egress default-deny em hipervisor/firewall externo, espelho aprovado sem proxy upstream, execução de bootstrap/demo/test/test-e2e/validate-interop/exit-test/restore-test/acceptance, logs de DNS e conexões inclusive tentativas negadas, SBOM de build e runtime, revisão de origem e licenças, manifesto assinado e comparação de builds independentes. Falhar se evidência faltar. Testar A01–A19 com matriz rastreável, sem inventar conteúdo dos cenários. Nenhum dado sintético em sistemas oficiais de produção.

O script audit-locks.py é apenas gate preliminar. Não existe prova de build ou runtime independente nesta revisão. Não fazer merge em master. Usar branch de trabalho baseada na distribuição SUS, respeitando AGENTS.md e openemr-cmd.
