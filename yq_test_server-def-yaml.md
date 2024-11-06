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


## Verification
1. The yaml used for validation is below
    ```bash
    # コメント
    cat yq_test_server.yaml
    ```
    - The results are below
        ```yaml
        servers:
        - name: web#1
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
    ```bash
    yq '(
    .servers.[]
    | select(.name == "web#1")
    | .middlewears
    | .node
    | .base-dir
    )' yq_test_server.yaml
    ```
    - 結果は以下
        ```
        /user/local/bin/
        ```
1. Run the command below
    ```bash
    yq '(
    .servers.[]
    | select(.name == "web#1")
    | .middlewears
    | .node
    )' yq_test_server.yaml
    ```
    - The results are below
        ```
        base-dir: /user/local/bin/
        port: 5000
        ```
1. Run the command below
    ```bash
    yq '(
    .servers.[]
    | select(.name == "web#1")
    | .middlewears
    )' yq_test_server.yaml
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
    ```
    yq '(
    .servers.[] 
    | select(.name == "web#1")
    | .middlewears
    | .nginx
    )' yq_test_server.yaml
    ```
    - The results are below
        ```
        base-dir: /user/local/bin/
        ```
1. Run the command below
    ```
    yq '(
    .servers.[]
    | select(.name == "web#2")
    | .middlewears
    | .node
    | .base-dir
    )' yq_test_server.yaml
    ```
    - The results are below
        ```
        /user/local/bin/
        ```
1. Run the command below
    ```
    yq '(
    .servers.[]
    | select(.name == "web#2")
    | .middlewears
    | .node
    )' yq_test_server.yaml
    ```
    - The results are below
        ```
        base-dir: /user/local/bin/
        port: 5000
        ```
1. Run the command below
    ```bash
    yq '(
    .servers.[] 
    | select(.name == "web#2")
    | .middlewears
    | .nginx
    )' yq_test_server.yaml
    ```
    - The results are below
        ```
        null
        ```
1. Run the command below
    ```bash
    yq '(
    .servers.[]
    | select(.name == "web#3")
    | .middlewears
    | .node
    )' yq_test_server.yaml
    ```
    - The results are below
        ```
        base-dir: /user/local/bin/
        port: 5000
        ```
1. Run the command below
    ```bash
    yq '(
    .servers.[]
    | select(.name == "web#3")
    | .middlewears
    | .nginx
    )' yq_test_server.yaml
    ```
    - The results are below
    ```
        null
    ```

## YAMLのアンカー（`&`）やエイリアス（`*`）名に使える文字は、次のように制約があります。

### 使用できる文字

YAMLのアンカーやエイリアス名には、基本的に**アルファベット、数字、アンダースコア `_`、ハイフン `-`** が使用可能です。ただし、以下の点に注意してください。

1. **アルファベットと数字**: `&anchor_name1` や `*alias2` のように、アルファベットと数字の組み合わせは問題なく使用できます。
2. **アンダースコア `_`**: 識別子の一部として使用できます（例：`&my_anchor` や `*my_alias`）。
3. **ハイフン `-`**: ハイフンも使えますが、識別子の先頭に置くことは避けるのが無難です（例：`&my-anchor`）。

### 使用できない文字

- **特殊文字 `#`、`!`、`$`、`@`、`%` など**: これらはYAMLで特別な意味を持つため、アンカーやエイリアス名には使えません。
- **空白（スペース）**: アンカー名やエイリアス名に空白を含めることはできません。

### 推奨される命名例

アンカーやエイリアス名はシンプルかつわかりやすい名前にすることが推奨されます。例えば：

```yaml
servers:
  - name: server1
    middlewares: &server1_middlewares
      - nginx
      - nodejs

  - name: server2
    middlewares: *server1_middlewares
```

アンカー名やエイリアス名にアルファベット、数字、アンダースコア、ハイフンだけを使用することで、YAMLファイルのパースエラーを避けることができます。