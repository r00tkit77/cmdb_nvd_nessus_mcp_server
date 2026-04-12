# CMDB-CVE MCP Server

A basic **Model Context Protocol (MCP) server** for vulnerability intelligence automation. This project combines a Configuration Management Database (CMDB) with real-time CVE ingestion from NIST NVD to identify potential exposure across our assets.

---

## Overview

This MCP server enables an AI agent (e.g., Claude Desktop) to:

* Query a **read-only CMDB** (asset inventory)
* Fetch recent **CVE data from NVD** via NVD REST API
* Correlate affected assets against known assets in CMDB
* Generate and send **structured vulnerability report** via email

---

## Data Flow

1. Load assets from CMDB
2. Fetch CVEs from NVD
3. Correlate CVEs with assets
4. Generate vulnerability report
5. Send report via email

---

## Architecture

```
cmdb-cve-mcp/
├── server.py          # MCP server 
├── cmdb.py            # SQLite-based read-only CMDB with sample assets
├── nvd_client.py      # Client to query NVD CVE API
├── email_sender.py    # SMTP email utility
├── requirements.txt
└── README.md
```

---

## Available MCP Tools

| Tool                        | Description                      | Example Prompt                                                                                                |
| --------------------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `list_assets`               | View all CMDB assets (read-only) | "Show me all assets in my CMDB"                                                                               |
| `fetch_latest_cves`         | Retrieve recent CVEs from NVD    | "Fetch CVEs from the last 7 days with CVSS >= 8"                                                              |
| `check_vulnerabilities`     | Match CVEs against CMDB assets   | "Check my assets for vulnerabilities in the last 14 days"                                                     |
| `send_vulnerability_report` | Email formatted report           | "Send a vulnerability report for the last 7 days to [user@example.com](mailto:user@example.com)"      |
| `run_full_workflow`         | End-to-end CVE scan + report     | "Run full vulnerability workflow for the last 30 days and send it to [user@example.com](mailto:user@example.com)" |

---

## Guardrails

**Security Guardrails**

* 🔒 **Read-only CMDB** – prevents any asset modification or prompt injection
* 🛡️ **Trusted data source** – CVEs fetched only from official NVD API
* ⚙️ **Restricted tool scope** – no arbitrary command execution
* 📧 **Secure config** – credentials managed via environment variables

**Operational Guardrails**

* ⏱️ **API constraints enforced** – CVE queries capped (max 120 days)
* 🚦 **Rate-limit aware fetching** – respects NVD API limits
* 📊 **Bounded results** – limits output content to save API tokens
* ⚠️ **Heuristic matching** – Avoids false negatives but may increase false positives

---


