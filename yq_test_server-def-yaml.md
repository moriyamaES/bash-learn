# bashのyaml用ツールyqを使ってみた

## 参考サイト
- 使い方はChat-Gptに教わった
    ```
    https://www.evernote.com/shard/s10/nl/1269458/9ac778e3-ee5d-472a-9afb-4f31d79e13a0
    ```
- 公式のGitHubは以下
    ```
    https://github.com/mikefarah/yq
    ```
## Verification
1. The yaml used for validation is below
    ```sh
    cat yq_test_server.yaml
    ```
    - The results are below
        ```sh
        servers:
        - name: web#1
            env-def:
            ip-adress: 10.1.1.1
            middlewears: &web1-middlewears
            nginx:
                base-dir: /user/local/bin/
            node:
                base-dir: /user/local/bin/
                port: 5000
            node2:
                base-dir: /user/local/bin/
        - name: web#2
            ip-adress: 10.1.1.10
            middlewears: &web2-middlewears
            <<: *web1-middlewears
            nginx: null
        - name: web#3
            ip-adress: 10.1.1.11
            middlewears:
            <<: *web2-middlewears
        ```
1. Run the command below
    ```sh
    yq '(
    .servers.[]
    | select(.name == "web#1")
    | .middlewears
    | .node
    | .base-dir
    )' yq_test_server.yaml
    ```
    - 結果は以下
        ```sh
        /user/local/bin/
        ```
1. Run the command below
    ```sh
    yq '(
    > .servers.[]
    > | select(.name == "web#1")
    > | .middlewears
    > | .node
    > )' yq_test_server.yaml
    ```
    - The results are below
        ```
        base-dir: /user/local/bin/
        port: 5000
        ```
1. Run the command below
    ```sh
    yq '(
    > .servers.[]
    > | select(.name == "web#1")
    > | .middlewears
    > )' yq_test_server.yaml
    ```
    - The results are below
        ```
        &web1-middlewears
        nginx:
        base-dir: /user/local/bin/
        node:
        base-dir: /user/local/bin/
        port: 5000
        node2:
        base-dir: /user/local/bin/    
        ```
1. Run the command below
    ```sh
    yq '(
    > .servers.[]
    > | select(.name == "web#2")
    > | .middlewears
    > | .node
    > | .base-dir
    > )' yq_test_server.yaml
    ```
    - The results are below
        ```sh
        /user/local/bin/
        ```

1. Run the command below


    ```sh
    $ yq '(
    > .servers.[]
    > | select(.name == "web#2")
    > | .middlewears
    > | .node
    > )' yq_test_server.yaml
    base-dir: /user/local/bin/
    port: 5000
    ```
    ```sh
