#!/bin/bash
# ZION Backup — Substitui 6 scripts quebrados em 1 so
# Em nome do Senhor Jesus Cristo, nosso Salvador
set -euo pipefail

DATE=$(date +%Y%m%d_%H%M)
BACKUP_DIR="$HOME/.zion/backups/$DATE"
LOG="$HOME/.zion/logs/backup.log"

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG"; }

log "=== Backup $DATE starting ==="

# 1. Backup ZION state
mkdir -p "$BACKUP_DIR"
cp -r "$HOME/.zion/agents" "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$HOME/.zion/valentes" "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$HOME/.zion/evolution" "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$HOME/.zion/shared" "$BACKUP_DIR/" 2>/dev/null || true
cp -r "$HOME/.zion/revenue" "$BACKUP_DIR/" 2>/dev/null || true

# 2. Backup memory files
mkdir -p "$BACKUP_DIR/memory"
cp "$HOME/.claude/projects/-home-administrador/memory/"*.md "$BACKUP_DIR/memory/" 2>/dev/null || true

# 3. Backup secrets (encrypted location only)
cp "$HOME/.secrets.env" "$BACKUP_DIR/.secrets.env.bak" 2>/dev/null || true
chmod 600 "$BACKUP_DIR/.secrets.env.bak" 2>/dev/null || true

# 4. Git commit israel-one changes
cd "$HOME/israel-one"
git add -A 2>/dev/null || true
git commit -m "auto-backup $DATE" 2>/dev/null || true

# 5. Git commit padrao-bitcoin-backup
cd "$HOME/padrao-bitcoin-backup" 2>/dev/null && git add -A && git commit -m "auto-backup $DATE" 2>/dev/null || true

# 6. Cleanup old backups (keep last 10)
ls -dt "$HOME/.zion/backups"/*/ 2>/dev/null | tail -n +11 | xargs rm -rf 2>/dev/null || true

SIZE=$(du -sh "$BACKUP_DIR" 2>/dev/null | cut -f1)
log "Backup complete: $SIZE at $BACKUP_DIR"
