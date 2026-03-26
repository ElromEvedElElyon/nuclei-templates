# Machine Optimization — i3 M370 3.3GB RAM

## PROBLEMA: OOM Crashes Frequentes
- Claude Code + MCP servers + browser = facilmente 2.5GB+
- Session 25 crash: 15+ Chrome processes = OOM kill
- Session 26 crash: muitos agentes paralelos

## REGRAS PARA NAO CRASHAR

### Limitar processos simultaneos
- MAX 4-5 agentes Claude paralelos
- 1 instancia browser por vez (headless=true SEMPRE)
- Matar Chrome/Firefox quando nao em uso: `pkill -f chrome; pkill -f firefox`
- Load average > 10 = perigo. `uptime` para checar

### Monitorar memoria
```bash
free -h                          # Ver memoria disponivel
ps aux --sort=-%mem | head -10   # Top 10 processos por RAM
```

### MCP Servers (consomem ~60MB cada!)
- Cada MCP server = ~60-100MB (Node.js process)
- Com 5 servers = 300-500MB so de MCP
- Desabilitar servers nao usados em ~/.claude.json

### Chrome/Firefox
- Headless mode SEMPRE (sem UI = menos RAM)
- 1 tab por vez
- `google-chrome --headless --disable-gpu --no-sandbox`
- Firefox Snap consome MAIS memoria que Chrome

### Claude Code
- Sessoes CURTAS (evitar acumulo de contexto)
- Sonnet para 90% das tarefas (mais rapido, menos processamento)
- Opus SOMENTE para auditorias criticas
- Background agents: verificar que completaram antes de lancar mais
- `run_in_background: true` para tarefas longas

### Swap (3.6GB configurado)
- Swap ja ativo e ajuda, mas I/O lento
- Se swap usage > 2GB = sistema muito lento
- `swapon --show` para verificar

### Quando crashar:
1. Verificar o que estava rodando (`ps aux --sort=-%mem`)
2. Matar processos orfaos (`pkill -f chrome; pkill -f node`)
3. `free -h` para confirmar memoria liberada
4. Reiniciar Claude Code
5. Checar memory files para retomar trabalho

## DICA: Auto-Backup
- Timer systemd ativo (hourly)
- Cron backup ativo
- Memory files em ~/.claude/ persistem entre sessions
- Git commits como checkpoints
