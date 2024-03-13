# GlobalExamSolver
Résolution des exercices GlobalExam automatique et simple d'utilisation. Automatic and user frendly exercice solver for GlobalExam.


<div id="header" align="center">
  <img src="https://content.globalexam.cloud/vi/media/logos/natural/global-exam-natural.png"> 
</div>

## Explication de l'outil
Cet outil a pour vocation de résoudre la plupart des exercices de global exam.
Il est complémentaire au script de [MartinPELCAT](https://github.com/MartinPELCAT/GlobalExamFinisher).

Il permet de justifier le nombre d'heures ajouté en plus en stipulant que vous avez effectué tous les exercices jusqu'à avoir 100%.

Ainsi, si un professeur vera que vous êtes assidu dans votre travail !

## Installation
```bash
pip install -r requirements.txt

git clone https://github.com/Nv3l/GlobalExamSolver.git
```
## Pré-requis
> Tester sur Python 3.8.5 et Windows 10 x64

> Utilisable uniquement sur Firefox

> Script adapté pour les OS Windows et Linux avec interface graphique
<br>

## Utilisation

Lancer le fichier [globalexam.exe](globalexam.exe)
<br>

## Configuration

Il vous suffit de renseigner votre identifiant et mot de passe GlobalExam, de choisir la catégorie (exam ou general) et de cliquer sur "Solve exercice" pour commencer la résolution des exercices.

L'interface se divise en 2 parties :

- La partie de gauche permet de résoudre tous les exercices d'une catégorie. (exam ou général)


<div id="left_pannel" align="center">
  <img src="img/left pannel.png"> 
</div>


- La partie de droite permet de résoudre un exercice spécifique. (exam ou général)

<div id="right_pannel" align="center">
  <img src="img/right pannel.png"> 
</div>

<br>

## Fonctionnalités

- Résolution automatique des exercices GlobalExam
- Résolution des exercices de grammaire exam et général
- Résolution de tous les exercices en continu
- Résolution d'un exercice spécifique
- Choix du temps de réponse
- Utilisation adaptative pour toute connexion internet

<br>

## Résolutions de problème

Si vous avez résolu plusieurs exercices à la fin de la page, il est possible que le programme ne puisse pas résoudre les exercices suivants.
Il en va de même si vous avez plusieurs exercices qui affichent en définitif un résultat négatif.

Pour résoudre ce problème, il suffit de renseigner le nombre d'exercices que vous avez fait dans la partie "Skip step".


<br>

<div id="skip_step" align="center">
  <img src="img/Skip Step.png"> 
</div>

<br>

Si la fenêtre "freeze" au lancement, cela est normal. Le programme télécharge le driver de Firefox pour la première fois. Il suffit d'attendre quelques secondes pour que la fenêtre se lance.

## Support

Pour tout report de bug, vous pouvez ouvrir une issue sur le repository.
