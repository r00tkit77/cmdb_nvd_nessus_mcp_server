import sqlite3


SAMPLE_ASSETS = [
    {"name": "web-prod-01",            "type": "server",         "os": "Ubuntu 22.04",  "software": "nginx 1.24.0, openssl 3.0.2, python 3.10.12",              "owner": "platform-team",  "env": "prod"},
    {"name": "web-prod-02",            "type": "server",         "os": "Ubuntu 22.04",  "software": "nginx 1.24.0, openssl 3.0.2, python 3.10.12",              "owner": "platform-team",  "env": "prod"},
    {"name": "api-gateway-01",         "type": "server",         "os": "Debian 11",     "software": "nginx 1.22.1, openssl 1.1.1n, node 18.12.0",               "owner": "backend-team",   "env": "prod"},
    {"name": "db-prod-01",             "type": "server",         "os": "CentOS 7.9",    "software": "postgresql 14.5, openssl 1.0.2k",                          "owner": "dba-team",       "env": "prod"},
    {"name": "db-prod-02",             "type": "server",         "os": "CentOS 7.9",    "software": "postgresql 14.5, redis 7.0.5",                             "owner": "dba-team",       "env": "prod"},
    {"name": "auth-service-01",        "type": "server",         "os": "Ubuntu 20.04",  "software": "python 3.9.16, openssl 1.1.1f, openssh 8.2p1",             "owner": "security-team",  "env": "prod"},
    {"name": "k8s-worker-01",          "type": "server",         "os": "Ubuntu 22.04",  "software": "docker 24.0.5, kubernetes 1.27.3, containerd 1.6.21",      "owner": "infra-team",     "env": "prod"},
    {"name": "k8s-worker-02",          "type": "server",         "os": "Ubuntu 22.04",  "software": "docker 24.0.5, kubernetes 1.27.3, containerd 1.6.21",      "owner": "infra-team",     "env": "prod"},
    {"name": "elk-stack-01",           "type": "server",         "os": "Debian 12",     "software": "elasticsearch 8.9.0, kibana 8.9.0, logstash 8.9.0, java 17.0.7", "owner": "devops-team", "env": "prod"},
    {"name": "jenkins-01",             "type": "server",         "os": "Ubuntu 20.04",  "software": "java 11.0.20, jenkins 2.414.1, git 2.25.1",                "owner": "devops-team",    "env": "prod"},
    {"name": "staging-web-01",         "type": "server",         "os": "Ubuntu 22.04",  "software": "nginx 1.18.0, openssl 3.0.2, python 3.11.0",               "owner": "platform-team",  "env": "staging"},
    {"name": "staging-db-01",          "type": "server",         "os": "Ubuntu 20.04",  "software": "mysql 8.0.33, redis 6.2.13",                               "owner": "dba-team",       "env": "staging"},
    {"name": "dev-workstation-alice",  "type": "workstation",    "os": "Ubuntu 22.04",  "software": "python 3.11.0, docker 24.0.5, vscode 1.81.1, node 20.5.0", "owner": "alice",          "env": "dev"},
    {"name": "dev-workstation-bob",    "type": "workstation",    "os": "macOS 13.5",    "software": "python 3.11.0, node 18.17.0, docker 24.0.5, openssl 3.1.2","owner": "bob",            "env": "dev"},
    {"name": "firewall-core-01",       "type": "network-device", "os": "pfSense 2.7.0", "software": "openssl 1.1.1t, openssh 9.3p1",                            "owner": "network-team",   "env": "prod"},
    {"name": "frontend-prod-01",       "type": "server",         "os": "Ubuntu 22.04",  "software": "node 18.12.0, axios 1.14.0, nginx 1.24.0",                 "owner": "frontend-team",  "env": "prod"},
    {"name": "devops-mcp-server-01",   "type": "server",         "os": "Ubuntu 22.04",  "software": "aws-mcp-server 0.9.1, aws-cli 2.13.0, python 3.11.0",      "owner": "devops-team",    "env": "prod"},
]


class CMDB:
    def __init__(self, db_path: str = "cmdb.sqlite"):
        self.db_path = db_path
        self._init_db()

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Create the table and seed all assets if the DB is empty."""
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS assets (
                    id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    name       TEXT NOT NULL UNIQUE,
                    type       TEXT NOT NULL,
                    os         TEXT NOT NULL,
                    software   TEXT,
                    owner      TEXT DEFAULT 'unknown',
                    env        TEXT DEFAULT 'prod',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            existing = conn.execute("SELECT COUNT(*) FROM assets").fetchone()[0]
            if existing == 0:
                for a in SAMPLE_ASSETS:
                    try:
                        conn.execute(
                            "INSERT INTO assets (name, type, os, software, owner, env) VALUES (?,?,?,?,?,?)",
                            (a["name"], a["type"], a["os"], a["software"], a["owner"], a["env"]),
                        )
                    except Exception:
                        pass
                conn.commit()

    def list_assets(self) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute("SELECT * FROM assets ORDER BY env, name").fetchall()
        return [dict(r) for r in rows]
