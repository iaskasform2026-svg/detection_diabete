# Journal de bord - Projet IA de détection précoce du diabète

## 1. Présentation du projet
Ce projet porte sur la **détection précoce du diabète** à partir de données cliniques tabulaires.  
L’objectif est de concevoir un **outil d’aide à la décision** capable d’identifier les patients à risque dans un contexte hospitalier.

Le notebook ne se limite pas à l’entraînement d’un modèle. Il adopte une démarche complète, en intégrant :
- le cadrage métier,
- l’analyse de la qualité des données,
- les enjeux éthiques,
- la préparation des variables,
- la comparaison de plusieurs modèles,
- l’interprétation critique des résultats.

---

## 2. Cadrage initial
Le projet a été pensé comme une réponse à un besoin métier clair : **mieux repérer les patients susceptibles de développer un diabète** afin d’améliorer la prévention et de réduire les délais diagnostiques.

Dès le départ, une idée importante est posée : le modèle n’a pas vocation à remplacer un professionnel de santé.  
Il doit être utilisé comme **support d’aide à la décision**, ce qui est cohérent avec les exigences du domaine médical.

Le notebook prend aussi en compte plusieurs dimensions essentielles :
- la confidentialité des données,
- le risque de faux négatifs,
- la nécessité d’expliquer les prédictions,
- la responsabilité humaine dans l’usage final du modèle.

---

## 3. Chargement et compréhension des données
Une première étape a consisté à charger et contrôler le jeu de données.

Les constats principaux sont les suivants :
- le dataset contient **800 lignes et 16 colonnes** ;
- aucune **valeur manquante** n’a été détectée ;
- aucun **doublon exact** n’a été repéré.

Ces éléments montrent que les données sont techniquement propres.  
En revanche, un point critique apparaît très vite : la variable cible est **fortement déséquilibrée**.

Répartition observée :
- classe `1` : **759 observations**
- classe `0` : **41 observations**

Cela signifie qu’environ **94,9 %** des cas appartiennent à la classe positive.  
Ce déséquilibre est majeur, car il peut donner de très bons scores apparents à des modèles qui prédisent presque toujours la même classe.

---

## 4. Analyse exploratoire des données
L’analyse exploratoire a eu pour objectif de :
- comprendre les distributions,
- visualiser les tendances principales,
- identifier les variables potentiellement informatives,
- détecter les éventuels problèmes méthodologiques.

Cette phase a permis de confirmer que certaines variables cliniques portent bien un signal utile pour la prédiction.  
Mais surtout, elle a mis en évidence un **risque de fuite de cible** à travers les colonnes :

- `diabetes_type`
- `diabetes_cause`

Ces variables sont trop directement liées au résultat à prédire.  
Les conserver dans l’apprentissage aurait pu fausser totalement l’évaluation du modèle.

Cette étape a donc joué un rôle essentiel : elle a permis de sécuriser la suite du projet sur le plan méthodologique.

---

## 5. Préparation des données
La phase de préparation a consisté à structurer les données pour l’apprentissage automatique.

Les principales décisions retenues sont :
- exclusion de `patient_id`, qui n’apporte pas d’information prédictive utile ;
- suppression des colonnes à fuite de cible ;
- séparation des variables **numériques** et **catégorielles** ;
- mise en place d’un pipeline de transformation avec imputation, encodage et standardisation selon le type de variable ;
- découpage **train/test** avec stratification pour conserver le déséquilibre de la cible.

Cette organisation présente plusieurs avantages :
- elle rend la démarche reproductible ;
- elle évite les erreurs de prétraitement entre apprentissage et test ;
- elle permet de comparer plusieurs modèles dans un cadre homogène.

---

## 6. Choix des modèles
Le notebook adopte une démarche comparative.  
Il ne se contente pas d’un seul algorithme, mais teste plusieurs approches :

- une **baseline** avec `DummyClassifier`,
- une **régression logistique pondérée**,
- un **arbre de décision pondéré**,
- une **forêt aléatoire pondérée**.

L’intérêt de cette stratégie est double :
1. disposer d’un point de comparaison minimal ;
2. observer comment différents modèles réagissent face à un dataset fortement déséquilibré.

Le projet montre ainsi une vraie logique scientifique : on ne cherche pas uniquement à obtenir un score élevé, mais à comprendre ce que valent réellement les modèles dans ce contexte.

