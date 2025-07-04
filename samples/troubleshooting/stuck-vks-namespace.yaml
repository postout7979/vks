# vSphere Namespace가 삭제 되지 않는 경우

## Supervisor Control Plane SSH

https://knowledge.broadcom.com/external/article/323407/troubleshooting-vsphere-with-tanzu-tkgs.html

- vCenter shell 모드 접속해서 SCV password 확인

```bash
/usr/lib/vmware-wcp/decryptK8Pwd.py

ssh root@[IP address]
```

## Supervisor VM에서 실행

```bash
kubectl get namespace "stucked-namespace" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/"stucked-namespace"/finalize -f -
```

제거 되지 않을 경우에는 리소스 구성 요소 잔여 상태 확인 후, 모두 하나씩 제거

```yaml
for resource in `kubectl api-resources | grep -v [stucked-namespace] | awk '{print $1}'`; do echo $resource; kubectl get $resource -A 2> /dev/null | grep [stucked-namespace] ; done
```

- vCenter에서 wcp 재 실행

```bash
vmon-cli --restart wcp
```

## Supervisor VM에서 다시 실행

```bash
kubectl get namespace "stucked-namespace" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/"stucked-namespace"/finalize -f -
```

-

---

# Kubernetes namespace가 삭제 되지 않는 경우

```bash
kubectl get namespace "stucked-namespace" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/"stucked-namespace"/finalize -f -
```

+++
