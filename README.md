⚠️ Critical RCE in Ingress-NGINX via Configuration Injection (CVE-2025-1974 and more)

This repository contains a proof-of-concept (PoC) exploit for CVE-2025-1974, a Critical (CVSS 9.8) vulnerability in the Ingress-NGINX controller for Kubernetes. This flaw allows unauthenticated remote code execution via unsafe configuration injection when using the Validating Admission Controller. It is the most serious of a set of five vulnerabilities disclosed and patched on March 26, 2025.

⸻

📌 Impact:
•	Affected Versions: Ingress-NGINX controller prior to v1.12.1 / v1.11.5
•	Attack Surface:
	•	Exploitable by any workload on the Pod network — no credentials or admin privileges required
	•	Attackers can inject arbitrary NGINX directives (e.g., content_by_lua_block) via annotations like configuration-snippet
	•	When combined with misconfigurations, attackers can exfiltrate Secrets or achieve full cluster compromise
•	Scope:
	•	Ingress-NGINX often has access to all cluster Secrets by default
	•	Pods in a typical cloud VPC or corporate network can reach the admission controller endpoint
	•	Affected clusters include those running Ingress-NGINX with admission control enabled (default in many setups)

⸻

🛡️ Mitigation:
•	Upgrade to Ingress-NGINX v1.12.1 or v1.11.5
•	Disable risky annotations (configuration-snippet, server-snippet, etc.)
•	Lock down network access to the Validating Admission Webhook
•	Apply strict RBAC to prevent unauthorized Ingress creation

⸻

🧪 This PoC demonstrates how attackers can leverage the vulnerability to run arbitrary code inside the ingress controller pod — which often has access to internal services and secrets — escalating to full cluster takeover in vulnerable configurations.

🚨 Disclaimer: This PoC is for educational and research purposes only. Do not use it without explicit permission.
