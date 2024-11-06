# bashのyaml用ツールyqを使ってみた

## 参考サイト

- yq コマンドは2種類ある模様
    - https://zenn.dev/gkz/articles/yq-beginners-guide#3-1.-2%E7%A8%AE%E9%A1%9E%E3%81%AEyq%E3%82%B3%E3%83%9E%E3%83%B3%E3%83%89

    - jqのYAML/XMLラッパー
        - kislyuk/yq: Command-line YAML and XML processor - jq wrapper for YAML/XML documents
            - https://github.com/kislyuk/yq
        - こちらは、```pip``` でインストールする模様 → そのうち、調査

    - コマンドライン版yq <span style="color: red; ">★ここではこれを使用</span>
        - mikefarah/yq: yq is a portable command-line YAML processor
            - https://github.com/mikefarah/yq

            - このコマンドはChat-Gptに教わった
                - https://www.evernote.com/shard/s10/nl/1269458/9ac778e3-ee5d-472a-9afb-4f31d79e13a0

            - インストールて手順

                1. インストールコマンドを実行する
                    ```
                    sudo wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/local/bin/yq && chmod +x /usr/local/bin/yq
                    ```
                1. インストールの成功を確認するため、バージョンを確認する
                    ```
                    yq --version
                    ```

            - 詳しい使い方はここで解説
                - https://mikefarah.gitbook.io/yq/operators/anchor-and-alias-operators

## yq_test_server-ip.yaml の調査

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
