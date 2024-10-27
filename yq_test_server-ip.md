# yq_test_server-ip.yaml の調査

- ``yq_test_server-ip.yaml``を``yq``でデータ読取を行う

- 参考資料は以下
https://mikefarah.gitbook.io/yq/operators/anchor-and-alias-operators

1. 以下のコマンドで全て表示する
    ```
    yq '(
    explode(.)
    )' yq_test_server-ip.yaml
    ```
    
1. 以下のコマンドでサーバを絞り込むことができる    
    
    ```bash
     yq '(
    .servers.[] 
    | select(.name[0] == "l3-lb")
    | explode(.)
    )' yq_test_server-ip.yaml
    ```    
    - 結果は以下
        ```yaml
        name:
        - l3-lb
        ip-addresses:
        - ip-address:
            - 10.19.84.252
            - vip: yes
        - url: http://portamhs.bb.local
        middleware:
        - type: service
          port:
            - 80
        destinations:
          - name:
              - rev-proxy#3
            ip-address:
              - 10.86.2.109
            port:
              - 80
          - name:
              - rev-proxy#4
            ip-address:
              - 10.86.2.110
            port:
              - 80        
        ```
