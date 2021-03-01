# python_test
Exemplo de execução
Python
```
$ cat urls.txt | python -m run 
```
Docker 
```
$ docker build -t cialdnb .
```
```
$ cat urls.txt | docker run -i cialdnb 
```
ou
```
$ cat urls.txt | docker run -i cialdnb > output.json 
```