---

## 7. Résultats obtenus
Les résultats les plus marquants du notebook sont les suivants :

- **DummyClassifier** :  
  - recall = **1.00**
  - spécificité = **0.00**
  - ROC-AUC = **0.50**

- **Régression logistique pondérée** :  
  - recall ≈ **0.533**
  - spécificité ≈ **0.625**
  - ROC-AUC ≈ **0.565**

- **Arbre de décision pondéré** :  
  - recall ≈ **0.539**
  - spécificité = **0.50**
  - ROC-AUC ≈ **0.520**

- **Forêt aléatoire pondérée** :  
  - recall = **1.00**
  - spécificité = **0.00**
  - ROC-AUC ≈ **0.565**

---

## 8. Interprétation critique
L’un des enseignements majeurs du projet est que les métriques doivent être interprétées avec prudence.

Le `DummyClassifier` et la forêt aléatoire obtiennent un recall très élevé, mais cela s’explique en grande partie par le fait qu’ils prédisent presque tout en classe positive.  
Dans un dataset où près de 95 % des cas sont positifs, cette stratégie peut sembler performante alors qu’elle n’a **aucune réelle capacité à reconnaître les cas négatifs**.

C’est pourquoi le notebook ne s’appuie pas uniquement sur le recall.  
Il mobilise aussi :
- la spécificité,
- la balanced accuracy,
- la ROC-AUC.

Cette lecture plus complète permet d’éviter une conclusion trompeuse.

Le modèle le plus défendable dans ce contexte est la **régression logistique pondérée**.  
Elle n’est pas la plus spectaculaire en apparence, mais elle est :
- plus interprétable,
- plus honnête dans ses performances,
- plus crédible pour une soutenance.

---

## 9. Mise en situation d’exploitation
Le notebook ne s’arrête pas à l’expérimentation technique.  
Il envisage également une intégration dans un cadre métier réel.

Le modèle pourrait être exploité via :
- une **API sécurisée**,
- un outil de tri clinique,
- un tableau de bord hospitalier.

Un exemple d’inférence sur un patient fictif est aussi présenté pour illustrer le fonctionnement du pipeline.

Cette partie montre que le projet s’inscrit dans une logique d’**industrialisation** :
- contrôle qualité des données,
- pipeline de préparation,
- service de prédiction,
- suivi des performances,
- amélioration continue.

---

## 10. Limites du projet
Le notebook met clairement en évidence plusieurs limites :

- **déséquilibre extrême** de la cible ;
- **risque de fuite de cible** dans certaines colonnes ;
- difficulté à obtenir une bonne discrimination entre positifs et négatifs ;
- performances qui peuvent être artificiellement valorisées si l’on regarde une seule métrique.

Le projet montre donc que le principal problème ne vient pas du code, mais du **jeu de données lui-même**.

---

## 11. Enseignements personnels / professionnels
Ce travail permet de tirer plusieurs leçons importantes :

- un projet d’IA ne se résume pas à entraîner un modèle ;
- la **qualité du dataset** est aussi importante que l’algorithme choisi ;
- un bon score apparent ne garantit pas une solution fiable ;
- dans un domaine sensible comme la santé, il faut toujours garder une **lecture critique** des résultats ;
- l’interprétabilité et la cohérence métier sont essentielles.

Ce notebook montre une démarche sérieuse, car il ne cherche pas à masquer les faiblesses du dataset.  
Au contraire, il les met en avant et en fait un élément central de l’analyse.

---

## 12. Conclusion
En conclusion, ce projet suit une progression logique et professionnelle :

1. cadrage métier ;
2. contrôle de la qualité des données ;
3. analyse exploratoire ;
4. préparation des variables ;
5. comparaison de plusieurs modèles ;
6. évaluation multicritère ;
7. projection vers un usage réel.

Le point fort du travail n’est pas d’avoir trouvé un modèle “parfait”, mais d’avoir su montrer que :
- les données sont déséquilibrées,
- certaines variables posent un risque méthodologique,
- les performances doivent être interprétées avec prudence,
- une solution crédible doit reposer sur des données mieux équilibrées et mieux contrôlées.

Ce recul critique donne de la valeur au projet et renforce sa crédibilité.