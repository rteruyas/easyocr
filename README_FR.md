# Extraction de texte a partir d'un image avec easyOCR
- Cette version correspond au [Lab3](https://github.com/hrhouma/begining_IA_part1/blob/main/lab3.md) pour le cours de Mise en place Ecosysteme IA
- streamlit utilisé comme frontend
- fastAPI utilisé comme backend
- mlflow utilisé pour faire le suivi des experiences
- docker-compose utilisé pour le deploiement

## Utilisation
A partir de la console, lancer la commande
```
docker-compose up
```

## Description de la solution

![alt text](./resources/modele_ml.png)
- Au moment de demarrer les services, on telecharge le model et le garde local dans le container fastAPI
- A ce moment aussi, on va loader l'experiment 'EASYOCR' dans mlflow (dans l'initialisation de fastAPI)
- L'utilisateur télécharge une image dans le site web (streamlit)
- L'image est envoyée au container fastAPI pour le traitement. On appele /extract pour faire l'extraction du texte de l'image
- fastAPI calcule le temps pour l'extraction du text a partir de l'image. Ce valeur est envoyé comme metric vers mlflow
- Le texte trouvé est envoyé de retour au site web en format json
- Le site web affiche les résultats

## docker-compose

![alt text](./resources/docker_compose.png)
- On a 3 services dans le fichier yaml: streamlit, fastapi et mlflow
- Chaque service lance un Dockerfile pour demarrer
- Les 3 services sont connectés dans la meme resseau 'skynet' 🤖
- On ajoute aussi les dépéndances entre les services


## streamlit
L'instruction pour lancer le service streamlit est inclu dans le fichier Dockerfile.streamlit
```
streamlit run app.py
```
- Streamlit est l'inferface utilisateur.  
Voici au moment de rouler pour la 1ere fois  
![Streamlit 1er fois](./resources/streamlit_01.png)
  
- Voici apres telecharge l'image.  
Notez que le modele 'robot' est en train de s'executer  'bip bip bip'  
![Streamlit apres telechargement](./resources/streamlit_02.png)
  
- Voici apres les résultats.  
![Streamlit avec resultats](./resources/streamlit_03.png)  
![Streamlit avec resultats](./resources/streamlit_04.png)
 
## fastAPI
L'instruction pour lancer le service fastapi est inclu dans le fichier Dockerfile.fastapi 
```
uvicorn main:app --host 0.0.0.0 --port 8000 
```
- Avec fastAPI on va créer un API pour que tout le monde peut s'en servir.  
- J'ai developpé 2 methodes: / pour afficher un message type 'Hello World' et /extract pour faire l'extraction du texte a partir d'une image  
  
![fastAPI](./resources/fastapi.png)
 

## mlFlow
L'instruction pour lancer le service mlflow est inclu  dans le fichier Dockerfile.mlflow
```
mlflow server --host 0.0.0.0 --port 5000
```  
mlflow permet de gérer le cycle de vie du machine learning de bout en bout.  
Dans mon cas, je n'ai pas de nouveau modele a generer ou entrainer, donc je vais m'en servir pour mesurer a chaque fois combien de temps ca prend pour faire l'extraction du texte.  
Ce n'est pas une métrique compliqué, mais ca sert a comprendre l'interaction entre les différents services (fastapi et mlflow)  

![fastAPI](./resources/mlflow.png)

## Commentaires

![alt text](./resources/structure_projet.png)

- Le projet a été cree avec visual studio et tester avec ubuntu.  
- Chacune des 3 images ont été créés a partir d'une image python3.11 'clean' de dockerhub. J'ajoute par la suite de packages avec requirements.txt
- J'ai trouvé cette facon d'organiser les fichier Dockerfile et docker-compose.yaml dans intéressant. Il sont tous dans le meme niveau/repertoire et on change la référence dans chaque Dockerfile
- Le modele easyOCR était deja entrainé. Comme amelioration je pourrais chercher comment l'entrainer moi-meme, mais ca prends plus de temps et plus de resources machine.  
Pour l'instant le modele vient tel-que de la libraire easyOCR avec 2 langues: anglais (en) et francais (fr). J'ai testé seulement le modele en anglais.
- Si vous decidez de tester ce projet, faire attention a la taille des images. Ca prend beaucoup de temps pour créer l'image fastAPI
- Beaucoup de temps investi pour comprendre comment ca marche le fichier yaml et faire debugging. Dans la liste de choses que j'ai appris avec ce projet :
1. Le nom du service dans le fichier yaml devient le 'url' pour l'appeler si tous les containers sont dans le meme network  
2. On peut pas tester directement l'url du service dans notre environnement dev (visual studio par exemple) parce qu'on n'est pas das le resseau partagé par les containers  
3. docker-compose logs et docker exec it bash sont mes meilleurs amis  
4. docker network ls d'afficher chaque network defini
5. docker network inspect _nom_ permet de voir quels sont les containers connectés.   
![alt text](./resources/docker_network.png)
- Dans la liste de choses que je n'ai pas encore compris:  
1. Si on change le code python dans visual studio, el container est aussi modifié. Je ne comprends pas pourquoi ca m'a arrivé mais j'ai gagné des heures de travail et de rebuild image
2. Comment ca marche quand on a besoin d'utiliser CUDA ou pareil. J'avais trouvé un modele pour tensorflow mais j'ai eu de la misere au moment de faire le setup de l'environnement et meme pour tester.  
  C'etait pour reconnaisance d'image CIFAR10 mais le modele que j'ai trouvé utilisait GPU