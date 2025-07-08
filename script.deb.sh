#!/bin/bash

# ==========================================
# Uptime Monitoring Additions
# ==========================================

# Webhook URL for status reporting (replace with your endpoint)
STATUS_WEBHOOK="https://your-status-page.com/api/update"

# Service to monitor (change to your service name)
MONITOR_SERVICE="pufferpanel"

# Log file location
LOG_FILE="/var/log/pufferpanel_monitor.log"

report_status() {
  local status=$1
  curl -X POST -H "Content-Type: application/json" -d \
    "{\"service\":\"$MONITOR_SERVICE\",\"status\":\"$status\",\"timestamp\":\"$(date -Is)\"}" \
    $STATUS_WEBHOOK >> $LOG_FILE 2>&1
}

check_service() {
  if ! systemctl is-active --quiet $MONITOR_SERVICE; then
    echo "[$(date)] Service $MONITOR_SERVICE is down! Restarting..." >> $LOG_FILE
    report_status "down"
    systemctl restart $MONITOR_SERVICE
    report_status "restarted"
  fi
}

# ==========================================
# Original Installation Script (Modified)
# ==========================================

[Previous script content remains the same until the final main() section]

main ()
{
  # Original installation steps
  detect_os
  curl_check
  gpg_check
  detect_apt_version
  [rest of original main function...]

  # After successful installation
  echo -n "Configuring uptime monitoring... "
  
  # Create systemd service monitor
  cat > /etc/systemd/system/pufferpanel-monitor.service <<EOF
[Unit]
Description=PufferPanel Uptime Monitor
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'while true; do $0 check_service; sleep 60; done'
Restart=always

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable pufferpanel-monitor
  systemctl start pufferpanel-monitor
  report_status "installed"
  echo "done."
}

# ==========================================
# New Command Line Arguments
# ==========================================

case "$1" in
  install)
    main
    ;;
  check)
    check_service
    ;;
  *)
    echo "Usage: $0 {install|check}"
    exit 1
esac
